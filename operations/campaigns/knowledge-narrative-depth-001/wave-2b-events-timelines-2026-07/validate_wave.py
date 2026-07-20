"""Validate Wave 2B."""
from __future__ import annotations
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; HERE=Path(__file__).resolve().parent; BUILD=HERE/"build_wave.py"
REQ={"title","seo_title","seo_description","knowledge_status","as_of","confidence","evidence_basis","known_limitations","research_gaps","review_after"}
def sha(p): return hashlib.sha256(p.read_text(encoding="utf-8").replace("\r\n","\n").encode()).hexdigest()
def run(*a): return subprocess.run(a,cwd=ROOT,text=True,encoding="utf-8",errors="replace",capture_output=True,check=False)
def meta(t): return set(re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):",t.split("---",2)[1],re.M)) if t.startswith("---\n") else set()
def main():
 errors=[]; inv=json.loads((HERE/"page-inventory.json").read_text(encoding="utf-8")); pages=[ROOT/x["path"] for x in inv["pages"]]; generated=sorted(HERE.glob("*.json"))+sorted((HERE/"evidence-packets").glob("*.json")); before={str(p):sha(p) for p in generated}; a=run(sys.executable,str(BUILD)); middle={str(p):sha(p) for p in generated}; c=run(sys.executable,str(BUILD)); after={str(p):sha(p) for p in generated}
 checks={"deterministic_generation":a.returncode==c.returncode==0 and before==middle==after,"page_count":len(pages)==11,"required_metadata":all(REQ<=meta(p.read_text(encoding="utf-8")) for p in pages),"review_sections":all("## Review status" in p.read_text(encoding="utf-8") for p in pages),"packet_count":len(list((HERE/"evidence-packets").glob("*.json")))==11}
 broken=[]
 for p in pages:
  for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)",p.read_text(encoding="utf-8")):
   if target.startswith(("http://","https://","#")): continue
   clean=target.split("#",1)[0]
   if clean and not (p.parent/clean).resolve().exists(): broken.append(f"{p.relative_to(ROOT)} -> {target}")
 checks["internal_links"]=not broken; changed=set(run("git","diff","--name-only","origin/main...HEAD").stdout.splitlines())|set(run("git","diff","--name-only").stdout.splitlines()); checks["scope"]=not any(x.startswith(("archive/","graph/","publication/")) for x in changed); checks["git_diff_check"]=run("git","diff","--check").returncode==0
 errors.extend(f"failed check: {k}" for k,v in checks.items() if not v); errors.extend(broken); status="PASS" if not errors else "FAIL"; report={"campaign_id":"knowledge-narrative-depth-wave-2b-events-timelines-2026-07","status":status,"checks":checks,"errors":errors}; (HERE/"validation-report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8",newline="\n"); (HERE/"validation-report.md").write_text("# Wave 2B Validation\n\n**Result:** `"+status+"`\n\n"+"\n".join(f"- {'PASS' if v else 'FAIL'}: {k}" for k,v in checks.items())+"\n",encoding="utf-8",newline="\n"); print(json.dumps(report)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
