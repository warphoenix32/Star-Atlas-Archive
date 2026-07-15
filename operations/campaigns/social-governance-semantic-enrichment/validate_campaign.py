#!/usr/bin/env python3
"""Dependency-free integrity validation for the social/governance campaign."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse


REPO = Path(__file__).resolve().parents[3]
OPS = REPO / "operations/campaigns/social-governance-semantic-enrichment"
CAMPAIGN_ROOTS = [
    REPO / "archive/raw/social-governance-semantic-enrichment",
    REPO / "archive/normalized/social-governance-semantic-enrichment",
    REPO / "archive/source-records/social-governance-semantic-enrichment",
    REPO / "archive/semantic/social-media",
    REPO / "archive/semantic/governance",
    OPS,
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    failures: list[str] = []
    files = sorted({p for root in CAMPAIGN_ROOTS for p in root.rglob("*") if p.is_file()})
    parsed_json = 0
    parsed_jsonl = 0
    for path in files:
        if path.suffix.lower() != ".xlsx":
            try:
                path.read_text(encoding="utf-8")
            except UnicodeError as exc:
                failures.append(f"UTF-8: {path.relative_to(REPO)}: {exc}")
        try:
            if path.suffix.lower() == ".json":
                json.loads(path.read_text(encoding="utf-8")); parsed_json += 1
            elif path.suffix.lower() == ".jsonl":
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    if line.strip(): json.loads(line); parsed_jsonl += 1
        except (UnicodeError, json.JSONDecodeError) as exc:
            failures.append(f"JSON: {path.relative_to(REPO)}: {exc}")

    raw_csv = REPO / "archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv"
    with raw_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    normalized_path = REPO / "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"
    posts = [json.loads(x) for x in normalized_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    semantic = [json.loads(x) for x in (REPO / "archive/semantic/social-media/staratlas-posts-semantic.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    pips = json.loads((REPO / "archive/semantic/governance/pip-registry-semantic.json").read_text(encoding="utf-8"))["proposals"]
    seed = json.loads((REPO / "archive/normalized/social-governance-semantic-enrichment/governance/pip-1-33-registry-seed.json").read_text(encoding="utf-8"))

    def require(condition: bool, message: str) -> None:
        if not condition: failures.append(message)

    require(len(rows) == 799, f"raw row count is {len(rows)}, expected 799")
    require(len(posts) == len(semantic) == 796, "normalized/semantic social counts do not both equal 796")
    require({x["post_id"] for x in posts} == {x["post_id"] for x in semantic}, "social post IDs do not reconcile")
    require(len({x["post_id"] for x in posts}) == 796, "normalized post IDs are not unique")
    require(sum(not x["is_retweet"] for x in posts) == 528 and sum(bool(x["is_retweet"]) for x in posts) == 268, "original/retweet counts do not reconcile")
    require(all(x["content"] == next(p["content"] for p in posts if p["post_id"] == x["post_id"]) for x in semantic), "semantic social content differs from normalized evidence")
    require(all(not x["promotion_targets"] for x in semantic if x["is_retweet"]), "a retweet has a promotion target")
    require(all(urlparse(x["post_url"]).scheme == "https" for x in semantic), "a social URL is not HTTPS")
    require(len(pips) == len(seed) == 33 and [x["pip_number"] for x in pips] == list(range(1, 34)), "PIP sequence does not reconcile")
    require({x["proposal_uuid"] for x in pips} == {x["proposal_uuid"] for x in seed}, "PIP UUIDs do not reconcile")
    require(len(list((REPO / "archive/raw/social-governance-semantic-enrichment/governance/pip-captures").glob("*.json"))) == 33, "raw PIP capture count is not 33")
    require(all(x["execution_state"] == "UNKNOWN" and not x["execution_evidence"] for x in pips), "execution was inferred without evidence")
    for pip in pips:
        raw = next((REPO / "archive/raw/social-governance-semantic-enrichment/governance/pip-captures").glob(f"pip-{pip['pip_number']:02d}-{pip['proposal_uuid']}.json"), None)
        require(raw is not None and digest(raw) == pip["content_checksum"], f"PIP-{pip['pip_number']} raw checksum mismatch")
        require((REPO / f"archive/source-records/social-governance-semantic-enrichment/governance/{pip['source_id']}.json").exists(), f"PIP-{pip['pip_number']} source record missing")

    manifest = json.loads((OPS / "manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["preserved_inputs"] + manifest["generated_outputs"]:
        path = REPO / entry["path"]
        require(path.exists(), f"manifest file missing: {entry['path']}")
        if path.exists():
            require(path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"], f"manifest mismatch: {entry['path']}")

    campaign_source_ids = {x["source_id"] for x in posts} | {x["source_id"] for x in pips}
    require(len(campaign_source_ids) == 829, "campaign source IDs are not unique")
    other_record_names = {p.stem for p in (REPO / "archive/source-records").rglob("*.json") if "social-governance-semantic-enrichment" not in p.parts}
    require(not (campaign_source_ids & other_record_names), "campaign source IDs collide with existing source-record filenames")

    status = "PASS" if not failures else "FAIL"
    print(json.dumps({
        "status": status, "campaign_files_checked": len(files), "json_documents_parsed": parsed_json,
        "jsonl_records_parsed": parsed_jsonl, "manifest_entries_checked": len(manifest["preserved_inputs"]) + len(manifest["generated_outputs"]),
        "failures": failures,
    }, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
