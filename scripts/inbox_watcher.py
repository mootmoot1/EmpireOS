#!/usr/bin/env python3
import os, time, requests
from pathlib import Path
INBOX = Path.home()/"iCloud Drive"/"Jarvis-Inbox"
if not INBOX.exists(): INBOX = Path.home()/"Desktop"/"Jarvis-Inbox"
REPO=os.environ.get("GITHUB_REPOSITORY"); TOKEN=os.environ.get("GITHUB_TOKEN"); API="https://api.github.com"
def issue(t,b):
  r=requests.post(f"{API}/repos/{REPO}/issues",headers={"Authorization":f"Bearer {TOKEN}","Accept":"application/vnd.github+json"},json={"title":t[:256],"body":b,"labels":["jarvis:task"]}); r.raise_for_status(); return r.json()["html_url"]
def go():
  INBOX.mkdir(parents=True,exist_ok=True)
  seen=set()
  while True:
    for f in INBOX.glob("*.txt"):
      key=(f.name,f.stat().st_mtime,f.stat().st_size)
      if key in seen: continue
      lines=f.read_text(encoding="utf-8",errors="ignore").splitlines()
      url=issue(lines[0] if lines else "Jarvis task","\n".join(lines[1:]) or "(no body)")
      f.with_suffix(".done.txt").write_text(f"Issue: {url}\n",encoding="utf-8")
      f.unlink()
      print("✅",url); seen.add(key)
    time.sleep(3)
if __name__=="__main__": go()
