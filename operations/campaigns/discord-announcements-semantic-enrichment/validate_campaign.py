#!/usr/bin/env python3
"""Validate the Discord announcement campaign and stacked reconciliation outputs."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
SEM = REPO / "archive/semantic/discord-announcements"
RECON = REPO / "archive/semantic/reconciliation"
RAW = REPO / "archive/raw/discord-announcements/star-atlas-discord-announcements.md"


def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def jsonl(path: Path) -> list[dict]: return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
def run(args: list[str]): return subprocess.run(args, cwd=REPO, text=True, capture_output=True, encoding="utf-8", errors="replace")


def main() -> None:
    failures, checks = [], {}
    def require(ok, name, detail):
        checks[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok: failures.append(f"{name}: {detail}")
    deterministic = sorted([p for root in (SEM, RECON, OPS, REPO / "archive/source-records/discord-announcements") for p in root.rglob("*") if p.is_file() and p.name not in {"manifest.json", "validation-report.json", "validation-report.md"} and (OPS / "input-package") not in p.parents and p.suffix != ".pyc"])
    before = {p.relative_to(REPO).as_posix(): digest(p) for p in deterministic}
    generated = run([sys.executable, str(OPS / "build_campaign.py")])
    after = {p.relative_to(REPO).as_posix(): digest(p) for p in deterministic}
    require(generated.returncode == 0 and before == after, "deterministic_regeneration", "generator must reproduce every output byte-for-byte")
    records = jsonl(SEM / "announcement-semantic-records.jsonl")
    promotions = jsonl(SEM / "promotion-candidate-decisions.jsonl")
    timelines = jsonl(SEM / "timeline-candidate-decisions.jsonl")
    pc = json.loads((SEM / "promotion-candidates.json").read_text(encoding="utf-8"))["candidates"]
    tc = json.loads((SEM / "timeline-candidates.json").read_text(encoding="utf-8"))["candidates"]
    clusters = json.loads((SEM / "duplicate-clusters.json").read_text(encoding="utf-8"))["clusters"]
    ids = {r["source_id"] for r in records}
    require(len(records) == len(promotions) == len(timelines) == len(ids) == 1071, "record_and_decision_coverage", "exactly 1,071 unique messages and two complete decision layers")
    require(min(r["timestamp"] for r in records).startswith("2021-03-16") and max(r["timestamp"] for r in records).startswith("2026-07-12"), "date_coverage", "earliest 2021-03-16 and latest 2026-07-12")
    by_id = {r["source_id"]: r for r in records}
    require(all(p["supporting_captions"] and p["supporting_captions"][0]["text"] == by_id[p["source_id"]]["content"] and (p["candidate_reasons"] if p["eligible"] else p["exclusion_reason"]) for p in promotions), "promotion_decisions_supported", "every inclusion/exclusion has exact source text and reasons")
    require(all(t["supporting_captions"] and t["supporting_captions"][0]["text"] == by_id[t["source_id"]]["content"] and ((t["event_type"] and t["date_basis"] and t["timeline_reasons"]) if t["eligible"] else t["exclusion_reason"]) for t in timelines), "timeline_decisions_supported", "every timeline decision has exact text plus event/date basis or exclusion")
    require({x["source_id"] for x in pc} == {x["source_id"] for x in promotions if x["eligible"]} and {x["source_id"] for x in tc} == {x["source_id"] for x in timelines if x["eligible"]}, "candidate_reconciliation", "candidate indexes equal eligible decisions")
    require(all(r["author_attribution_status"] == "INFERRED_FROM_EXPORT_GROUPING_NOT_INDEPENDENTLY_VERIFIED" and "SOURCE_EXPORT_COLLECTION_COMPLETE_FALSE_WARNING_PRESERVED" in r["research_gaps"] for r in records), "provenance_warnings", "collection and authorship warnings preserved on every record")
    require(all((REPO / f"archive/source-records/discord-announcements/{source_id}.json").exists() for source_id in ids), "no_orphan_messages", "every semantic message has a source record")
    require(all(set(c["member_source_ids"]) <= ids and c["strongest_candidate_id"] in c["member_source_ids"] and c["evidence_preserved"] for c in clusters), "duplicate_clusters", "clusters reference preserved evidence and a strongest member")
    require(digest(RAW) == "568ac1560e76f60eb908515caef3ca35e84931313eb2ce65c5316759c85da335", "raw_export_checksum", "original Discord export byte-for-byte checksum")
    parsed = 0
    for root in (SEM, RECON, OPS, REPO / "archive/source-records/discord-announcements"):
        for path in root.rglob("*"):
            if not path.is_file(): continue
            try:
                if path.suffix == ".json": json.loads(path.read_text(encoding="utf-8")); parsed += 1
                elif path.suffix == ".jsonl": [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]; parsed += 1
                elif path.suffix in {".md", ".py"}: path.read_text(encoding="utf-8")
            except Exception as exc: failures.append(f"parse failure {path.relative_to(REPO)}: {exc}")
    require(not any("parse failure" in x for x in failures), "json_utf8_parse", f"parsed {parsed} JSON/JSONL artifacts")
    manifest = json.loads((OPS / "manifest.json").read_text(encoding="utf-8"))
    require(all((REPO / e["path"]).exists() and (REPO / e["path"]).stat().st_size == e["bytes"] and digest(REPO / e["path"]) == e["sha256"] for e in manifest["preserved_inputs"] + manifest["generated_outputs"]), "manifest_reconciliation", "all recorded bytes and SHA-256 values match")
    branch_files = run(["git", "diff", "--name-only", "ingestion/social-governance-semantic-enrichment...HEAD"]).stdout.splitlines() + [x[3:] for x in run(["git", "status", "--porcelain"]).stdout.splitlines() if len(x) > 3]
    require(not any(x.startswith(("knowledge/", "graph/", "publication/")) for x in branch_files), "canonical_layers_unchanged", "knowledge, graph, and publication are untouched")
    require(not any("Star_Atlas_Discord_Announcements_Semantic_Enrichment.zip" in x for x in branch_files), "discord_not_duplicated", "nested Discord ZIP is not ingested")
    require(run(["git", "diff", "--check"]).returncode == 0, "git_diff_check", "no whitespace errors")
    report = {"campaign_id": "discord-announcements-semantic-enrichment", "status": "PASS" if not failures else "FAIL", "counts": {"semantic_records": len(records), "promotion_candidates": len(pc), "timeline_candidates": len(tc), "duplicate_clusters": len(clusters)}, "checks": checks, "warnings": ["Source export states Collection complete: no.", "Author grouping is not independently verified.", "Candidate confidence is extraction quality, not factual truth."], "failures": failures}
    (OPS / "validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OPS / "validation-report.md").write_text("# Validation Report\n\nOverall status: **" + report["status"] + "**\n\n" + "\n".join(f"- **{v['status']} — {k}**: {v['detail']}" for k,v in checks.items()) + ("\n\n## Failures\n\n" + "\n".join(f"- {x}" for x in failures) if failures else "") + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures: raise SystemExit(1)


if __name__ == "__main__": main()
