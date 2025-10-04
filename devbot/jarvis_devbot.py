#!/usr/bin/env python3
"""
Jarvis DevBot – minimal repo helper used by GitHub Actions and local runs.

Usage:
  python devbot/jarvis_devbot.py --test    # CI self-check (fast, no edits)
  python devbot/jarvis_devbot.py --once    # one-shot maintenance task
  python devbot/jarvis_devbot.py           # idle loop placeholder (future)

Env (from .env in repo root):
  OPENAI_API_KEY   = sk-...
  GITHUB_TOKEN     = ghp_...
  GITHUB_REPO      = owner/EmpireOS
  JARVIS_DEVBOT_ACTIVE = true
  JARVIS_DEVBOT_NAME   = JarvisDevBot
"""

from __future__ import annotations
import argparse
import os
import sys
import time
import shlex
import subprocess
from pathlib import Path

# Paths
HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[1] if HERE.name else Path.cwd()

# ---------------- helpers ----------------
def ok(msg: str) -> None:
    print(f"✅ {msg}")

def info(msg: str) -> None:
    print(f"ℹ️  {msg}")

def warn(msg: str) -> None:
    print(f"⚠️  {msg}")

def fail(msg: str, code: int = 1) -> None:
    print(f"❌ {msg}")
    sys.exit(code)

def run(cmd: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return the CompletedProcess (text mode)."""
    info(f"$ {cmd}")
    p = subprocess.run(
        shlex.split(cmd),
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        env=os.environ.copy(),
    )
    if p.stdout:
        print(p.stdout.strip())
    if p.stderr:
        print(p.stderr.strip())
    if check and p.returncode != 0:
        fail(f"Command failed: {cmd} (exit {p.returncode})")
    return p

# ---------------- env ----------------
def load_env(dotenv_path: Path | None = None) -> None:
    """Tiny .env loader (KEY=VALUE lines)."""
    p = dotenv_path or (REPO_ROOT / ".env")
    if not p.exists():
        warn(f".env not found at {p}")
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip())

def require_env(keys: list[str]) -> None:
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        fail(f"Missing required env vars: {', '.join(missing)}")

# ---------------- checks ----------------
def check_git() -> None:
    p = run("git rev-parse --is-inside-work-tree", check=False)
    if p.returncode != 0 or "true" not in (p.stdout or "").lower():
        fail("Not inside a git repository (run from repo root)")

def check_docker() -> None:
    # Docker might not be installed on the CI runner; make this non-fatal in CI
    p = run("docker ps", check=False)
    if p.returncode == 0:
        ok("Docker CLI available")
    else:
        warn("Docker CLI not available (ok for CI)")

# ---------------- tasks ----------------
def test_mode() -> int:
    """Fast self-check for CI."""
    ok("Jarvis DevBot test mode")

    # Load .env if present (local dev); on CI, secrets may come via env
    load_env()

    # Required keys for later phases; keep test tolerant for local first run
    required = ["GITHUB_REPO"]
    # Only require tokens if set as active
    if os.environ.get("JARVIS_DEVBOT_ACTIVE", "").lower() in ("1", "true", "yes"):
        required += ["OPENAI_API_KEY", "GITHUB_TOKEN"]
    require_env(required)

    # Tooling checks
    check_git()
    ok(".env check complete")
    check_docker()
    ok("Self-check passed")
    return 0

def one_shot_maintenance() -> int:
    """Create/confirm baseline project folders and leave a breadcrumb."""
    load_env()
    wf_dir = REPO_ROOT / ".github" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    ok(f"Workflows dir ready at {wf_dir}")

    marker = REPO_ROOT / ".jarvis_devbot.ok"
    marker.write_text("JarvisDevBot baseline initialized.\n")
    ok(f"Wrote marker: {marker}")

    # Example: ensure memory dir exists for future phases
    mem = REPO_ROOT / "memory"
    mem.mkdir(exist_ok=True)
    (mem / "memory.txt").touch(exist_ok=True)
    ok("Memory store ensured")

    return 0

# ---------------- main ----------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="Run quick self-check & exit")
    ap.add_argument("--once", action="store_true", help="Run one maintenance cycle & exit")
    args = ap.parse_args()

    if args.test:
        return test_mode()

    if args.once:
        return one_shot_maintenance()

    # Idle loop placeholder (for future: watch repo, open PRs, etc.)
    load_env()
    ok("Jarvis DevBot is active (idle). Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nBye!")
        return 0

if __name__ == "__main__":
    sys.exit(main())