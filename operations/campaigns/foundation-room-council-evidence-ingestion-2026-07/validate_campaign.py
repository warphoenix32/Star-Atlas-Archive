#!/usr/bin/env python3
"""Validate the Foundation Room and Council evidence ingestion campaign."""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
CAMPAIGN_ID = "foundation-room-council-evidence-ingestion-2026-07"
BUILD = OPS / "build_campaign.py"
COUNCIL_RAW = (
    REPO
    / "archive/raw/governance/council-pip-tracker/snapshots/2026-07-23"
    / "Star Atlas DAO Council -- PIP Tracker & Grading Rubric - Tracker.csv"
)
COUNCIL_NORM = REPO / "archive/normalized/governance/council-pip-tracker/snapshots/2026-07-23"
COUNCIL_RECORDS = REPO / "archive/source-records/governance/council-pip-tracker/snapshots/2026-07-23"
DISCORD_NORM = REPO / "archive/normalized/discord/star-atlas"
DISCORD_RAW = REPO / "archive/raw/discord/star-atlas"
DISCORD_PROV = REPO / "archive/provenance/discord/star-atlas"
DISCORD_RECORDS = REPO / "archive/source-records/discord/star-atlas"
ARCHIVE_MANIFEST = REPO / "archive/manifests/foundation-room-council-evidence-ingestion-2026-07.json"
EXPECTED_RAW = {
    "foundation-room": {
        "path": DISCORD_RAW / "foundation-room/discord-foundation-room-2026-07-23T12-18-57-639Z.json.gz",
        "bytes": 7_844_471,
        "sha256": "e5000077fee2223d58eda82334f868a56c3db2648a2f760fa9cb0a0841482480",
        "messages": 4_464,
        "participants": 180,
        "earliest": "2025-01-22T02:59:55.987Z",
        "latest": "2026-07-23T01:07:23.600Z",
    },
    "fr-chat": {
        "path": DISCORD_RAW / "fr-chat/discord-fr-chat-2026-07-23T08-24-13-992Z.json.gz",
        "bytes": 261_351_795,
        "sha256": "d251ef982cee3dec9ec93e02d14b9f8ea297d630e37babf7d2cbc090e790c90e",
        "messages": 186_430,
        "participants": 469,
        "earliest": "2022-01-25T19:05:55.773Z",
        "latest": "2026-07-23T01:03:04.526Z",
    },
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                raise ValueError(f"{path}:{number}: blank JSONL record")
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{number}: record must be an object")
            yield number, value


def generated_hashes() -> dict[str, str]:
    roots = [
        COUNCIL_NORM,
        REPO / "archive/provenance/governance/council-pip-tracker/snapshots/2026-07-23.json",
        COUNCIL_RECORDS,
        DISCORD_NORM,
        DISCORD_PROV,
        DISCORD_RECORDS,
        OPS,
        ARCHIVE_MANIFEST,
    ]
    excluded = {"build_campaign.py", "validate_campaign.py", "validation-report.json", "validation-report.md"}
    paths = sorted(
        path
        for root in roots
        if root.exists()
        for path in (root.rglob("*") if root.is_dir() else [root])
        if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts
    )
    return {path.relative_to(REPO).as_posix(): digest(path) for path in paths}


def main() -> int:
    checks: dict[str, dict[str, Any]] = {}
    failures: list[str] = []
    warnings: list[str] = []

    def check(name: str, passed: bool, detail: Any) -> None:
        checks[name] = {"status": "PASS" if passed else "FAIL", "detail": detail}
        if not passed:
            failures.append(f"{name}: {detail}")

    council_sha = digest(COUNCIL_RAW)
    check(
        "council_raw_checksum",
        COUNCIL_RAW.stat().st_size == 12_894
        and council_sha == "533d4578c00f949d9c38653190f084681c336e9c135b84c29a7a9cf5741cff9b",
        {"bytes": COUNCIL_RAW.stat().st_size, "sha256": council_sha},
    )

    raw_before = {
        path.relative_to(REPO).as_posix(): digest(path)
        for path in [COUNCIL_RAW, *[item["path"] for item in EXPECTED_RAW.values()]]
    }
    before = generated_hashes()
    build = subprocess.run(
        [sys.executable, str(BUILD)],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    after = generated_hashes()
    raw_after = {
        path.relative_to(REPO).as_posix(): digest(path)
        for path in [COUNCIL_RAW, *[item["path"] for item in EXPECTED_RAW.values()]]
    }
    check(
        "deterministic_regeneration",
        build.returncode == 0 and before == after,
        {"returncode": build.returncode, "generated_file_count": len(after), "stderr": build.stderr[-2000:]},
    )
    check("raw_evidence_immutable", raw_before == raw_after, raw_after)

    all_message_ids: set[str] = set()
    all_source_ids: set[str] = set()
    discord_total = 0
    participant_total = 0
    unresolved_reply_count = 0
    for slug, expected in EXPECTED_RAW.items():
        compressed = expected["path"].read_bytes()
        header_mtime = int.from_bytes(compressed[4:8], "little")
        with gzip.open(expected["path"], "rb") as stream:
            original = stream.read()
        check(
            f"{slug}_lossless_raw_reconstruction",
            len(original) == expected["bytes"] and hashlib.sha256(original).hexdigest() == expected["sha256"],
            {
                "original_bytes": len(original),
                "original_sha256": hashlib.sha256(original).hexdigest(),
                "compressed_bytes": len(compressed),
                "gzip_header_mtime": header_mtime,
            },
        )
        check(f"{slug}_deterministic_gzip_header", header_mtime == 0, {"gzip_header_mtime": header_mtime})

        collection = load_json(DISCORD_NORM / slug / "collection.json")
        file_index = load_json(DISCORD_NORM / slug / "message-file-index.json")
        participant_ids = {
            value["participantId"]
            for _, value in load_jsonl(DISCORD_NORM / slug / "participants.jsonl")
        }
        participant_total += len(participant_ids)
        check(
            f"{slug}_participant_count",
            len(participant_ids) == expected["participants"],
            {"actual": len(participant_ids), "expected": expected["participants"]},
        )
        timestamps: list[str] = []
        channel_message_ids: set[str] = set()
        channel_source_ids: set[str] = set()
        actual_by_file: dict[str, int] = {}
        referenced_participants_ok = True
        reply_ids: set[str] = set()
        for file_entry in file_index["files"]:
            path = REPO / file_entry["path"]
            count = 0
            for _, record in load_jsonl(path):
                count += 1
                message_id = str(record.get("message_id") or "")
                source_id = str(record.get("source_id") or "")
                if not message_id or message_id in channel_message_ids or message_id in all_message_ids:
                    failures.append(f"{slug}: missing or duplicate message ID {message_id}")
                if not source_id or source_id in channel_source_ids or source_id in all_source_ids:
                    failures.append(f"{slug}: missing or duplicate Source ID {source_id}")
                channel_message_ids.add(message_id)
                channel_source_ids.add(source_id)
                timestamps.append(record["timestamp_iso"])
                if record.get("participant_id") not in participant_ids:
                    referenced_participants_ok = False
                reply = record.get("reply")
                if isinstance(reply, dict) and reply.get("messageId"):
                    reply_ids.add(str(reply["messageId"]))
            actual_by_file[file_entry["path"]] = count
            check(
                f"{slug}_{file_entry['month']}_file_reconciliation",
                count == file_entry["message_count"]
                and path.stat().st_size == file_entry["bytes"]
                and digest(path) == file_entry["sha256"],
                {"records": count, "path": file_entry["path"]},
            )
        unresolved_reply_count += len(reply_ids - channel_message_ids)
        all_message_ids.update(channel_message_ids)
        all_source_ids.update(channel_source_ids)
        discord_total += len(channel_message_ids)
        check(
            f"{slug}_message_count",
            len(channel_message_ids) == expected["messages"] == file_index["message_count"],
            {"actual": len(channel_message_ids), "expected": expected["messages"]},
        )
        check(
            f"{slug}_date_bounds",
            min(timestamps) == expected["earliest"] and max(timestamps) == expected["latest"],
            {"earliest": min(timestamps), "latest": max(timestamps)},
        )
        check(f"{slug}_participant_references", referenced_participants_ok, {"participants": len(participant_ids)})
        check(
            f"{slug}_partial_coverage_preserved",
            collection["collection"]["complete"] is False
            and collection["collection"]["coverage"]["status"] == "partial"
            and collection["collection"]["loadOlder"]["stopReason"] == "no-progress-limit",
            collection["collection"]["coverage"],
        )
        source_records = list((DISCORD_RECORDS / slug).glob("*.json"))
        check(
            f"{slug}_collection_source_record",
            len(source_records) == 1
            and load_json(source_records[0])["source_id"] == collection["collection_source_id"],
            {"source_record_count": len(source_records)},
        )

    check(
        "discord_global_identity",
        discord_total == 190_894
        and len(all_message_ids) == discord_total
        and len(all_source_ids) == discord_total,
        {"messages": discord_total, "source_ids": len(all_source_ids), "participant_records": participant_total},
    )
    warnings.append(
        f"{unresolved_reply_count} reply targets fall outside their captured channel window or are otherwise unresolved; "
        "the reply references remain preserved."
    )

    council_records = [value for _, value in load_jsonl(COUNCIL_NORM / "tracker-records.jsonl")]
    council_source_ids = [item["source_id"] for item in council_records]
    check(
        "council_record_reconciliation",
        len(council_records) == 40
        and sum(item.get("pip_id") is not None for item in council_records) == 34
        and len(council_source_ids) == len(set(council_source_ids))
        and len(list(COUNCIL_RECORDS.glob("*.json"))) == 40,
        {
            "records": len(council_records),
            "numbered_pips": sum(item.get("pip_id") is not None for item in council_records),
            "source_records": len(list(COUNCIL_RECORDS.glob("*.json"))),
        },
    )
    controlled = {
        "REQUESTED",
        "AUTHORIZED",
        "COUNCIL_REPORTED",
        "UNVERIFIED",
        "MISSING_ONCHAIN_EVIDENCE",
    }
    states_ok = all(
        item["payment"]["authorization_state"] in controlled
        and item["payment"]["payment_state"] in controlled
        and item["payment"]["onchain_verification_state"] in controlled
        for item in council_records
    )
    check("council_treasury_state_taxonomy", states_ok, sorted(controlled))
    check(
        "council_authority_boundary",
        all(
            item["assessment_type"] == "COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT"
            and item["independent_verification_status"] == "UNKNOWN"
            for item in council_records
        ),
        "All Council records remain attributed operational assessments.",
    )
    reconciliation = load_json(OPS / "council-snapshot-reconciliation.json")
    check(
        "council_snapshot_reconciliation",
        reconciliation["snapshot_record_count"] == 40
        and reconciliation["promotion_authorized"] is False,
        {
            "records": reconciliation["snapshot_record_count"],
            "prior_records_found": reconciliation["prior_record_count"],
        },
    )

    review = load_json(OPS / "manual-review-queue.json")
    check(
        "manual_review_queue",
        review["open_count"] == 5
        and {item["review_id"] for item in review["items"]}
        == {"FRC-001", "FRC-002", "FRC-003", "FRC-004", "FRC-005"},
        {"open_count": review["open_count"]},
    )

    manifest = load_json(OPS / "manifest.json")
    archive_manifest = load_json(ARCHIVE_MANIFEST)
    entries = manifest["preserved_inputs"] + manifest["generated_outputs"]
    manifest_ok = (
        manifest == archive_manifest
        and all(
            (REPO / item["path"]).is_file()
            and (REPO / item["path"]).stat().st_size == item["bytes"]
            and digest(REPO / item["path"]) == item["sha256"]
            for item in entries
        )
    )
    check("manifest_reconciliation", manifest_ok, {"entries": len(entries)})

    oversized = [
        path.relative_to(REPO).as_posix()
        for path in REPO.rglob("*")
        if path.is_file()
        and (
            path.is_relative_to(DISCORD_RAW)
            or path.is_relative_to(DISCORD_NORM)
            or path.is_relative_to(COUNCIL_NORM)
        )
        and path.stat().st_size >= 100_000_000
    ]
    check("github_file_size_limit", not oversized, {"oversized_files": oversized})

    diff = subprocess.run(
        ["git", "diff", "--check"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    check("git_diff_check", diff.returncode == 0, (diff.stdout + diff.stderr)[-4000:])

    changed = subprocess.run(
        ["git", "status", "--short"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    ).stdout.splitlines()
    prohibited = [
        line
        for line in changed
        if any(
            marker in line.replace("\\", "/")
            for marker in (" knowledge/", " graph/", " publication/")
        )
    ]
    check("canonical_and_publication_paths_untouched", not prohibited, {"prohibited": prohibited})

    report = {
        "campaign_id": CAMPAIGN_ID,
        "status": "PASS" if not failures else "FAIL",
        "counts": {
            "council_records": len(council_records),
            "discord_messages": discord_total,
            "discord_participant_records": participant_total,
            "discord_channels": 2,
            "manual_review_items": review["open_count"],
        },
        "checks": checks,
        "warnings": warnings,
        "failures": failures,
    }
    (OPS / "validation-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (OPS / "validation-report.md").write_text(
        "# Validation Report\n\n"
        f"Overall status: **{report['status']}**\n\n"
        + "\n".join(
            f"- **{value['status']} — {name}**: {json.dumps(value['detail'], ensure_ascii=False)}"
            for name, value in checks.items()
        )
        + "\n\n## Warnings\n\n"
        + "\n".join(f"- {warning}" for warning in warnings)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": report["status"], "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
