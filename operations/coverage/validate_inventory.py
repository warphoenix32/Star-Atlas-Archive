"""Validate the Phase 1 repository/evidence baseline without network access."""

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
    PROGRAM / "README.md",
    PROGRAM / "program-status.json",
    PROGRAM / "program-status.md",
    PROGRAM / "phase-gates.json",
    PROGRAM / "dependency-register.json",
    PROGRAM / "human-adjudication-queue.md",
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
    check("coverage_records", len(coverage) == 15, len(coverage))
    check("coverage_evidence_paths_resolve", not evidence_missing, evidence_missing)
    check("coverage_gaps_reconcile", not unknown_gaps, unknown_gaps)
    check("campaign_registry", len(campaigns) == 19, len(campaigns))
    missing_campaign_evidence = sorted(row["status_evidence"] for row in campaigns if not (ROOT / row["status_evidence"]).exists())
    check("campaign_status_evidence_resolves", not missing_campaign_evidence, missing_campaign_evidence)

    holdings = parsed.get("repository-holdings.json", {})
    archive = next((row for row in holdings.get("domains", []) if row.get("path") == "archive"), {})
    check("archive_holdings_reconcile", archive.get("files") == 8291, archive)
    check("normalized_inventory_boundary", holdings.get("normalized_url_inventory", {}).get("records") == 3232 and holdings.get("normalized_url_inventory", {}).get("status") == "STALE_REQUIRES_RECONCILIATION", holdings.get("normalized_url_inventory"))

    cleanup = parsed.get("cleanup-register.json", {})
    check("no_unconditional_repository_deletions", cleanup.get("immediate_safe_repository_deletions") == [], cleanup.get("immediate_safe_repository_deletions"))

    phases = parsed.get("program-status.json", {}).get("phases", [])
    check("seven_phase_roadmap", [row.get("phase") for row in phases] == list(range(1, 8)), [row.get("phase") for row in phases])
    check("phase_one_active", parsed.get("program-status.json", {}).get("current_phase") == 1 and phases[0].get("status") == "READY_FOR_REVIEW", phases[0] if phases else None)

    library = subprocess.run(["node", "publication/site/scripts/build-search-index.mjs", "--check"], cwd=ROOT, capture_output=True, text=True, check=False)
    check("library_index_fixed_point", library.returncode == 0, (library.stdout + library.stderr).strip())
    social_summary = json.loads((ROOT / "operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json").read_text(encoding="utf-8"))
    social_validation = json.loads((ROOT / "operations/campaigns/social-governance-semantic-enrichment/validation-report.json").read_text(encoding="utf-8"))
    check("social_campaign_status_reconciled", social_summary.get("status") == social_validation.get("status") == "PASS", {"summary": social_summary.get("status"), "validation": social_validation.get("status")})

    passed = all(row["passed"] for row in checks)
    report = {"program_id": "star-atlas-library-roadmap-phase-1", "as_of": "2026-07-20", "baseline_sha": "9dc39e47393d707f60d792227cf9f150a1031b28", "result": "PASS" if passed else "FAIL", "checks": checks, "limitations": ["The register is a repository snapshot, not proof of external corpus completeness.", "Freshness adapters are policy-defined but not implemented.", "Windows lore fixed-point comparison remains sensitive to Git CRLF conversion; Linux repository CI is authoritative until line-ending policy is added."]}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Phase 1 Validation Report", "", f"**Result:** `{report['result']}`", "", "## Checks", ""]
    lines.extend(f"- **{'PASS' if row['passed'] else 'FAIL'} — {row['name']}:** {row['detail']}" for row in checks)
    lines += ["", "## Limitations", ""] + [f"- {item}" for item in report["limitations"]] + [""]
    (HERE / "validation-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{report['result']}: {sum(row['passed'] for row in checks)}/{len(checks)} checks")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
