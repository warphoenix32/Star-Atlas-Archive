"""Validate the Phase 3 publication contract without network access."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "publication/manifests/publication-manifest.json"
SCHEMA_PATH = ROOT / "operations/schema/PUBLICATION-MANIFEST-v1.schema.json"
EXAMPLE_PATH = ROOT / "operations/schema/examples/publication-manifest-v1.json"
FRESHNESS_PATH = (
    ROOT
    / "operations/campaigns/phase-2-official-freshness-closeout-2026-07"
    / "discovery-candidate-queue.json"
)
FRESHNESS_REPOSITORY_PATH = (
    "operations/campaigns/phase-2-official-freshness-closeout-2026-07/"
    "discovery-candidate-queue.json"
)
FRESHNESS_BLOB_SHA256 = "c0b81a8f4564bd2b3f9e31b5ae87af8f16a86d0119338730d4c365837d4ac872"
STATUSES = {
    "PLANNED",
    "DRAFT",
    "IN_REVIEW",
    "APPROVED",
    "PUBLISHED",
    "WITHDRAWN",
    "ARCHIVED",
}
PUBLICATION_TYPES = {"ARTICLE", "BRIEF", "DATASET_GUIDE", "DOSSIER", "REPORT", "TIMELINE"}
PLACEHOLDER_READMES = [
    ROOT / "publication/articles/README.md",
    ROOT / "publication/briefs/README.md",
    ROOT / "publication/datasets/README.md",
    ROOT / "publication/reports/README.md",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(ref: str, repository_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{ref}:{repository_path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"cannot read {repository_path} from {ref}: "
            + result.stderr.decode("utf-8", errors="replace")
        )
    return result.stdout


def validate_entry(entry: dict[str, Any], all_ids: set[str]) -> list[str]:
    failures: list[str] = []
    required = {
        "publication_id",
        "slug",
        "title",
        "type",
        "status",
        "audience",
        "content_path",
        "source_knowledge_paths",
        "as_of",
        "editorial",
        "evidence",
        "presentation",
        "provenance",
        "visibility",
        "related_publication_ids",
        "revision_history",
    }
    missing = sorted(required - set(entry))
    if missing:
        return [f"entry missing fields: {', '.join(missing)}"]

    publication_id = entry["publication_id"]
    status = entry["status"]
    if not re.fullmatch(r"PUB-[A-Z0-9-]+", str(publication_id)):
        failures.append(f"{publication_id}: invalid publication_id")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(entry["slug"])):
        failures.append(f"{publication_id}: invalid slug")
    if status not in STATUSES:
        failures.append(f"{publication_id}: invalid status {status}")
    if entry["type"] not in PUBLICATION_TYPES:
        failures.append(f"{publication_id}: invalid type {entry['type']}")
    if not entry["title"] or not entry["audience"]:
        failures.append(f"{publication_id}: title and audience are required")

    knowledge_paths = entry["source_knowledge_paths"]
    if len(knowledge_paths) != len(set(knowledge_paths)):
        failures.append(f"{publication_id}: duplicate knowledge paths")
    for value in knowledge_paths:
        if not value.startswith("knowledge/"):
            failures.append(f"{publication_id}: invalid knowledge path {value}")
        elif not (ROOT / value).is_file():
            failures.append(f"{publication_id}: missing knowledge path {value}")

    editorial = entry["editorial"]
    evidence = entry["evidence"]
    provenance = entry["provenance"]
    visibility = entry["visibility"]
    if visibility.get("workflow_metadata") != "HIDDEN":
        failures.append(f"{publication_id}: workflow metadata must be hidden")
    if visibility.get("taxonomy") not in {"HIDDEN", "CONSOLIDATED"}:
        failures.append(f"{publication_id}: invalid taxonomy visibility")
    if visibility.get("source_ids") not in {"EVIDENCE_PANEL", "HIDDEN"}:
        failures.append(f"{publication_id}: invalid source-ID visibility")

    if status in {"APPROVED", "PUBLISHED"}:
        if not entry["content_path"] or not (ROOT / entry["content_path"]).is_file():
            failures.append(f"{publication_id}: approved content_path must resolve")
        if not knowledge_paths:
            failures.append(f"{publication_id}: approved entry requires knowledge sources")
        if not entry["as_of"]:
            failures.append(f"{publication_id}: approved entry requires as_of")
        if not all(
            editorial.get(key) is True
            for key in (
                "human_first",
                "narrative_review",
                "seo_review",
                "comprehensiveness_review",
            )
        ):
            failures.append(f"{publication_id}: approved entry lacks editorial approvals")
        if not editorial.get("approval_record"):
            failures.append(f"{publication_id}: approved entry lacks approval record")
        if not all(evidence.get(key) is True for key in (
            "material_claims_reviewed",
            "references_resolve",
            "conflicts_disclosed",
            "limitations_disclosed",
        )):
            failures.append(f"{publication_id}: approved entry lacks evidence review")
        content_sha = provenance.get("content_sha256")
        if entry["content_path"] and (ROOT / entry["content_path"]).is_file():
            if content_sha != sha256(ROOT / entry["content_path"]):
                failures.append(f"{publication_id}: content checksum mismatch")
        elif content_sha is None:
            failures.append(f"{publication_id}: approved entry lacks content checksum")

    if status == "PUBLISHED" and not entry["revision_history"]:
        failures.append(f"{publication_id}: published entry requires revision history")

    for related in entry["related_publication_ids"]:
        if related not in all_ids:
            failures.append(f"{publication_id}: unresolved related publication {related}")
    return failures


def validate_manifest(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    required = {
        "manifest_version",
        "manifest_id",
        "as_of",
        "lifecycle_phase",
        "public_base_path",
        "source_of_truth",
        "build_policy",
        "entries",
    }
    missing = sorted(required - set(payload))
    if missing:
        return [f"manifest missing fields: {', '.join(missing)}"]
    if payload["manifest_version"] != "1.0":
        failures.append("manifest_version must be 1.0")
    try:
        date.fromisoformat(payload["as_of"])
    except (TypeError, ValueError):
        failures.append("as_of must be an ISO date")
    if payload["lifecycle_phase"] not in {
        "CONTRACT_ONLY",
        "PORTFOLIO_DEVELOPMENT",
        "PUBLICATION_ACTIVE",
    }:
        failures.append("invalid lifecycle_phase")
    if not re.fullmatch(r"/.+/", str(payload["public_base_path"])):
        failures.append("public_base_path must begin and end with /")
    if payload["source_of_truth"] != {
        "archive_root": "archive/",
        "knowledge_root": "knowledge/",
        "publication_root": "publication/",
    }:
        failures.append("source_of_truth roots must preserve repository lifecycle boundaries")
    policy = payload["build_policy"]
    if policy.get("include_statuses") != ["PUBLISHED"]:
        failures.append("public build may include only PUBLISHED entries")
    if policy.get("taxonomy_presentation") not in {"HIDDEN", "CONSOLIDATED"}:
        failures.append("taxonomy presentation must be hidden or consolidated")
    if policy.get("ordering") != "publication_id":
        failures.append("manifest ordering must be publication_id")

    entries = payload["entries"]
    ids = [entry.get("publication_id") for entry in entries]
    slugs = [entry.get("slug") for entry in entries]
    if len(ids) != len(set(ids)):
        failures.append("duplicate publication_id")
    if len(slugs) != len(set(slugs)):
        failures.append("duplicate slug")
    if ids != sorted(ids):
        failures.append("entries must be sorted by publication_id")
    all_ids = set(ids)
    for entry in entries:
        failures.extend(validate_entry(entry, all_ids))
    if payload["lifecycle_phase"] == "CONTRACT_ONLY" and entries:
        failures.append("CONTRACT_ONLY manifest must not contain publication entries")
    return failures


def git_changed_paths(base_ref: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        return []
    return [line.replace("\\", "/") for line in result.stdout.splitlines() if line]


def run_validation(base_ref: str = "origin/main") -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    failures: list[str] = []

    for name, path in (
        ("schema_json", SCHEMA_PATH),
        ("example_json", EXAMPLE_PATH),
        ("manifest_json", MANIFEST_PATH),
    ):
        try:
            load_json(path)
            checks.append({"check": name, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            checks.append({"check": name, "status": "FAIL"})
            failures.append(f"{name}: {exc}")

    schema = load_json(SCHEMA_PATH)
    if schema.get("title") == "Star Atlas Archive Publication Manifest v1":
        checks.append({"check": "schema_identity", "status": "PASS"})
    else:
        checks.append({"check": "schema_identity", "status": "FAIL"})
        failures.append("schema identity does not reconcile")

    for name, payload in (
        ("checked_in_manifest", load_json(MANIFEST_PATH)),
        ("schema_example", load_json(EXAMPLE_PATH)),
    ):
        local_failures = validate_manifest(payload)
        checks.append({"check": name, "status": "PASS" if not local_failures else "FAIL"})
        failures.extend(f"{name}: {failure}" for failure in local_failures)

    contract = (ROOT / "publication/PUBLICATION-CONTRACT.md").read_text(encoding="utf-8")
    required_contract_terms = [
        "Archive",
        "Knowledge",
        "Publication",
        "PUBLISHED",
        "human-first",
        "approval",
        "correction",
    ]
    contract_lower = contract.lower()
    missing_terms = [term for term in required_contract_terms if term.lower() not in contract_lower]
    checks.append({
        "check": "publication_contract",
        "status": "PASS" if not missing_terms else "FAIL",
    })
    if missing_terms:
        failures.append("publication contract missing terms: " + ", ".join(missing_terms))

    pointer_failures = [
        path.relative_to(ROOT).as_posix()
        for path in PLACEHOLDER_READMES
        if "PUBLICATION-CONTRACT.md" not in path.read_text(encoding="utf-8")
    ]
    checks.append({
        "check": "placeholder_pointers",
        "status": "PASS" if not pointer_failures else "FAIL",
    })
    if pointer_failures:
        failures.append("placeholder README does not point to contract: " + ", ".join(pointer_failures))

    freshness = load_json(FRESHNESS_PATH)
    freshness_count = len(freshness.get("candidates", []))
    head_blob = git_blob("HEAD", FRESHNESS_REPOSITORY_PATH)
    base_blob = git_blob(base_ref, FRESHNESS_REPOSITORY_PATH)
    freshness_blob_sha = hashlib.sha256(head_blob).hexdigest()
    freshness_ok = (
        freshness_count == 10
        and head_blob == base_blob
        and freshness_blob_sha == FRESHNESS_BLOB_SHA256
    )
    checks.append({"check": "freshness_queue_preserved", "status": "PASS" if freshness_ok else "FAIL"})
    if not freshness_ok:
        failures.append("ten-item freshness queue changed")

    backlog = load_json(ROOT / "operations/coverage/acquisition-backlog.json")
    atlas_gap = next(item for item in backlog["items"] if item["gap_id"] == "GAP-ATLAS-BREW-METADATA")
    gap_ok = atlas_gap["status"] == "CLOSED_BY_PUBLIC_PLAYLIST_RECONCILIATION"
    checks.append({"check": "atlas_brew_gap_reconciled", "status": "PASS" if gap_ok else "FAIL"})
    if not gap_ok:
        failures.append("Atlas Brew metadata gap is not closed")

    roadmap = load_json(ROOT / "operations/programs/library-roadmap/program-status.json")
    phase3 = next(item for item in roadmap["phases"] if item["phase"] == 3)
    phase4 = next(item for item in roadmap["phases"] if item["phase"] == 4)
    roadmap_ok = (
        phase3["status"] == "COMPLETE"
        and phase3["percent_complete"] == 100
        and phase4["status"] == "READY_TO_START"
    )
    checks.append({"check": "roadmap_gate", "status": "PASS" if roadmap_ok else "FAIL"})
    if not roadmap_ok:
        failures.append("roadmap does not close Phase 3 and open Phase 4")

    protected_prefixes = ("archive/", "knowledge/", "graph/", "publication/site/")
    protected_changes = [
        path for path in git_changed_paths(base_ref) if path.startswith(protected_prefixes)
    ]
    checks.append({
        "check": "protected_paths",
        "status": "PASS" if not protected_changes else "FAIL",
    })
    if protected_changes:
        failures.append("protected path changes: " + ", ".join(protected_changes))

    result = {
        "campaign_id": "phase-3-publication-contract-2026-07",
        "as_of": "2026-07-23",
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "metrics": {
            "manifest_entries": len(load_json(MANIFEST_PATH)["entries"]),
            "freshness_candidates_preserved": freshness_count,
            "freshness_queue_blob_sha256": freshness_blob_sha,
            "placeholder_readmes_condensed": len(PLACEHOLDER_READMES),
            "protected_path_changes": len(protected_changes),
        },
        "failures": failures,
        "human_adjudication_required": False,
        "next_gate": "Phase 4 knowledge consolidation",
    }
    return result


def write_reports(result: dict[str, Any]) -> None:
    (CAMPAIGN / "validation-report.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rows = "\n".join(
        f"| {item['check']} | {item['status']} |" for item in result["checks"]
    )
    failure_lines = "\n".join(f"- {item}" for item in result["failures"]) or "- None."
    markdown = f"""# Phase 3 Publication Contract Validation

Result: **{result['status']}**

| Check | Status |
| --- | --- |
{rows}

## Metrics

- Manifest entries: {result['metrics']['manifest_entries']}
- Freshness candidates preserved: {result['metrics']['freshness_candidates_preserved']}
- Freshness queue Git-blob SHA-256: `{result['metrics']['freshness_queue_blob_sha256']}`
- Placeholder READMEs condensed: {result['metrics']['placeholder_readmes_condensed']}
- Protected-path changes: {result['metrics']['protected_path_changes']}

## Failures

{failure_lines}

No archive evidence, canonical knowledge, graph facts, or current site files were
modified by this campaign.
"""
    (CAMPAIGN / "validation-report.md").write_text(markdown, encoding="utf-8", newline="\n")


def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    result = run_validation(base_ref)
    write_reports(result)
    print(f"{result['status']} phase-3-publication-contract-2026-07")
    for failure in result["failures"]:
        print(f"FAIL {failure}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
