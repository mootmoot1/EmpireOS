#!/usr/bin/env python3
import os, sys, time, json, textwrap, subprocess, requests
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GITHUB_API = "https://api.github.com"

def sh(cmd, cwd=REPO_ROOT):
    print(f"$ {cmd}")
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
