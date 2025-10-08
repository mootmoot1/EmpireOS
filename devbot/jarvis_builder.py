#!/usr/bin/env python3
import os, subprocess, textwrap, requests
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
def sh(cmd): return subprocess.check_output(cmd, shell=True, cwd=str(ROOT)).decode()
def gh_get(path,tok):
  r=requests.get(API+path,headers={"Authorization":f"Bearer {tok}","Accept":"application/vnd.github+json"});r.raise_for_status();return r.json()
def gh_post(path,tok,data):
  r=requests.post(API+path,headers={"Authorization":f"Bearer {tok}","Accept":"application/vnd.github+json"},json=data);r.raise_for_status();return r.json()
def scaffold(branch,issue_no,title,body):
  (ROOT/"scaffolds").mkdir(exist_ok=True); (ROOT/"tests").mkdir(exist_ok=True)
  (ROOT/"scaffolds"/f"ISSUE_{issue_no}_PLAN.md").write_text(textwrap.dedent(f"""# Build Plan for Issue #{issue_no}: {title}
## Notes
{body or "(no body)"}
## TODO
- [ ] Implement code
- [ ] Add/adjust tests
- [ ] Update README
"""),encoding="utf-8")
  (ROOT/"tests"/f"test_issue_{issue_no}.py").write_text("def test_placeholder():\n    assert True\n",encoding="utf-8")
  sh("git add scaffolds tests && git commit -m \"Jarvis scaffold for issue #%d: %s\""%(issue_no,title.replace('"','')))
  sh(f"git push -u origin {branch}")
def main():
  tok=os.environ["GITHUB_TOKEN"]; repo=os.environ["GITHUB_REPOSITORY"]
  sh('git config user.name "Jarvis DevBot"'); sh('git config user.email "bot@jarvis.local"')
  issues=gh_get(f"/repos/{repo}/issues?state=open&labels=jarvis:task",tok)
  if not issues: print("No jarvis:task issues"); return
  for it in issues:
    n=it["number"]; title=it["title"]; body=it.get("body") or ""
    branch=f"jarvis/issue-{n}"
    sh("git fetch origin main"); sh("git checkout -B "+branch+" origin/main")
    scaffold(branch,n,title,body)
    pr=gh_post(f"/repos/{repo}/pulls",tok,{"title":f"[Jarvis] {title}","head":branch,"base":"main","body":f"Automated scaffold for issue #{n}. Edit files in `scaffolds/` and `tests/`."})
    print(f"Opened PR #{pr['number']} for issue #{n}")
if __name__=="__main__": main()
