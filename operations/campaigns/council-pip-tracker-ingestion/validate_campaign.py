#!/usr/bin/env python3
"""Validate the Council tracker archival ingestion."""

from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
RAW = REPO / "archive/raw/governance/council-pip-tracker/Star_Atlas_DAO_Council_PIP_Tracker_and_Grading_Rubric.xlsx"
NORM = REPO / "archive/normalized/governance/council-pip-tracker"
SEM = REPO / "archive/semantic/governance/council-pip-tracker"
RECORDS = REPO / "archive/source-records/governance/council-pip-tracker"
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def jsonl(p): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def run(a): return subprocess.run(a,cwd=REPO,text=True,capture_output=True,encoding="utf-8",errors="replace")

def main():
    failures=[]; checks={}
    def req(ok,name,detail): checks[name]={"status":"PASS" if ok else "FAIL","detail":detail}; failures.extend([] if ok else [f"{name}: {detail}"])
    paths=sorted([p for root in (SEM,RECORDS,OPS) for p in root.rglob("*") if p.is_file() and p.name not in {"manifest.json","validation-report.json","validation-report.md"} and (OPS/"input-package") not in p.parents and p.suffix!=".pyc"])
    before={p.relative_to(REPO).as_posix():digest(p) for p in paths}; generated=run([sys.executable,str(OPS/"build_campaign.py")]); after={p.relative_to(REPO).as_posix():digest(p) for p in paths}
    req(generated.returncode==0 and before==after,"deterministic_regeneration","Council generator reproduces all outputs")
    tracker=jsonl(SEM/"council-pip-tracker-semantic-records.jsonl"); rubric=jsonl(SEM/"pip-evaluation-rubric-records.jsonl")
    req(len(tracker)==39,"tracker_records","39 operational tracker records")
    req(len(rubric)==80,"rubric_records","80 review-guidance records")
    req(len({x["source_id"] for x in tracker+rubric})==119 and len(list(RECORDS.glob("*.json")))==119,"source_record_reconciliation","119 unique source records")
    req(all(x["source_class"]=="TIER_1_COUNCIL_OPERATIONAL_TRACKER" and x["attribution_required"] for x in tracker),"operational_attribution","all tracker claims retain Council attribution")
    req(all(x["source_class"]=="TIER_1_COUNCIL_REVIEW_GUIDANCE" and "NOT_BINDING_LAW" in x["canonical_status"] for x in rubric),"rubric_authority_boundary","rubrics remain nonbinding review guidance")
    req(digest(RAW)=="6a477ee0ce428df4f04cd32b4a24bfb21b80bfa23341be38b192d2e4b0dadc24" and digest(NORM/"Star_Atlas_DAO_Council_Tracker_Normalized.xlsx")=="222aea1425fb358717a14d0a55e118b773ce09a22b6176087dc5d850e1cbb982","workbook_checksums","raw and normalized workbook hashes match package")
    sheet_files=["tracker","accomplishment_numbers","pip_step_process","lanzer_grading_rubric","carlos_grading_rubric"]
    req(all((NORM/f"{x}.csv").exists() and (NORM/f"{x}.json").exists() for x in sheet_files),"five_sheets_preserved","CSV and JSON for all five sheets")
    manifest=json.loads((OPS/"manifest.json").read_text(encoding="utf-8")); req(all((REPO/e["path"]).exists() and digest(REPO/e["path"])==e["sha256"] and (REPO/e["path"]).stat().st_size==e["bytes"] for e in manifest["preserved_inputs"]+manifest["generated_outputs"]),"manifest_reconciliation","all bytes and checksums reconcile")
    req(not list((REPO/"archive/raw/governance/council-pip-tracker").glob("*.zip")),"discord_not_duplicated","no nested Discord ZIP archived")
    req(run(["git","diff","--check"]).returncode==0,"git_diff_check","no whitespace errors")
    report={"campaign_id":"council-pip-tracker-ingestion","status":"PASS" if not failures else "FAIL","counts":{"source_sheets":5,"tracker_records":len(tracker),"rubric_records":len(rubric),"source_records":len(list(RECORDS.glob('*.json')))},"checks":checks,"warnings":["Modified timestamp is not preserved in the supplied package.","Artifact-tool import could not render the workbook because an embedded person entry lacks displayName; preserved normalized exports were used without rewriting the workbook."],"failures":failures}
    (OPS/"validation-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OPS/"validation-report.md").write_text("# Validation Report\n\nOverall status: **"+report["status"]+"**\n\n"+"\n".join(f"- **{v['status']} — {k}**: {v['detail']}" for k,v in checks.items())+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2));
    if failures: raise SystemExit(1)
if __name__=="__main__": main()
