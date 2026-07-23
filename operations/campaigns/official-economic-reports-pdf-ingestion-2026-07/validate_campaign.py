"""Validate the committed official economic-report PDF campaign without network access."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parent
RAW = ROOT / "archive/raw/economic-reports/official"
PROVENANCE = ROOT / "archive/provenance/economic-reports/official"
NORMALIZED = ROOT / "archive/normalized/economic-reports/official"
SOURCE_RECORDS = ROOT / "archive/source-records/economic-reports/official"
EXTRACTIONS = ROOT / "archive/ingestion-packages/economic-reports-official/extractions"
ARCHIVE_MANIFEST = ROOT / "archive/manifests/official-economic-reports-pdf-ingestion-2026-07.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    input_manifest = json.loads((CAMPAIGN / "input-package-manifest.json").read_text(encoding="utf-8"))
    members = input_manifest["members"]
    raw_paths = sorted(RAW.glob("*.pdf"))
    raw_by_name = {path.name: path for path in raw_paths}
    check("input_file_count", len(members) == len(raw_paths) == 18, {"manifest": len(members), "raw": len(raw_paths)})
    raw_mismatches = [row["filename"] for row in members if row["filename"] not in raw_by_name or sha256(raw_by_name[row["filename"]]) != row["sha256"]]
    check("raw_checksums", not raw_mismatches, raw_mismatches)
    check("pdf_signatures", all(path.read_bytes().startswith(b"%PDF-") for path in raw_paths), len(raw_paths))

    check("operator_exclusion_applied", "q4-2026.pdf" not in raw_by_name and input_manifest["operator_exclusions"][0]["manual_review_required"] is False, "mislabeled q4-2026 upload is excluded")

    normalized_paths = sorted(NORMALIZED.glob("*.json"))
    source_json = sorted(SOURCE_RECORDS.glob("*.json"))
    source_md = sorted(SOURCE_RECORDS.glob("*.md"))
    extractions = sorted(EXTRACTIONS.glob("*.json"))
    ids = [path.stem for path in normalized_paths]
    check("unique_document_count", len(ids) == len(set(ids)) == 18, len(ids))
    check("paired_artifacts", {path.stem for path in normalized_paths} == {path.stem for path in source_json} == {path.stem for path in source_md} == {path.stem for path in extractions}, ids)
    check("no_false_2026_q4_record", "SRC-ECON-2026-Q4" not in ids, ids)
    check("quarterly_series_count", sum(1 for source_id in ids if source_id.startswith("SRC-ECON-20") and "PAPER" not in source_id) == 17, ids)
    check("economics_paper_present", "SRC-ECON-PAPER-2021" in ids, ids)

    parse_errors: list[str] = []
    page_errors: list[str] = []
    total_pages = 0
    for path in normalized_paths + source_json + extractions:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            parse_errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        if path.parent == NORMALIZED:
            if payload.get("source_id") != path.stem or payload.get("page_count") != len(payload.get("pages", [])):
                page_errors.append(path.name)
            total_pages += payload.get("page_count", 0)
    check("json_parses", not parse_errors, parse_errors)
    check("page_boundaries_reconcile", not page_errors and total_pages == 294, {"errors": page_errors, "pages": total_pages})

    duplicate_ledger = json.loads((CAMPAIGN / "duplicate-ledger.json").read_text(encoding="utf-8"))
    duplicate = duplicate_ledger["duplicates"]
    exclusions = duplicate_ledger["resolved_input_exclusions"]
    check("duplicate_ledger", not duplicate and len(exclusions) == 1 and exclusions[0]["manual_review_required"] is False and exclusions[0]["preserved_raw"] is False, duplicate_ledger)
    summary = json.loads((CAMPAIGN / "campaign-summary.json").read_text(encoding="utf-8"))
    check("summary_reconciles", summary["input_package_files"] == 18 and summary["unique_documents"] == 18 and summary["quarterly_reports"] == 17 and summary["exact_duplicates"] == 0 and summary["operator_exclusions"] == 1 and not summary["manual_review_queue"] and summary["urls_fetched_for_body"] is False, summary)
    visual = json.loads((CAMPAIGN / "visual-validation.json").read_text(encoding="utf-8"))
    check("visual_validation", visual["result"] == "PASS" and visual["first_pages_rendered"] == 18 and len(visual["representative_pages_inspected"]) == 8, visual)

    manifest = json.loads(ARCHIVE_MANIFEST.read_text(encoding="utf-8"))
    manifest_errors = []
    for artifact in manifest["artifacts"]:
        path = ROOT / artifact["path"]
        if not path.exists() or path.stat().st_size != artifact["byte_count"] or sha256(path) != artifact["sha256"]:
            manifest_errors.append(artifact["path"])
    check("manifest_checksums", not manifest_errors and manifest["artifact_count"] == len(manifest["artifacts"]), manifest_errors)
    package = json.loads((ROOT / "archive/ingestion-packages/economic-reports-official/official-economic-reports-pdf-ingestion-2026-07.v2.1.json").read_text(encoding="utf-8"))
    check("schema_v2_1_package", package["metadata"]["repository_schema"] == "2.1" and len(package["sources"]) == 18, package["metadata"])

    passed = all(row["passed"] for row in checks)
    report = {
        "campaign_id": "official-economic-reports-pdf-ingestion-2026-07",
        "as_of": "2026-07-22",
        "result": "PASS" if passed else "FAIL",
        "checks": checks,
        "manual_review_required": [],
        "limitations": [
            "Validation proves archival integrity and extraction reconciliation, not the independent accuracy of publisher-reported economic claims.",
            "Charts and table geometry remain authoritative only in the raw PDFs.",
            "No on-chain verification or semantic promotion was performed.",
        ],
    }
    (CAMPAIGN / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    lines = ["# Official Economic Reports PDF Validation", "", f"**Result:** `{report['result']}`", "", "## Checks", ""]
    lines.extend(f"- **{'PASS' if row['passed'] else 'FAIL'} - {row['name']}:** {row['detail']}" for row in checks)
    lines += ["", "## Manual review", "", "None. The operator-confirmed mislabeled `q4-2026.pdf` upload is excluded from the campaign.", "", "## Limitations", ""]
    lines.extend(f"- {value}" for value in report["limitations"])
    (CAMPAIGN / "validation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{report['result']}: {sum(row['passed'] for row in checks)}/{len(checks)} checks")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
