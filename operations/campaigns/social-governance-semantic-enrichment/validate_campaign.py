#!/usr/bin/env python3
"""Strict deterministic validation for the reviewed social/governance campaign."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse


REPO = Path(__file__).resolve().parents[3]
OPS = REPO / "operations/campaigns/social-governance-semantic-enrichment"
SOCIAL = REPO / "archive/semantic/social-media"
GOVERNANCE = REPO / "archive/semantic/governance"
GENERATOR = OPS / "build_campaign.py"
ALLOWED_REVISION_PREFIXES = ("archive/semantic/social-media/", "archive/semantic/governance/", "operations/campaigns/social-governance-semantic-enrichment/")
CAMPAIGN_ROOTS = [
    REPO / "archive/raw/social-governance-semantic-enrichment",
    REPO / "archive/normalized/social-governance-semantic-enrichment",
    REPO / "archive/source-records/social-governance-semantic-enrichment",
    SOCIAL, GOVERNANCE, OPS,
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=REPO, text=True, capture_output=True, encoding="utf-8", errors="replace")


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    failures: list[str] = []
    warnings = [
        "Inherited Wave 1.5 reconciliation baseline contains 962 records while the legacy validator expects 960; unrelated reconciliation records are unchanged.",
        "Confidence measures extraction quality, not factual truth.",
        "Linked social-media binaries remain outside the supplied package.",
    ]
    checks: dict[str, object] = {}

    deterministic_paths = sorted([p for root in (SOCIAL, GOVERNANCE, OPS) for p in root.rglob("*") if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts and p.name not in {"manifest.json", "validation-report.json", "validation-report.md"} and (OPS / "input-package") not in p.parents])
    before = {p.relative_to(REPO).as_posix(): digest(p) for p in deterministic_paths}
    generated = command([sys.executable, str(GENERATOR)])
    after = {p.relative_to(REPO).as_posix(): digest(p) for p in deterministic_paths}
    checks["deterministic_regeneration"] = generated.returncode == 0 and before == after
    if not checks["deterministic_regeneration"]:
        failures.append("deterministic regeneration changed outputs or failed")

    files = sorted({p for root in CAMPAIGN_ROOTS for p in root.rglob("*") if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts})
    parsed_json = parsed_jsonl = 0
    for path in files:
        try:
            if path.suffix.lower() != ".xlsx":
                path.read_text(encoding="utf-8")
            if path.suffix.lower() == ".json":
                json.loads(path.read_text(encoding="utf-8")); parsed_json += 1
            elif path.suffix.lower() == ".jsonl":
                for line in path.read_text(encoding="utf-8").splitlines():
                    if line.strip(): json.loads(line); parsed_jsonl += 1
        except (UnicodeError, json.JSONDecodeError) as exc:
            failures.append(f"parse failure: {path.relative_to(REPO)}: {exc}")
    checks.update({"campaign_files_checked": len(files), "json_documents_parsed": parsed_json, "jsonl_records_parsed": parsed_jsonl})

    raw_csv = REPO / "archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv"
    with raw_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    posts = jsonl(REPO / "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl")
    semantic = jsonl(SOCIAL / "staratlas-posts-semantic.jsonl")
    promotion_decisions = jsonl(SOCIAL / "promotion-candidate-decisions.jsonl")
    timeline_decisions = jsonl(SOCIAL / "timeline-candidate-decisions.jsonl")
    promotions = json.loads((SOCIAL / "promotion-candidates.json").read_text(encoding="utf-8"))["candidates"]
    timelines = json.loads((SOCIAL / "timeline-candidates.json").read_text(encoding="utf-8"))["candidates"]
    clusters = json.loads((SOCIAL / "duplicate-clusters.json").read_text(encoding="utf-8"))["clusters"]
    pips = json.loads((GOVERNANCE / "pip-registry-semantic.json").read_text(encoding="utf-8"))["proposals"]
    seed = json.loads((REPO / "archive/normalized/social-governance-semantic-enrichment/governance/pip-1-33-registry-seed.json").read_text(encoding="utf-8"))

    def require(condition: bool, name: str, failure: str) -> None:
        checks[name] = bool(condition)
        if not condition: failures.append(failure)

    post_ids = {x["post_id"] for x in posts}
    source_ids = {x["source_id"] for x in posts}
    require(len(rows) == 799, "raw_rows", f"raw row count is {len(rows)}, expected 799")
    require(len(posts) == len(semantic) == len(promotion_decisions) == len(timeline_decisions) == 796, "social_decision_coverage", "social or decision count does not equal 796")
    require(len(post_ids) == 796 and post_ids == {x["post_id"] for x in semantic} == {x["post_id"] for x in promotion_decisions} == {x["post_id"] for x in timeline_decisions}, "unique_post_ids_reconcile", "post IDs do not reconcile")
    require(sum(not x["is_retweet"] for x in posts) == 528 and sum(bool(x["is_retweet"]) for x in posts) == 268, "original_retweet_counts", "original/retweet counts do not reconcile")
    require(all(x["content"] == next(p["content"] for p in posts if p["post_id"] == x["post_id"]) for x in semantic), "semantic_text_preserved", "semantic social text differs from normalized evidence")
    retweet_ids = {x["source_id"] for x in semantic if x["is_retweet"]}
    require(all(not x["eligible"] and x["decision"] == "NOT_ELIGIBLE" for x in promotion_decisions if x["source_id"] in retweet_ids), "retweets_not_promoted", "a retweet is eligible for first-party promotion")
    require(all(x["decision_reasons"] and x["supporting_text"] and (x["eligible"] or x["exclusion_reason"]) for x in promotion_decisions), "promotion_decisions_complete", "a promotion decision lacks support/reasons")
    require(all(x["timeline_reasons"] and x["supporting_text"] and (not x["eligible"] or (x["event_type"] and x["event_date"] and x["date_basis"])) and (x["eligible"] or x["exclusion_reason"]) for x in timeline_decisions), "timeline_decisions_complete", "a timeline decision lacks event/date support or exclusion reason")
    require({x["source_id"] for x in promotions} == {x["source_id"] for x in promotion_decisions if x["eligible"]}, "promotion_candidates_reconcile", "promotion candidates do not reconcile to decisions")
    require({x["source_id"] for x in timelines} == {x["source_id"] for x in timeline_decisions if x["eligible"]}, "timeline_candidates_reconcile", "timeline candidates do not reconcile to decisions")
    require(all(set(cluster["member_source_ids"]) <= source_ids and cluster["strongest_candidate_id"] in cluster["member_source_ids"] for cluster in clusters), "duplicate_clusters_reconcile", "duplicate cluster references an invalid source ID")
    require(all(urlparse(x["post_url"]).scheme == "https" for x in semantic), "social_urls_valid", "a social URL is not HTTPS")

    require(len(pips) == len(seed) == 33 and [x["pip_number"] for x in pips] == list(range(1, 34)), "pip_sequence", "PIP sequence does not reconcile")
    require({x["proposal_uuid"] for x in pips} == {x["proposal_uuid"] for x in seed} and len({x["proposal_uuid"] for x in pips}) == 33, "pip_uuids", "PIP UUIDs do not reconcile")
    require(all(x["title"] and x["reviewed_title"] and x["author"] and x["proposal_category"] and x["publication_date"] and x["vote_start"] and x["vote_end"] and x["proposal_text"] and x["proposal_brief"] for x in pips), "pip_required_metadata", "a PIP is missing required reviewed or source metadata")
    require(all(x["human_review_status"] == "REVIEWED" and x["reviewed_institutional_significance"] for x in pips), "pip_human_review_complete", "not all PIPs have reviewed institutional records")
    binary = [x for x in pips if x["vote_mechanism"] == "BINARY_PVP"]
    elections = [x for x in pips if x["vote_mechanism"] == "RANKED_CHOICE_ELECTION"]
    require(all(x["reviewed_result"] == ("PASSED" if Decimal(x["yes_pvp"]) > Decimal(x["no_pvp"]) else "FAILED") for x in binary), "binary_result_rule", "binary result does not follow YES > NO")
    require(all("ABSTAIN_RECORDED_NOT_DECISIVE" in x["decision_formula"] for x in binary), "abstention_non_decisive", "binary formula does not preserve abstention boundary")
    require({x["pip_number"] for x in elections} == {6, 7, 11, 25, 27} and all(x["yes_pvp"] is None and x["no_pvp"] is None for x in elections), "elections_not_binary", "an election was processed as binary")
    require(all(next(x for x in pips if x["pip_number"] == n)["reviewed_result"] == "FAILED" for n in [13, 15, 19, 26]), "required_failed_pips", "PIP-13, 15, 19, or 26 is not failed")
    require(all(next(x for x in pips if x["pip_number"] == n)["reviewed_result"] == "UNKNOWN" and not next(x for x in pips if x["pip_number"] == n)["election_winners"] for n in [11, 25, 27]), "unresolved_elections", "PIP-11, 25, or 27 improperly has a winner")
    require(next(x for x in pips if x["pip_number"] == 23)["supersedes"] == [4], "pip_23_supersedes_4", "PIP-23 does not supersede PIP-4")
    require(all(x["raw_portal_status"] == "Proposal_Activated_Pending_Open_Voting" and x["reviewed_result"] != x["raw_portal_status"] for x in pips), "stale_status_separated", "stale portal status was treated as final result")
    require(all(x["execution_state"] not in {"IMPLEMENTED", "PARTIALLY_IMPLEMENTED"} and not x["execution_evidence"] and x["execution_evidence_status"] == "MISSING_INDEPENDENT_PRIMARY_EVIDENCE" for x in pips), "implementation_evidence_boundary", "implementation was inferred without independent evidence")
    require(len(json.loads((GOVERNANCE / "pip-promotion-candidates.json").read_text(encoding="utf-8"))["candidates"]) == 33, "pip_promotion_inputs", "not all PIPs have promotion inputs")
    require(all((REPO / f"archive/source-records/social-governance-semantic-enrichment/governance/{x['source_id']}.json").exists() for x in pips), "no_orphan_pips", "a PIP source record is missing")
    require(all((REPO / f"archive/source-records/social-governance-semantic-enrichment/social-media/{x['source_id']}.json").exists() for x in semantic), "no_orphan_social_records", "a social source record is missing")
    for pip in pips:
        raw = next((REPO / "archive/raw/social-governance-semantic-enrichment/governance/pip-captures").glob(f"pip-{pip['pip_number']:02d}-{pip['proposal_uuid']}.json"), None)
        require(raw is not None and digest(raw) == pip["content_checksum"], f"pip_{pip['pip_number']}_checksum", f"PIP-{pip['pip_number']} raw checksum mismatch")

    campaign_source_ids = {x["source_id"] for x in posts} | {x["source_id"] for x in pips}
    require(len(campaign_source_ids) == 829, "source_ids_unique", "campaign source IDs are not unique")
    other_names = {p.stem for p in (REPO / "archive/source-records").rglob("*.json") if "social-governance-semantic-enrichment" not in p.parts}
    require(not (campaign_source_ids & other_names), "no_source_id_collisions", "campaign source IDs collide with another source family")

    schema = command([sys.executable, "operations/tests/schema/test_schema_compatibility.py"])
    require(schema.returncode == 0, "schema_tests", "schema compatibility tests failed")
    sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "operations/pipeline/src"))
    try:
        from operations.tests.pipeline.test_inventory import test_audiovisual_content_is_retained_as_deferred_metadata, test_flatten_deduplicates_and_preserves_provenance
        from operations.tests.pipeline.test_normalize import test_does_not_merge_http_and_https_without_evidence, test_normalizes_youtube_variants, test_removes_tracking_and_fragment_and_sorts_query
        for test in [test_flatten_deduplicates_and_preserves_provenance, test_audiovisual_content_is_retained_as_deferred_metadata, test_removes_tracking_and_fragment_and_sorts_query, test_normalizes_youtube_variants, test_does_not_merge_http_and_https_without_evidence]: test()
        checks["pipeline_tests"] = True
    except Exception as exc:
        checks["pipeline_tests"] = False; failures.append(f"pipeline tests failed: {exc}")

    branch_paths = command(["git", "diff", "--name-only", "origin/main...HEAD"]).stdout.splitlines()
    branch_paths += [line[3:].strip().strip('"') for line in command(["git", "status", "--porcelain"]).stdout.splitlines() if len(line) >= 4]
    require(not any(path.startswith(("knowledge/", "graph/", "publication/")) for path in branch_paths), "canonical_layers_unchanged", "knowledge, graph, or publication changed")
    working_paths = [line[3:].strip().strip('"') for line in command(["git", "status", "--porcelain"]).stdout.splitlines() if len(line) >= 4]
    require(all(path.startswith(ALLOWED_REVISION_PREFIXES) for path in working_paths), "revision_allowed_paths_only", "revision changed a path outside semantic/operations scope")
    diff_check = command(["git", "diff", "--check"])
    require(diff_check.returncode == 0, "git_diff_check", "git diff --check failed")

    status = "PASS" if not failures else "FAIL"
    report = {"campaign_id": "social-governance-semantic-enrichment", "status": status, "checks": checks, "warnings": warnings, "failures": failures}
    (OPS / "validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Validation report", "", f"Overall status: **{status}**", "", "## Checks", ""]
    lines.extend(f"- **{'PASS' if bool(value) else 'FAIL'} — {name}**: `{value}`" for name, value in checks.items())
    lines += ["", "## Warnings", ""] + [f"- {warning}" for warning in warnings]
    if failures: lines += ["", "## Failures", ""] + [f"- {failure}" for failure in failures]
    (OPS / "validation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest_path = OPS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in manifest["generated_outputs"]:
        if entry["path"] in {"operations/campaigns/social-governance-semantic-enrichment/validation-report.json", "operations/campaigns/social-governance-semantic-enrichment/validation-report.md"}:
            path = REPO / entry["path"]; entry.update({"sha256": digest(path), "bytes": path.stat().st_size})
    manifest["status"] = status; manifest["validation"] = report
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for entry in manifest["preserved_inputs"] + manifest["generated_outputs"]:
        path = REPO / entry["path"]
        if not path.exists() or path.stat().st_size != entry["bytes"] or digest(path) != entry["sha256"]:
            failures.append(f"manifest mismatch: {entry['path']}")
    if failures and status == "PASS":
        raise SystemExit("manifest validation failed after report generation")
    print(json.dumps({"status": status, "campaign_files_checked": len(files), "json_documents_parsed": parsed_json, "jsonl_records_parsed": parsed_jsonl, "promotion_candidates": len(promotions), "timeline_candidates": len(timelines), "duplicate_clusters": len(clusters), "manifest_entries_checked": len(manifest["preserved_inputs"]) + len(manifest["generated_outputs"]), "failures": failures}, indent=2))
    if failures: raise SystemExit(1)


if __name__ == "__main__":
    main()
