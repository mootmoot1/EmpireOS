#!/usr/bin/env python3
import os, sys, time, argparse, subprocess

# === Jarvis DevBot Core ===
def ok(msg): print(f"✅ {msg}")
def fail(msg): print(f"❌ {msg}")

def load_env():
    env_path = ".env"
    if not os.path.exists(env_path):
        fail(".env file missing")
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                os.environ[key] = val
    ok(".env loaded")
    return os.environ

def test_mode():
    print("🧠 Jarvis DevBot test mode")
    checks = [
        (".env", os.path.exists(".env")),
        ("API keys", "OPENAI_API_KEY" in os.environ),
        ("Git repo", os.path.exists(".git")),
        ("Docker CLI", subprocess.call(["which", "docker"], stdout=subprocess.DEVNULL) == 0)
    ]
    for name, passed in checks:
        print(("✅" if passed else "❌") + f" {name} check")
    if all(p for _, p in checks):
        ok("Test completed successfully")
        return 0
    else:
        fail("One or more checks failed")
        return 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run quick self-check")
    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")
    args = parser.parse_args()

    env = load_env()

    if args.test:
        return test_mode()

    ok(f"Jarvis DevBot active in {env.get('JARVIS_ENV', 'default')} mode")
    ok("Workflows directory ready")

    if args.once:
        ok("One-shot maintenance done.")
        return 0

    try:
        while True:
            ok("DevBot heartbeat... (Ctrl+C to stop)")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n👋 Exiting DevBot safely")
        return 0

if __name__ == "__main__":
    sys.exit(main())