import os
import sys
import shutil
import pytest
from pathlib import Path

from tests.helpers import (
    PROJECT_ROOT,
    SRC_DIR,
    create_dummy_asar,
    create_mock_antigravity_dir,
)


@pytest.fixture
def project_root():
    return PROJECT_ROOT


@pytest.fixture
def src_dir():
    return SRC_DIR


@pytest.fixture
def patcher_py():
    return SRC_DIR / "patcher.py"


@pytest.fixture
def patcher_js():
    return SRC_DIR / "patcher.js"


@pytest.fixture
def dummy_asar_fixture(tmp_path):
    files = {
        "package.json": '{"name": "antigravity", "version": "2.15.0"}',
        "dist/preload.js": "console.log('original preload');",
        "dist/updater.js": "console.log('original updater');",
        "assets/icon.png": b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01",
    }
    asar_path = tmp_path / "test_app.asar"
    return create_dummy_asar(asar_path, files)


@pytest.fixture
def mock_antigravity_clean(tmp_path):
    base_dir = tmp_path / "clean_install"
    return create_mock_antigravity_dir(
        base_dir,
        version="2.15.0",
        is_patched=False,
        include_backup=False,
    )


@pytest.fixture
def mock_antigravity_with_backup(tmp_path):
    base_dir = tmp_path / "installed_with_backup"
    return create_mock_antigravity_dir(
        base_dir,
        version="2.15.0",
        is_patched=True,
        include_backup=True,
        backup_version="2.15.0",
        backup_mtime_offset=-100.0,
    )


@pytest.fixture
def mock_antigravity_official_update(tmp_path):
    """
    Simulates a case where an official update (v2.16.0) replaced app.asar,
    while an older backup (v2.15.0) already exists.
    """
    base_dir = tmp_path / "official_update"
    return create_mock_antigravity_dir(
        base_dir,
        version="2.16.0",
        is_patched=False,
        include_backup=True,
        backup_version="2.15.0",
        backup_mtime_offset=-200.0,
    )
