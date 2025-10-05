#!/usr/bin/env python3
import sys
print("Jarvis DevBot core script alive ✅")
sys.exit(0)
=======
import subprocess, sys, time
from typing import Optional, List
from pathlib import Path

def run(cmd: List[str], cwd: Optional[Path] = None, check: bool = False):
    """Run a system command safely and log output."""
    print(f"🔧 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error ({result.returncode}): {result.stderr.strip()}")
    else:
        print(f"✅ Success: {result.stdout.strip()}")
    return result

def one_shot():
    print("🤖 Jarvis DevBot started (one-time maintenance)")
    run(["git", "status"])
    run(["git", "pull"])
    print("🧠 Maintenance complete.")
    return 0

def idle_loop():
    print("💤 Jarvis DevBot idle mode (CI-safe loop)")
    while True:
        run(["echo", "Checking system health..."])
        time.sleep(5)

if __name__ == "__main__":
    if "--once" in sys.argv:
        sys.exit(one_shot())
    else:
        sys.exit(idle_loop())
