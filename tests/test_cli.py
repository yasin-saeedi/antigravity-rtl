import os
import sys
import json
import subprocess
import pytest
from pathlib import Path

from tests.helpers import (
    PROJECT_ROOT,
    SRC_DIR,
    create_mock_antigravity_dir,
)

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import patcher


class TestCliInterface:
    """
    Tests CLI argument parsing, non-interactive execution with closed stdin (DEVNULL),
    and flag semantics for both Python and Node.js implementations.
    """

    def test_check_only_unpatched_python_and_node(self, tmp_path):
        """
        Verify --check-only outputs '0' and exits code 0 for unpatched installation.
        """
        mock_dir = tmp_path / "check_unpatched"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)

        # Python test
        py_proc = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "--check-only", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        assert py_proc.returncode == 0, f"Python --check-only failed: {py_proc.stderr}"
        assert py_proc.stdout.strip() == "0", f"Expected '0' for unpatched, got: {py_proc.stdout.strip()}"

        # Node test
        node_proc = subprocess.run(
            ["node", str(SRC_DIR / "patcher.js"), "--check-only", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        assert node_proc.returncode == 0, f"Node --check-only failed: {node_proc.stderr}"
        assert node_proc.stdout.strip() == "0", f"Expected '0' for unpatched, got: {node_proc.stdout.strip()}"

    def test_check_only_patched_python_and_node(self, tmp_path):
        """
        Verify --check-only outputs '1' and exits code 0 for already patched installation.
        """
        mock_dir = tmp_path / "check_patched"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=True)

        # Python test
        py_proc = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "--check-only", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        assert py_proc.returncode == 0
        assert py_proc.stdout.strip() == "1", f"Expected '1' for patched, got: {py_proc.stdout.strip()}"

        # Node test
        node_proc = subprocess.run(
            ["node", str(SRC_DIR / "patcher.js"), "--check-only", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        assert node_proc.returncode == 0
        assert node_proc.stdout.strip() == "1", f"Expected '1' for patched, got: {node_proc.stdout.strip()}"

    def test_no_kill_non_interactive_execution_python(self, tmp_path):
        """
        Verify that running patcher.py with --no-kill and closed stdin (DEVNULL)
        executes non-interactively without raising EOFError or hanging on input().
        """
        mock_dir = tmp_path / "nokill_py"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)

        proc = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "--no-kill", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )

        assert "EOFError" not in proc.stderr, f"EOFError detected in stderr: {proc.stderr}"
        assert proc.returncode == 0, f"Process exited with non-zero code {proc.returncode}. Output: {proc.stdout} Err: {proc.stderr}"

        # Verify that patch was applied
        asar_path = mock_dir / "resources" / "app.asar"
        preload = patcher.extract_file_from_asar(str(asar_path), "dist/preload.js")
        assert "__ANTIGRAVITY_RTL_INJECTED__" in (preload or ""), "Mock installation must be patched"

    def test_no_kill_non_interactive_execution_node(self, tmp_path):
        """
        Verify that running patcher.js with --no-kill and closed stdin executes
        cleanly without hanging or failing.
        """
        mock_dir = tmp_path / "nokill_node"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)

        proc = subprocess.run(
            ["node", str(SRC_DIR / "patcher.js"), "--no-kill", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )

        assert proc.returncode == 0, f"Node process exited with code {proc.returncode}. Err: {proc.stderr}"

        asar_path = mock_dir / "resources" / "app.asar"
        preload = patcher.extract_file_from_asar(str(asar_path), "dist/preload.js")
        assert "__ANTIGRAVITY_RTL_INJECTED__" in (preload or ""), "Mock installation must be patched by Node"

    def test_closed_stdin_eof_resilience_without_flags(self, tmp_path):
        """
        Verify that invoking patcher.py with closed stdin (DEVNULL) and only --path
        handles EOF cleanly without raising an unhandled EOFError traceback.
        """
        mock_dir = tmp_path / "eof_resilience"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)

        proc = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )

        assert "EOFError" not in proc.stderr, f"Unhandled EOFError in patcher.py: {proc.stderr}"
        assert proc.returncode == 0, f"Expected clean exit 0 on closed stdin, got {proc.returncode}"

    def test_wait_for_update_flag_non_interactive_python(self, tmp_path):
        """
        Verify that --wait-for-update runs non-interactively without prompt or stall,
        detects an application update via mtime change, and executes patching.
        """
        import threading
        import time

        mock_dir = tmp_path / "wait_update_py"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)
        asar_path = mock_dir / "resources" / "app.asar"

        def simulate_update():
            time.sleep(0.8)
            now = time.time()
            try:
                os.utime(asar_path, (now + 100, now + 100))
            except Exception:
                pass

        updater_thread = threading.Thread(target=simulate_update)
        updater_thread.daemon = True
        updater_thread.start()

        proc = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "--wait-for-update", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )

        assert proc.returncode == 0, f"--wait-for-update failed: {proc.stderr}"
        assert "EOFError" not in proc.stderr

    def test_wait_for_update_flag_non_interactive_node(self, tmp_path):
        """
        Verify that --wait-for-update in Node runs non-interactively without prompt,
        detects an application update via mtime change, and executes patching.
        """
        import threading
        import time

        mock_dir = tmp_path / "wait_update_node"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)
        asar_path = mock_dir / "resources" / "app.asar"

        def simulate_update():
            time.sleep(0.8)
            now = time.time()
            try:
                os.utime(asar_path, (now + 100, now + 100))
            except Exception:
                pass

        updater_thread = threading.Thread(target=simulate_update)
        updater_thread.daemon = True
        updater_thread.start()

        proc = subprocess.run(
            ["node", str(SRC_DIR / "patcher.js"), "--wait-for-update", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=25,
        )

        assert proc.returncode == 0, f"Node --wait-for-update failed: {proc.stderr}"

    def test_no_kill_boolean_semantics_node(self):
        """
        Verify that passing --no-kill does NOT set kill=true in Node.js patcher.
        (Guards against the inverted boolean flaw where noKill was passed to kill=false).
        """
        eval_script = f"""
        const path = require('path');
        const fs = require('fs');
        const patcherCode = fs.readFileSync(path.resolve('{SRC_DIR.as_posix()}', 'patcher.js'), 'utf8');

        // Check argument parsing logic in patcher.js
        const noKillRegex = /const\\s+noKill\\s*=\\s*args\\.includes\\('--no-kill'\\);/;
        assert = require('assert');
        assert(noKillRegex.test(patcherCode), "patcher.js must parse --no-kill");

        // Verify that kill is false when --no-kill is present
        const killRegex = /const\\s+kill\\s*=\\s*args\\.includes\\('--kill'\\)\\s*&&\\s*!noKill/;
        const hasFixedKill = killRegex.test(patcherCode) || patcherCode.includes('kill = !noKill') || !patcherCode.includes('doPatch(targetDir, noKill)');
        assert(hasFixedKill, "Inverted boolean bug found: doPatch(targetDir, noKill) must NOT pass noKill as kill parameter");
        console.log(JSON.stringify({{ passed: true }}));
        """

        proc = subprocess.run(
            ["node", "-e", eval_script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert proc.returncode == 0, f"Node --no-kill semantics check failed:\n{proc.stderr}"

    def test_install_shortcuts_flag_support_python_and_node(self, tmp_path):
        """
        Verify that --install-shortcuts and -s are accepted without error
        and execute safely in both Python and Node.js patcher.
        """
        mock_dir = tmp_path / "shortcuts_test"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)

        # Python with --install-shortcuts
        proc_py = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "--no-kill", "--install-shortcuts", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        assert proc_py.returncode == 0, f"Python failed with --install-shortcuts: {proc_py.stderr}"

        # Node with --install-shortcuts
        mock_dir_node = tmp_path / "shortcuts_node"
        create_mock_antigravity_dir(mock_dir_node, version="2.15.0", is_patched=False)

        proc_node = subprocess.run(
            ["node", str(SRC_DIR / "patcher.js"), "--no-kill", "--install-shortcuts", "--path", str(mock_dir_node)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        assert proc_node.returncode == 0, f"Node failed with --install-shortcuts: {proc_node.stderr}"

    def test_default_shortcuts_disabled_in_patch_functions(self):
        """
        Verify that deploy_permanent_engine and do_patch in patcher.py
        have install_shortcuts=False by default.
        """
        import inspect
        import patcher

        sig_patch = inspect.signature(patcher.do_patch)
        assert "install_shortcuts" in sig_patch.parameters, "do_patch must have install_shortcuts parameter"
        assert sig_patch.parameters["install_shortcuts"].default is False, "do_patch must default install_shortcuts to False"

        sig_deploy = inspect.signature(patcher.deploy_permanent_engine)
        assert "install_shortcuts" in sig_deploy.parameters, "deploy_permanent_engine must have install_shortcuts parameter"
        assert sig_deploy.parameters["install_shortcuts"].default is False, "deploy_permanent_engine must default install_shortcuts to False"

    def test_option_3_cli_argument_python_and_node(self, tmp_path):
        """
        Verify that passing '3' as a command-line argument successfully executes
        in both Python and Node.js patchers.
        """
        mock_dir_py = tmp_path / "opt3_py"
        create_mock_antigravity_dir(mock_dir_py, version="2.15.0", is_patched=False)

        proc_py = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "3", "--no-kill", "--path", str(mock_dir_py)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        assert proc_py.returncode == 0, f"Python failed with '3': {proc_py.stderr}"

        mock_dir_node = tmp_path / "opt3_node"
        create_mock_antigravity_dir(mock_dir_node, version="2.15.0", is_patched=False)

        proc_node = subprocess.run(
            ["node", str(SRC_DIR / "patcher.js"), "3", "--no-kill", "--path", str(mock_dir_node)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        assert proc_node.returncode == 0, f"Node failed with '3': {proc_node.stderr}"

    def test_option_4_and_diagnostics_flag_python(self, tmp_path):
        """
        Verify that passing '4' or '--diagnostics' runs system diagnostics and exits cleanly.
        """
        mock_dir = tmp_path / "diag_test"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False)

        proc = subprocess.run(
            [sys.executable, str(SRC_DIR / "patcher.py"), "4", "--path", str(mock_dir)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        assert proc.returncode == 0, f"Python failed with '4': {proc.stderr}"
        assert "DIAGNOSTICS & SYSTEM HEALTH" in proc.stdout, "Diagnostics header missing from output"

