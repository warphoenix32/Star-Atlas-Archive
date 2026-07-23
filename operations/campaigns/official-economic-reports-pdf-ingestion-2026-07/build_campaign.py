"""Build the official Star Atlas economic-report PDF ingestion campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parent
CAMPAIGN_ID = "official-economic-reports-pdf-ingestion-2026-07"
AS_OF = "2026-07-22"
RAW = ROOT / "archive/raw/economic-reports/official"
PROVENANCE = ROOT / "archive/provenance/economic-reports/official"
NORMALIZED = ROOT / "archive/normalized/economic-reports/official"
SOURCE_RECORDS = ROOT / "archive/source-records/economic-reports/official"
INGESTION = ROOT / "archive/ingestion-packages/economic-reports-official"
EXTRACTIONS = INGESTION / "extractions"
ARCHIVE_MANIFEST = ROOT / "archive/manifests/official-economic-reports-pdf-ingestion-2026-07.json"
INPUT_MANIFEST = CAMPAIGN / "input-package-manifest.json"

ECONOMICS_PAPER_URL = "https://staratlas.com/files/star-atlas-economics-paper.pdf?pdf=Economics-Paper"
QUARTER_RE = re.compile(r"q([1-4])-(20\d{2})\.pdf$")
OPERATOR_EXCLUDED_FILENAMES = {"q4-2026.pdf"}
PUBLICATION_DATE_OVERRIDES = {
    "star-atlas-economics-paper.pdf": {
        "date": "2021-08-17",
        "basis": "Official Discord release announcement",
        "source_id": "SA-DISCORD-ANN-34E32306A962395F",
    },
    "q1-2026.pdf": {
        "date": "2026-04-02",
        "basis": "Official Star Atlas X release post",
        "source_id": "SRC-X-STARATLAS-2039802551043055822",
    },
    "q2-2026.pdf": {
        "date": "2026-07-01",
        "basis": "Official Star Atlas X release post",
        "source_id": "SRC-X-STARATLAS-2072427112053846335",
    },
}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = "\n".join(line.rstrip() for line in text.splitlines()).rstrip()
    path.write_text(clean + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_pdf_date(value: str | None) -> str | None:
    if not value:
        return None
    match = re.match(r"D:(\d{4})(\d{2})(\d{2})", value)
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}" if match else None


def source_metadata(filename: str) -> dict[str, object]:
    if filename == "star-atlas-economics-paper.pdf":
        return {
            "source_id": "SRC-ECON-PAPER-2021",
            "title": "Star Atlas Economics Paper",
            "series": "Star Atlas Economics Paper",
            "period": "2021",
            "year": 2021,
            "quarter": None,
            "document_classification": "TECHNICAL_DOCUMENTATION",
            "document_type": "OFFICIAL_ECONOMICS_PAPER",
            "canonical_url": ECONOMICS_PAPER_URL,
        }
    match = QUARTER_RE.match(filename)
    if not match:
        raise ValueError(f"unsupported PDF filename: {filename}")
    quarter, year_text = match.groups()
    year = int(year_text)
    return {
        "source_id": f"SRC-ECON-{year}-Q{quarter}",
        "title": f"Star Atlas State of the Economy - {year} Q{quarter}",
        "series": "Star Atlas State of the Economy",
        "period": f"{year} Q{quarter}",
        "year": year,
        "quarter": f"Q{quarter}",
        "document_classification": "ECONOMIC_REPORT",
        "document_type": "OFFICIAL_QUARTERLY_ECONOMIC_REPORT",
        "canonical_url": f"https://storage.googleapis.com/sa-cdn-prod/dao/economy/{year}/q{quarter}.pdf",
    }


def capture_input_package(zip_path: Path) -> dict[str, object]:
    members: list[dict[str, object]] = []
    with zipfile.ZipFile(zip_path) as package:
        for info in sorted((row for row in package.infolist() if row.filename.lower().endswith(".pdf")), key=lambda row: row.filename):
            filename = Path(info.filename).name.lower()
            if filename in OPERATOR_EXCLUDED_FILENAMES:
                continue
            target = RAW / filename
            with package.open(info) as source, target.open("wb") as destination:
                shutil.copyfileobj(source, destination)
            members.append({
                "archive_member": info.filename,
                "filename": filename,
                "byte_count": info.file_size,
                "crc32": f"{info.CRC:08x}",
                "zip_timestamp_original": "%04d-%02d-%02dT%02d:%02d:%02d" % info.date_time,
                "sha256": sha256(target),
            })
    payload = {
        "schema_version": "1.0.0",
        "campaign_id": CAMPAIGN_ID,
        "source_type": "OPERATOR_PROVIDED_LOCAL_PACKAGE",
        "source_package_filename": zip_path.name,
        "source_package_sha256": sha256(zip_path),
        "captured_as_of": AS_OF,
        "members": members,
        "operator_exclusions": [{
            "filename": "q4-2026.pdf",
            "disposition": "DISREGARDED_OPERATOR_CONFIRMED_MISLABELED_UPLOAD",
            "preserved_raw": False,
            "manual_review_required": False,
        }],
    }
    write_json(INPUT_MANIFEST, payload)
    return payload


def image_count(page: object) -> int:
    try:
        resources = page.get("/Resources") or {}
        xobjects = resources.get("/XObject") or {}
        return sum(1 for value in xobjects.values() if value.get_object().get("/Subtype") == "/Image")
    except Exception:  # noqa: BLE001 - PDF resource dictionaries vary
        return 0


def markdown_source_record(record: dict[str, object]) -> str:
    observed = "\n".join(f"- `{value}`" for value in record["observed_filenames"])
    limitations = "\n".join(f"- {value}" for value in record["known_limitations"])
    return f"""# {record['title']}

## Metadata

- Source ID: `{record['source_id']}`
- Publisher: ATMTA, Inc. / Star Atlas
- Author: {record['author']}
- Document type: `{record['document_type']}`
- Classification: `{record['document_classification']}`
- Period: {record['period']}
- Publication date: {record['publication_date_original'] or 'UNKNOWN'}
- Publication-date basis: {record['publication_date_basis']}
- Updated date: UNKNOWN
- Canonical URL: {record['canonical_url']}
- Raw PDF: `{record['raw_path']}`
- Raw SHA-256: `{record['raw_sha256']}`
- Pages: {record['page_count']}

## Source Lineage

- Publication: Star Atlas / ATMTA, Inc.
- Publication role: `REFERENCE`
- Relationship: `REPORTS_ON`
- Primary sources: `UNKNOWN`
- Original creators: {record['author']}
- Lineage confidence: `{record['lineage_confidence']}`

## Archival Abstract

{record['archival_abstract']}

## Major Topics

- Star Atlas economy
- ATLAS and POLIS systems
- Period-bound economic methodology and measurements

## Claims

No claims were promoted by this ingestion campaign. Statements and figures remain attributed to this report, its period, methodology, and publisher until semantic review.

## Historical Value

This preserved PDF provides first-party evidence of how ATMTA described and measured the Star Atlas economy at the stated period.

## Current Validity

`HISTORICAL_PERIOD_BOUND`. Current applicability is not inferred from the report's publication or preservation.

## Observed Filenames

{observed}

## Known Limitations

{limitations}

## Open Questions

- Which metrics remain methodologically comparable with adjacent reports?
- Which reported measurements have independent or on-chain verification?
- Are later corrections or revised editions available?

## Extraction Confidence

`{record['extraction_confidence']}`. Text is preserved page by page; charts and tables require consultation of the raw PDF.
"""


def normalized_markdown(payload: dict[str, object]) -> str:
    sections = [f"# {payload['title']}", "", f"Source ID: `{payload['source_id']}`", "", "This is a page-preserving text extraction. Visual interpretation must use the raw PDF.", ""]
    for page in payload["pages"]:
        sections.extend([f"## Page {page['page_number']}", "", page["text"] or "[NO EXTRACTABLE TEXT]", ""])
    return "\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-zip", type=Path)
    args = parser.parse_args()
    for directory in (RAW, PROVENANCE, NORMALIZED, SOURCE_RECORDS, EXTRACTIONS):
        directory.mkdir(parents=True, exist_ok=True)

    input_manifest = capture_input_package(args.input_zip) if args.input_zip else json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    expected = {row["filename"]: row for row in input_manifest["members"]}
    supplied_files = sorted(RAW.glob("*.pdf"), key=lambda path: path.name)
    if {path.name for path in supplied_files} != set(expected):
        raise RuntimeError("raw PDF set does not match the frozen input-package manifest")
    for path in supplied_files:
        if sha256(path) != expected[path.name]["sha256"]:
            raise RuntimeError(f"raw checksum mismatch: {path.name}")

    unique_files = supplied_files
    records: list[dict[str, object]] = []
    artifacts: list[dict[str, object]] = []
    total_pages = 0
    total_characters = 0

    for path in unique_files:
        meta = source_metadata(path.name)
        reader = PdfReader(path)
        pdf_meta = {str(key): str(value) for key, value in sorted((reader.metadata or {}).items())}
        pages: list[dict[str, object]] = []
        for number, page in enumerate(reader.pages, 1):
            extracted = (page.extract_text() or "").replace("\r\n", "\n").replace("\r", "\n")
            text = "\n".join(line.rstrip() for line in extracted.splitlines()).strip()
            pages.append({
                "page_number": number,
                "text": text,
                "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "character_count": len(text),
                "embedded_image_count": image_count(page),
            })
        full_text = "\n\n".join(page["text"] for page in pages)
        total_pages += len(pages)
        total_characters += len(full_text)
        author = pdf_meta.get("/Author", "UNKNOWN").strip() or "UNKNOWN"
        override = PUBLICATION_DATE_OVERRIDES.get(path.name)
        publication_date = override["date"] if override else parse_pdf_date(pdf_meta.get("/CreationDate"))
        publication_date_basis = override["basis"] if override else ("Embedded PDF CreationDate" if publication_date else "UNKNOWN")
        official_cross_references = [override["source_id"]] if override else []
        observed_filenames = [path.name]
        empty_pages = sum(1 for page in pages if not page["text"])
        confidence = "HIGH" if len(full_text) >= 5000 and empty_pages == 0 else "MEDIUM"
        limitations = [
            "Quantitative claims are publisher-reported and were not independently or on-chain verified by this campaign.",
            "Text extraction does not preserve chart geometry, table layout, typography, or graphical annotations.",
            "Metric continuity across quarters requires later methodology reconciliation.",
        ]
        if empty_pages:
            limitations.append(f"{empty_pages} page(s) contain no extractable text and require visual consultation of the PDF.")
        archival_abstract = (
            f"Official ATMTA period-bound economic publication for {meta['period']}. "
            "The complete extractable text is preserved with page boundaries. This record does not treat reported measurements, forecasts, or methodology as independently verified facts."
        )
        normalized = {
            "schema_version": "1.0.0",
            **meta,
            "publisher": "ATMTA, Inc. / Star Atlas",
            "author": author,
            "publication_date_original": publication_date,
            "publication_date_normalized": publication_date,
            "publication_date_basis": publication_date_basis,
            "updated_date_original": None,
            "updated_date_normalized": None,
            "official_cross_references": official_cross_references,
            "raw_path": path.relative_to(ROOT).as_posix(),
            "raw_sha256": sha256(path),
            "raw_byte_count": path.stat().st_size,
            "page_count": len(pages),
            "pages": pages,
            "full_text": full_text,
            "pdf_metadata": pdf_meta,
            "observed_filenames": observed_filenames,
            "temporal_validity": "HISTORICAL_PERIOD_BOUND",
            "extraction_confidence": confidence,
            "known_limitations": limitations,
            "provenance": {
                "source_package_filename": input_manifest["source_package_filename"],
                "source_package_sha256": input_manifest["source_package_sha256"],
                "acquisition_method": "OPERATOR_PROVIDED_PDF_PACKAGE",
                "urls_fetched_for_body": False,
                "captured_as_of": AS_OF,
            },
        }
        normalized_path = NORMALIZED / f"{meta['source_id']}.json"
        write_json(normalized_path, normalized)
        write_text(NORMALIZED / f"{meta['source_id']}.md", normalized_markdown(normalized))

        record = {key: normalized[key] for key in (
            "source_id", "title", "series", "period", "year", "quarter", "publisher", "author",
            "publication_date_original", "publication_date_normalized", "publication_date_basis", "updated_date_original", "updated_date_normalized", "official_cross_references",
            "document_classification", "document_type", "canonical_url", "raw_path", "raw_sha256", "raw_byte_count",
            "page_count", "observed_filenames", "temporal_validity", "extraction_confidence", "known_limitations",
        )}
        record.update({
            "schema_version": "1.0.0",
            "archival_abstract": archival_abstract,
            "lineage_confidence": "HIGH" if author != "UNKNOWN" else "MEDIUM",
            "normalized_json_path": normalized_path.relative_to(ROOT).as_posix(),
            "normalized_markdown_path": (NORMALIZED / f"{meta['source_id']}.md").relative_to(ROOT).as_posix(),
            "manual_review_required": False,
        })
        write_json(SOURCE_RECORDS / f"{meta['source_id']}.json", record)
        write_text(SOURCE_RECORDS / f"{meta['source_id']}.md", markdown_source_record(record))

        extraction = {
            "schema_version": "1.0.0",
            "source_id": meta["source_id"],
            "title": meta["title"],
            "canonical_url": meta["canonical_url"],
            "document_classification": meta["document_classification"],
            "publisher": normalized["publisher"],
            "author": author,
            "period": meta["period"],
            "page_count": len(pages),
            "article_text": full_text,
            "pages": pages,
            "claims": [],
            "entities": [],
            "events": [],
            "relationships": [],
            "products": [],
            "governance": [],
            "lore": [],
            "actors": [],
            "guilds": [],
            "source_lineage": {
                "publication_role": "REFERENCE",
                "relationship": "REPORTS_ON",
                "primary_sources": ["UNKNOWN"],
                "original_creators": [author],
                "lineage_confidence": record["lineage_confidence"],
            },
            "semantic_enrichment_status": "NOT_PERFORMED",
            "extraction_confidence": confidence,
        }
        write_json(EXTRACTIONS / f"{meta['source_id']}.json", extraction)
        provenance = {
            "schema_version": "1.0.0",
            "campaign_id": CAMPAIGN_ID,
            "source_id": meta["source_id"],
            "observed_filenames": observed_filenames,
            "raw_path": normalized["raw_path"],
            "raw_sha256": normalized["raw_sha256"],
            "raw_byte_count": normalized["raw_byte_count"],
            "canonical_url": meta["canonical_url"],
            "body_retrieval_source": "OPERATOR_PROVIDED_PDF_PACKAGE",
            "urls_fetched_for_body": False,
            "source_package_filename": input_manifest["source_package_filename"],
            "source_package_sha256": input_manifest["source_package_sha256"],
            "captured_as_of": AS_OF,
        }
        write_json(PROVENANCE / f"{meta['source_id']}.json", provenance)
        records.append(record)

    duplicate_ledger = {
        "schema_version": "1.0.0",
        "campaign_id": CAMPAIGN_ID,
        "duplicates": [],
        "resolved_input_exclusions": [{
            "filename": "q4-2026.pdf",
            "disposition": "DISREGARDED_OPERATOR_CONFIRMED_MISLABELED_UPLOAD",
            "decision_basis": "Operator correction received 2026-07-22",
            "preserved_raw": False,
            "source_record_created": False,
            "manual_review_required": False,
        }],
    }
    write_json(CAMPAIGN / "duplicate-ledger.json", duplicate_ledger)

    package = {
        "metadata": {
            "package_id": "INGEST-OFFICIAL-ECONOMIC-REPORTS-001",
            "repository_schema": "2.1",
            "campaign_id": CAMPAIGN_ID,
            "generated_as_of": AS_OF,
        },
        "sources": [{
            "source_id": record["source_id"],
            "source_record": (SOURCE_RECORDS / f"{record['source_id']}.json").relative_to(ROOT).as_posix(),
            "extraction": (EXTRACTIONS / f"{record['source_id']}.json").relative_to(ROOT).as_posix(),
        } for record in records],
    }
    write_json(INGESTION / f"{CAMPAIGN_ID}.v2.1.json", package)

    summary = {
        "schema_version": "1.0.0",
        "campaign_id": CAMPAIGN_ID,
        "status": "INGESTION_COMPLETE",
        "as_of": AS_OF,
        "input_package_files": len(supplied_files),
        "valid_pdf_files": len(supplied_files),
        "unique_documents": len(records),
        "quarterly_reports": sum(1 for record in records if record["document_type"] == "OFFICIAL_QUARTERLY_ECONOMIC_REPORT"),
        "economics_papers": sum(1 for record in records if record["document_type"] == "OFFICIAL_ECONOMICS_PAPER"),
        "exact_duplicates": 0,
        "operator_exclusions": 1,
        "source_records": len(records),
        "normalized_records": len(records),
        "extractions": len(records),
        "total_unique_pages": total_pages,
        "total_extracted_characters": total_characters,
        "quarterly_coverage": {"first": "2022 Q2", "last": "2026 Q2"},
        "body_acquisition": "OPERATOR_PROVIDED_PDF_PACKAGE",
        "urls_fetched_for_body": False,
        "manual_review_queue": [],
        "semantic_enrichment": "NOT_PERFORMED",
        "knowledge_promotion": "NOT_PERFORMED",
        "visual_validation_status": "PASS_REPRESENTATIVE_RENDER_REVIEW",
    }
    write_json(CAMPAIGN / "campaign-summary.json", summary)
    write_text(CAMPAIGN / "campaign-summary.md", f"""# Official Economic Reports PDF Ingestion Summary

- Status: `{summary['status']}`
- Supplied PDF files: {summary['input_package_files']}
- Valid PDF files: {summary['valid_pdf_files']}
- Unique documents: {summary['unique_documents']}
- Quarterly reports: {summary['quarterly_reports']} ({summary['quarterly_coverage']['first']} through {summary['quarterly_coverage']['last']})
- Economics papers: {summary['economics_papers']}
- Exact duplicates: {summary['exact_duplicates']}
- Operator-confirmed excluded uploads: {summary['operator_exclusions']}
- Source Records / normalized records / extractions: {len(records)} each
- Unique pages preserved: {total_pages}
- Extracted text characters: {total_characters}
- Visual validation: representative render review passed
- Article-body URLs fetched: no

The supplied PDFs, not the 17 discovery URLs, are the preserved document bodies. The URLs remain identifiers and cross-references only.

## Operator adjudication

The operator confirmed that `q4-2026.pdf` was an accidentally mislabeled upload. It is excluded from the preserved corpus and generated artifacts. No 2026-Q4 Source Record was created, and no manual-review item remains open.

## Boundaries

No semantic claims, longitudinal metric series, knowledge pages, graph facts, or publication outputs were created or modified.
""")

    generated_paths = []
    for directory in (RAW, PROVENANCE, NORMALIZED, SOURCE_RECORDS, INGESTION):
        generated_paths.extend(path for path in directory.rglob("*") if path.is_file())
    for path in sorted(generated_paths):
        artifacts.append({"path": path.relative_to(ROOT).as_posix(), "byte_count": path.stat().st_size, "sha256": sha256(path)})
    manifest = {"schema_version": "1.0.0", "campaign_id": CAMPAIGN_ID, "generated_as_of": AS_OF, "artifact_count": len(artifacts), "artifacts": artifacts}
    write_json(ARCHIVE_MANIFEST, manifest)
    write_json(CAMPAIGN / "manifest.json", manifest)
    print(f"Built {len(records)} unique documents from {len(supplied_files)} supplied PDFs ({total_pages} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
