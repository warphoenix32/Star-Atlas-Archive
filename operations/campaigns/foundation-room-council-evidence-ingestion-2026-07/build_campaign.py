#!/usr/bin/env python3
"""Build the Council snapshot and Foundation Room Discord evidence campaign."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import shutil
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
CAMPAIGN_ID = "foundation-room-council-evidence-ingestion-2026-07"
SNAPSHOT_DATE = "2026-07-23"
COUNCIL_URL = "https://docs.google.com/spreadsheets/d/1QWkFjcLwhw4GHqk5Stz72H3WRwIb52f-UDnKne7hTtY/edit"

COUNCIL_RAW = (
    REPO
    / "archive/raw/governance/council-pip-tracker/snapshots/2026-07-23"
    / "Star Atlas DAO Council -- PIP Tracker & Grading Rubric - Tracker.csv"
)
COUNCIL_NORM = REPO / "archive/normalized/governance/council-pip-tracker/snapshots/2026-07-23"
COUNCIL_PROV = REPO / "archive/provenance/governance/council-pip-tracker/snapshots/2026-07-23.json"
COUNCIL_RECORDS = REPO / "archive/source-records/governance/council-pip-tracker/snapshots/2026-07-23"
PRIOR_COUNCIL = (
    REPO
    / "archive/semantic/governance/council-pip-tracker"
    / "council-pip-tracker-semantic-records.jsonl"
)

DISCORD_SOURCES = (
    {
        "slug": "foundation-room",
        "channel_category": "foundation-room",
        "raw": REPO
        / "archive/raw/discord/star-atlas/foundation-room"
        / "discord-foundation-room-2026-07-23T12-18-57-639Z.json.gz",
        "original_filename": "discord-😎┃foundation-room-2026-07-23T12-18-57-639Z.json",
        "original_sha256": "e5000077fee2223d58eda82334f868a56c3db2648a2f760fa9cb0a0841482480",
        "original_bytes": 7_844_471,
    },
    {
        "slug": "fr-chat",
        "channel_category": "foundation-room-chat",
        "raw": REPO
        / "archive/raw/discord/star-atlas/fr-chat"
        / "discord-fr-chat-2026-07-23T08-24-13-992Z.json.gz",
        "original_filename": "discord-💥┃fr-chat-2026-07-23T08-24-13-992Z.json",
        "original_sha256": "d251ef982cee3dec9ec93e02d14b9f8ea297d630e37babf7d2cbc090e790c90e",
        "original_bytes": 261_351_795,
    },
)
DISCORD_NORM = REPO / "archive/normalized/discord/star-atlas"
DISCORD_PROV = REPO / "archive/provenance/discord/star-atlas"
DISCORD_RECORDS = REPO / "archive/source-records/discord/star-atlas"
ARCHIVE_MANIFEST = REPO / "archive/manifests/foundation-room-council-evidence-ingestion-2026-07.json"

CONTROLLED_PAYMENT_STATES = {
    "REQUESTED",
    "AUTHORIZED",
    "COUNCIL_REPORTED",
    "UNVERIFIED",
    "MISSING_ONCHAIN_EVIDENCE",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def jsonl_line(record: dict[str, Any]) -> str:
    # Python's str.splitlines() treats U+2028/U+2029 as record boundaries even
    # though JSON permits them inside strings. Escaping only those separators
    # keeps one physical JSONL record per LF without changing text semantics.
    return (
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(jsonl_line(record) + "\n")


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:16].upper()}"


def clean_header(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def optional(value: str | None) -> str | None:
    text = (value or "").strip()
    return text or None


def normalized_number(value: str | None) -> str | None:
    text = optional(value)
    if text is None or text in {"?", "N/A"}:
        return None
    try:
        number = Decimal(text.replace(",", "").replace("%", ""))
    except InvalidOperation:
        return None
    if text.endswith("%"):
        number /= Decimal(100)
    return format(number.normalize(), "f")


def normalized_date(value: str | None) -> str | None:
    text = optional(value)
    if text is None:
        return None
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def data_row(record: dict[str, str]) -> bool:
    ignored = {"PDF sent to Foundation", "Markdown sent to ATMTA"}
    return any(optional(value) for key, value in record.items() if key and key not in ignored)


def council_states(record: dict[str, str]) -> dict[str, Any]:
    result = (record.get("Vote Result") or "").strip().casefold()
    phase = (record.get("PIP Phase") or "").strip().casefold()
    note = (record.get("Note") or "").strip().casefold()
    amount = normalized_number(record.get("Amount"))
    paid_fields = [
        record.get("Total Amount Paid (USDC)"),
        record.get("Total Amount Left (USDC)"),
        record.get("Total Amount Paid (ATLAS)"),
        record.get("Total Amount Left (ATLAS)"),
    ]
    numeric_payment = any(normalized_number(value) is not None for value in paid_fields)
    unknown_payment = any(optional(value) == "?" for value in paid_fields)
    monetary = amount not in (None, "0") or numeric_payment or unknown_payment

    authorization_state = "AUTHORIZED" if result == "passed" else "REQUESTED"
    if numeric_payment:
        payment_state = "COUNCIL_REPORTED"
    else:
        payment_state = "UNVERIFIED"

    completed = normalized_number(record.get("Completed Milestones"))
    total = normalized_number(record.get("Total Payment Milestones"))
    if "will not be implemented" in note or phase in {"withdrawn", "terminated", "cancelled", "canceled"}:
        implementation_state = "COUNCIL_REPORTED_NOT_IMPLEMENTED"
    elif completed is not None and total is not None and Decimal(total) > 0:
        implementation_state = (
            "COUNCIL_REPORTED_COMPLETE"
            if Decimal(completed) >= Decimal(total)
            else "COUNCIL_REPORTED_PARTIAL"
        )
    else:
        implementation_state = "UNKNOWN"

    return {
        "authorization_state": authorization_state,
        "payment_state": payment_state,
        "onchain_verification_state": "MISSING_ONCHAIN_EVIDENCE" if monetary else "UNVERIFIED",
        "implementation_state": implementation_state,
        "monetary_proposal_or_program": monetary,
    }


def build_council() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    raw_bytes = COUNCIL_RAW.read_bytes()
    rows = list(csv.reader(raw_bytes.decode("utf-8-sig").splitlines()))
    header_index = next(index for index, row in enumerate(rows) if "PIP" in row)
    headers = [clean_header(value) for value in rows[header_index]]
    source_sha = sha256_bytes(raw_bytes)

    if COUNCIL_NORM.exists():
        shutil.rmtree(COUNCIL_NORM)
    if COUNCIL_RECORDS.exists():
        shutil.rmtree(COUNCIL_RECORDS)
    COUNCIL_NORM.mkdir(parents=True, exist_ok=True)
    COUNCIL_RECORDS.mkdir(parents=True, exist_ok=True)

    normalized: list[dict[str, Any]] = []
    future_dates: list[dict[str, Any]] = []
    for csv_index, row in enumerate(rows[header_index + 1 :], start=header_index + 2):
        mapped = {
            header: row[index].strip()
            for index, header in enumerate(headers)
            if header and index < len(row)
        }
        if not data_row(mapped):
            continue
        pip_text = optional(mapped.get("PIP"))
        pip_match = re.fullmatch(r"PIP-(\d+)", pip_text or "", flags=re.IGNORECASE)
        pip_number = int(pip_match.group(1)) if pip_match else None
        title = optional(mapped.get("PIP Name"))
        identity = f"{source_sha}:{csv_index}:{json.dumps(row, ensure_ascii=False, separators=(',', ':'))}"
        source_id = stable_id("SA-COUNCIL-SNAPSHOT", identity)
        dates = {
            "draft": {"original": optional(mapped.get("Draft Date")), "normalized": normalized_date(mapped.get("Draft Date"))},
            "vote_started": {"original": optional(mapped.get("Voted Started")), "normalized": normalized_date(mapped.get("Voted Started"))},
            "vote_ended": {"original": optional(mapped.get("Vote Ended")), "normalized": normalized_date(mapped.get("Vote Ended"))},
        }
        for field, value in dates.items():
            if value["normalized"] and value["normalized"] > SNAPSHOT_DATE:
                future_dates.append(
                    {
                        "source_id": source_id,
                        "pip_id": pip_text,
                        "title": title,
                        "field": field,
                        "value": value,
                    }
                )
        states = council_states(mapped)
        record = {
            "schema_version": "1.0.0",
            "source_id": source_id,
            "source_class": "TIER_1_COUNCIL_OPERATIONAL_TRACKER",
            "assessment_source": "STAR_ATLAS_COUNCIL_TRACKER",
            "assessment_type": "COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT",
            "independent_verification_status": "UNKNOWN",
            "snapshot_date": SNAPSHOT_DATE,
            "csv_record_number": csv_index,
            "pip_id": pip_text,
            "pip_number": pip_number,
            "title": title,
            "phase": optional(mapped.get("PIP Phase")),
            "status": optional(mapped.get("Status")),
            "dates": dates,
            "step_number": optional(mapped.get("Step #")),
            "proposal_amount": {
                "original": optional(mapped.get("Amount")),
                "normalized": normalized_number(mapped.get("Amount")),
                "asset": optional(mapped.get("Type")),
            },
            "council_roi_assessment": optional(mapped.get("DAO ROI What did it accomplish?")),
            "ecosystem_fund": optional(mapped.get("Ecosystem Fund?")),
            "vote": {
                "result": optional(mapped.get("Vote Result")),
                "ballot_count": normalized_number(mapped.get("# of Votes")),
                "pvp_voted_m": normalized_number(mapped.get("PVP Voted (M)")),
                "pvp_participation": normalized_number(mapped.get("PVP Participation")),
                "total_pvp_m": normalized_number(mapped.get("Total PVP (M)")),
                "yes": normalized_number(mapped.get("Yes")),
                "no": normalized_number(mapped.get("No")),
                "abstain": normalized_number(mapped.get("Abstain")),
            },
            "category": optional(mapped.get("Category")),
            "council_term": optional(mapped.get("SAC Term")),
            "note": optional(mapped.get("Note")),
            "payment": {
                "paid_usdc": {"original": optional(mapped.get("Total Amount Paid (USDC)")), "normalized": normalized_number(mapped.get("Total Amount Paid (USDC)"))},
                "left_usdc": {"original": optional(mapped.get("Total Amount Left (USDC)")), "normalized": normalized_number(mapped.get("Total Amount Left (USDC)"))},
                "paid_atlas": {"original": optional(mapped.get("Total Amount Paid (ATLAS)")), "normalized": normalized_number(mapped.get("Total Amount Paid (ATLAS)"))},
                "left_atlas": {"original": optional(mapped.get("Total Amount Left (ATLAS)")), "normalized": normalized_number(mapped.get("Total Amount Left (ATLAS)"))},
                "completed_milestones": {"original": optional(mapped.get("Completed Milestones")), "normalized": normalized_number(mapped.get("Completed Milestones"))},
                "total_milestones": {"original": optional(mapped.get("Total Payment Milestones")), "normalized": normalized_number(mapped.get("Total Payment Milestones"))},
                **states,
            },
            "evidence_limits": [
                "Council-authored tracker fields are operational assessments, not independent verification.",
                "Reported payments are not on-chain verified by this campaign.",
                "Proposal, vote, authorization, payment, implementation, and completion remain distinct states.",
            ],
            "raw_fields": mapped,
        }
        normalized.append(record)
        write_json(
            COUNCIL_RECORDS / f"{source_id}.json",
            {
                "source_id": source_id,
                "source_class": record["source_class"],
                "title": title,
                "pip_id": pip_text,
                "snapshot_date": SNAPSHOT_DATE,
                "csv_record_number": csv_index,
                "source_url": COUNCIL_URL,
                "raw_path": COUNCIL_RAW.relative_to(REPO).as_posix(),
                "raw_sha256": source_sha,
                "attribution": "STAR_ATLAS_COUNCIL_TRACKER",
                "assessment_type": record["assessment_type"],
                "independent_verification_status": "UNKNOWN",
                "limitations": record["evidence_limits"],
            },
        )

    write_jsonl(COUNCIL_NORM / "tracker-records.jsonl", normalized)
    write_json(
        COUNCIL_NORM / "tracker.json",
        {
            "schema_version": "1.0.0",
            "snapshot_date": SNAPSHOT_DATE,
            "source_sha256": source_sha,
            "headers": headers,
            "record_count": len(normalized),
            "records": normalized,
        },
    )
    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "source_kind": "operator_supplied_csv_export",
        "title": "Star Atlas DAO Council -- PIP Tracker & Grading Rubric - Tracker",
        "snapshot_date": SNAPSHOT_DATE,
        "source_url": COUNCIL_URL,
        "raw_path": COUNCIL_RAW.relative_to(REPO).as_posix(),
        "raw_bytes": len(raw_bytes),
        "raw_sha256": source_sha,
        "authority": "COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT",
        "independent_verification_status": "UNKNOWN",
        "onchain_verification_performed": False,
    }
    write_json(COUNCIL_PROV, provenance)

    prior = []
    if PRIOR_COUNCIL.exists():
        prior = [
            json.loads(line)
            for line in PRIOR_COUNCIL.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    prior_by_key = {
        (item.get("pip_id") or (item.get("title") or "").casefold()): item
        for item in prior
    }
    comparisons = []
    compare_fields = ("title", "phase", "status", "vote_result", "note")
    for item in normalized:
        key = item.get("pip_id") or (item.get("title") or "").casefold()
        old = prior_by_key.get(key)
        new_view = {
            "title": item.get("title"),
            "phase": item.get("phase"),
            "status": item.get("status"),
            "vote_result": item["vote"].get("result"),
            "note": item.get("note"),
            "payment_fields": item["payment"],
        }
        old_view = (
            {field: old.get(field) for field in compare_fields}
            | {"payment_fields": old.get("payment_fields")}
            if old
            else None
        )
        comparisons.append(
            {
                "snapshot_source_id": item["source_id"],
                "pip_id": item.get("pip_id"),
                "title": item.get("title"),
                "prior_source_id": old.get("source_id") if old else None,
                "reconciliation_status": "PRIOR_RECORD_FOUND" if old else "NEW_OR_UNNUMBERED_RECORD",
                "changed": old_view != new_view if old_view else True,
                "prior": old_view,
                "snapshot": new_view,
            }
        )
    return provenance, normalized, future_dates, comparisons


def discord_original_bytes(path: Path) -> bytes:
    with gzip.open(path, "rb") as stream:
        return stream.read()


def build_discord(source: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw_bytes = discord_original_bytes(source["raw"])
    if sha256_bytes(raw_bytes) != source["original_sha256"] or len(raw_bytes) != source["original_bytes"]:
        raise SystemExit(f"Discord raw reconstruction failed: {source['slug']}")
    document = json.loads(raw_bytes.decode("utf-8"))
    metadata = document["metadata"]
    source_meta = document["source"]
    collection = document["collection"]
    diagnostics = document["diagnostics"]
    messages = sorted(
        document["messages"],
        key=lambda item: (item.get("timestamp") or "", item.get("messageId") or ""),
    )
    participants = {item["participantId"]: item for item in document["participants"]}
    channel = source_meta["conversation"]
    workspace = source_meta["workspace"]
    collection_source_id = stable_id(
        "SA-DISCORD-EXPORT",
        f"{metadata['exportId']}:{source['original_sha256']}",
    )

    norm_dir = DISCORD_NORM / source["slug"]
    record_dir = DISCORD_RECORDS / source["slug"]
    if norm_dir.exists():
        shutil.rmtree(norm_dir)
    if record_dir.exists():
        shutil.rmtree(record_dir)
    norm_dir.mkdir(parents=True, exist_ok=True)
    record_dir.mkdir(parents=True, exist_ok=True)

    participant_records = []
    for participant in sorted(document["participants"], key=lambda item: item["participantId"]):
        participant_records.append(
            {
                **participant,
                "collection_source_id": collection_source_id,
                "server_id": workspace.get("id"),
                "channel_id": channel.get("id"),
                "identity_limit": "DISPLAY_NAMES_AND_ALIASES_ARE_EXPORT_OBSERVATIONS_NOT_LEGAL_IDENTITY_PROOF",
            }
        )
    write_jsonl(norm_dir / "participants.jsonl", participant_records)

    month_streams: dict[str, Any] = {}
    month_counts: defaultdict[str, int] = defaultdict(int)
    try:
        for ordinal, message in enumerate(messages, 1):
            timestamp = message.get("timestamp")
            month = timestamp[:7] if isinstance(timestamp, str) and re.match(r"^\d{4}-\d{2}", timestamp) else "unknown"
            if month not in month_streams:
                path = norm_dir / "messages" / f"{month}.jsonl"
                path.parent.mkdir(parents=True, exist_ok=True)
                month_streams[month] = path.open("w", encoding="utf-8", newline="\n")
            month_counts[month] += 1
            participant = participants.get(message.get("participantId"), {})
            native = (message.get("provenance") or {}).get("discordNative") or {}
            message_id = str(message["messageId"])
            message_source_id = stable_id(
                "SA-DISCORD-MSG",
                f"{workspace.get('id')}:{channel.get('id')}:{message_id}",
            )
            content = message.get("content") or {}
            normalized = {
                "source_id": message_source_id,
                "collection_source_id": collection_source_id,
                "server_or_community_name": workspace.get("name"),
                "canonical_channel_name": source["slug"],
                "observed_channel_name": channel.get("name"),
                "channel_category": source["channel_category"],
                "channel_id": channel.get("id"),
                "message_id": message_id,
                "timestamp_iso": timestamp,
                "author": participant.get("displayName"),
                "author_id": participant.get("platformUserId"),
                "participant_id": message.get("participantId"),
                "author_inferred": bool((message.get("flags") or {}).get("authorInferred")),
                "content": content.get("text") or "",
                "reply": message.get("reply"),
                "mentions": message.get("mentions") or [],
                "attachments": message.get("attachments") or [],
                "flags": message.get("flags") or {},
                "jump_link": native.get("jumpLink"),
                "raw_message_ordinal": ordinal,
            }
            if content.get("format") not in (None, "plain") or content.get("kind") not in (None, "text"):
                normalized["content_metadata"] = {
                    "format": content.get("format"),
                    "kind": content.get("kind"),
                }
            month_streams[month].write(
                jsonl_line(normalized) + "\n"
            )
    finally:
        for stream in month_streams.values():
            stream.close()

    message_files = []
    for month, count in sorted(month_counts.items()):
        path = norm_dir / "messages" / f"{month}.jsonl"
        message_files.append(
            {
                "month": month,
                "path": path.relative_to(REPO).as_posix(),
                "message_count": count,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    write_json(
        norm_dir / "message-file-index.json",
        {
            "schema_version": "1.0.0",
            "collection_source_id": collection_source_id,
            "message_count": len(messages),
            "files": message_files,
        },
    )

    collection_record = {
        "schema_version": "1.0.0",
        "collection_source_id": collection_source_id,
        "metadata": metadata,
        "source": source_meta,
        "collection": collection,
        "diagnostics": diagnostics,
        "provenance": {
            **document["provenance"],
            "raw_archive_path": source["raw"].relative_to(REPO).as_posix(),
            "raw_compressed_sha256": sha256_file(source["raw"]),
            "raw_original_filename": source["original_filename"],
            "raw_original_bytes": source["original_bytes"],
            "raw_original_sha256": source["original_sha256"],
        },
        "normalized_counts_by_month": dict(sorted(month_counts.items())),
    }
    write_json(norm_dir / "collection.json", collection_record)
    write_json(
        record_dir / f"{collection_source_id}.json",
        {
            "source_id": collection_source_id,
            "source_class": "NATIVE_DISCORD_CHANNEL_EXPORT",
            "platform": "discord",
            "server": workspace,
            "channel": channel,
            "source_url": source_meta.get("url"),
            "capture_timestamp": metadata.get("exportedAt"),
            "coverage": collection.get("coverage"),
            "collection_complete": collection.get("complete"),
            "message_count": len(messages),
            "participant_count": len(participants),
            "raw_path": source["raw"].relative_to(REPO).as_posix(),
            "raw_original_sha256": source["original_sha256"],
            "authority_scope": "Evidence of captured Discord messages and conversation context; message claims are not automatically factual or canonical.",
            "identity_limit": "Display-name and exporter identity observations do not independently prove real-world identity.",
            "media_limit": {
                "excluded_media": diagnostics.get("excludedMedia") or [],
                "treatment": "Attachment metadata and URLs are retained when present; excluded media binaries were not part of the supplied export.",
            },
        },
    )
    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "collection_source_id": collection_source_id,
        "original_filename": source["original_filename"],
        "raw_archive_path": source["raw"].relative_to(REPO).as_posix(),
        "raw_original_bytes": len(raw_bytes),
        "raw_original_sha256": sha256_bytes(raw_bytes),
        "raw_compressed_bytes": source["raw"].stat().st_size,
        "raw_compressed_sha256": sha256_file(source["raw"]),
        "lossless_reconstruction_verified": True,
        "gzip_header_mtime": 0,
        "export_metadata": metadata,
        "source": source_meta,
        "coverage": collection.get("coverage"),
        "collection_complete": collection.get("complete"),
        "diagnostics": diagnostics,
    }
    write_json(DISCORD_PROV / f"{source['slug']}-2026-07-23.json", provenance)
    return collection_record, participant_records


def listed_files(roots: list[Path], excluded_names: set[str] | None = None) -> list[dict[str, Any]]:
    excluded_names = excluded_names or set()
    paths = sorted(
        path
        for root in roots
        if root.exists()
        for path in (root.rglob("*") if root.is_dir() else [root])
        if path.is_file() and path.name not in excluded_names and "__pycache__" not in path.parts
    )
    return [
        {
            "path": path.relative_to(REPO).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in paths
    ]


def main() -> None:
    OPS.mkdir(parents=True, exist_ok=True)
    council_prov, council_records, future_dates, comparisons = build_council()
    write_json(
        OPS / "council-snapshot-reconciliation.json",
        {
            "campaign_id": CAMPAIGN_ID,
            "snapshot_date": SNAPSHOT_DATE,
            "prior_record_count": sum(1 for item in comparisons if item["prior_source_id"]),
            "snapshot_record_count": len(comparisons),
            "records": comparisons,
            "promotion_authorized": False,
        },
    )

    discord_collections = []
    participant_count = 0
    for source in DISCORD_SOURCES:
        collection, participants = build_discord(source)
        discord_collections.append(collection)
        participant_count += len(participants)

    coverage = {
        "campaign_id": CAMPAIGN_ID,
        "scope": "Imported native-ID Discord exports; each channel is represented independently.",
        "channels": [
            {
                "collection_source_id": item["collection_source_id"],
                "server": item["source"]["workspace"],
                "channel": item["source"]["conversation"],
                "requested_range": item["collection"].get("requestedRange"),
                "actual_range": item["collection"].get("actualRange"),
                "coverage": item["collection"].get("coverage"),
                "collection_complete": item["collection"].get("complete"),
                "message_count": item["collection"].get("messageCount"),
                "participant_count": item["collection"].get("participantCount"),
                "stop_reason": (item["collection"].get("loadOlder") or {}).get("stopReason"),
                "warnings": item["diagnostics"].get("warnings") or [],
            }
            for item in discord_collections
        ],
        "completeness_claim": "PARTIAL_EXPORTS_PRESERVED_WITH_COLLECTOR_LIMITS",
    }
    write_json(OPS / "discord-channel-coverage.json", coverage)

    unknown_payment = [
        {
            "source_id": item["source_id"],
            "pip_id": item.get("pip_id"),
            "title": item.get("title"),
            "payment": item["payment"],
        }
        for item in council_records
        if any(
            value.get("original") == "?"
            for key, value in item["payment"].items()
            if isinstance(value, dict)
        )
    ]
    unnumbered = [
        {"source_id": item["source_id"], "title": item.get("title"), "phase": item.get("phase")}
        for item in council_records
        if not item.get("pip_id")
    ]
    review_items = [
        {
            "review_id": "FRC-001",
            "type": "DISCORD_TEMPORAL_COVERAGE",
            "subject": "foundation-room",
            "status": "OPEN",
            "finding": "Collector stopped at the no-progress limit; requested 2021 start was not reached.",
            "recommendation": "Preserve as partial. A future resumable export should target messages before 2025-01-22.",
            "defer_allowed": True,
        },
        {
            "review_id": "FRC-002",
            "type": "DISCORD_TEMPORAL_COVERAGE",
            "subject": "fr-chat",
            "status": "OPEN",
            "finding": "Collector stopped at the no-progress limit; requested 2021 start was not reached.",
            "recommendation": "Preserve as partial. A future resumable export should target messages before 2022-01-25.",
            "defer_allowed": True,
        },
        {
            "review_id": "FRC-003",
            "type": "COUNCIL_FUTURE_DATE",
            "subject": future_dates,
            "status": "OPEN" if future_dates else "NOT_APPLICABLE",
            "finding": "One or more tracker dates occur after the supplied snapshot date.",
            "recommendation": "Retain original text and normalized date; determine whether each value is a planned date or a data-entry error.",
            "defer_allowed": True,
        },
        {
            "review_id": "FRC-004",
            "type": "COUNCIL_UNKNOWN_PAYMENT_OR_MILESTONE",
            "subject": unknown_payment,
            "status": "OPEN" if unknown_payment else "NOT_APPLICABLE",
            "finding": "The Council snapshot uses question marks for unresolved payment or milestone values.",
            "recommendation": "Keep UNVERIFIED until Council documentation or transaction-level evidence is supplied.",
            "defer_allowed": True,
        },
        {
            "review_id": "FRC-005",
            "type": "COUNCIL_UNNUMBERED_PIPELINE_ITEMS",
            "subject": unnumbered,
            "status": "OPEN" if unnumbered else "NOT_APPLICABLE",
            "finding": "Six substantive tracker rows have titles but no PIP number.",
            "recommendation": "Do not assign PIP identifiers without an authoritative source.",
            "defer_allowed": True,
        },
    ]
    write_json(
        OPS / "manual-review-queue.json",
        {
            "campaign_id": CAMPAIGN_ID,
            "open_count": sum(item["status"] == "OPEN" for item in review_items),
            "items": review_items,
        },
    )

    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "GENERATED",
        "scope": "PRESERVE_AND_NORMALIZE_ONLY",
        "council_snapshot": {
            "record_count": len(council_records),
            "numbered_pip_count": sum(item.get("pip_id") is not None for item in council_records),
            "unnumbered_pipeline_item_count": len(unnumbered),
            "future_date_review_count": len(future_dates),
            "unknown_payment_review_count": len(unknown_payment),
            "raw_sha256": council_prov["raw_sha256"],
        },
        "discord": {
            "channel_export_count": len(discord_collections),
            "message_count": sum(item["collection"]["messageCount"] for item in discord_collections),
            "participant_record_count": participant_count,
            "collection_complete_count": sum(bool(item["collection"]["complete"]) for item in discord_collections),
            "collection_partial_count": sum(not bool(item["collection"]["complete"]) for item in discord_collections),
        },
        "knowledge_promotions": 0,
        "graph_changes": 0,
        "publication_changes": 0,
        "manual_review_open_count": sum(item["status"] == "OPEN" for item in review_items),
    }
    write_json(OPS / "campaign-summary.json", summary)
    (OPS / "campaign-summary.md").write_text(
        "# Foundation Room and Council Evidence Ingestion\n\n"
        f"- Council snapshot records: **{summary['council_snapshot']['record_count']}**\n"
        f"- Numbered PIPs: **{summary['council_snapshot']['numbered_pip_count']}**\n"
        f"- Unnumbered Council pipeline items: **{summary['council_snapshot']['unnumbered_pipeline_item_count']}**\n"
        f"- Discord channel exports: **{summary['discord']['channel_export_count']}**\n"
        f"- Discord messages: **{summary['discord']['message_count']}**\n"
        f"- Complete Discord collections: **{summary['discord']['collection_complete_count']}**\n"
        f"- Partial Discord collections: **{summary['discord']['collection_partial_count']}**\n"
        f"- Open human-review items: **{summary['manual_review_open_count']}**\n\n"
        "The Council tracker remains a Council-authored operational assessment. Payment and milestone "
        "values are not on-chain verified. Both Discord exports preserve native message, channel, server, "
        "reply, author, timestamp, and attachment metadata, but both are partial according to their own "
        "collector coverage records. No Knowledge, graph, or publication promotion is performed.\n",
        encoding="utf-8",
        newline="\n",
    )

    preserved = listed_files(
        [
            COUNCIL_RAW,
            *[source["raw"] for source in DISCORD_SOURCES],
        ]
    )
    generated = listed_files(
        [
            COUNCIL_NORM,
            COUNCIL_PROV,
            COUNCIL_RECORDS,
            DISCORD_NORM,
            DISCORD_PROV,
            DISCORD_RECORDS,
            OPS,
        ],
        excluded_names={
            "build_campaign.py",
            "validate_campaign.py",
            "manifest.json",
            "validation-report.json",
            "validation-report.md",
        },
    )
    manifest = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": SNAPSHOT_DATE,
        "preserved_inputs": preserved,
        "generated_outputs": generated,
        "counts": summary,
    }
    write_json(OPS / "manifest.json", manifest)
    write_json(ARCHIVE_MANIFEST, manifest)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
