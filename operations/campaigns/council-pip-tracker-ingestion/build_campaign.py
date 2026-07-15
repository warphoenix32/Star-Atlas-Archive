#!/usr/bin/env python3
"""Build source records and provenance metadata for the Council tracker package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
RAW = REPO / "archive/raw/governance/council-pip-tracker/Star_Atlas_DAO_Council_PIP_Tracker_and_Grading_Rubric.xlsx"
NORMALIZED = REPO / "archive/normalized/governance/council-pip-tracker"
SEMANTIC = REPO / "archive/semantic/governance/council-pip-tracker"
RECORDS = REPO / "archive/source-records/governance/council-pip-tracker"
CAMPAIGN_ID = "council-pip-tracker-ingestion"
SOURCE_URL = "https://docs.google.com/spreadsheets/d/1QWkFjcLwhw4GHqk5Stz72H3WRwIb52f-UDnKne7hTtY/edit"
SHEETS = ["Tracker", "Accomplishment Numbers", "PIP Step Process", "Lanzer Grading Rubric", "Carlos Grading Rubric"]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    tracker = read_jsonl(SEMANTIC / "council-pip-tracker-semantic-records.jsonl")
    rubric = read_jsonl(SEMANTIC / "pip-evaluation-rubric-records.jsonl")
    if len(tracker) != 39 or len(rubric) != 80: raise SystemExit("Council semantic record counts do not reconcile")
    metadata = {
        "title": "Star Atlas DAO Council -- PIP Tracker & Grading Rubric",
        "google_sheets_file_id": "1QWkFjcLwhw4GHqk5Stz72H3WRwIb52f-UDnKne7hTtY",
        "source_url": SOURCE_URL, "sheet_names": SHEETS,
        "capture_timestamp": "2026-07-15T11:26:23.262446+00:00",
        "modified_timestamp": "UNKNOWN_NOT_PRESERVED_IN_SUPPLIED_PACKAGE",
        "raw_workbook_sha256": digest(RAW),
        "normalized_workbook_sha256": digest(NORMALIZED / "Star_Atlas_DAO_Council_Tracker_Normalized.xlsx"),
        "spreadsheet_import_note": "The bundled artifact-tool importer rejected an embedded workbook person entry lacking displayName; the supplied normalized workbook and source-derived semantic records were preserved without rewriting the source workbook.",
    }
    write_json(SEMANTIC / "source-metadata.json", metadata)
    for item in tracker:
        write_json(RECORDS / f"{item['source_id']}.json", {"source_id": item["source_id"], "source_class": "TIER_1_COUNCIL_OPERATIONAL_TRACKER", "sheet": item["sheet"], "row_number": item["row_number"], "pip_id": item.get("pip_id"), "title": item.get("title"), "source_url": SOURCE_URL, "raw_workbook_sha256": metadata["raw_workbook_sha256"], "attribution": "STAR_ATLAS_COUNCIL_TRACKER", "independent_verification_status": "UNKNOWN", "limitations": ["Council operational and ROI assessments are attributed, not independent verification.", "Reported payment and milestones require primary evidence reconciliation."]})
    for item in rubric:
        write_json(RECORDS / f"{item['source_id']}.json", {"source_id": item["source_id"], "source_class": "TIER_1_COUNCIL_REVIEW_GUIDANCE", "sheet": item["sheet"], "row_number": item["row_number"], "source_url": SOURCE_URL, "raw_workbook_sha256": metadata["raw_workbook_sha256"], "canonical_status": "REVIEW_GUIDANCE_NOT_BINDING_LAW_UNLESS_GROUNDED_IN_APPROVED_PIP_OR_OFFICIAL_DAO_KNOWLEDGE_BASE", "attribution_required": True})
    summary = {"campaign_id": CAMPAIGN_ID, "status": "GENERATED", "source_sheets": len(SHEETS), "sheet_names": SHEETS, "tracker_records": len(tracker), "rubric_guidance_records": len(rubric), "source_records": len(tracker) + len(rubric), "raw_workbook_sha256": metadata["raw_workbook_sha256"], "normalized_workbook_sha256": metadata["normalized_workbook_sha256"], "discord_package_duplicates_ingested": 0, "source_authority": ["TIER_1_COUNCIL_OPERATIONAL_TRACKER", "TIER_1_COUNCIL_REVIEW_GUIDANCE"]}
    write_json(OPS / "campaign-summary.json", summary)
    (OPS / "campaign-summary.md").write_text("# Council PIP Tracker Archival Ingestion\n\n" + "\n".join(f"- {key.replace('_',' ').title()}: **{value}**" for key, value in summary.items() if key not in {"campaign_id", "sheet_names", "source_authority"}) + "\n\nAll five sheets and both workbooks are preserved. Council operational claims and ROI statements retain attribution; rubric records are review guidance, not automatically binding governance law. The nested Discord ZIP was byte-identical to the standalone package and was not ingested a second time.\n", encoding="utf-8")
    (OPS / "README.md").write_text("# Council PIP Tracker Ingestion\n\nThis campaign preserves the original and normalized Council workbooks, five sheet exports, 39 operational tracker records, 80 review-guidance records, source schemas, and provenance metadata. It does not convert Council assessments into independently verified fact.\n\nRun `python operations/campaigns/council-pip-tracker-ingestion/build_campaign.py` then `python operations/campaigns/council-pip-tracker-ingestion/validate_campaign.py`.\n", encoding="utf-8")
    inputs = sorted([p for root in (REPO / "archive/raw/governance/council-pip-tracker", NORMALIZED, OPS / "input-package") for p in root.rglob("*") if p.is_file()])
    outputs = sorted([p for root in (SEMANTIC, RECORDS, OPS) for p in root.rglob("*") if p.is_file() and p.name not in {"manifest.json", "validation-report.json", "validation-report.md"} and (OPS / "input-package") not in p.parents and p.suffix != ".pyc"])
    write_json(OPS / "manifest.json", {"campaign_id": CAMPAIGN_ID, "status": "GENERATED", "preserved_inputs": [{"path": p.relative_to(REPO).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in inputs], "generated_outputs": [{"path": p.relative_to(REPO).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in outputs]})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
