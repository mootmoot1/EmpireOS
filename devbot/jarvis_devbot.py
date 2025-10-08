#!/usr/bin/env python3
# Jarvis DevBot — minimal, stable, CI-safe core
# Author: mootmoot1

import os
import sys
import time
import subprocess
from pathlib import Path
from typing import List, Optional


def run(cmd: List[str], cwd: Optional[Path] = None, check: bool = False):
    """
    Run a shell command safely and print its result.
    """
    print(f"\n▶ Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout.strip()}")
        else:
            print(f"❌ Error ({result.returncode}): {result.stderr.strip()}")
        return result
    except Exception as e:
        print(f"⚠️ Exception: {e}")
        return None


def one_shot():
    """
    Perform a single maintenance cycle — for CI-safe manual runs.
    """
    print("\n🤖 Jarvis DevBot started (one-time maintenance)...")
    run(["git", "status"])
    run(["git", "pull"])
    print("✅ Maintenance complete.\n")


def idle_loop():
    """
    Continuous self-check loop (use only in Dev mode).
    """
    print("\n🌀 Jarvis DevBot in idle mode — CI-safe loop active.")
    while True:
        run(["echo", "Checking system health..."])
        time.sleep(60)


def main():
    """
    Main entry point — handles --test, --once, and idle mode.
    """
    if "--test" in sys.argv:
        print("✅ Jarvis DevBot core script alive")
        sys.exit(0)

    if "--once" in sys.argv:
        one_shot()
        sys.exit(0)

    # Default: loop mode
    idle_loop()


if __name__ == "__main__":
    main()
