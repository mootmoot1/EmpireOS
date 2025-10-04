<<<<<<< HEAD
#!/usr/bin/env python3
<<<<<<< HEAD
import os, sys, time, json, textwrap, subprocess, base64
from pathlib import Path
import requests
=======
import os, sys, time, json, textwrap, subprocess, requests
from pathlib import Path
>>>>>>> ff34bfc (devbot: target dev branch for PRs)

REPO_ROOT = Path(__file__).resolve().parents[1]
GITHUB_API = "https://api.github.com"

def sh(cmd, cwd=REPO_ROOT):
    print(f"$ {cmd}")
<<<<<<< HEAD
    out = subprocess.check_output(cmd, shell=True, cwd=str(cwd))
    return out.decode().strip()

def gh_get(path, token):
    r = requests.get(f"{GITHUB_API}{path}", headers={"Authorization": f"Bearer {token}", "Accept":"application/vnd.github+json"})
    r.raise_for_status()
    return r.json()

def gh_post(path, token, data):
    r = requests.post(f"{GITHUB_API}{path}",
                      headers={"Authorization": f"Bearer {token}", "Accept":"application/vnd.github+json"},
                      json=data)
    r.raise_for_status()
    return r.json()

def ensure_git_identity():
    try:
      sh('git config user.name')
    except:
      sh('git config user.name "Jarvis DevBot"')
      sh('git config user.email "bot@jarvis.local"')

def process_issues():
    token = os.environ["GITHUB_TOKEN"]
    repo_full = os.environ["REPO_FULL"]  # e.g. mootmoot1/EmpireOS
    # 1) fetch open issues with label jarvis:task
    issues = gh_get(f"/repos/{repo_full}/issues?state=open&labels=jarvis:task", token)
    if not issues:
        print("No jarvis:task issues found.")
        return 0

    ensure_git_identity()

    for issue in issues:
        number = issue["number"]
        title  = issue["title"]
        body   = issue.get("body") or ""
        branch = f"jarvis/issue-{number}"

        # Skip if a PR already exists for this issue
        prs = gh_get(f"/repos/{repo_full}/pulls?head={repo_full.split('/')[0]}:{branch}&state=open", token)
        if prs:
            print(f"Issue #{number}: PR already open. Skipping.")
            continue

        # 2) Create a branch from main
        sh("git fetch origin main")
        sh("git checkout -B " + branch + " origin/main")

        # 3) Make a visible, harmless change to prove the loop (edit README.md)
        readme = REPO_ROOT / "README.md"
        stamp  = f"\n\n> Jarvis DevBot touched this in response to Issue #{number}: **{title}**\n"
        readme.write_text(readme.read_text() + stamp, encoding="utf-8")

        sh("git add README.md")
        sh(f'git commit -m "Jarvis: link issue #{number} ({title})"')
        sh(f"git push -u origin {branch}")

        # 4) Open a PR
        pr = gh_post(f"/repos/{repo_full}/pulls", token, {
            "title": f"[Jarvis] {title}",
            "head": branch,
            "base": "main",
            "body": textwrap.dedent(f"""
            Automated PR for Issue #{number}.

            **Issue Title:** {title}

            ---
            _This is a smoke test PR created by Jarvis DevBot. Once you confirm the flow,
            we will switch from README edits to real code changes inside `api/` and `hud/`._
            """).strip()
        })
        print(f"Opened PR #{pr['number']} for Issue #{number}")

    return 0

if __name__ == "__main__":
    if "--test" in sys.argv:
        print("✅ DevBot core script loads.")
        sys.exit(0)
    if "--process-issues" in sys.argv:
        sys.exit(process_issues())
    print("Usage: jarvis_devbot.py [--test|--process-issues]")
    sys.exit(2)
=======
    return subprocess.check_output(cmd, shell=True, cwd=str(cwd)).decode().strip()

def gh_get(p,t): r=requests.get(f"{GITHUB_API}{p}",headers={"Authorization":f"Bearer {t}","Accept":"application/vnd.github+json"});r.raise_for_status();return r.json()
def gh_post(p,t,d): r=requests.post(f"{GITHUB_API}{p}",headers={"Authorization":f"Bearer {t}","Accept":"application/vnd.github+json"},json=d);r.raise_for_status();return r.json()

def ensure_git_identity():
    try: sh('git config user.name')
    except: sh('git config user.name "Jarvis DevBot"');sh('git config user.email "bot@jarvis.local"')

def process_issues():
    t=os.environ["GITHUB_TOKEN"]; repo=os.environ["REPO_FULL"]
    issues=gh_get(f"/repos/{repo}/issues?state=open&labels=jarvis:task",t)
    if not issues: print("No jarvis:task issues found."); return 0
    ensure_git_identity()
    for i in issues:
        n=i["number"]; title=i["title"]; body=i.get("body") or ""; branch=f"jarvis/issue-{n}"
        prs=gh_get(f"/repos/{repo}/pulls?head={repo.split('/')[0]}:{branch}&state=open",t)
        if prs: print(f"Issue #{n}: PR already open."); continue
        sh("git fetch origin main"); sh("git checkout -B "+branch+" origin/main")
        readme=REPO_ROOT/"README.md"; stamp=f"\n\n> Jarvis touched this for issue #{n}: **{title}**\n"
        readme.write_text(readme.read_text()+stamp,encoding="utf-8")
        sh("git add README.md"); sh(f'git commit -m "Jarvis: link issue #{n} ({title})"'); sh(f"git push -u origin {branch}")
        pr=gh_post(f"/repos/{repo}/pulls",t,{"title":f"[Jarvis] {title}","head":branch,"base":"dev",
            "body":textwrap.dedent(f"Automated PR for issue #{n}: {title}")}); print(f"Opened PR #{pr['number']}")
    return 0

if __name__=="__main__":
    if "--test" in sys.argv: print("✅ DevBot core script loads."); sys.exit(0)
    if "--process-issues" in sys.argv: sys.exit(process_issues())
    print("Usage: jarvis_devbot.py [--test|--process-issues]"); sys.exit(2)
>>>>>>> ff34bfc (devbot: target dev branch for PRs)
=======
import os, sys, shutil, subprocess
def ok(msg): print(f"✅ {msg}")
def fail(msg): print(f"❌ {msg}"); sys.exit(1)

def have(cmd): return shutil.which(cmd) is not None
def main():
    ok("Jarvis DevBot test start")
    # optional .env che       if os.path.exists(".env"):
        ok(".env present")
    else:
        print("ℹ️ .env not found (ok for CI)")
    if have("git"): ok("git available")
    else: fail(   t missing")
    ok("Test completed")
if __name__ == "__main__": main()
>>>>>>> 44dcaef (Reset to minimal, stable CI (dev→PR, nightly self-check, devbot CI))
