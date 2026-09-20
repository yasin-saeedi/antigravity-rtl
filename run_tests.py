#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
Antigravity RTL Unified Test Runner
Executes comprehensive automated test suite across all verified tiers:
- Tier 1: CLI Argument Dispatch & Non-Interactive Resilience
- Tier 2: CSS Selector Escaping & Template Literal V8 Evaluation
- Tier 3: ASAR 16-byte Header & Round-trip Integrity
- Tier 4: Updater Persistence & Downgrade Prevention
- Tier 5: Runtime Performance & Layout Thrashing Elimination
====================================================================
"""

import os
import sys
import time
from pathlib import Path

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def print_banner():
    banner = """
====================================================================
    ✦ Antigravity Smart RTL Automated Test Suite Runner ✦
       Automated Verification, Hardening & Integrity Suite
====================================================================
    """
    print(banner.strip())
    print()


def main():
    print_banner()

    try:
        import pytest
    except ImportError:
        print("[-] Error: pytest is required to run the test suite.")
        print("    Install it with: pip install pytest")
        sys.exit(1)

    # Forward any CLI arguments or use default clean verbose run
    args = sys.argv[1:]
    if not args:
        args = ["-v", str(TESTS_DIR)]
    elif not any(a.startswith("tests") or a.endswith(".py") for a in args):
        args = args + [str(TESTS_DIR)]

    start_time = time.time()
    exit_code = pytest.main(args)
    elapsed = time.time() - start_time

    print()
    print("=" * 68)
    if exit_code == 0:
        print(f"[✓] ALL TEST TIERS PASSED SUCCESSFULLY in {elapsed:.2f}s (Exit code: 0)")
    else:
        print(f"[-] TEST SUITE FAILED with exit code {exit_code} in {elapsed:.2f}s")
    print("=" * 68)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
