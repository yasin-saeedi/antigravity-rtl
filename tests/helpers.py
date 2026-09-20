import os
import sys
import json
import struct
import hashlib
import shutil
import tempfile
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def compute_sha256_blocks(data: bytes, block_size: int = 4 * 1024 * 1024):
    blocks = []
    for i in range(0, len(data), block_size):
        chunk = data[i:i + block_size]
        blocks.append(hashlib.sha256(chunk).hexdigest())
    return {
        "algorithm": "SHA256",
        "hash": hashlib.sha256(data).hexdigest(),
        "blockSize": block_size,
        "blocks": blocks,
    }


def create_dummy_asar(dest_path: Path, files: dict):
    """
    Creates a valid Electron ASAR archive from a mapping of {rel_path: str | bytes}.
    """
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    header_files = {}
    payload_chunks = []
    current_offset = 0

    for rel_path, content in files.items():
        if isinstance(content, str):
            data = content.encode("utf-8")
        else:
            data = bytes(content)

        parts = rel_path.replace("\\", "/").strip("/").split("/")
        curr = header_files
        for part in parts[:-1]:
            if part not in curr:
                curr[part] = {"files": {}}
            curr = curr[part]["files"]

        filename = parts[-1]
        curr[filename] = {
            "size": len(data),
            "offset": str(current_offset),
            "integrity": compute_sha256_blocks(data),
        }
        payload_chunks.append(data)
        current_offset += len(data)

    header = {"files": header_files}
    json_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
    json_len = len(json_bytes)
    padding_len = (4 - (json_len % 4)) % 4
    padding = b"\0" * padding_len

    size_header = json_len + padding_len + 4
    size_total = size_header + 4
    header_prefix = struct.pack("<IIII", 4, size_total, size_header, json_len)

    with open(dest_path, "wb") as f:
        f.write(header_prefix)
        f.write(json_bytes)
        f.write(padding)
        for chunk in payload_chunks:
            f.write(chunk)

    return dest_path


def create_mock_antigravity_dir(
    base_dir: Path,
    version: str = "2.15.0",
    is_patched: bool = False,
    include_backup: bool = False,
    backup_version: str = "2.15.0",
    backup_mtime_offset: float = -100.0,
):
    """
    Sets up a mock Antigravity installation layout under base_dir:
    resources/
      app.asar
      (optional) app.asar.original_backup
    """
    base_dir = Path(base_dir)
    res_dir = base_dir / "resources"
    res_dir.mkdir(parents=True, exist_ok=True)

    # Create dummy Antigravity.exe so path detectors recognize it as a valid install
    (base_dir / "Antigravity.exe").write_bytes(b"MZ_DUMMY_ANTIGRAVITY_EXE")

    preload_content = "console.log('original preload');"
    if is_patched:
        preload_content = "/* __ANTIGRAVITY_RTL_INJECTED__ */\nconsole.log('patched preload');"

    files = {
        "package.json": json.dumps({"name": "antigravity", "version": version}),
        "dist/preload.js": preload_content,
        "dist/updater.js": "console.log('updater');",
        "node_modules/electron-updater/out/NsisUpdater.js": "console.log('nsis');",
        "node_modules/electron-updater/out/BaseUpdater.js": "console.log('base');",
    }

    asar_path = res_dir / "app.asar"
    create_dummy_asar(asar_path, files)

    if include_backup:
        backup_files = {
            "package.json": json.dumps({"name": "antigravity", "version": backup_version}),
            "dist/preload.js": "console.log('original factory preload');",
            "dist/updater.js": "console.log('factory updater');",
            "node_modules/electron-updater/out/NsisUpdater.js": "console.log('nsis');",
            "node_modules/electron-updater/out/BaseUpdater.js": "console.log('base');",
        }
        backup_path = res_dir / "app.asar.original_backup"
        create_dummy_asar(backup_path, backup_files)
        # Set mtime of backup relative to asar
        asar_mtime = os.path.getmtime(asar_path)
        os.utime(backup_path, (asar_mtime + backup_mtime_offset, asar_mtime + backup_mtime_offset))

    return base_dir
