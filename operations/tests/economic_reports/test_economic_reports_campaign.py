import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = ROOT / "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07"
RAW = ROOT / "archive/raw/economic-reports/official"
NORMALIZED = ROOT / "archive/normalized/economic-reports/official"


def test_adjudicated_pdf_set_is_preserved():
    manifest = json.loads((CAMPAIGN / "input-package-manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["members"]) == 18
    for row in manifest["members"]:
        path = RAW / row["filename"]
        assert path.exists()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    assert (RAW / "q4-2025.pdf").exists()
    assert not (RAW / "q4-2026.pdf").exists()
    assert manifest["operator_exclusions"][0]["manual_review_required"] is False


def test_unique_source_records_do_not_invent_2026_q4():
    ids = {path.stem for path in NORMALIZED.glob("*.json")}
    assert len(ids) == 18
    assert "SRC-ECON-2026-Q4" not in ids
    assert "SRC-ECON-2025-Q4" in ids
    assert "SRC-ECON-PAPER-2021" in ids


def test_page_boundaries_and_raw_checksums_reconcile():
    total_pages = 0
    for path in NORMALIZED.glob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["page_count"] == len(record["pages"])
        assert hashlib.sha256((ROOT / record["raw_path"]).read_bytes()).hexdigest() == record["raw_sha256"]
        total_pages += record["page_count"]
    assert total_pages == 294
