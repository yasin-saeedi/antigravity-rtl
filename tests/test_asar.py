import os
import sys
import json
import struct
import hashlib
import subprocess
import pytest
from pathlib import Path

from tests.helpers import (
    PROJECT_ROOT,
    SRC_DIR,
    create_dummy_asar,
    compute_sha256_blocks,
)

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import patcher


class TestAsarHeaderAndIntegrity:
    def test_asar_16byte_header_format(self, dummy_asar_fixture):
        """
        Verify the 16-byte Electron ASAR header structure:
        - Bytes 0-3: magic uint32 (must equal 4)
        - Bytes 4-7: size_total uint32 (must equal size_header + 4)
        - Bytes 8-11: size_header uint32 (must equal json_len + padding + 4)
        - Bytes 12-15: json_len uint32 (byte length of JSON directory tree)
        - Padding: (4 - (json_len % 4)) % 4 bytes
        - Total header + payload offset: 4-byte aligned
        """
        with open(dummy_asar_fixture, "rb") as f:
            header_raw = f.read(16)
            assert len(header_raw) == 16, "Header must be at least 16 bytes"

            magic, size_total, size_header, json_len = struct.unpack("<IIII", header_raw)

            assert magic == 4, f"ASAR magic must be 4, got {magic}"
            assert size_total == size_header + 4, (
                f"size_total ({size_total}) must be size_header + 4 ({size_header + 4})"
            )

            padding = (4 - (json_len % 4)) % 4
            assert size_header == json_len + padding + 4, (
                f"size_header ({size_header}) must equal json_len + padding + 4 ({json_len + padding + 4})"
            )

            payload_start = 16 + json_len + padding
            assert payload_start % 4 == 0, f"Payload start ({payload_start}) must be 4-byte aligned"

            json_bytes = f.read(json_len)
            assert len(json_bytes) == json_len, "Read JSON bytes length must match json_len"

            parsed_header = json.loads(json_bytes.decode("utf-8"))
            assert "files" in parsed_header, "Parsed header JSON must contain 'files' root dictionary"
            assert "package.json" in parsed_header["files"], "Must contain package.json"
            assert "dist" in parsed_header["files"], "Must contain dist directory"

    def test_extract_file_from_asar_python(self, dummy_asar_fixture):
        """
        Verify Python extract_file_from_asar correctly parses the directory tree
        and reads exact file payloads by offset and size.
        """
        pkg = patcher.extract_file_from_asar(dummy_asar_fixture, "package.json")
        assert pkg is not None, "package.json must be extractable"
        parsed_pkg = json.loads(pkg)
        assert parsed_pkg.get("name") == "antigravity"
        assert parsed_pkg.get("version") == "2.15.0"

        preload = patcher.extract_file_from_asar(dummy_asar_fixture, "dist/preload.js")
        assert preload == "console.log('original preload');"

        updater = patcher.extract_file_from_asar(dummy_asar_fixture, "dist/updater.js")
        assert updater == "console.log('original updater');"

        nonexistent = patcher.extract_file_from_asar(dummy_asar_fixture, "missing/path.js")
        assert nonexistent is None, "Non-existent path must return None"

    def test_extract_file_from_asar_node(self, dummy_asar_fixture):
        """
        Verify Node.js extractFromAsar in src/patcher.js can read the synthetic ASAR archive.
        """
        node_script = f"""
        const fs = require('fs');
        const path = require('path');
        const patcherJs = path.resolve('{SRC_DIR.as_posix()}', 'patcher.js');
        const content = fs.readFileSync(patcherJs, 'utf8');

        // Extract extractFromAsar function definition
        const fnMatch = content.match(/function\\s+extractFromAsar\\s*\\([\\s\\S]*?\\n\\}}/);
        if (!fnMatch) {{
            console.error('extractFromAsar function not found in patcher.js');
            process.exit(1);
        }}

        eval(fnMatch[0]);

        const asarPath = path.resolve('{dummy_asar_fixture.as_posix()}');
        const pkg = extractFromAsar(asarPath, 'package.json');
        const preload = extractFromAsar(asarPath, 'dist/preload.js');
        const missing = extractFromAsar(asarPath, 'nonexistent.js');

        const result = {{
            pkg: JSON.parse(pkg),
            preload: preload,
            missing: missing
        }};
        console.log(JSON.stringify(result));
        """
        proc = subprocess.run(
            ["node", "-e", node_script],
            capture_output=True,
            text=True,
            check=True,
        )
        res = json.loads(proc.stdout.strip())
        assert res["pkg"]["name"] == "antigravity"
        assert res["pkg"]["version"] == "2.15.0"
        assert res["preload"] == "console.log('original preload');"
        assert res["missing"] is None

    def test_patch_asar_roundtrip_integrity(self, tmp_path):
        """
        Verify patch_asar updates designated files, recomputes SHA-256 block hashes,
        updates offsets, preserves un-modified files, and generates a valid 16-byte header.
        """
        input_asar = tmp_path / "original.asar"
        output_asar = tmp_path / "patched.asar"

        initial_files = {
            "dist/preload.js": "const originalPreload = true;",
            "dist/updater.js": "const originalUpdater = true;",
            "package.json": '{"name": "test-pkg", "version": "1.0.0"}',
            "data/readme.txt": "Hello from readme",
        }
        create_dummy_asar(input_asar, initial_files)

        new_preload = "/* __ANTIGRAVITY_RTL_INJECTED__ */\nconst patchedPreload = true;"
        replacements = {
            "dist/preload.js": new_preload,
        }

        patcher.patch_asar(str(input_asar), str(output_asar), replacements)

        assert output_asar.exists(), "Output patched ASAR must exist"

        # Verify extracted content
        extracted_preload = patcher.extract_file_from_asar(str(output_asar), "dist/preload.js")
        assert extracted_preload == new_preload, "Patched file must match replacement exactly"

        extracted_updater = patcher.extract_file_from_asar(str(output_asar), "dist/updater.js")
        assert extracted_updater == initial_files["dist/updater.js"], "Unmodified file must be preserved"

        extracted_pkg = patcher.extract_file_from_asar(str(output_asar), "package.json")
        assert extracted_pkg == initial_files["package.json"], "Unmodified package.json must be preserved"

        # Verify 16-byte header of output
        with open(output_asar, "rb") as f:
            header_raw = f.read(16)
            magic, size_total, size_header, json_len = struct.unpack("<IIII", header_raw)
            assert magic == 4
            assert size_total == size_header + 4
            padding = (4 - (json_len % 4)) % 4
            assert size_header == json_len + padding + 4

            json_bytes = f.read(json_len)
            header = json.loads(json_bytes.decode("utf-8"))

            preload_node = header["files"]["dist"]["files"]["preload.js"]
            assert preload_node["size"] == len(new_preload.encode("utf-8"))
            expected_hash = hashlib.sha256(new_preload.encode("utf-8")).hexdigest()
            assert preload_node["integrity"]["hash"] == expected_hash

    def test_cross_engine_asar_compatibility(self, tmp_path):
        """
        Verify cross-engine compatibility:
        - An ASAR produced by Python patch_asar is extracted by Node.js extractFromAsar.
        - An ASAR produced by Node.js patchAsar is extracted by Python extract_file_from_asar.
        """
        input_asar = tmp_path / "base.asar"
        create_dummy_asar(input_asar, {
            "dist/preload.js": "console.log('original');",
            "package.json": '{"version": "1.0.0"}',
        })

        py_patched_asar = tmp_path / "py_patched.asar"
        patcher.patch_asar(
            str(input_asar),
            str(py_patched_asar),
            {"dist/preload.js": "console.log('python patched');"},
        )

        # Node extracts Python-patched ASAR
        node_verify_script = f"""
        const fs = require('fs');
        const path = require('path');
        const content = fs.readFileSync(path.resolve('{SRC_DIR.as_posix()}', 'patcher.js'), 'utf8');
        const fnMatch = content.match(/function\\s+extractFromAsar\\s*\\([\\s\\S]*?\\n\\}}/);
        eval(fnMatch[0]);

        const extracted = extractFromAsar(path.resolve('{py_patched_asar.as_posix()}'), 'dist/preload.js');
        console.log(extracted);
        """
        proc = subprocess.run(
            ["node", "-e", node_verify_script],
            capture_output=True,
            text=True,
            check=True,
        )
        assert proc.stdout.strip() == "console.log('python patched');"

        # Now Node patches the ASAR
        node_patched_asar = tmp_path / "node_patched.asar"
        node_patch_script = f"""
        const fs = require('fs');
        const path = require('path');
        const crypto = require('crypto');
        const content = fs.readFileSync(path.resolve('{SRC_DIR.as_posix()}', 'patcher.js'), 'utf8');
        
        // Extract sha256Blocks and patchAsar
        const shaMatch = content.match(/function\\s+sha256Blocks\\s*\\([\\s\\S]*?\\n\\}}/);
        const patchMatch = content.match(/function\\s+patchAsar\\s*\\([\\s\\S]*?\\n\\}}/);
        eval(shaMatch[0]);
        eval(patchMatch[0]);

        patchAsar(
            path.resolve('{input_asar.as_posix()}'),
            path.resolve('{node_patched_asar.as_posix()}'),
            {{ 'dist/preload.js': 'console.log("node patched");' }}
        );
        """
        subprocess.run(
            ["node", "-e", node_patch_script],
            capture_output=True,
            text=True,
            check=True,
        )

        # Python extracts Node-patched ASAR
        py_extracted = patcher.extract_file_from_asar(str(node_patched_asar), "dist/preload.js")
        assert py_extracted == 'console.log("node patched");'

    def test_corrupt_asar_header_detection(self, tmp_path):
        """
        Verify invalid magic numbers or corrupt headers are detected and raise ValueError.
        """
        corrupt_file = tmp_path / "corrupt.asar"
        out_file = tmp_path / "corrupt_out.asar"
        # Write invalid magic (42 instead of 4)
        with open(corrupt_file, "wb") as f:
            f.write(struct.pack("<IIII", 42, 100, 96, 50))
            f.write(b"x" * 50)

        with pytest.raises(ValueError, match="Magic"):
            patcher.patch_asar(str(corrupt_file), str(out_file), {})
