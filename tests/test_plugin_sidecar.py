"""
Automated verification tests for Antigravity RTL Native Plugin & Sidecar Architecture.
"""

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = REPO_ROOT / "plugin.json"
SIDECAR_JSON = REPO_ROOT / "sidecars" / "rtl" / "sidecar.json"
INSTALL_PS1 = REPO_ROOT / "install.ps1"
RTL_ENGINE_JS = REPO_ROOT / "src" / "injector" / "rtl-engine.js"
CDP_BRIDGE_JS = REPO_ROOT / "src" / "sidecar" / "cdp-bridge.js"
CLI_JS = REPO_ROOT / "bin" / "cli.js"


def test_plugin_manifest_structure():
    assert PLUGIN_JSON.is_file(), "plugin.json must exist in repo root"
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    assert data.get("name") == "antigravity-rtl"
    assert data.get("version") == "2.0.0"
    assert "Persian" in data.get("displayName", "")


def test_sidecar_configuration():
    assert SIDECAR_JSON.is_file(), "sidecars/rtl/sidecar.json must exist"
    data = json.loads(SIDECAR_JSON.read_text(encoding="utf-8"))
    assert data.get("command") == "node"
    assert "../../src/sidecar/index.js" in data.get("args", [])
    assert data.get("restart_policy") == "always"


def test_install_ps1_syntax():
    assert INSTALL_PS1.is_file(), "install.ps1 must exist"
    content = INSTALL_PS1.read_text(encoding="utf-8")
    assert "$ErrorActionPreference" in content
    assert "antigravity-rtl" in content
    assert "install-plugin.js" in content
    # Validate PowerShell syntax without execution
    proc = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"[System.Management.Automation.Language.Parser]::ParseInput((Get-Content -Raw '{INSTALL_PS1}'), [ref]$null, [ref]$null)",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, f"PowerShell syntax error in install.ps1: {proc.stderr}"


def test_rtl_engine_features():
    assert RTL_ENGINE_JS.is_file(), "src/injector/rtl-engine.js must exist"
    code = RTL_ENGINE_JS.read_text(encoding="utf-8")
    assert "0.7" in code, "Should enforce 70% Persian/Arabic letter ratio threshold"
    assert "title-menu-bar" in code, "Appearance menu must be mounted to title-menu-bar"
    assert "MutationObserver" in code, "Must observe DOM changes for streaming chat"
    assert "input" in code, "Must attach dynamic input listeners for RTL typing"


def test_cdp_bridge_syntax_and_exports():
    assert CDP_BRIDGE_JS.is_file(), "src/sidecar/cdp-bridge.js must exist"
    code = CDP_BRIDGE_JS.read_text(encoding="utf-8")
    assert "class CdpBridge" in code
    assert "DevToolsActivePort" in code


def test_cli_status_execution():
    assert CLI_JS.is_file(), "bin/cli.js must exist"
    proc = subprocess.run(
        ["node", str(CLI_JS), "status"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(REPO_ROOT),
    )
    assert proc.returncode == 0, f"CLI status failed: {proc.stderr}"
    assert "Antigravity RTL" in proc.stdout
    assert "Plugin Status" in proc.stdout
