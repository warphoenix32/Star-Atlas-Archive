#!/usr/bin/env python3
"""Build the deterministic community wallet-attribution register."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "community-wallet-attribution-ingestion-2026-07"
SCHEMA_VERSION = "1.0.0"
AS_OF = "2026-07-20"
ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_DIR = Path(__file__).resolve().parent
RAW_REL = Path("archive/raw/community-wallet-attributions/Star Atlas Team Wallets.xlsx")
RAW_PATH = ROOT / RAW_REL
PROVENANCE_REL = Path("archive/provenance/community-wallet-attributions/star-atlas-team-wallets.json")
NORMALIZED_DIR_REL = Path("archive/normalized/community-wallet-attributions")
NORMALIZED_RECORDS_REL = NORMALIZED_DIR_REL / "wallet-attributions.jsonl"
NORMALIZED_METADATA_REL = NORMALIZED_DIR_REL / "metadata.json"
SOURCE_RECORD_DIR_REL = Path("archive/source-records/community-wallet-attributions")
SOURCE_ID = "SRC-COMMUNITY-WALLET-0F03FBCA3053"
SOURCE_RECORD_JSON_REL = SOURCE_RECORD_DIR_REL / f"{SOURCE_ID}.json"
SOURCE_RECORD_MD_REL = SOURCE_RECORD_DIR_REL / f"{SOURCE_ID}.md"
ARCHIVE_MANIFEST_REL = Path(f"archive/manifests/{CAMPAIGN_ID}.json")
EXPECTED_SHA256 = "0f03fbca30538564e818e2a7c4a83e72ca6ef360e1b09b3a4b6e0edca4b85cfa"
EXPECTED_HEADERS = ["ADDRESS", "NAME", "Major Group"]
EXPECTED_GROUP_COUNTS = {"DAO": 4, "FTX": 5, "Liquidity": 38, "Private Sale": 2, "Rewards": 10, "Team": 25}

DECISIONS = [
    {
        "decision_id": "WAL-001",
        "status": "ACCEPTED",
        "decision": "Classify the workbook as a COMMUNITY_ATTRIBUTED_SOLANA_WALLET_REGISTER, not a confirmed register of team-owned wallets.",
        "authority": "repository operator",
    },
    {
        "decision_id": "WAL-002",
        "status": "ACCEPTED",
        "decision": "Preserve and normalize the register in Archive scope; do not promote ownership claims to knowledge or public Library outputs without stronger evidence.",
        "authority": "repository operator",
    },
    {
        "decision_id": "WAL-003",
        "status": "ACCEPTED",
        "decision": "Leave compiler, source location, creation date, update date, and methodology UNKNOWN.",
        "authority": "repository operator",
    },
    {
        "decision_id": "WAL-004",
        "status": "ACCEPTED",
        "decision": "Perform no on-chain verification; record ownership and control as UNVERIFIED and on-chain observation as NOT_CHECKED.",
        "authority": "repository operator",
    },
]

RESEARCH_GAPS = [
    {"gap_id": "RG01_COMPILER", "description": "Workbook compiler and maintainer are UNKNOWN.", "priority": "MEDIUM"},
    {"gap_id": "RG02_METHODOLOGY", "description": "Attribution methodology and row-level evidence are unavailable.", "priority": "HIGH"},
    {"gap_id": "RG03_TEMPORAL_SCOPE", "description": "Creation, update, and effective dates are unavailable.", "priority": "HIGH"},
    {"gap_id": "RG04_OWNERSHIP_CONTROL", "description": "No official or on-chain ownership/control verification was performed.", "priority": "HIGH"},
]

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58_INDEX = {char: index for index, char in enumerate(BASE58_ALPHABET)}
XML_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def dump_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)


def column_index(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference)
    if not letters:
        raise ValueError(f"invalid XLSX cell reference: {reference}")
    value = 0
    for char in letters.group(0):
        value = value * 26 + ord(char) - 64
    return value - 1


def load_workbook_rows(path: Path) -> tuple[str, list[list[str]]]:
    """Read the first worksheet using only deterministic XLSX XML structures."""
    with zipfile.ZipFile(path) as package:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in package.namelist():
            root = ET.fromstring(package.read("xl/sharedStrings.xml"))
            for item in root.findall("m:si", XML_NS):
                shared.append("".join(node.text or "" for node in item.findall(".//m:t", XML_NS)))

        workbook = ET.fromstring(package.read("xl/workbook.xml"))
        first_sheet = workbook.find("m:sheets/m:sheet", XML_NS)
        if first_sheet is None:
            raise ValueError("workbook contains no worksheet")
        sheet_name = first_sheet.attrib["name"]
        rel_id = first_sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        rels = ET.fromstring(package.read("xl/_rels/workbook.xml.rels"))
        targets = {item.attrib["Id"]: item.attrib["Target"] for item in rels.findall("r:Relationship", REL_NS)}
        target = targets[rel_id].lstrip("/")
        sheet_path = target if target.startswith("xl/") else f"xl/{target}"
        sheet = ET.fromstring(package.read(sheet_path))

        rows: list[list[str]] = []
        for row_node in sheet.findall("m:sheetData/m:row", XML_NS):
            cells: dict[int, str] = {}
            for cell in row_node.findall("m:c", XML_NS):
                index = column_index(cell.attrib["r"])
                cell_type = cell.attrib.get("t")
                if cell_type == "inlineStr":
                    value = "".join(node.text or "" for node in cell.findall(".//m:t", XML_NS))
                else:
                    value_node = cell.find("m:v", XML_NS)
                    raw_value = "" if value_node is None else value_node.text or ""
                    value = shared[int(raw_value)] if cell_type == "s" and raw_value else raw_value
                cells[index] = value
            if cells:
                rows.append([cells.get(index, "") for index in range(max(cells) + 1)])
        return sheet_name, rows


def decode_base58(value: str) -> bytes:
    number = 0
    for char in value:
        if char not in BASE58_INDEX:
            raise ValueError(f"invalid base58 character {char!r}")
        number = number * 58 + BASE58_INDEX[char]
    decoded = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return b"\x00" * (len(value) - len(value.lstrip("1"))) + decoded


def address_status(address: str) -> str:
    try:
        return "VALID_SOLANA_PUBLIC_KEY_SYNTAX" if len(decode_base58(address)) == 32 else "INVALID_SOLANA_PUBLIC_KEY_LENGTH"
    except ValueError:
        return "INVALID_BASE58_SYNTAX"


def record_id(address: str) -> str:
    return f"SA-WALLET-ATTR-{hashlib.sha256(address.encode('utf-8')).hexdigest()[:16].upper()}"


def load_source_rows() -> tuple[str, list[dict[str, str]]]:
    sheet_name, rows = load_workbook_rows(RAW_PATH)
    if not rows:
        raise ValueError("workbook has no rows")
    headers = rows[0]
    if headers != EXPECTED_HEADERS:
        raise ValueError(f"unexpected workbook headers: {headers!r}")
    records = []
    for row_number, values in enumerate(rows[1:], start=2):
        padded = values + [""] * (len(headers) - len(values))
        records.append({**dict(zip(headers, padded[: len(headers)])), "_row_number": str(row_number)})
    return sheet_name, records


def build_records(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in rows:
        address = row["ADDRESS"]
        records.append({
            "record_id": record_id(address),
            "schema_version": SCHEMA_VERSION,
            "record_type": "community_wallet_attribution",
            "network": "Solana",
            "address": address,
            "address_format_status": address_status(address),
            "observed_label": row["NAME"],
            "observed_major_group": row["Major Group"],
            "text_policy": "PRESERVED_EXACTLY_AS_CAPTURED",
            "relationship_claim": "COMMUNITY_ATTRIBUTED_ASSOCIATION",
            "attribution": {
                "source_class": "COMMUNITY_EFFORT",
                "operator_assessment": "HIGH_LIKELIHOOD",
                "official_confirmation_status": "UNCONFIRMED",
                "ownership_verification_status": "UNVERIFIED",
                "control_verification_status": "UNVERIFIED",
                "onchain_observation_status": "NOT_CHECKED",
                "methodology": "UNKNOWN",
                "effective_from": None,
                "effective_to": None,
            },
            "source": {
                "source_id": SOURCE_ID,
                "path": RAW_REL.as_posix(),
                "worksheet": "SA Wallet List",
                "row_number": int(row["_row_number"]),
                "sha256": EXPECTED_SHA256,
            },
            "evidence_notes": [
                "The supplied label and group are community attributions, not verified ownership or control.",
                "Syntactic public-key validity establishes neither identity nor transaction history.",
                "No on-chain analysis was performed in this campaign.",
            ],
            "manual_review_required": True,
            "research_gap_ids": [gap["gap_id"] for gap in RESEARCH_GAPS],
        })
    return records


def source_record_json() -> dict[str, Any]:
    return {
        "source_id": SOURCE_ID,
        "title": "Star Atlas Team Wallets (community-attributed register)",
        "document_type": "COMMUNITY_ATTRIBUTED_SOLANA_WALLET_REGISTER",
        "source_type": "operator_submitted_workbook",
        "publisher": "UNKNOWN",
        "creator": ["UNKNOWN"],
        "published_at_original": None,
        "published_at_normalized": None,
        "updated_at_original": None,
        "updated_at_normalized": None,
        "captured_at": AS_OF,
        "access": "operator_provided",
        "canonical_url": None,
        "artifact_chain": {
            "raw": RAW_REL.as_posix(),
            "provenance": PROVENANCE_REL.as_posix(),
            "normalized_records": NORMALIZED_RECORDS_REL.as_posix(),
            "normalized_metadata": NORMALIZED_METADATA_REL.as_posix(),
            "source_record_json": SOURCE_RECORD_JSON_REL.as_posix(),
            "source_record_markdown": SOURCE_RECORD_MD_REL.as_posix(),
        },
        "source_lineage": {
            "publication": "UNKNOWN community compilation",
            "publication_role": "COMMUNITY_ATTRIBUTION_REGISTER",
            "relationship": "ATTRIBUTES_ASSOCIATION",
            "primary_sources": ["UNKNOWN"],
            "original_creators": ["UNKNOWN"],
            "lineage_confidence": "LOW",
        },
        "authority": {
            "classification": "COMMUNITY_UNCONFIRMED",
            "operator_assessment": "HIGH_LIKELIHOOD",
            "scope": "Attribution likelihood only; not proof of ownership, control, activity, purpose, or temporal duration.",
        },
        "quality": {
            "extraction_confidence": "HIGH",
            "attribution_confidence": "QUALIFIED_HIGH_LIKELIHOOD_OPERATOR_ASSESSMENT",
            "manual_review_required": True,
            "limitations": [gap["description"] for gap in RESEARCH_GAPS],
        },
        "provenance": {
            "acquisition_method": "submitted directly by repository operator",
            "original_filename": "Star Atlas Team Wallets.xlsx",
            "raw_path": RAW_REL.as_posix(),
            "raw_sha256": EXPECTED_SHA256,
            "preservation_policy": "byte-for-byte raw preservation",
        },
    }


def source_record_markdown() -> str:
    return f"""# Star Atlas Team Wallets (community-attributed register)

## Metadata

- **Source ID:** `{SOURCE_ID}`
- **Document type:** `COMMUNITY_ATTRIBUTED_SOLANA_WALLET_REGISTER`
- **Publisher / compiler:** `UNKNOWN`
- **Publication date:** `UNKNOWN`
- **Update date:** `UNKNOWN`
- **Raw artifact:** `{RAW_REL.as_posix()}`
- **SHA-256:** `{EXPECTED_SHA256}`
- **Extraction confidence:** `HIGH`
- **Manual review required:** `true`

## Source Lineage

- **Publication role:** `COMMUNITY_ATTRIBUTION_REGISTER`
- **Relationship:** `ATTRIBUTES_ASSOCIATION`
- **Primary sources:** `UNKNOWN`
- **Original creators:** `UNKNOWN`
- **Lineage confidence:** `LOW`

## Archival Scope

This workbook contains 84 community-attributed Solana wallet records. The repository operator assesses the associations as highly likely, but neither the Star Atlas team nor an on-chain verification campaign confirmed ownership or control. The supplied address, label, and major-group text are preserved exactly as captured.

The normalized register is evidence of the community attribution itself. It is not proof that a named person or organization owns, controls, currently uses, or historically used an address for the purpose implied by its label.

## Verification Boundary

- All 84 addresses are syntactically valid 32-byte Solana public keys.
- `official_confirmation_status` remains `UNCONFIRMED`.
- Ownership and control remain `UNVERIFIED`.
- `onchain_observation_status` remains `NOT_CHECKED`.
- No wallet association is promoted to `knowledge/`, `graph/`, or `publication/` by this campaign.

## Known Limitations and Research Gaps

1. Workbook compiler and maintainer are unknown.
2. Attribution methodology and row-level supporting evidence are unavailable.
3. Creation, update, and effective dates are unknown.
4. On-chain activity, ownership, control, and historical duration were not verified.
"""


def build_artifacts() -> dict[str, str]:
    sheet_name, rows = load_source_rows()
    records = build_records(rows)
    raw_bytes = RAW_PATH.read_bytes()
    group_counts = dict(sorted(Counter(row["Major Group"] for row in rows).items()))
    label_counts = dict(sorted(Counter(row["NAME"] for row in rows).items()))

    provenance = {
        "source_id": SOURCE_ID,
        "artifact_type": "community_attributed_solana_wallet_register",
        "campaign_id": CAMPAIGN_ID,
        "custody": {
            "acquired_at": AS_OF,
            "acquisition_method": "submitted directly by repository operator",
            "original_filename": "Star Atlas Team Wallets.xlsx",
            "compiler": "UNKNOWN",
            "source_location": "UNKNOWN",
            "created_at": "UNKNOWN",
            "updated_at": "UNKNOWN",
            "methodology": "UNKNOWN",
            "preservation_policy": "byte-for-byte raw preservation",
        },
        "raw_artifact": {
            "path": RAW_REL.as_posix(),
            "sha256": sha256_bytes(raw_bytes),
            "byte_length": len(raw_bytes),
            "format": "Microsoft Excel Open XML workbook",
            "worksheet": sheet_name,
        },
        "authority": {
            "source_class": "COMMUNITY_EFFORT",
            "operator_assessment": "HIGH_LIKELIHOOD",
            "official_confirmation_status": "UNCONFIRMED",
            "ownership_verification_status": "UNVERIFIED",
            "onchain_observation_status": "NOT_CHECKED",
        },
        "status": "RAW_PRESERVED_ATTRIBUTION_QUALIFIED",
    }

    metadata = {
        "campaign_id": CAMPAIGN_ID,
        "schema_version": SCHEMA_VERSION,
        "source_id": SOURCE_ID,
        "source_path": RAW_REL.as_posix(),
        "source_sha256": EXPECTED_SHA256,
        "worksheet": sheet_name,
        "headers": EXPECTED_HEADERS,
        "record_count": len(records),
        "unique_address_count": len({record["address"] for record in records}),
        "address_format_counts": dict(sorted(Counter(record["address_format_status"] for record in records).items())),
        "major_group_counts": group_counts,
        "repeated_label_counts": {key: value for key, value in label_counts.items() if value > 1},
        "normalization_policy": {
            "observed_text": "PRESERVED_EXACTLY_AS_CAPTURED",
            "community_attribution": "PRESERVED_AS_QUALIFIED_CLAIM",
            "ownership_control": "UNVERIFIED",
            "onchain_analysis": "NOT_PERFORMED",
            "knowledge_promotion": "PROHIBITED_WITHOUT_STRONGER_EVIDENCE",
        },
        "research_gaps": RESEARCH_GAPS,
    }

    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "COMPLETE_WITH_RETAINED_RESEARCH_GAPS",
        "source_artifacts": 1,
        "records_extracted": len(records),
        "unique_addresses": len({record["address"] for record in records}),
        "syntactically_valid_solana_public_keys": sum(record["address_format_status"] == "VALID_SOLANA_PUBLIC_KEY_SYNTAX" for record in records),
        "group_counts": group_counts,
        "duplicate_addresses": len(records) - len({record["address"] for record in records}),
        "manual_review_records": len(records),
        "onchain_analysis_performed": False,
        "knowledge_promotions": 0,
        "accepted_human_decisions": len(DECISIONS),
        "research_gap_count": len(RESEARCH_GAPS),
    }

    summary_md = """# Community Wallet Attribution Ingestion — Campaign Summary

The campaign preserved one operator-provided workbook and normalized all 84 supplied wallet-attribution rows without converting community assertions into verified ownership claims.

## Results

- Source artifacts preserved: 1
- Wallet-attribution records extracted: 84
- Unique addresses: 84
- Syntactically valid 32-byte Solana public keys: 84
- Duplicate addresses: 0
- Records retaining manual review: 84
- On-chain analyses performed: 0
- Knowledge, graph, or publication promotions: 0

## Attribution Boundary

The repository operator assesses these associations as highly likely. That assessment is preserved separately from verification. The campaign does not assert that ATMTA confirmed the register, nor that an address is owned, controlled, active, or historically continuous.

## Group Counts

| Observed major group | Records |
|---|---:|
| DAO | 4 |
| FTX | 5 |
| Liquidity | 38 |
| Private Sale | 2 |
| Rewards | 10 |
| Team | 25 |

## Retained Research Gaps

- Compiler, source location, and methodology are unknown.
- Creation, update, and effective dates are unknown.
- Row-level attribution evidence is unavailable.
- Ownership, control, and on-chain activity remain unverified and were not checked.
"""

    decisions_payload = {
        "campaign_id": CAMPAIGN_ID,
        "decision_count": len(DECISIONS),
        "open_decision_count": 0,
        "decisions": DECISIONS,
    }

    artifacts: dict[str, str] = {
        PROVENANCE_REL.as_posix(): dump_json(provenance),
        NORMALIZED_RECORDS_REL.as_posix(): dump_jsonl(records),
        NORMALIZED_METADATA_REL.as_posix(): dump_json(metadata),
        SOURCE_RECORD_JSON_REL.as_posix(): dump_json(source_record_json()),
        SOURCE_RECORD_MD_REL.as_posix(): source_record_markdown(),
        f"operations/campaigns/{CAMPAIGN_ID}/normalized-preview.jsonl": dump_jsonl(records),
        f"operations/campaigns/{CAMPAIGN_ID}/curator-decisions.json": dump_json(decisions_payload),
        f"operations/campaigns/{CAMPAIGN_ID}/campaign-summary.json": dump_json(summary),
        f"operations/campaigns/{CAMPAIGN_ID}/campaign-summary.md": summary_md,
    }

    manifest_entries = [{
        "path": path,
        "sha256": sha256_bytes(content.encode("utf-8")),
        "byte_length": len(content.encode("utf-8")),
    } for path, content in sorted(artifacts.items())]
    manifest_entries.insert(0, {
        "path": RAW_REL.as_posix(),
        "sha256": sha256_bytes(raw_bytes),
        "byte_length": len(raw_bytes),
    })
    manifest = {
        "campaign_id": CAMPAIGN_ID,
        "generated_as_of": AS_OF,
        "artifact_count": len(manifest_entries),
        "artifacts": manifest_entries,
    }
    manifest_text = dump_json(manifest)
    artifacts[ARCHIVE_MANIFEST_REL.as_posix()] = manifest_text
    artifacts[f"operations/campaigns/{CAMPAIGN_ID}/manifest.json"] = manifest_text
    return artifacts


def write_artifacts() -> dict[str, str]:
    artifacts = build_artifacts()
    for relative, content in artifacts.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    return artifacts


def main() -> int:
    if not RAW_PATH.is_file():
        raise SystemExit(f"missing source workbook: {RAW_PATH}")
    if sha256(RAW_PATH) != EXPECTED_SHA256:
        raise SystemExit("source workbook SHA-256 does not match the accepted artifact")
    write_artifacts()
    print(f"Built {CAMPAIGN_ID}: 84 qualified wallet-attribution records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
