"""Validate the repository coverage and Phase 2 closeout without network access."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROGRAM = ROOT / "operations" / "programs" / "library-roadmap"
GENERATED = [
    HERE / "repository-holdings.json",
    HERE / "repository-holdings.md",
    HERE / "source-coverage-register.json",
    HERE / "source-coverage-register.md",
    HERE / "acquisition-backlog.json",
    HERE / "acquisition-backlog.md",
    HERE / "campaign-status-register.json",
    HERE / "campaign-status-register.md",
    HERE / "cleanup-register.json",
    HERE / "cleanup-register.md",
    HERE / "refresh-policy.json",
    HERE / "url-disposition-overlay.jsonl",
    HERE / "url-disposition-summary.json",
    HERE / "url-disposition-summary.md",
    HERE / "economic-report-branch-assessment.json",
    HERE / "economic-report-branch-assessment.md",
    PROGRAM / "README.md",
    PROGRAM / "program-status.json",
    PROGRAM / "program-status.md",
    PROGRAM / "phase-gates.json",
    PROGRAM / "dependency-register.json",
    PROGRAM / "human-adjudication-queue.md",
    PROGRAM / "recovery-campaign-schedule.json",
    PROGRAM / "recovery-campaign-schedule.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_builder() -> None:
    result = subprocess.run([sys.executable, str(HERE / "build_inventory.py")], cwd=ROOT, check=False, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    before = {path.relative_to(ROOT).as_posix(): digest(path) for path in GENERATED if path.exists()}
    run_builder()
    middle = {path.relative_to(ROOT).as_posix(): digest(path) for path in GENERATED if path.exists()}
    run_builder()
    after = {path.relative_to(ROOT).as_posix(): digest(path) for path in GENERATED if path.exists()}
    check("deterministic_generation", before == middle == after and len(after) == len(GENERATED), {"expected": len(GENERATED), "generated": len(after)})

    json_paths = sorted(HERE.glob("*.json")) + sorted(PROGRAM.glob("*.json"))
    parsed: dict[str, object] = {}
    errors: list[str] = []
    for path in json_paths:
        try:
            parsed[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    check("json_parses", not errors, {"files": len(json_paths), "errors": errors})

    coverage = parsed.get("source-coverage-register.json", {}).get("records", [])
    gaps = parsed.get("acquisition-backlog.json", {}).get("items", [])
    campaigns = parsed.get("campaign-status-register.json", {}).get("campaigns", [])
    gap_ids = {row.get("gap_id") for row in gaps}
    evidence_missing = sorted({path for row in coverage for path in row.get("evidence_paths", []) if not (ROOT / path).exists()})
    unknown_gaps = sorted({gid for row in coverage for gid in row.get("gap_ids", []) if gid not in gap_ids})
    check("coverage_records", len(coverage) == 17, len(coverage))
    check("coverage_evidence_paths_resolve", not evidence_missing, evidence_missing)
    check("coverage_gaps_reconcile", not unknown_gaps, unknown_gaps)
    check("campaign_registry", len(campaigns) == 23, len(campaigns))
    missing_campaign_evidence = sorted(row["status_evidence"] for row in campaigns if not (ROOT / row["status_evidence"]).exists())
    check("campaign_status_evidence_resolves", not missing_campaign_evidence, missing_campaign_evidence)

    holdings = parsed.get("repository-holdings.json", {})
    archive = next((row for row in holdings.get("domains", []) if row.get("path") == "archive"), {})
    check("archive_holdings_reconcile", archive.get("files") == 9646, archive)
    inventory_boundary = holdings.get("normalized_url_inventory", {})
    check("normalized_inventory_boundary", inventory_boundary.get("records") == 3232 and inventory_boundary.get("status") == "RECONCILED_BY_OVERLAY", inventory_boundary)

    overlay_path = HERE / "url-disposition-overlay.jsonl"
    overlay_errors: list[str] = []
    overlay: list[dict] = []
    for line_number, line in enumerate(overlay_path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            overlay.append(json.loads(line))
        except Exception as exc:  # noqa: BLE001
            overlay_errors.append(f"line {line_number}: {exc}")
    expected_dispositions = {
        "INGESTED_CONFIRMED": 480,
        "EXCLUDED_NON_WRITTEN": 247,
        "EXCLUDED_NAVIGATION": 4,
        "EXCLUDED_EXTERNAL_WRITTEN": 12,
        "RETRIEVAL_FAILED": 4,
        "PENDING_UNRECONCILED": 251,
        "DEFERRED_UNRECONCILED": 2234,
    }
    actual_dispositions: dict[str, int] = {}
    for row in overlay:
        disposition = row.get("current_disposition")
        actual_dispositions[disposition] = actual_dispositions.get(disposition, 0) + 1
    check("url_overlay_jsonl_parses", not overlay_errors, overlay_errors)
    check("url_overlay_reconciles", len(overlay) == 3232 and len({row.get('url_id') for row in overlay}) == 3232 and actual_dispositions == expected_dispositions, {"rows": len(overlay), "dispositions": actual_dispositions})
    missing_overlay_artifacts = sorted({path for row in overlay for path in row.get("artifact_paths", []) if not (ROOT / path).exists()})
    missing_overlay_evidence = sorted({evidence.get("path") for row in overlay for evidence in row.get("evidence", []) if not (ROOT / evidence.get("path", "")).exists()})
    check("url_overlay_references_resolve", not missing_overlay_artifacts and not missing_overlay_evidence, {"artifacts": missing_overlay_artifacts, "evidence": missing_overlay_evidence})

    economic = parsed.get("economic-report-branch-assessment.json", {})
    check("economic_branch_closed", economic.get("decision") == "CLOSED_REPLACED_BY_PR57" and economic.get("discovery_urls") == 17 and economic.get("merge_or_cherry_pick") is False, economic)
    recovery = parsed.get("recovery-campaign-schedule.json", {})
    complete_batches = [row for row in recovery.get("batches", []) if row.get("status") == "COMPLETE"]
    herald_batch = next((row for row in recovery.get("batches", []) if row.get("source_family") == "Intergalactic Herald"), {})
    check(
        "raw_recovery_selected_scope_complete",
        recovery.get("status") == "SELECTED_SCOPE_COMPLETE"
        and recovery.get("collection_started") is True
        and recovery.get("milestone_closed") is True
        and sum(row.get("records", 0) for row in recovery.get("batches", [])) == 800
        and recovery.get("selected_scope_records") == recovery.get("selected_scope_completed_records") == 541
        and sum(row.get("captured_records", 0) for row in complete_batches) == 541
        and recovery.get("total_raw_bodies_preserved") == 546
        and herald_batch.get("captured_records") == 5
        and herald_batch.get("status") == "DEFERRED_BY_OPERATOR",
        recovery,
    )

    cleanup = parsed.get("cleanup-register.json", {})
    check("no_unconditional_repository_deletions", cleanup.get("immediate_safe_repository_deletions") == [], cleanup.get("immediate_safe_repository_deletions"))

    phases = parsed.get("program-status.json", {}).get("phases", [])
    check("seven_phase_roadmap", [row.get("phase") for row in phases] == list(range(1, 8)), [row.get("phase") for row in phases])
    check("phase_one_complete", phases[0].get("status") == "COMPLETE" and phases[0].get("percent_complete") == 100 and phases[0].get("remaining_gate_items") == [], phases[0] if phases else None)
    check("phase_two_complete", phases[1].get("status") == "COMPLETE" and phases[1].get("percent_complete") == 100 and phases[1].get("remaining_gate_items") == [], phases[1] if len(phases) > 1 else None)
    check("phase_three_ready", parsed.get("program-status.json", {}).get("current_phase") == 3 and phases[2].get("status") == "READY_TO_START" and phases[2].get("percent_complete") == 0, phases[2] if len(phases) > 2 else None)

    freshness = ROOT / "operations/campaigns/phase-2-official-freshness-closeout-2026-07/campaign-summary.json"
    freshness_summary = json.loads(freshness.read_text(encoding="utf-8"))
    check(
        "phase_two_freshness_gate",
        freshness_summary.get("status") == "PHASE_2_GATE_COMPLETE"
        and freshness_summary.get("surfaces_checked") == 7
        and freshness_summary.get("candidates_queued") == 10
        and freshness_summary.get("human_adjudication_required") is False,
        freshness_summary,
    )

    library = subprocess.run(["node", "publication/site/scripts/build-search-index.mjs", "--check"], cwd=ROOT, capture_output=True, text=True, check=False)
    library_detail = (library.stdout + library.stderr).strip()
    if library.returncode:
        # The script compares bytes. Windows CRLF checkout can therefore fail
        # while regenerated content has the committed Git object hash. Preserve
        # and restore the checkout bytes around that filtered-hash comparison.
        library_path = ROOT / "publication/site/assets/library-index.json"
        checkout_bytes = library_path.read_bytes()
        try:
            regenerated = subprocess.run(["node", "publication/site/scripts/build-search-index.mjs"], cwd=ROOT, capture_output=True, text=True, check=False)
            generated_hash = subprocess.run(["git", "hash-object", "publication/site/assets/library-index.json"], cwd=ROOT, capture_output=True, text=True, check=False)
            committed_hash = subprocess.run(["git", "rev-parse", "HEAD:publication/site/assets/library-index.json"], cwd=ROOT, capture_output=True, text=True, check=False)
            library_passed = regenerated.returncode == generated_hash.returncode == committed_hash.returncode == 0 and generated_hash.stdout.strip() == committed_hash.stdout.strip()
        finally:
            library_path.write_bytes(checkout_bytes)
        library_detail = {
            "byte_check": library_detail,
            "regeneration": (regenerated.stdout + regenerated.stderr).strip(),
            "generated_git_hash": generated_hash.stdout.strip(),
            "committed_git_hash": committed_hash.stdout.strip(),
            "windows_line_ending_fallback": library_passed,
        }
    else:
        library_passed = True
    if library_passed:
        library_records = json.loads((ROOT / "publication/site/assets/library-index.json").read_text(encoding="utf-8"))
        library_detail = f"PASS search index fixed point: {len(library_records)} records"
    check("library_index_fixed_point", library_passed, library_detail)
    social_summary = json.loads((ROOT / "operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json").read_text(encoding="utf-8"))
    social_validation = json.loads((ROOT / "operations/campaigns/social-governance-semantic-enrichment/validation-report.json").read_text(encoding="utf-8"))
    check("social_campaign_status_reconciled", social_summary.get("status") == social_validation.get("status") == "PASS", {"summary": social_summary.get("status"), "validation": social_validation.get("status")})

    passed = all(row["passed"] for row in checks)
    report = {"program_id": "star-atlas-library-roadmap-phase-2-closeout", "as_of": "2026-07-22", "baseline_sha": "1b47c2bdaf1aa683b5b8905323abe24cf0a02525", "result": "PASS" if passed else "FAIL", "checks": checks, "limitations": ["The register is a repository snapshot, not proof of external corpus completeness.", "The selected written-recovery scope is complete for Aephia, HNN, and Official; the remaining 254 Herald records are deferred and are not represented as recovered.", "The 2,485 unreconciled URL rows remain a historical research backlog and do not block Phase 3.", "The freshness campaign queued ten candidates but did not ingest them.", "Automated freshness adapters are not implemented; this closeout used a bounded manual check.", "Discord and transcript metadata gaps require new operator-supplied artifacts and remain explicitly incomplete.", "Windows lore fixed-point comparison remains sensitive to Git CRLF conversion; Linux repository CI is authoritative until line-ending policy is added."]}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Phase 2 Closeout Validation", "", f"**Result:** `{report['result']}`", "", "## Checks", ""]
    lines.extend(f"- **{'PASS' if row['passed'] else 'FAIL'} — {row['name']}:** {row['detail']}" for row in checks)
    lines += ["", "## Limitations", ""] + [f"- {item}" for item in report["limitations"]] + [""]
    (HERE / "validation-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{report['result']}: {sum(row['passed'] for row in checks)}/{len(checks)} checks")
    for row in checks:
        if not row["passed"]:
            print(f"FAIL {row['name']}: {row['detail']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
