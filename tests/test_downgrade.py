import os
import sys
import json
import time
import subprocess
import pytest
from pathlib import Path

from tests.helpers import (
    SRC_DIR,
    create_dummy_asar,
    create_mock_antigravity_dir,
)

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import patcher


class TestDowngradePrevention:
    """
    Verifies that official Antigravity updates are never overwritten by outdated
    factory backups (app.asar.original_backup) during patching or restoration.
    """

    def test_clean_install_creates_backup_and_patches(self, tmp_path):
        """
        On a fresh install without existing backup, do_patch creates app.asar.original_backup
        from app.asar and successfully applies the RTL patch.
        """
        mock_dir = tmp_path / "clean_antigravity"
        create_mock_antigravity_dir(mock_dir, version="2.15.0", is_patched=False, include_backup=False)

        res_dir = mock_dir / "resources"
        asar_path = res_dir / "app.asar"
        backup_path = res_dir / "app.asar.original_backup"

        assert asar_path.exists()
        assert not backup_path.exists()

        success = patcher.do_patch(str(mock_dir), interactive=False, kill=False)
        assert success is True, "do_patch should succeed"

        # Backup must have been created
        assert backup_path.exists(), "app.asar.original_backup must be created"
        backup_pkg = json.loads(patcher.extract_file_from_asar(str(backup_path), "package.json"))
        assert backup_pkg["version"] == "2.15.0"
        backup_preload = patcher.extract_file_from_asar(str(backup_path), "dist/preload.js")
        assert "__ANTIGRAVITY_RTL_INJECTED__" not in backup_preload, "Backup must remain unpatched"

        # app.asar must be patched
        patched_preload = patcher.extract_file_from_asar(str(asar_path), "dist/preload.js")
        assert "__ANTIGRAVITY_RTL_INJECTED__" in patched_preload, "app.asar must contain RTL injection"
        patched_pkg = json.loads(patcher.extract_file_from_asar(str(asar_path), "package.json"))
        assert patched_pkg["version"] == "2.15.0"

    def test_official_update_prevents_downgrade_python(self, tmp_path):
        """
        CRITICAL TEST:
        Simulate an official Antigravity update from v2.15.0 to v2.16.0:
        - Outdated backup (v2.15.0) exists from a previous patch.
        - Google updater replaces app.asar with official unpatched v2.16.0 build.
        - do_patch is executed.
        - The patcher MUST NOT use the old v2.15.0 backup as source_asar!
        - The backup MUST be refreshed with v2.16.0.
        - The final app.asar MUST be version 2.16.0 with RTL patch applied.
        """
        mock_dir = tmp_path / "update_scenario"
        create_mock_antigravity_dir(
            mock_dir,
            version="2.16.0",       # New official release
            is_patched=False,       # Clean, unpatched from Google
            include_backup=True,    # Existing old backup from prior version
            backup_version="2.15.0",
            backup_mtime_offset=-200.0,
        )

        res_dir = mock_dir / "resources"
        asar_path = res_dir / "app.asar"
        backup_path = res_dir / "app.asar.original_backup"

        success = patcher.do_patch(str(mock_dir), interactive=False, kill=False)
        assert success is True, "do_patch should succeed"

        # Verify final app.asar is v2.16.0 (NOT downgraded to v2.15.0!)
        final_pkg = json.loads(patcher.extract_file_from_asar(str(asar_path), "package.json"))
        assert final_pkg["version"] == "2.16.0", (
            f"SILENT DOWNGRADE DETECTED! Expected app.asar to be v2.16.0, but got v{final_pkg['version']}"
        )

        # Verify final app.asar is patched
        final_preload = patcher.extract_file_from_asar(str(asar_path), "dist/preload.js")
        assert "__ANTIGRAVITY_RTL_INJECTED__" in final_preload

        # Verify backup was refreshed with the official v2.16.0 build
        refreshed_backup_pkg = json.loads(patcher.extract_file_from_asar(str(backup_path), "package.json"))
        assert refreshed_backup_pkg["version"] == "2.16.0", (
            f"Backup was not refreshed with the official release! Expected v2.16.0, got v{refreshed_backup_pkg['version']}"
        )
        backup_preload = patcher.extract_file_from_asar(str(backup_path), "dist/preload.js")
        assert "__ANTIGRAVITY_RTL_INJECTED__" not in backup_preload, "Refreshed backup must be pristine/unpatched"

    def test_official_update_prevents_downgrade_node(self, tmp_path):
        """
        Verify that Node.js patcher (src/patcher.js) also prevents silent downgrade
        when an official update replaces app.asar.
        """
        mock_dir = tmp_path / "update_scenario_node"
        create_mock_antigravity_dir(
            mock_dir,
            version="2.16.0",
            is_patched=False,
            include_backup=True,
            backup_version="2.15.0",
            backup_mtime_offset=-300.0,
        )

        res_dir = mock_dir / "resources"
        asar_path = res_dir / "app.asar"
        backup_path = res_dir / "app.asar.original_backup"

        node_script = f"""
        const fs = require('fs');
        const path = require('path');
        const patcherJs = path.resolve('{SRC_DIR.as_posix()}', 'patcher.js');
        const content = fs.readFileSync(patcherJs, 'utf8');

        // Execute patcher.js via CLI invocation
        """

        # Run patcher.js with --path and --no-kill
        proc = subprocess.run(
            ["node", str(SRC_DIR / "patcher.js"), "--path", str(mock_dir), "--no-kill"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )

        # Inspect resulting app.asar using Python extract helper
        final_pkg = json.loads(patcher.extract_file_from_asar(str(asar_path), "package.json"))
        assert final_pkg["version"] == "2.16.0", (
            f"SILENT DOWNGRADE IN NODE! Expected app.asar to be v2.16.0, got v{final_pkg['version']}"
        )

        refreshed_backup_pkg = json.loads(patcher.extract_file_from_asar(str(backup_path), "package.json"))
        assert refreshed_backup_pkg["version"] == "2.16.0", (
            f"Backup in Node was not refreshed! Expected v2.16.0, got v{refreshed_backup_pkg['version']}"
        )

    def test_do_restore_never_downgrades_newer_official_app(self, tmp_path):
        """
        Verify do_restore does NOT overwrite a newer official app.asar (v2.16.0)
        with an older backup (v2.15.0).
        """
        mock_dir = tmp_path / "restore_safety"
        create_mock_antigravity_dir(
            mock_dir,
            version="2.16.0",
            is_patched=False,
            include_backup=True,
            backup_version="2.15.0",
            backup_mtime_offset=-500.0,
        )

        res_dir = mock_dir / "resources"
        asar_path = res_dir / "app.asar"

        # Calling restore when app.asar is already clean and newer
        patcher.do_restore(str(mock_dir), kill=False)

        # app.asar must still be version 2.16.0!
        current_pkg = json.loads(patcher.extract_file_from_asar(str(asar_path), "package.json"))
        assert current_pkg["version"] == "2.16.0", (
            "do_restore downgraded the application from v2.16.0 to v2.15.0!"
        )
