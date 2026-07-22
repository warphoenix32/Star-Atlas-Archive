#!/usr/bin/env python3
"""Freeze, retrieve, and validate legacy written-source raw evidence.

This campaign is intentionally narrow. It reads the 800 successful extraction
records promoted by Campaigns Alpha through Delta, but it never rewrites those
extractions or their Source Records. Retrieval stores exact public HTTP
response bytes plus provenance for an explicitly approved record selection.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


CAMPAIGN_ID = "legacy-written-raw-recovery-2026-07"
SCHEMA_VERSION = "1.0.0"
AS_OF = "2026-07-20"
CAMPAIGN_DIR = Path(__file__).resolve().parent
REPO_ROOT = CAMPAIGN_DIR.parents[2]
RAW_ROOT = REPO_ROOT / "archive" / "raw" / "legacy-written-recovery"
PROVENANCE_ROOT = REPO_ROOT / "archive" / "provenance" / "legacy-written-recovery"
ARCHIVE_MANIFEST = REPO_ROOT / "archive" / "manifests" / f"{CAMPAIGN_ID}.json"

FROZEN_MANIFEST = CAMPAIGN_DIR / "frozen-manifest.json"
PILOT_SELECTION = CAMPAIGN_DIR / "pilot-selection.json"
EXPANSION_BATCH_ID = "aephia-family-remaining-59"
EXPANSION_SELECTION = CAMPAIGN_DIR / "expansion-aephia-selection.json"
RETRIEVAL_LEDGER = CAMPAIGN_DIR / "retrieval-ledger.jsonl"
RETRY_LEDGER = CAMPAIGN_DIR / "retry-ledger.jsonl"
MANUAL_REVIEW_QUEUE = CAMPAIGN_DIR / "manual-review-queue.jsonl"
EXPANSION_RETRIEVAL_LEDGER = CAMPAIGN_DIR / "expansion-aephia-retrieval-ledger.jsonl"
EXPANSION_RETRY_LEDGER = CAMPAIGN_DIR / "expansion-aephia-retry-ledger.jsonl"
EXPANSION_MANUAL_REVIEW_QUEUE = CAMPAIGN_DIR / "expansion-aephia-manual-review-queue.jsonl"
HNN_BATCH_ID = "hnn-written-family-completion-156"
HNN_SELECTION = CAMPAIGN_DIR / "expansion-hnn-selection.json"
HNN_RESOLUTION_LEDGER = CAMPAIGN_DIR / "expansion-hnn-archive-resolution-ledger.jsonl"
HNN_RETRIEVAL_LEDGER = CAMPAIGN_DIR / "expansion-hnn-retrieval-ledger.jsonl"
HNN_RETRY_LEDGER = CAMPAIGN_DIR / "expansion-hnn-retry-ledger.jsonl"
HNN_MANUAL_REVIEW_QUEUE = CAMPAIGN_DIR / "expansion-hnn-manual-review-queue.jsonl"
OFFICIAL_BATCH_ID = "official-written-family-completion-316"
OFFICIAL_SELECTION = CAMPAIGN_DIR / "expansion-official-selection.json"
OFFICIAL_RETRIEVAL_LEDGER = CAMPAIGN_DIR / "expansion-official-retrieval-ledger.jsonl"
OFFICIAL_RETRY_LEDGER = CAMPAIGN_DIR / "expansion-official-retry-ledger.jsonl"
OFFICIAL_MANUAL_REVIEW_QUEUE = CAMPAIGN_DIR / "expansion-official-manual-review-queue.jsonl"
CAMPAIGN_SUMMARY_JSON = CAMPAIGN_DIR / "campaign-summary.json"
CAMPAIGN_SUMMARY_MD = CAMPAIGN_DIR / "campaign-summary.md"
VALIDATION_REPORT_JSON = CAMPAIGN_DIR / "validation-report.json"
VALIDATION_REPORT_MD = CAMPAIGN_DIR / "validation-report.md"

CAMPAIGNS = (
    {
        "campaign_id": "campaign-alpha-aephia",
        "source_family": "aephia",
        "publisher_label": "Aephia",
        "expected_count": 64,
    },
    {
        "campaign_id": "campaign-bravo-intergalactic-herald",
        "source_family": "intergalactic-herald",
        "publisher_label": "Intergalactic Herald",
        "expected_count": 259,
    },
    {
        "campaign_id": "campaign-charlie-hnn",
        "source_family": "hologram-news-network",
        "publisher_label": "Hologram News Network",
        "expected_count": 157,
    },
    {
        "campaign_id": "campaign-delta-official",
        "source_family": "official-star-atlas",
        "publisher_label": "Official Star Atlas",
        "expected_count": 320,
    },
)

PILOT_SOURCE_IDS = (
    "SRC-AEPHIA-0182787CF88DD0DA",
    "SRC-AEPHIA-1285F1BCA85AB55F",
    "SRC-AEPHIA-19357309E964FAF8",
    "SRC-AEPHIA-21D7FE432327A762",
    "SRC-AEPHIA-F749E3A20669A520",
    "SRC-HNN-03991C709B75E22E",
    "SRC-HNN-04DD15F547F461E7",
    "SRC-HNN-0AE69C9EB1A49845",
    "SRC-HNN-66B32FB7A224EB14",
    "SRC-HNN-E7FADD27A4FD57B6",
    "SRC-IH-01FCC742522C1676",
    "SRC-IH-73A1B12100BA1F26",
    "SRC-IH-C9AD5B9C924908F3",
    "SRC-IH-D1F9C624BF245EC7",
    "SRC-IH-F4C2A6A0B64F3E98",
    "SRC-OFF-0333A5B22A207D88",
    "SRC-OFF-076F496F0A6CA989",
    "SRC-OFF-0A646AE069AFFBA5",
    "SRC-OFF-17012CC0302537A1",
    "SRC-OFF-B4F9EB92DD60A7A8",
)

EXPANSION_EXPECTED_COUNT = 59
EXPANSION_ALLOWED_HOST = "aephia.com"
EXPANSION_ALLOWED_PATH_PREFIX = "/wp-json/wp/v2/"
HNN_EXPECTED_COUNT = 156
HNN_FAMILY_TOTAL = 157
HNN_PRESERVED_BASELINE_SOURCE_IDS = ("SRC-HNN-04DD15F547F461E7",)
HNN_ALLOWED_SOURCE_HOSTS = {"medium.com", "web.archive.org"}
OFFICIAL_EXPECTED_COUNT = 316
OFFICIAL_FAMILY_TOTAL = 320
OFFICIAL_PRESERVED_BASELINE_SOURCE_IDS = (
    "SRC-OFF-076F496F0A6CA989",
    "SRC-OFF-0A646AE069AFFBA5",
    "SRC-OFF-17012CC0302537A1",
    "SRC-OFF-B4F9EB92DD60A7A8",
)
OFFICIAL_ALLOWED_SOURCE_HOSTS = {
    "api.github.com",
    "build.staratlas.com",
    "experience.staratlas.com",
    "staratlas.com",
    "support.staratlas.com",
}
REQUEST_DELAY_SECONDS = 0.25
HNN_REQUEST_DELAY_SECONDS = 0.35
OFFICIAL_REQUEST_DELAY_SECONDS = 0.25
PILOT_BASELINE_SHA256 = {
    "manual-review-queue.jsonl": "8c946c6cd84988d9dfe01c4aedce53bc1bb879582fa5ed7cb07841f91c332b67",
    "pilot-selection.json": "bffd2bb7d92c30b2846f47ac8f6a3fb91d14c49ee8a78c142bf4065ca4ca54f9",
    "retrieval-ledger.jsonl": "e9fd39b62e705958799d0ab23d6026f3da995bcd9f9baf86eed12ac7586d7b08",
    "retry-ledger.jsonl": "dba694d4c148efd1438d92fe77ddfb4f89c93c4910ba8a93ebd92987fdc0fedc",
}
PILOT_ARTIFACT_SET_SHA256 = "7370f2f123f157178cdba0acf115f00d7ffd6ad289106d7939c9bc9cd480c63e"

USER_AGENT = "StarAtlasArchive-RawRecovery/1.0 (+https://github.com/warphoenix32/Star-Atlas-Archive)"
MAX_ATTEMPTS = 3
TIMEOUT_SECONDS = 45

CAPTURED_DISPOSITIONS = {
    "CAPTURED_LIVE",
    "CAPTURED_ARCHIVE",
    "CAPTURED_IMMUTABLE_GIT",
}
ACCESS_BLOCK_STATUSES = {401, 403, 429}


class AccessChallenge(RuntimeError):
    """A public host returned an access/challenge page instead of evidence."""


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


_CANONICAL_BLOB_CACHE: dict[str, bytes] = {}
_PORTABLE_WORKTREE_CHANGES: set[str] | None = None
_PORTABLE_STAGED_CHANGES: set[str] | None = None


def preload_canonical_repository_bytes(paths: Iterable[Path]) -> None:
    requested = sorted({relative(path) for path in paths if path.exists()} - set(_CANONICAL_BLOB_CACHE))
    if not requested:
        return
    payload = "".join(f"HEAD:{path}\n" for path in requested).encode("utf-8")
    try:
        output = subprocess.check_output(
            ["git", "cat-file", "--batch"],
            cwd=REPO_ROOT,
            input=payload,
            stderr=subprocess.DEVNULL,
        )
        offset = 0
        for rel in requested:
            end = output.index(b"\n", offset)
            header = output[offset:end].decode("utf-8", errors="replace")
            offset = end + 1
            parts = header.rsplit(" ", 2)
            if len(parts) != 3 or parts[1] != "blob":
                continue
            size = int(parts[2])
            _CANONICAL_BLOB_CACHE[rel] = output[offset:offset + size]
            offset += size + 1
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return


def canonical_repository_bytes(path: Path) -> bytes:
    """Read the Git blob, not platform-dependent checkout line endings.

    The frozen inputs predate this campaign and are protected from edits. Git's
    blob is therefore their portable repository identity on Windows and Linux.
    """
    rel = relative(path)
    if rel in _CANONICAL_BLOB_CACHE:
        return _CANONICAL_BLOB_CACHE[rel]
    try:
        return subprocess.check_output(
            ["git", "show", f"HEAD:{rel}"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return path.read_bytes()


def portable_artifact_bytes(path: Path) -> bytes:
    """Use changed generated bytes, otherwise the platform-neutral Git blob."""
    global _PORTABLE_STAGED_CHANGES, _PORTABLE_WORKTREE_CHANGES
    rel = relative(path)
    try:
        if _PORTABLE_WORKTREE_CHANGES is None:
            _PORTABLE_WORKTREE_CHANGES = set(
                subprocess.check_output(
                    ["git", "diff", "--name-only"],
                    cwd=REPO_ROOT,
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).splitlines()
            )
        if _PORTABLE_STAGED_CHANGES is None:
            _PORTABLE_STAGED_CHANGES = set(
                subprocess.check_output(
                    ["git", "diff", "--cached", "--name-only", "HEAD"],
                    cwd=REPO_ROOT,
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).splitlines()
            )
        if rel in _PORTABLE_WORKTREE_CHANGES:
            return path.read_bytes()
        if rel in _PORTABLE_STAGED_CHANGES:
            return subprocess.check_output(
                ["git", "show", f":{rel}"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL
            )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return path.read_bytes()
    return canonical_repository_bytes(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, values: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for value in values
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalized_url(value: str | None) -> str | None:
    if not value or not value.startswith(("http://", "https://")):
        return None
    parsed = urllib.parse.urlsplit(value)
    path = re.sub(r"/+", "/", parsed.path or "/").rstrip("/") or "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def medium_post_id(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"(?:/p/|[-/])([0-9a-f]{12})(?:[/?#]|$)", value, re.I)
    return match.group(1).lower() if match else None


def valid_http_url(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def choose_retrieval_url(source: dict[str, Any], retrieval: dict[str, Any]) -> tuple[str, str]:
    """Use the prior successful retrieval surface where available.

    WordPress campaigns were extracted from the public REST response, while
    HNN often used a specific Internet Archive capture. Re-capturing that same
    public surface preserves the evidence actually underlying the extraction.
    """
    requested = retrieval.get("requested_url")
    final = retrieval.get("final_url")
    source_url = source.get("url")
    if valid_http_url(requested):
        return requested, "PRIOR_REQUESTED_URL"
    if valid_http_url(final):
        return final, "PRIOR_FINAL_URL"
    if valid_http_url(source_url):
        return source_url, "SOURCE_CANONICAL_URL"
    raise ValueError(f"No public HTTP URL is available for {source.get('source_id')}")


def extraction_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    pilot = set(PILOT_SOURCE_IDS)
    protected_inputs: list[Path] = []
    for specification in CAMPAIGNS:
        protected_inputs.extend(
            (REPO_ROOT / "archive" / "ingestion-packages" / specification["campaign_id"] / "extractions").glob("*.json")
        )
        protected_inputs.extend(
            (REPO_ROOT / "archive" / "source-records" / specification["campaign_id"]).glob("*.md")
        )
    preload_canonical_repository_bytes(protected_inputs)
    for specification in CAMPAIGNS:
        extraction_dir = (
            REPO_ROOT
            / "archive"
            / "ingestion-packages"
            / specification["campaign_id"]
            / "extractions"
        )
        paths = sorted(extraction_dir.glob("*.json"), key=lambda item: item.name)
        if len(paths) != specification["expected_count"]:
            raise RuntimeError(
                f"{specification['campaign_id']} has {len(paths)} extraction JSON files; "
                f"expected {specification['expected_count']}"
            )
        for path in paths:
            raw = canonical_repository_bytes(path)
            extraction = json.loads(raw.decode("utf-8"))
            source = extraction.get("source") or {}
            retrieval = extraction.get("retrieval") or {}
            source_id = source.get("source_id")
            if not source_id:
                raise RuntimeError(f"Missing source.source_id in {relative(path)}")
            retrieval_url, retrieval_url_basis = choose_retrieval_url(source, retrieval)
            source_record = (
                REPO_ROOT
                / "archive"
                / "source-records"
                / specification["campaign_id"]
                / f"{source_id}.md"
            )
            article_text = extraction.get("article_text") or ""
            content_sha = extraction.get("content_hash") or sha256_bytes(article_text.encode("utf-8"))
            records.append(
                {
                    "author": source.get("author"),
                    "campaign_id": specification["campaign_id"],
                    "existing_content_sha256": content_sha,
                    "existing_extraction_path": relative(path),
                    "existing_extraction_sha256": sha256_bytes(raw),
                    "existing_retrieval": {
                        "content_type": retrieval.get("content_type"),
                        "final_url": retrieval.get("final_url"),
                        "http_status": retrieval.get("http_status"),
                        "requested_url": retrieval.get("requested_url"),
                        "retrieved_at": retrieval.get("retrieved_at") or source.get("retrieved_at"),
                        "retrieval_mode": retrieval.get("retrieval_mode"),
                    },
                    "existing_source_record_path": relative(source_record) if source_record.exists() else None,
                    "existing_source_record_sha256": sha256_bytes(canonical_repository_bytes(source_record)) if source_record.exists() else None,
                    "inventory_url": source.get("inventory_url"),
                    "original_url": source.get("url"),
                    "pilot_selected": source_id in pilot,
                    "published_at": source.get("published_at"),
                    "publisher": source.get("publisher") or specification["publisher_label"],
                    "recovery_disposition": "ELIGIBLE_FOR_RAW_RECOVERY",
                    "retrieval_url": retrieval_url,
                    "retrieval_url_basis": retrieval_url_basis,
                    "source_family": specification["source_family"],
                    "source_id": source_id,
                    "title": source.get("title"),
                    "updated_at": source.get("updated_at"),
                }
            )
    records.sort(key=lambda item: item["source_id"])
    return records


def build_frozen_manifest() -> dict[str, Any]:
    records = extraction_records()
    counts = Counter(record["campaign_id"] for record in records)
    pilot_present = sorted(record["source_id"] for record in records if record["pilot_selected"])
    if len(records) != 800:
        raise RuntimeError(f"Frozen manifest must contain 800 records, found {len(records)}")
    if pilot_present != sorted(PILOT_SOURCE_IDS):
        missing = sorted(set(PILOT_SOURCE_IDS) - set(pilot_present))
        raise RuntimeError(f"Approved pilot IDs missing from extraction corpus: {missing}")
    return {
        "as_of": AS_OF,
        "campaign_counts": dict(sorted(counts.items())),
        "campaign_id": CAMPAIGN_ID,
        "freeze_basis": "EXISTING_SUCCESSFUL_ALPHA_THROUGH_DELTA_EXTRACTION_JSON",
        "frozen_record_count": len(records),
        "pilot_record_count": len(pilot_present),
        "pilot_source_ids": pilot_present,
        "records": records,
        "schema_version": SCHEMA_VERSION,
    }


def expansion_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    pilot = set(PILOT_SOURCE_IDS)
    records = [
        record
        for record in manifest["records"]
        if record["source_family"] == "aephia" and record["source_id"] not in pilot
    ]
    records.sort(key=lambda item: item["source_id"])
    if len(records) != EXPANSION_EXPECTED_COUNT:
        raise RuntimeError(
            f"{EXPANSION_BATCH_ID} must contain {EXPANSION_EXPECTED_COUNT} records; "
            f"found {len(records)}"
        )
    for record in records:
        parsed = urllib.parse.urlsplit(record["retrieval_url"])
        if parsed.netloc.lower() != EXPANSION_ALLOWED_HOST:
            raise RuntimeError(f"Expansion host outside allowlist: {record['source_id']} {parsed.netloc}")
        if not parsed.path.startswith(EXPANSION_ALLOWED_PATH_PREFIX):
            raise RuntimeError(f"Expansion endpoint outside policy: {record['source_id']} {parsed.path}")
        if record["retrieval_url_basis"] != "PRIOR_FINAL_URL":
            raise RuntimeError(f"Expansion URL basis is not prior final URL: {record['source_id']}")
    return records


def pilot_artifact_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    paths = {
        item[key]
        for item in read_jsonl(RETRIEVAL_LEDGER)
        for key in ("body_path", "provenance_path")
        if item.get(key)
    }
    # Preserve the approved baseline's historical ordering: raw artifacts first,
    # then provenance artifacts, with deterministic lexical order inside each
    # layer. The aggregate checksum is order-sensitive.
    for rel in sorted(paths, key=lambda item: (0 if item.startswith("archive/raw/") else 1, item)):
        path = REPO_ROOT / rel
        entries.append({"path": rel, "sha256": sha256_bytes(canonical_repository_bytes(path))})
    return entries


def pilot_artifact_set_sha256(entries: list[dict[str, Any]]) -> str:
    payload = "".join(f"{item['path']}\0{item['sha256']}\n" for item in entries).encode("utf-8")
    return sha256_bytes(payload)


def build_expansion_selection(manifest: dict[str, Any]) -> dict[str, Any]:
    records = expansion_records(manifest)
    artifact_entries = pilot_artifact_entries()
    return {
        "allowed_host": EXPANSION_ALLOWED_HOST,
        "allowed_path_prefix": EXPANSION_ALLOWED_PATH_PREFIX,
        "authorization_status": "AUTHORIZED_FOR_RETRIEVAL",
        "batch_id": EXPANSION_BATCH_ID,
        "campaign_id": CAMPAIGN_ID,
        "deferred_scope": [
            "campaign-bravo-intergalactic-herald",
            "campaign-charlie-hnn",
            "campaign-delta-official",
        ],
        "expected_record_count": EXPANSION_EXPECTED_COUNT,
        "frozen_manifest_sha256": sha256_bytes(canonical_repository_bytes(FROZEN_MANIFEST)),
        "pilot_artifact_entries": artifact_entries,
        "pilot_artifact_set_sha256": pilot_artifact_set_sha256(artifact_entries),
        "pilot_baseline_sha256": dict(sorted(PILOT_BASELINE_SHA256.items())),
        "pilot_source_ids_excluded": sorted(PILOT_SOURCE_IDS),
        "records": [
            {
                "retrieval_url": record["retrieval_url"],
                "retrieval_url_basis": record["retrieval_url_basis"],
                "source_id": record["source_id"],
            }
            for record in records
        ],
        "schema_version": SCHEMA_VERSION,
        "selection_rule": "AEPHIA_FAMILY_AND_NOT_PILOT",
    }


def hnn_completion_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    preserved = set(HNN_PRESERVED_BASELINE_SOURCE_IDS)
    records = [
        record
        for record in manifest["records"]
        if record["source_family"] == "hologram-news-network" and record["source_id"] not in preserved
    ]
    records.sort(key=lambda item: item["source_id"])
    if len(records) != HNN_EXPECTED_COUNT:
        raise RuntimeError(
            f"{HNN_BATCH_ID} must contain {HNN_EXPECTED_COUNT} records; found {len(records)}"
        )
    for record in records:
        host = urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower()
        if host not in HNN_ALLOWED_SOURCE_HOSTS:
            raise RuntimeError(f"HNN recovery surface outside allowlist: {record['source_id']} {host}")
        if record["retrieval_url_basis"] != "PRIOR_REQUESTED_URL":
            raise RuntimeError(
                f"HNN recovery URL basis is not the prior successful request: {record['source_id']}"
            )
    return records


def build_hnn_selection(manifest: dict[str, Any]) -> dict[str, Any]:
    records = hnn_completion_records(manifest)
    pilot = set(PILOT_SOURCE_IDS)
    return {
        "authorization_status": "AUTHORIZED_FOR_RETRIEVAL",
        "batch_id": HNN_BATCH_ID,
        "campaign_id": CAMPAIGN_ID,
        "carrier_policy": (
            "Reuse exact prior Wayback snapshots; resolve blocked Medium URLs to the earliest "
            "public Wayback HTML capture and preserve the resolution separately."
        ),
        "deferred_scope": [
            "campaign-bravo-intergalactic-herald",
            "campaign-delta-official",
        ],
        "expected_record_count": HNN_EXPECTED_COUNT,
        "family_record_count": HNN_FAMILY_TOTAL,
        "frozen_manifest_sha256": sha256_bytes(canonical_repository_bytes(FROZEN_MANIFEST)),
        "pilot_source_ids_repaired": sorted(record["source_id"] for record in records if record["source_id"] in pilot),
        "preserved_baseline_source_ids": sorted(HNN_PRESERVED_BASELINE_SOURCE_IDS),
        "records": [
            {
                "original_url": record["original_url"],
                "published_at": record.get("published_at"),
                "retrieval_url": record["retrieval_url"],
                "retrieval_url_basis": record["retrieval_url_basis"],
                "source_id": record["source_id"],
                "source_surface": urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower(),
            }
            for record in records
        ],
        "schema_version": SCHEMA_VERSION,
        "selection_rule": "HNN_FAMILY_EXCEPT_VERIFIED_PILOT_CHECKPOINT",
    }


def official_completion_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    preserved = set(OFFICIAL_PRESERVED_BASELINE_SOURCE_IDS)
    records = [
        record
        for record in manifest["records"]
        if record["source_family"] == "official-star-atlas" and record["source_id"] not in preserved
    ]
    records.sort(key=lambda item: item["source_id"])
    if len(records) != OFFICIAL_EXPECTED_COUNT:
        raise RuntimeError(
            f"{OFFICIAL_BATCH_ID} must contain {OFFICIAL_EXPECTED_COUNT} records; found {len(records)}"
        )
    for record in records:
        host = urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower()
        if host not in OFFICIAL_ALLOWED_SOURCE_HOSTS:
            raise RuntimeError(f"Official recovery surface outside allowlist: {record['source_id']} {host}")
        if record["retrieval_url_basis"] not in {"PRIOR_FINAL_URL", "PRIOR_REQUESTED_URL"}:
            raise RuntimeError(
                f"Official recovery URL basis is unsupported: {record['source_id']} {record['retrieval_url_basis']}"
            )
    return records


def build_official_selection(manifest: dict[str, Any]) -> dict[str, Any]:
    records = official_completion_records(manifest)
    pilot = set(PILOT_SOURCE_IDS)
    return {
        "allowed_hosts": sorted(OFFICIAL_ALLOWED_SOURCE_HOSTS),
        "authorization_status": "AUTHORIZED_FOR_RETRIEVAL",
        "batch_id": OFFICIAL_BATCH_ID,
        "campaign_id": CAMPAIGN_ID,
        "deferred_scope": ["campaign-bravo-intergalactic-herald"],
        "expected_record_count": OFFICIAL_EXPECTED_COUNT,
        "family_record_count": OFFICIAL_FAMILY_TOTAL,
        "frozen_manifest_sha256": sha256_bytes(canonical_repository_bytes(FROZEN_MANIFEST)),
        "pilot_source_ids_repaired": sorted(
            record["source_id"] for record in records if record["source_id"] in pilot
        ),
        "preserved_baseline_source_ids": sorted(OFFICIAL_PRESERVED_BASELINE_SOURCE_IDS),
        "records": [
            {
                "original_url": record["original_url"],
                "retrieval_url": record["retrieval_url"],
                "retrieval_url_basis": record["retrieval_url_basis"],
                "source_id": record["source_id"],
                "source_surface": urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower(),
            }
            for record in records
        ],
        "schema_version": SCHEMA_VERSION,
        "selection_rule": "OFFICIAL_FAMILY_EXCEPT_VERIFIED_PILOT_CHECKPOINTS",
    }


def freeze() -> None:
    manifest = build_frozen_manifest()
    write_json(FROZEN_MANIFEST, manifest)
    write_json(EXPANSION_SELECTION, build_expansion_selection(manifest))
    write_json(HNN_SELECTION, build_hnn_selection(manifest))
    write_json(OFFICIAL_SELECTION, build_official_selection(manifest))
    write_archive_manifest()
    print(
        f"Frozen {manifest['frozen_record_count']} records; "
        f"approved pilot contains {manifest['pilot_record_count']} records; "
        f"{EXPANSION_BATCH_ID} contains {EXPANSION_EXPECTED_COUNT} records; "
        f"{HNN_BATCH_ID} contains {HNN_EXPECTED_COUNT} records; "
        f"{OFFICIAL_BATCH_ID} contains {OFFICIAL_EXPECTED_COUNT} records."
    )


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[dict[str, Any]] = []

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        self.chain.append({"from": req.full_url, "http_status": code, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def wayback_timestamp(value: str) -> str | None:
    match = re.search(r"web\.archive\.org/web/(\d{14})", value)
    return match.group(1) if match else None


def resolve_medium_wayback(record: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode(
        [
            ("url", record["retrieval_url"]),
            ("output", "json"),
            ("fl", "timestamp,original,statuscode,mimetype,digest"),
            ("filter", "statuscode:200"),
            ("filter", "mimetype:text/html"),
            ("collapse", "digest"),
        ]
    )
    index_url = f"https://web.archive.org/cdx/search/cdx?{query}"
    last_error: str | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = urllib.request.Request(
            index_url,
            headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                payload = response.read()
                status = response.getcode()
            rows = json.loads(payload.decode("utf-8"))
            captures = [row for row in rows[1:] if isinstance(row, list) and len(row) >= 5]
            if not captures:
                return {
                    "index_http_status": status,
                    "index_response_sha256": sha256_bytes(payload),
                    "original_retrieval_url": record["retrieval_url"],
                    "resolved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "resolved_retrieval_url": None,
                    "resolution_attempts": attempt,
                    "resolution_error": "NO_PUBLIC_HTML_CAPTURE",
                    "resolution_status": "SNAPSHOT_NOT_FOUND",
                    "snapshot_timestamp": None,
                    "source_id": record["source_id"],
                }
            selected = sorted(captures, key=lambda row: (row[0], row[1], row[4]))[0]
            timestamp, original = str(selected[0]), str(selected[1])
            return {
                "index_http_status": status,
                "index_response_sha256": sha256_bytes(payload),
                "original_retrieval_url": record["retrieval_url"],
                "resolved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "resolved_retrieval_url": f"https://web.archive.org/web/{timestamp}id_/{original}",
                "resolution_attempts": attempt,
                "resolution_error": None,
                "resolution_policy": "EARLIEST_PUBLIC_200_HTML_CAPTURE",
                "resolution_status": "RESOLVED_CDX_EARLIEST_CAPTURE",
                "snapshot_digest": str(selected[4]),
                "snapshot_timestamp": timestamp,
                "source_id": record["source_id"],
            }
        except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout, ssl.SSLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = f"{type(exc).__name__}:{exc}"
            if attempt < MAX_ATTEMPTS:
                time.sleep(attempt)
    return {
        "index_http_status": None,
        "index_response_sha256": None,
        "original_retrieval_url": record["retrieval_url"],
        "resolved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "resolved_retrieval_url": None,
        "resolution_attempts": MAX_ATTEMPTS,
        "resolution_error": last_error,
        "resolution_status": "RESOLUTION_FAILED",
        "snapshot_timestamp": None,
        "source_id": record["source_id"],
    }


def resolve_hnn_carriers(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prior = {item["source_id"]: item for item in read_jsonl(HNN_RESOLUTION_LEDGER)}
    resolved: list[dict[str, Any]] = []
    for record in records:
        source_id = record["source_id"]
        previous = prior.get(source_id)
        if previous and (
            previous.get("resolved_retrieval_url")
            or previous.get("resolution_status") in {"SNAPSHOT_NOT_FOUND", "RESOLUTION_FAILED"}
        ):
            resolved.append(previous)
            continue
        retrieval_url = record["retrieval_url"]
        timestamp = wayback_timestamp(retrieval_url)
        if timestamp:
            item = {
                "index_http_status": None,
                "index_response_sha256": None,
                "original_retrieval_url": retrieval_url,
                "resolved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "resolved_retrieval_url": retrieval_url,
                "resolution_attempts": 0,
                "resolution_error": None,
                "resolution_policy": "REUSE_PRIOR_EXACT_WAYBACK_CAPTURE",
                "resolution_status": "RESOLVED_PRIOR_EXACT_WAYBACK",
                "snapshot_timestamp": timestamp,
                "source_id": source_id,
            }
        else:
            item = resolve_medium_wayback(record)
        resolved.append(item)
        write_jsonl(HNN_RESOLUTION_LEDGER, sorted(resolved, key=lambda value: value["source_id"]))
        print(f"Resolved {source_id}: {item['resolution_status']}", flush=True)
        if item.get("resolution_status") == "RESOLVED_CDX_EARLIEST_CAPTURE":
            time.sleep(REQUEST_DELAY_SECONDS)
    resolved.sort(key=lambda item: item["source_id"])
    write_jsonl(HNN_RESOLUTION_LEDGER, resolved)
    return resolved


def extract_identity(body: bytes, content_type: str | None) -> dict[str, Any]:
    text = body.decode("utf-8", errors="replace")
    observed: dict[str, Any] = {
        "canonical_url": None,
        "document_title": None,
        "response_format": "BINARY_OR_UNKNOWN",
    }
    if "json" in (content_type or "").lower() or text.lstrip().startswith(("{", "[")):
        try:
            parsed = json.loads(text)
            item = parsed[0] if isinstance(parsed, list) and parsed else parsed
            if isinstance(item, dict):
                # Zendesk Help Center responses wrap the canonical article
                # metadata and body in a top-level ``article`` object.
                if isinstance(item.get("article"), dict):
                    item = item["article"]
                title = item.get("title")
                if isinstance(title, dict):
                    title = title.get("rendered")
                observed.update(
                    {
                        "canonical_url": item.get("link") or item.get("html_url"),
                        "document_title": html.unescape(re.sub("<[^>]+>", "", title or "")) or None,
                        "response_format": "JSON",
                    }
                )
                return observed
        except json.JSONDecodeError:
            pass
    if "html" in (content_type or "").lower() or re.search(br"<html\b", body[:4096], re.I):
        canonical_patterns = (
            r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
            r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)',
        )
        title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        canonical = None
        for pattern in canonical_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                canonical = html.unescape(match.group(1).strip())
                break
        observed.update(
            {
                "canonical_url": canonical,
                "document_title": html.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else None,
                "response_format": "HTML",
            }
        )
    return observed


def compare_identity(record: dict[str, Any], final_url: str, observed: dict[str, Any]) -> dict[str, Any]:
    expected = normalized_url(record.get("original_url"))
    final = normalized_url(final_url)
    canonical = normalized_url(observed.get("canonical_url"))
    candidates = [value for value in (final, canonical) if value]
    expected_github = urllib.parse.urlsplit(record.get("retrieval_url") or "")
    github_match = re.fullmatch(r"/repos/([^/]+)/([^/]+)/readme", expected_github.path.rstrip("/"), re.I)
    final_github = urllib.parse.urlsplit(final_url)
    if expected_github.netloc.lower() == "api.github.com" and github_match and final_github.netloc.lower() == "raw.githubusercontent.com":
        owner, repository = github_match.groups()
        expected_raw_prefix = f"/{owner}/{repository}/".lower()
        if final_github.path.lower().startswith(expected_raw_prefix):
            return {
                "expected_url": record.get("original_url"),
                "observed_canonical_url": observed.get("canonical_url"),
                "observed_final_url": final_url,
                "reasons": ["IMMUTABLE_GITHUB_REPOSITORY_AND_README_PATH_MATCH"],
                "status": "CONSISTENT",
            }
    if expected and expected in candidates:
        return {
            "expected_url": record.get("original_url"),
            "observed_canonical_url": observed.get("canonical_url"),
            "observed_final_url": final_url,
            "reasons": ["EXPECTED_URL_MATCHES_OBSERVED_URL"],
            "status": "MATCH",
        }
    expected_medium_id = medium_post_id(expected)
    candidate_medium_ids = {medium_post_id(value) for value in candidates}
    candidate_medium_ids.discard(None)
    if expected_medium_id and expected_medium_id in candidate_medium_ids:
        return {
            "expected_url": record.get("original_url"),
            "observed_canonical_url": observed.get("canonical_url"),
            "observed_final_url": final_url,
            "reasons": ["STABLE_MEDIUM_POST_ID_MATCH_AFTER_PUBLICATION_PATH_CHANGE"],
            "status": "CONSISTENT",
        }
    expected_parts = urllib.parse.urlsplit(expected) if expected else None
    for candidate in candidates:
        parts = urllib.parse.urlsplit(candidate)
        if expected_parts and parts.netloc == expected_parts.netloc and parts.path == expected_parts.path:
            return {
                "expected_url": record.get("original_url"),
                "observed_canonical_url": observed.get("canonical_url"),
                "observed_final_url": final_url,
                "reasons": ["HOST_AND_PATH_MATCH_AFTER_NORMALIZATION"],
                "status": "CONSISTENT",
            }
    retrieval_url = record.get("retrieval_url") or ""
    if "web.archive.org/web/" in retrieval_url and expected:
        if urllib.parse.urlsplit(expected).netloc in urllib.parse.unquote(retrieval_url):
            return {
                "expected_url": record.get("original_url"),
                "observed_canonical_url": observed.get("canonical_url"),
                "observed_final_url": final_url,
                "reasons": ["ARCHIVE_CAPTURE_CONTAINS_EXPECTED_ORIGIN"],
                "status": "CONSISTENT",
            }
    if not canonical and final and normalized_url(record.get("retrieval_url")) == final:
        return {
            "expected_url": record.get("original_url"),
            "observed_canonical_url": None,
            "observed_final_url": final_url,
            "reasons": ["RETRIEVAL_ENDPOINT_MATCHED_BUT_NO_CANONICAL_IDENTITY_WAS_EXPOSED"],
            "status": "UNRESOLVED",
        }
    return {
        "expected_url": record.get("original_url"),
        "observed_canonical_url": observed.get("canonical_url"),
        "observed_final_url": final_url,
        "reasons": ["OBSERVED_IDENTITY_DOES_NOT_MATCH_FROZEN_SOURCE_URL"],
        "status": "MISMATCH",
    }


def raw_paths(record: dict[str, Any]) -> tuple[Path, Path]:
    record_dir = RAW_ROOT / record["source_family"] / record["source_id"]
    provenance_path = PROVENANCE_ROOT / record["source_family"] / f"{record['source_id']}.json"
    return record_dir / "response-body.bin", provenance_path


def github_immutable_target(record: dict[str, Any], opener: Any) -> tuple[str, str]:
    parsed = urllib.parse.urlsplit(record["retrieval_url"])
    match = re.fullmatch(r"/repos/([^/]+)/([^/]+)/readme", parsed.path.rstrip("/"), re.I)
    if parsed.netloc.lower() != "api.github.com" or not match:
        raise ValueError(f"UNSUPPORTED_GITHUB_README_URL:{record['retrieval_url']}")
    owner, repository = match.groups()
    readme_request = urllib.request.Request(
        record["retrieval_url"],
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
    )
    with opener.open(readme_request, timeout=TIMEOUT_SECONDS) as response:
        readme = json.loads(response.read().decode("utf-8"))
    readme_path = readme.get("path") if isinstance(readme, dict) else None
    if not isinstance(readme_path, str) or not readme_path:
        raise ValueError("GITHUB_README_PATH_NOT_RESOLVED")
    query = urllib.parse.urlencode({"path": readme_path, "per_page": 1})
    api_url = f"https://api.github.com/repos/{owner}/{repository}/commits?{query}"
    request = urllib.request.Request(
        api_url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
    )
    with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, list) or not payload or not isinstance(payload[0].get("sha"), str):
        raise ValueError("GITHUB_COMMIT_SHA_NOT_RESOLVED")
    git_sha = payload[0]["sha"]
    encoded_path = "/".join(urllib.parse.quote(part, safe="") for part in readme_path.split("/"))
    return f"https://raw.githubusercontent.com/{owner}/{repository}/{git_sha}/{encoded_path}", git_sha


def retrieval_classification(record: dict[str, Any], retrieval_url: str, final_url: str, git_sha: str | None) -> tuple[str, str, str | None]:
    if git_sha:
        return "IMMUTABLE_GIT_COMMIT_OR_BLOB", "CAPTURED_IMMUTABLE_GIT", git_sha
    archive_match = re.search(r"web\.archive\.org/web/(\d{14})", retrieval_url)
    if archive_match:
        return "PUBLIC_WEB_ARCHIVE_EXACT_URL", "CAPTURED_ARCHIVE", archive_match.group(1)
    if normalized_url(record.get("original_url")) == normalized_url(final_url):
        return "EXACT_PUBLIC_LIVE_CANONICAL", "CAPTURED_LIVE", None
    return "PROVEN_FIRST_PARTY_REDIRECT_OR_REPLACEMENT", "CAPTURED_LIVE", None


def looks_like_access_challenge(body: bytes, content_type: str | None) -> bool:
    if "html" not in (content_type or "").lower() and b"<html" not in body[:4096].lower():
        return False
    sample = body[:200000].decode("utf-8", errors="ignore").lower()
    title_match = re.search(r"<title[^>]*>(.*?)</title>", sample, re.I | re.S)
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
    # Do not classify an archived application page as a challenge merely because
    # its configuration contains a reCAPTCHA key. Medium article HTML includes
    # those keys even when the full story body is present.
    if "cf-chl-" in sample:
        return True
    if title in {"just a moment...", "attention required! | cloudflare"}:
        return True
    if "verify you are human" in sample and len(body) < 100000:
        return True
    return bool(re.search(r'<(?:div|form)[^>]+class=["\'][^"\']*g-recaptcha', sample))


def temporal_qualifier(retrieval_tier: str, capture_utc: str, snapshot_or_sha: str | None) -> str:
    if retrieval_tier == "PUBLIC_WEB_ARCHIVE_EXACT_URL":
        return f"HISTORICAL_PUBLIC_ARCHIVE_SNAPSHOT_{snapshot_or_sha}"
    if retrieval_tier == "IMMUTABLE_GIT_COMMIT_OR_BLOB":
        return f"IMMUTABLE_GIT_BLOB_{snapshot_or_sha};NOT_PROVEN_AS_ORIGINAL_EXTRACTION_STATE"
    return f"LIVE_RECAPTURE_{capture_utc};NOT_PUBLICATION_DATE_BYTES"


def verified_checkpoint(record: dict[str, Any]) -> dict[str, Any] | None:
    body_path, provenance_path = raw_paths(record)
    if not body_path.exists() or not provenance_path.exists():
        return None
    try:
        provenance = read_json(provenance_path)
        body = body_path.read_bytes()
    except (OSError, json.JSONDecodeError):
        return None
    if provenance.get("raw_body", {}).get("sha256") != sha256_bytes(body):
        return None
    if provenance.get("source_id") != record["source_id"]:
        return None
    current_identity = provenance.get("identity_comparison", {})
    if current_identity.get("status") == "UNRESOLVED":
        observed = extract_identity(body, provenance.get("content_type"))
        identity = compare_identity(record, provenance["response"]["final_url"], observed)
        if identity.get("status") in {"MATCH", "CONSISTENT"}:
            git_sha = (
                provenance.get("snapshot_timestamp_or_git_sha")
                if provenance.get("retrieval_tier") == "IMMUTABLE_GIT_COMMIT_OR_BLOB"
                else None
            )
            retrieval_tier, captured_disposition, _ = retrieval_classification(
                record,
                provenance["request"]["retrieval_url"],
                provenance["response"]["final_url"],
                git_sha,
            )
            provenance["identity_comparison"] = identity
            provenance["manual_review_required"] = False
            provenance["observed_document"] = observed
            provenance["retrieval_tier"] = retrieval_tier
            provenance["terminal_disposition"] = captured_disposition
            write_json(provenance_path, provenance)
    return provenance


def ledger_from_provenance(record: dict[str, Any], provenance: dict[str, Any], checkpoint: bool) -> dict[str, Any]:
    ledger = {
        "body_bytes": provenance["raw_body"]["byte_length"],
        "body_path": provenance["raw_body"]["path"],
        "body_sha256": provenance["raw_body"]["sha256"],
        "captured_at": provenance["captured_at"],
        "checkpoint_reused": checkpoint,
        "final_url": provenance["response"]["final_url"],
        "http_status": provenance["response"]["http_status"],
        "identity_status": provenance["identity_comparison"]["status"],
        "manual_review_required": provenance["manual_review_required"],
        "provenance_path": provenance["provenance_path"],
        "retrieval_tier": provenance["retrieval_tier"],
        "retrieval_url": provenance["request"]["retrieval_url"],
        "source_family": record["source_family"],
        "source_id": record["source_id"],
        "terminal_disposition": provenance["terminal_disposition"],
    }
    if provenance.get("retrieval_batch_id"):
        ledger["retrieval_batch_id"] = provenance["retrieval_batch_id"]
    return ledger


def build_archive_manifest() -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = []
    artifact_paths = sorted(
        (
            path
            for root in (RAW_ROOT, PROVENANCE_ROOT)
            if root.exists()
            for path in root.rglob("*")
            if path.is_file()
        ),
        key=relative,
    )
    preload_canonical_repository_bytes(artifact_paths)
    for path in artifact_paths:
        data = portable_artifact_bytes(path)
        artifacts.append(
            {
                "byte_count": len(data),
                "path": relative(path),
                "sha256": sha256_bytes(data),
            }
        )
    return {
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "campaign_id": CAMPAIGN_ID,
        "expansion_batch_id": EXPANSION_BATCH_ID,
        "expansion_record_count": EXPANSION_EXPECTED_COUNT,
        "expansion_selection_path": relative(EXPANSION_SELECTION),
        "expansion_selection_sha256": sha256_bytes(portable_artifact_bytes(EXPANSION_SELECTION)) if EXPANSION_SELECTION.exists() else None,
        "frozen_manifest_path": relative(FROZEN_MANIFEST),
        "frozen_manifest_sha256": sha256_bytes(canonical_repository_bytes(FROZEN_MANIFEST)) if FROZEN_MANIFEST.exists() else None,
        "hnn_batch_id": HNN_BATCH_ID,
        "hnn_record_count": HNN_EXPECTED_COUNT,
        "hnn_resolution_ledger_path": relative(HNN_RESOLUTION_LEDGER),
        "hnn_resolution_ledger_sha256": sha256_bytes(portable_artifact_bytes(HNN_RESOLUTION_LEDGER)) if HNN_RESOLUTION_LEDGER.exists() else None,
        "hnn_selection_path": relative(HNN_SELECTION),
        "hnn_selection_sha256": sha256_bytes(portable_artifact_bytes(HNN_SELECTION)) if HNN_SELECTION.exists() else None,
        "official_batch_id": OFFICIAL_BATCH_ID,
        "official_record_count": OFFICIAL_EXPECTED_COUNT,
        "official_selection_path": relative(OFFICIAL_SELECTION),
        "official_selection_sha256": sha256_bytes(portable_artifact_bytes(OFFICIAL_SELECTION)) if OFFICIAL_SELECTION.exists() else None,
        "pilot_record_count": len(PILOT_SOURCE_IDS),
        "pilot_selection_path": relative(PILOT_SELECTION),
        "pilot_selection_sha256": sha256_bytes(canonical_repository_bytes(PILOT_SELECTION)) if PILOT_SELECTION.exists() else None,
        "schema_version": SCHEMA_VERSION,
    }


def write_archive_manifest() -> None:
    write_json(ARCHIVE_MANIFEST, build_archive_manifest())


def fetch_public_http_with_curl(retrieval_url: str) -> tuple[bytes, int, str, str | None, dict[str, str], list[dict[str, Any]]]:
    """Fetch a public page with curl when Medium rejects Python urllib's TLS client.

    This is an unauthenticated HTTP transport fallback, not a paywall or access
    bypass. It is used only for HNN Medium records whose public Wayback lookup
    has already returned no snapshot.
    """
    with tempfile.TemporaryDirectory(prefix="star-atlas-hnn-") as temp_dir:
        temp = Path(temp_dir)
        body_path = temp / "body.bin"
        header_path = temp / "headers.txt"
        result = subprocess.run(
            [
                "curl",
                "--location",
                "--silent",
                "--show-error",
                "--max-time",
                str(TIMEOUT_SECONDS),
                "--user-agent",
                USER_AGENT,
                "--header",
                "Accept: text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
                "--dump-header",
                str(header_path),
                "--output",
                str(body_path),
                "--write-out",
                "%{http_code}\n%{url_effective}\n%{content_type}",
                retrieval_url,
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS + 10,
            check=False,
        )
        if result.returncode != 0:
            raise OSError(f"CURL_EXIT_{result.returncode}:{result.stderr.strip()}")
        output = result.stdout.splitlines()
        if len(output) < 3 or not output[0].isdigit():
            raise ValueError("CURL_METADATA_INVALID")
        http_status = int(output[0])
        final_url = output[1]
        content_type = output[2] or None
        body = body_path.read_bytes()
        header_text = header_path.read_text(encoding="iso-8859-1", errors="replace")

    blocks = [block for block in re.split(r"\r?\n\r?\n", header_text) if block.startswith("HTTP/")]
    redirect_chain: list[dict[str, Any]] = []
    response_headers: dict[str, str] = {}
    for block in blocks:
        lines = block.splitlines()
        status_match = re.match(r"HTTP/\S+\s+(\d+)", lines[0])
        parsed_headers: dict[str, str] = {}
        for line in lines[1:]:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            parsed_headers[key.strip().lower()] = value.strip()
        if status_match and parsed_headers.get("location"):
            redirect_chain.append(
                {
                    "http_status": int(status_match.group(1)),
                    "location": parsed_headers["location"],
                }
            )
        response_headers = {
            key: value
            for key, value in parsed_headers.items()
            if key in {"content-type", "content-length", "etag", "last-modified", "date"}
        }
    return body, http_status, final_url, content_type, response_headers, redirect_chain


def retrieve_record(
    record: dict[str, Any], retrieval_batch_id: str | None = None
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    checkpoint = verified_checkpoint(record)
    if checkpoint:
        return ledger_from_provenance(record, checkpoint, True), []

    attempt_records: list[dict[str, Any]] = []
    last_error: str | None = None
    for attempt_number in range(1, MAX_ATTEMPTS + 1):
        started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        redirects = RedirectRecorder()
        opener = urllib.request.build_opener(redirects)
        retrieval_url = record["retrieval_url"]
        git_sha: str | None = None
        try:
            parsed_retrieval = urllib.parse.urlsplit(retrieval_url)
            if (
                parsed_retrieval.netloc.lower() == "api.github.com"
                and re.fullmatch(r"/repos/[^/]+/[^/]+/readme", parsed_retrieval.path.rstrip("/"), re.I)
            ):
                retrieval_url, git_sha = github_immutable_target(record, opener)
            request = urllib.request.Request(
                retrieval_url,
                headers={
                    "Accept": "text/html,application/json,application/xhtml+xml;q=0.9,*/*;q=0.5",
                    "User-Agent": USER_AGENT,
                },
            )
            if record.get("transport") == "CURL_PUBLIC_HTTP":
                body, http_status, final_url, content_type, headers, redirect_chain = fetch_public_http_with_curl(
                    retrieval_url
                )
            else:
                with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
                    body = response.read()
                    http_status = response.getcode()
                    final_url = response.geturl()
                    content_type = response.headers.get("Content-Type")
                    headers = {
                        key.lower(): value
                        for key, value in response.headers.items()
                        if key.lower() in {"content-type", "content-length", "etag", "last-modified", "date"}
                    }
                redirect_chain = redirects.chain
            if not 200 <= http_status < 300:
                raise urllib.error.HTTPError(final_url, http_status, "non-success response", None, None)
            if not body:
                raise ValueError("EMPTY_RESPONSE_BODY")
            if looks_like_access_challenge(body, content_type):
                raise AccessChallenge("ACCESS_CHALLENGE_PAGE")
            observed = extract_identity(body, content_type)
            identity = compare_identity(record, final_url, observed)
            manual_review = identity["status"] not in {"MATCH", "CONSISTENT"}
            retrieval_tier, captured_disposition, snapshot_or_sha = retrieval_classification(
                record, retrieval_url, final_url, git_sha
            )
            disposition = "AMBIGUOUS_MANUAL_REVIEW" if manual_review else captured_disposition
            body_path, provenance_path = raw_paths(record)
            body_path.parent.mkdir(parents=True, exist_ok=True)
            body_path.write_bytes(body)
            captured_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            provenance = {
                "byte_count": len(body),
                "campaign_id": CAMPAIGN_ID,
                "capture_utc": captured_at,
                "captured_at": captured_at,
                "content_type": content_type,
                "final_url": final_url,
                "headers": headers,
                "http_status": http_status,
                "identity_comparison": identity,
                "manual_review_required": manual_review,
                "observed_document": observed,
                "original_url": record.get("original_url"),
                "provenance_path": relative(provenance_path),
                "raw_sha256": sha256_bytes(body),
                "raw_body": {
                    "byte_length": len(body),
                    "path": relative(body_path),
                    "sha256": sha256_bytes(body),
                },
                "request": {
                    "method": "GET",
                    "public_unauthenticated_http": True,
                    "retrieval_url": retrieval_url,
                    "retrieval_url_basis": "IMMUTABLE_GITHUB_README_BLOB" if git_sha else record["retrieval_url_basis"],
                    "user_agent": USER_AGENT,
                },
                "redirect_chain": redirect_chain,
                "retrieval_batch_id": retrieval_batch_id,
                "retrieval_tier": retrieval_tier,
                "response": {
                    "content_type": content_type,
                    "final_url": final_url,
                    "headers": headers,
                    "http_status": http_status,
                    "redirect_chain": redirect_chain,
                },
                "schema_version": SCHEMA_VERSION,
                "snapshot_timestamp_or_git_sha": snapshot_or_sha,
                "source_family": record["source_family"],
                "source_id": record["source_id"],
                "temporal_qualifier": temporal_qualifier(retrieval_tier, captured_at, snapshot_or_sha),
                "terminal_disposition": disposition,
            }
            write_json(provenance_path, provenance)
            attempt_records.append(
                {
                    "attempt": attempt_number,
                    "completed_at": captured_at,
                    "error": None,
                    "http_status": http_status,
                    "retrieval_batch_id": retrieval_batch_id,
                    "source_id": record["source_id"],
                    "started_at": started_at,
                    "status": "CAPTURED",
                }
            )
            return ledger_from_provenance(record, provenance, False), attempt_records
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP_{exc.code}"
            http_status = exc.code
        except (urllib.error.URLError, socket.timeout, ssl.SSLError, TimeoutError) as exc:
            last_error = f"NETWORK_ERROR:{type(exc).__name__}:{exc}"
            http_status = None
        except AccessChallenge as exc:
            last_error = f"ACCESS_CHALLENGE:{exc}"
            http_status = 200
        except (OSError, ValueError) as exc:
            last_error = f"RETRIEVAL_ERROR:{type(exc).__name__}:{exc}"
            http_status = None
        attempt_records.append(
            {
                "attempt": attempt_number,
                "completed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "error": last_error,
                "http_status": http_status,
                "retrieval_batch_id": retrieval_batch_id,
                "source_id": record["source_id"],
                "started_at": started_at,
                "status": "FAILED",
            }
        )
        if attempt_number < MAX_ATTEMPTS:
            time.sleep(attempt_number)

    return (
        {
            "body_bytes": 0,
            "body_path": None,
            "body_sha256": None,
            "captured_at": attempt_records[-1]["completed_at"],
            "checkpoint_reused": False,
            "error": last_error,
            "final_url": None,
            "http_status": attempt_records[-1]["http_status"],
            "identity_status": "NOT_EVALUATED",
            "manual_review_required": True,
            "provenance_path": None,
            "retrieval_batch_id": retrieval_batch_id,
            "retrieval_url": record["retrieval_url"],
            "source_family": record["source_family"],
            "source_id": record["source_id"],
            "terminal_disposition": (
                "BLOCKED_ACCESS_OR_POLICY"
                if attempt_records[-1].get("http_status") in ACCESS_BLOCK_STATUSES
                or str(attempt_records[-1].get("error", "")).startswith("ACCESS_CHALLENGE")
                else "NOT_FOUND_EXHAUSTED"
            ),
        },
        attempt_records,
    )


def summarize_batch(ledger: list[dict[str, Any]], expected: int) -> dict[str, Any]:
    dispositions = Counter(item["terminal_disposition"] for item in ledger)
    identity = Counter(item["identity_status"] for item in ledger)
    preserved = [item for item in ledger if item.get("body_path")]
    return {
        "expected_records": expected,
        "identity_status_counts": dict(sorted(identity.items())),
        "manual_review_count": sum(bool(item["manual_review_required"]) for item in ledger),
        "raw_bodies_preserved": len(preserved),
        "terminal_disposition_counts": dict(sorted(dispositions.items())),
        "terminal_records": len(ledger),
        "urls_retrieved": len(preserved),
    }


def write_summary() -> None:
    pilot_ledger = read_jsonl(RETRIEVAL_LEDGER)
    expansion_ledger = read_jsonl(EXPANSION_RETRIEVAL_LEDGER)
    hnn_ledger = read_jsonl(HNN_RETRIEVAL_LEDGER)
    official_ledger = read_jsonl(OFFICIAL_RETRIEVAL_LEDGER)
    effective_by_source: dict[str, dict[str, Any]] = {}
    for item in pilot_ledger + expansion_ledger + hnn_ledger + official_ledger:
        effective_by_source[item["source_id"]] = item
    all_ledger = [effective_by_source[source_id] for source_id in sorted(effective_by_source)]
    dispositions = Counter(item["terminal_disposition"] for item in all_ledger)
    identity = Counter(item["identity_status"] for item in all_ledger)
    manual = [item for item in all_ledger if item["manual_review_required"]]
    preserved = [item for item in all_ledger if item.get("body_path")]
    expansion_complete = len(expansion_ledger) == EXPANSION_EXPECTED_COUNT
    hnn_terminal = len(hnn_ledger) == HNN_EXPECTED_COUNT
    hnn_effective = [item for item in all_ledger if item["source_family"] == "hologram-news-network"]
    hnn_preserved = [item for item in hnn_effective if item.get("body_path")]
    hnn_manual = [item for item in hnn_effective if item["manual_review_required"]]
    official_terminal = len(official_ledger) == OFFICIAL_EXPECTED_COUNT
    official_effective = [item for item in all_ledger if item["source_family"] == "official-star-atlas"]
    official_preserved = [item for item in official_effective if item.get("body_path")]
    official_manual = [item for item in official_effective if item["manual_review_required"]]
    if (
        expansion_complete
        and hnn_terminal
        and len(hnn_preserved) == HNN_FAMILY_TOTAL
        and not hnn_manual
        and official_terminal
        and len(official_preserved) == OFFICIAL_FAMILY_TOTAL
        and not official_manual
    ):
        status = "AEPHIA_HNN_AND_OFFICIAL_FAMILY_RECOVERY_COMPLETE"
    elif expansion_complete and hnn_terminal and len(hnn_preserved) == HNN_FAMILY_TOTAL and not hnn_manual and official_terminal:
        status = "AEPHIA_AND_HNN_COMPLETE_OFFICIAL_TERMINALLY_DISPOSITIONED_WITH_EXCEPTIONS"
    elif expansion_complete and hnn_terminal and len(hnn_preserved) == HNN_FAMILY_TOTAL and not hnn_manual:
        status = "AEPHIA_AND_HNN_COMPLETE_OFFICIAL_PENDING"
    elif expansion_complete and hnn_terminal:
        status = "AEPHIA_COMPLETE_HNN_TERMINALLY_DISPOSITIONED_WITH_EXCEPTIONS"
    elif expansion_complete:
        status = "AEPHIA_COMPLETE_HNN_PENDING"
    else:
        status = "FAMILY_EXPANSIONS_PENDING"
    summary = {
        "batches": {
            "pilot-20": summarize_batch(pilot_ledger, len(PILOT_SOURCE_IDS)),
            EXPANSION_BATCH_ID: summarize_batch(expansion_ledger, EXPANSION_EXPECTED_COUNT),
            HNN_BATCH_ID: summarize_batch(hnn_ledger, HNN_EXPECTED_COUNT),
            OFFICIAL_BATCH_ID: summarize_batch(official_ledger, OFFICIAL_EXPECTED_COUNT),
        },
        "campaign_id": CAMPAIGN_ID,
        "distinct_records_attempted": len({item["source_id"] for item in all_ledger}),
        "expansion_records": EXPANSION_EXPECTED_COUNT,
        "frozen_records": 800,
        "hnn_completion_records": HNN_EXPECTED_COUNT,
        "hnn_family_records": HNN_FAMILY_TOTAL,
        "hnn_manual_review_count": len(hnn_manual),
        "hnn_raw_bodies_preserved": len(hnn_preserved),
        "official_completion_records": OFFICIAL_EXPECTED_COUNT,
        "official_family_records": OFFICIAL_FAMILY_TOTAL,
        "official_manual_review_count": len(official_manual),
        "official_raw_bodies_preserved": len(official_preserved),
        "identity_status_counts": dict(sorted(identity.items())),
        "manual_review_count": len(manual),
        "pilot_records": len(PILOT_SOURCE_IDS),
        "raw_bodies_preserved": len(preserved),
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "terminal_disposition_counts": dict(sorted(dispositions.items())),
        "urls_attempted": len(all_ledger),
        "urls_retrieved": len(preserved),
    }
    write_json(CAMPAIGN_SUMMARY_JSON, summary)
    lines = [
        "# Legacy Written Raw Recovery — Phase 2 Family Summary",
        "",
        f"- Frozen records: {summary['frozen_records']}",
        f"- Pilot records: {summary['pilot_records']}",
        f"- Aephia expansion records: {summary['expansion_records']}",
        f"- HNN completion records: {summary['hnn_completion_records']}",
        f"- HNN family raw bodies preserved: {summary['hnn_raw_bodies_preserved']}/{summary['hnn_family_records']}",
        f"- HNN manual review: {summary['hnn_manual_review_count']}",
        f"- Official completion records: {summary['official_completion_records']}",
        f"- Official family raw bodies preserved: {summary['official_raw_bodies_preserved']}/{summary['official_family_records']}",
        f"- Official manual review: {summary['official_manual_review_count']}",
        f"- Distinct records attempted: {summary['distinct_records_attempted']}",
        f"- URLs attempted: {summary['urls_attempted']}",
        f"- URLs retrieved: {summary['urls_retrieved']}",
        f"- Raw bodies preserved: {summary['raw_bodies_preserved']}",
        f"- Manual review: {summary['manual_review_count']}",
        f"- Status: `{summary['status']}`",
        "",
        "## Terminal dispositions",
        "",
    ]
    lines.extend(f"- `{key}`: {value}" for key, value in sorted(dispositions.items()))
    lines.extend(["", "## Identity comparison", ""])
    lines.extend(f"- `{key}`: {value}" for key, value in sorted(identity.items()))
    lines.extend(["", "## Batch status", ""])
    for batch_id, batch in summary["batches"].items():
        lines.append(
            f"- `{batch_id}`: {batch['terminal_records']}/{batch['expected_records']} terminal; "
            f"{batch['urls_retrieved']} retrieved; {batch['manual_review_count']} manual review"
        )
    CAMPAIGN_SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def retrieve_batch(
    source_ids: Iterable[str],
    ledger_path: Path,
    retry_path: Path,
    manual_path: Path,
    retrieval_batch_id: str | None,
    retry_failures: bool = False,
    request_delay_seconds: float = 0.0,
    record_overrides: dict[str, dict[str, Any]] | None = None,
) -> None:
    if not FROZEN_MANIFEST.exists():
        raise RuntimeError("Run `freeze` before retrieval.")
    manifest = read_json(FROZEN_MANIFEST)
    records_by_id = {record["source_id"]: record for record in manifest["records"]}
    selected_ids = tuple(source_ids)
    existing_ledger = {item["source_id"]: item for item in read_jsonl(ledger_path)}
    existing_attempts: dict[str, list[dict[str, Any]]] = {}
    for attempt in read_jsonl(retry_path):
        existing_attempts.setdefault(attempt["source_id"], []).append(attempt)
    ledger: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    blocked_hosts: dict[str, str] = {}
    for source_id in selected_ids:
        record = dict(records_by_id[source_id])
        if record_overrides and source_id in record_overrides:
            record.update(record_overrides[source_id])
        previous = existing_ledger.get(source_id)
        checkpoint = verified_checkpoint(record)
        if previous and ((previous.get("body_path") and checkpoint) or (not previous.get("body_path") and not retry_failures)):
            ledger.append(ledger_from_provenance(record, checkpoint, True) if checkpoint else previous)
            attempts.extend(existing_attempts.get(source_id, []))
            reused = ledger[-1]
            print(f"Reusing terminal checkpoint {source_id}: {reused['terminal_disposition']}", flush=True)
            continue
        host = urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower()
        if host in blocked_hosts:
            item = {
                "body_bytes": 0,
                "body_path": None,
                "body_sha256": None,
                "captured_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "checkpoint_reused": False,
                "error": f"HOST_STOP_RULE_TRIGGERED:{blocked_hosts[host]}",
                "final_url": None,
                "http_status": None,
                "identity_status": "NOT_EVALUATED",
                "manual_review_required": True,
                "provenance_path": None,
                "retrieval_batch_id": retrieval_batch_id,
                "retrieval_tier": None,
                "retrieval_url": record["retrieval_url"],
                "source_family": record["source_family"],
                "source_id": source_id,
                "terminal_disposition": "BLOCKED_ACCESS_OR_POLICY",
            }
            item_attempts = []
            ledger.append(item)
            print(f"Skipping {source_id}: host stop rule for {host}", flush=True)
            continue
        print(f"Retrieving {source_id} ...", flush=True)
        item, item_attempts = retrieve_record(record, retrieval_batch_id)
        ledger.append(item)
        attempts.extend(item_attempts)
        restricted = [
            attempt for attempt in item_attempts
            if attempt.get("http_status") in ACCESS_BLOCK_STATUSES
            or str(attempt.get("error", "")).startswith("ACCESS_CHALLENGE")
        ]
        if len(restricted) >= 3 and restricted[-3:] == item_attempts[-3:]:
            blocked_hosts[host] = str(restricted[-1].get("error") or restricted[-1].get("http_status"))
        print(f"  {item['terminal_disposition']} ({item['identity_status']})", flush=True)
        if request_delay_seconds:
            time.sleep(request_delay_seconds)
    ledger.sort(key=lambda item: item["source_id"])
    attempts.sort(key=lambda item: (item["source_id"], item["attempt"]))
    manual = [item for item in ledger if item["manual_review_required"]]
    write_jsonl(ledger_path, ledger)
    write_jsonl(retry_path, attempts)
    write_jsonl(manual_path, manual)
    write_summary()
    write_archive_manifest()


def retrieve_pilot(retry_failures: bool = False) -> None:
    retrieve_batch(
        PILOT_SOURCE_IDS,
        RETRIEVAL_LEDGER,
        RETRY_LEDGER,
        MANUAL_REVIEW_QUEUE,
        None,
        retry_failures,
    )


def retrieve_expansion(retry_failures: bool = False) -> None:
    if not EXPANSION_SELECTION.exists():
        raise RuntimeError("Run `freeze` before expansion retrieval.")
    selection = read_json(EXPANSION_SELECTION)
    source_ids = ids_from_selection(selection)
    if len(source_ids) != EXPANSION_EXPECTED_COUNT:
        raise RuntimeError(
            f"{EXPANSION_BATCH_ID} selection must contain {EXPANSION_EXPECTED_COUNT} Source IDs."
        )
    retrieve_batch(
        source_ids,
        EXPANSION_RETRIEVAL_LEDGER,
        EXPANSION_RETRY_LEDGER,
        EXPANSION_MANUAL_REVIEW_QUEUE,
        EXPANSION_BATCH_ID,
        retry_failures,
        REQUEST_DELAY_SECONDS,
    )


def reconcile_hnn_identity_checkpoints(
    records_by_id: dict[str, dict[str, Any]],
    overrides: dict[str, dict[str, Any]],
) -> None:
    """Re-evaluate HNN identities from preserved bytes using stable Medium post IDs."""
    ledger = read_jsonl(HNN_RETRIEVAL_LEDGER)
    changed = False
    for item in ledger:
        if not item.get("body_path") or not item.get("provenance_path"):
            continue
        provenance_path = REPO_ROOT / item["provenance_path"]
        provenance = read_json(provenance_path)
        record = dict(records_by_id[item["source_id"]])
        record.update(overrides.get(item["source_id"], {}))
        identity = compare_identity(
            record,
            provenance.get("final_url") or record["retrieval_url"],
            provenance.get("observed_document") or {},
        )
        manual_review = identity["status"] not in {"MATCH", "CONSISTENT"}
        if (
            identity == provenance.get("identity_comparison")
            and manual_review == provenance.get("manual_review_required")
        ):
            continue
        provenance["identity_comparison"] = identity
        provenance["manual_review_required"] = manual_review
        if manual_review:
            disposition = "AMBIGUOUS_MANUAL_REVIEW"
        elif provenance.get("retrieval_tier") == "PUBLIC_WEB_ARCHIVE_EXACT_URL":
            disposition = "CAPTURED_ARCHIVE"
        else:
            disposition = "CAPTURED_LIVE"
        provenance["terminal_disposition"] = disposition
        write_json(provenance_path, provenance)
        item["identity_status"] = identity["status"]
        item["manual_review_required"] = manual_review
        item["terminal_disposition"] = disposition
        changed = True
    if changed:
        ledger.sort(key=lambda value: value["source_id"])
        write_jsonl(HNN_RETRIEVAL_LEDGER, ledger)
        write_jsonl(HNN_MANUAL_REVIEW_QUEUE, [item for item in ledger if item["manual_review_required"]])


def retrieve_hnn_completion(retry_failures: bool = False) -> None:
    if not HNN_SELECTION.exists():
        raise RuntimeError("Run `freeze` before HNN completion retrieval.")
    manifest = read_json(FROZEN_MANIFEST)
    records_by_id = {record["source_id"]: record for record in manifest["records"]}
    source_ids = ids_from_selection(read_json(HNN_SELECTION))
    if len(source_ids) != HNN_EXPECTED_COUNT:
        raise RuntimeError(f"{HNN_BATCH_ID} selection must contain {HNN_EXPECTED_COUNT} Source IDs.")
    records = [records_by_id[source_id] for source_id in source_ids]
    resolutions = resolve_hnn_carriers(records)
    resolution_by_id = {item["source_id"]: item for item in resolutions}
    resolved_ids = [
        source_id
        for source_id in source_ids
        if resolution_by_id[source_id].get("resolved_retrieval_url")
    ]
    live_fallback_ids = [
        source_id
        for source_id in source_ids
        if not resolution_by_id[source_id].get("resolved_retrieval_url")
        and urllib.parse.urlsplit(records_by_id[source_id]["retrieval_url"]).netloc.lower() == "medium.com"
    ]
    overrides = {
        source_id: {
            "retrieval_url": resolution_by_id[source_id]["resolved_retrieval_url"],
            "retrieval_url_basis": resolution_by_id[source_id]["resolution_status"],
        }
        for source_id in resolved_ids
    }
    overrides.update(
        {
            source_id: {
                "retrieval_url": records_by_id[source_id]["retrieval_url"],
                "retrieval_url_basis": "PUBLIC_LIVE_MEDIUM_FALLBACK_AFTER_NO_ARCHIVE_SNAPSHOT",
                "transport": "CURL_PUBLIC_HTTP",
            }
            for source_id in live_fallback_ids
        }
    )
    retrieve_batch(
        sorted(resolved_ids + live_fallback_ids),
        HNN_RETRIEVAL_LEDGER,
        HNN_RETRY_LEDGER,
        HNN_MANUAL_REVIEW_QUEUE,
        HNN_BATCH_ID,
        retry_failures,
        HNN_REQUEST_DELAY_SECONDS,
        overrides,
    )
    reconcile_hnn_identity_checkpoints(records_by_id, overrides)
    ledger_by_id = {item["source_id"]: item for item in read_jsonl(HNN_RETRIEVAL_LEDGER)}
    for source_id in source_ids:
        resolution = resolution_by_id[source_id]
        if source_id in ledger_by_id or resolution.get("resolved_retrieval_url") or source_id in live_fallback_ids:
            continue
        record = records_by_id[source_id]
        ledger_by_id[source_id] = {
            "body_bytes": 0,
            "body_path": None,
            "body_sha256": None,
            "captured_at": resolution["resolved_at"],
            "checkpoint_reused": False,
            "error": f"WAYBACK_{resolution['resolution_status']}:{resolution.get('resolution_error')}",
            "final_url": None,
            "http_status": resolution.get("index_http_status"),
            "identity_status": "NOT_EVALUATED",
            "manual_review_required": True,
            "provenance_path": None,
            "retrieval_batch_id": HNN_BATCH_ID,
            "retrieval_tier": None,
            "retrieval_url": record["retrieval_url"],
            "source_family": record["source_family"],
            "source_id": source_id,
            "terminal_disposition": "NOT_FOUND_EXHAUSTED",
        }
    ledger = [ledger_by_id[source_id] for source_id in sorted(ledger_by_id)]
    write_jsonl(HNN_RETRIEVAL_LEDGER, ledger)
    write_jsonl(HNN_MANUAL_REVIEW_QUEUE, [item for item in ledger if item["manual_review_required"]])
    write_summary()
    write_archive_manifest()


def retrieve_official_completion(retry_failures: bool = False) -> None:
    if not OFFICIAL_SELECTION.exists():
        raise RuntimeError("Run `freeze` before official-source completion retrieval.")
    source_ids = ids_from_selection(read_json(OFFICIAL_SELECTION))
    if len(source_ids) != OFFICIAL_EXPECTED_COUNT:
        raise RuntimeError(
            f"{OFFICIAL_BATCH_ID} selection must contain {OFFICIAL_EXPECTED_COUNT} Source IDs."
        )
    retrieve_batch(
        source_ids,
        OFFICIAL_RETRIEVAL_LEDGER,
        OFFICIAL_RETRY_LEDGER,
        OFFICIAL_MANUAL_REVIEW_QUEUE,
        OFFICIAL_BATCH_ID,
        retry_failures,
        OFFICIAL_REQUEST_DELAY_SECONDS,
    )


def ids_from_selection(value: Any) -> list[str]:
    if isinstance(value, dict):
        for key in ("pilot_source_ids", "source_ids"):
            if isinstance(value.get(key), list):
                return sorted(item for item in value[key] if isinstance(item, str))
        for key in ("records", "pilot_records", "selection"):
            if isinstance(value.get(key), list):
                return sorted(
                    item["source_id"]
                    for item in value[key]
                    if isinstance(item, dict) and isinstance(item.get("source_id"), str)
                )
    return []


def validate() -> bool:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "detail": detail, "status": "PASS" if passed else "FAIL"})

    write_summary()
    expected = build_frozen_manifest()
    actual = read_json(FROZEN_MANIFEST) if FROZEN_MANIFEST.exists() else None
    check("FROZEN_MANIFEST_EXISTS", actual is not None, relative(FROZEN_MANIFEST))
    check("FROZEN_MANIFEST_DETERMINISTIC", actual == expected, "Generated manifest equals the current 800-record extraction inventory.")
    if actual:
        records = actual.get("records", [])
        source_ids = [record.get("source_id") for record in records]
        check("FROZEN_RECORD_COUNT", len(records) == 800, f"observed={len(records)} expected=800")
        check("UNIQUE_SOURCE_IDS", len(source_ids) == len(set(source_ids)), f"unique={len(set(source_ids))} total={len(source_ids)}")
        check("PILOT_SOURCE_IDS", sorted(actual.get("pilot_source_ids", [])) == sorted(PILOT_SOURCE_IDS), "Approved 20-record pilot is frozen exactly.")
        check(
            "EXTRACTION_CHECKSUMS",
            all(
                sha256_bytes(canonical_repository_bytes(REPO_ROOT / record["existing_extraction_path"])) == record["existing_extraction_sha256"]
                for record in records
            ),
            "All frozen extraction checksums reconcile.",
        )
        check(
            "SOURCE_RECORD_REFERENCES",
            all(
                not record.get("existing_source_record_path")
                or (
                    (REPO_ROOT / record["existing_source_record_path"]).exists()
                    and sha256_bytes(canonical_repository_bytes(REPO_ROOT / record["existing_source_record_path"]))
                    == record.get("existing_source_record_sha256")
                )
                for record in records
            ),
            "Every declared Source Record path and frozen SHA-256 reconcile.",
        )
    if PILOT_SELECTION.exists():
        selection_ids = ids_from_selection(read_json(PILOT_SELECTION))
        check("PILOT_SELECTION_RECONCILES", selection_ids == sorted(PILOT_SOURCE_IDS), f"selection_ids={len(selection_ids)} expected=20")
    else:
        check("PILOT_SELECTION_RECONCILES", True, "No separate pilot-selection.json exists; the frozen manifest remains authoritative.")

    actual_expansion_selection = read_json(EXPANSION_SELECTION) if EXPANSION_SELECTION.exists() else None
    expected_expansion_selection = build_expansion_selection(actual) if actual else None
    check(
        "EXPANSION_SELECTION_DETERMINISTIC",
        actual_expansion_selection == expected_expansion_selection,
        f"batch={EXPANSION_BATCH_ID}",
    )
    expansion_ids = ids_from_selection(actual_expansion_selection or {})
    check(
        "EXPANSION_RECORD_COUNT",
        len(expansion_ids) == EXPANSION_EXPECTED_COUNT,
        f"observed={len(expansion_ids)} expected={EXPANSION_EXPECTED_COUNT}",
    )
    check(
        "EXPANSION_DISJOINT_FROM_PILOT",
        not set(expansion_ids).intersection(PILOT_SOURCE_IDS),
        "Expansion Source IDs exclude all 20 pilot records.",
    )
    if actual:
        records_by_id = {record["source_id"]: record for record in actual["records"]}
        aephia_pilot = {
            source_id
            for source_id in PILOT_SOURCE_IDS
            if records_by_id[source_id]["source_family"] == "aephia"
        }
        selected_records = [records_by_id[source_id] for source_id in expansion_ids if source_id in records_by_id]
        check(
            "AEPHIA_FAMILY_COVERAGE",
            len(aephia_pilot | set(expansion_ids)) == 64,
            f"pilot={len(aephia_pilot)} expansion={len(expansion_ids)} total={len(aephia_pilot | set(expansion_ids))}",
        )
        check(
            "EXPANSION_HOST_ALLOWLIST",
            all(urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower() == EXPANSION_ALLOWED_HOST for record in selected_records),
            f"allowed_host={EXPANSION_ALLOWED_HOST}",
        )
        check(
            "EXPANSION_ENDPOINT_POLICY",
            all(
                urllib.parse.urlsplit(record["retrieval_url"]).path.startswith(EXPANSION_ALLOWED_PATH_PREFIX)
                and record["retrieval_url_basis"] == "PRIOR_FINAL_URL"
                for record in selected_records
            ),
            f"path_prefix={EXPANSION_ALLOWED_PATH_PREFIX}; basis=PRIOR_FINAL_URL",
        )

    actual_hnn_selection = read_json(HNN_SELECTION) if HNN_SELECTION.exists() else None
    expected_hnn_selection = build_hnn_selection(actual) if actual else None
    check(
        "HNN_SELECTION_DETERMINISTIC",
        actual_hnn_selection == expected_hnn_selection,
        f"batch={HNN_BATCH_ID}",
    )
    hnn_ids = ids_from_selection(actual_hnn_selection or {})
    check(
        "HNN_COMPLETION_RECORD_COUNT",
        len(hnn_ids) == HNN_EXPECTED_COUNT and len(hnn_ids) == len(set(hnn_ids)),
        f"observed={len(hnn_ids)} expected={HNN_EXPECTED_COUNT}",
    )
    check(
        "HNN_VERIFIED_BASELINE_DISJOINT",
        not set(hnn_ids).intersection(HNN_PRESERVED_BASELINE_SOURCE_IDS),
        f"preserved_baseline={len(HNN_PRESERVED_BASELINE_SOURCE_IDS)}",
    )
    if actual:
        hnn_family_ids = {
            record["source_id"]
            for record in actual["records"]
            if record["source_family"] == "hologram-news-network"
        }
        check(
            "HNN_FAMILY_SELECTION_COVERAGE",
            set(hnn_ids) | set(HNN_PRESERVED_BASELINE_SOURCE_IDS) == hnn_family_ids,
            f"selection={len(hnn_ids)} baseline={len(HNN_PRESERVED_BASELINE_SOURCE_IDS)} family={len(hnn_family_ids)}",
        )
        hnn_selected_records = [records_by_id[source_id] for source_id in hnn_ids if source_id in records_by_id]
        check(
            "HNN_SOURCE_SURFACE_ALLOWLIST",
            all(
                urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower() in HNN_ALLOWED_SOURCE_HOSTS
                and record["retrieval_url_basis"] == "PRIOR_REQUESTED_URL"
                for record in hnn_selected_records
            ),
            f"allowed_hosts={sorted(HNN_ALLOWED_SOURCE_HOSTS)}; basis=PRIOR_REQUESTED_URL",
        )

    actual_official_selection = read_json(OFFICIAL_SELECTION) if OFFICIAL_SELECTION.exists() else None
    expected_official_selection = build_official_selection(actual) if actual else None
    check(
        "OFFICIAL_SELECTION_DETERMINISTIC",
        actual_official_selection == expected_official_selection,
        f"batch={OFFICIAL_BATCH_ID}",
    )
    official_ids = ids_from_selection(actual_official_selection or {})
    check(
        "OFFICIAL_COMPLETION_RECORD_COUNT",
        len(official_ids) == OFFICIAL_EXPECTED_COUNT and len(official_ids) == len(set(official_ids)),
        f"observed={len(official_ids)} expected={OFFICIAL_EXPECTED_COUNT}",
    )
    check(
        "OFFICIAL_VERIFIED_BASELINE_DISJOINT",
        not set(official_ids).intersection(OFFICIAL_PRESERVED_BASELINE_SOURCE_IDS),
        f"preserved_baseline={len(OFFICIAL_PRESERVED_BASELINE_SOURCE_IDS)}",
    )
    if actual:
        official_family_ids = {
            record["source_id"]
            for record in actual["records"]
            if record["source_family"] == "official-star-atlas"
        }
        check(
            "OFFICIAL_FAMILY_SELECTION_COVERAGE",
            set(official_ids) | set(OFFICIAL_PRESERVED_BASELINE_SOURCE_IDS) == official_family_ids,
            (
                f"selection={len(official_ids)} baseline={len(OFFICIAL_PRESERVED_BASELINE_SOURCE_IDS)} "
                f"family={len(official_family_ids)}"
            ),
        )
        official_selected_records = [
            records_by_id[source_id] for source_id in official_ids if source_id in records_by_id
        ]
        check(
            "OFFICIAL_SOURCE_SURFACE_ALLOWLIST",
            all(
                urllib.parse.urlsplit(record["retrieval_url"]).netloc.lower()
                in OFFICIAL_ALLOWED_SOURCE_HOSTS
                and record["retrieval_url_basis"] in {"PRIOR_FINAL_URL", "PRIOR_REQUESTED_URL"}
                for record in official_selected_records
            ),
            f"allowed_hosts={sorted(OFFICIAL_ALLOWED_SOURCE_HOSTS)}",
        )

    pilot_baseline_ok = all(
        (CAMPAIGN_DIR / name).exists()
        and sha256_bytes(canonical_repository_bytes(CAMPAIGN_DIR / name)) == expected_sha
        for name, expected_sha in PILOT_BASELINE_SHA256.items()
    )
    check("PILOT_LEDGERS_IMMUTABLE", pilot_baseline_ok, "All four approved pilot ledger hashes match the merged baseline.")
    current_pilot_artifacts = pilot_artifact_entries()
    current_pilot_set_sha = pilot_artifact_set_sha256(current_pilot_artifacts)
    check(
        "PILOT_RAW_AND_PROVENANCE_IMMUTABLE",
        len(current_pilot_artifacts) == 30 and current_pilot_set_sha == PILOT_ARTIFACT_SET_SHA256,
        f"artifacts={len(current_pilot_artifacts)} aggregate_sha256={current_pilot_set_sha}",
    )

    ledger = read_jsonl(RETRIEVAL_LEDGER)
    if ledger:
        ledger_ids = [item.get("source_id") for item in ledger]
        check("TERMINAL_DISPOSITIONS", sorted(ledger_ids) == sorted(PILOT_SOURCE_IDS) and len(ledger_ids) == len(set(ledger_ids)), f"terminal_records={len(ledger_ids)}")
        raw_ok = True
        provenance_ok = True
        required_provenance_fields = {
            "source_id", "original_url", "final_url", "retrieval_tier", "capture_utc",
            "http_status", "content_type", "byte_count", "headers", "redirect_chain",
            "raw_sha256", "snapshot_timestamp_or_git_sha", "identity_comparison", "temporal_qualifier",
        }
        fields_ok = True
        for item in ledger:
            if not item.get("body_path"):
                continue
            body_path = REPO_ROOT / item["body_path"]
            provenance_path = REPO_ROOT / item["provenance_path"]
            if not body_path.exists() or sha256_bytes(body_path.read_bytes()) != item["body_sha256"]:
                raw_ok = False
            if not provenance_path.exists():
                provenance_ok = False
            else:
                provenance = read_json(provenance_path)
                if provenance.get("source_id") != item["source_id"] or provenance.get("raw_body", {}).get("sha256") != item["body_sha256"]:
                    provenance_ok = False
                if not required_provenance_fields.issubset(provenance):
                    fields_ok = False
        check("RAW_BODY_CHECKSUMS", raw_ok, "Every successful raw body exists and matches its ledger SHA-256.")
        check("PROVENANCE_RECONCILES", provenance_ok, "Every successful provenance record reconciles to its Source ID and body checksum.")
        check("REQUIRED_PROVENANCE_FIELDS", fields_ok, "Every preserved response has the complete Phase 2 provenance field set.")
        manual = read_jsonl(MANUAL_REVIEW_QUEUE)
        check(
            "MANUAL_REVIEW_QUEUE",
            sorted(item["source_id"] for item in manual) == sorted(item["source_id"] for item in ledger if item.get("manual_review_required")),
            "Manual-review queue equals the flagged terminal records.",
        )
    else:
        check("PILOT_RETRIEVAL_PENDING", True, "No retrieval ledger exists; frozen-corpus validation only.")

    expansion_ledger = read_jsonl(EXPANSION_RETRIEVAL_LEDGER)
    expansion_attempts = read_jsonl(EXPANSION_RETRY_LEDGER)
    if expansion_ledger:
        expansion_ledger_ids = [item.get("source_id") for item in expansion_ledger]
        check(
            "EXPANSION_TERMINAL_IDS",
            sorted(expansion_ledger_ids) == sorted(expansion_ids)
            and len(expansion_ledger_ids) == len(set(expansion_ledger_ids)),
            f"terminal_records={len(expansion_ledger_ids)} expected={len(expansion_ids)}",
        )
        expansion_raw_ok = True
        expansion_provenance_ok = True
        expansion_fields_ok = True
        required_expansion_fields = {
            "source_id", "original_url", "final_url", "retrieval_tier", "capture_utc",
            "http_status", "content_type", "byte_count", "headers", "redirect_chain",
            "raw_sha256", "snapshot_timestamp_or_git_sha", "identity_comparison",
            "temporal_qualifier", "retrieval_batch_id",
        }
        for item in expansion_ledger:
            if not item.get("body_path"):
                continue
            body_path = REPO_ROOT / item["body_path"]
            provenance_path = REPO_ROOT / item["provenance_path"]
            if not body_path.exists() or sha256_bytes(body_path.read_bytes()) != item["body_sha256"]:
                expansion_raw_ok = False
            if not provenance_path.exists():
                expansion_provenance_ok = False
                continue
            provenance = read_json(provenance_path)
            if (
                provenance.get("source_id") != item["source_id"]
                or provenance.get("raw_body", {}).get("sha256") != item["body_sha256"]
                or provenance.get("retrieval_batch_id") != EXPANSION_BATCH_ID
            ):
                expansion_provenance_ok = False
            if not required_expansion_fields.issubset(provenance):
                expansion_fields_ok = False
        check("EXPANSION_RAW_BODY_CHECKSUMS", expansion_raw_ok, "Every expansion raw body matches its ledger SHA-256.")
        check("EXPANSION_PROVENANCE_RECONCILES", expansion_provenance_ok, "Every expansion provenance record reconciles to its batch, Source ID, and body.")
        check("EXPANSION_REQUIRED_PROVENANCE_FIELDS", expansion_fields_ok, "Every preserved expansion response has the complete provenance field set.")
        expansion_manual = read_jsonl(EXPANSION_MANUAL_REVIEW_QUEUE)
        check(
            "EXPANSION_MANUAL_REVIEW_QUEUE",
            sorted(item["source_id"] for item in expansion_manual)
            == sorted(item["source_id"] for item in expansion_ledger if item.get("manual_review_required")),
            "Expansion manual-review queue equals its flagged terminal records.",
        )
        check(
            "EXPANSION_RETRY_SCOPE",
            all(
                item.get("source_id") in set(expansion_ids)
                and item.get("retrieval_batch_id") == EXPANSION_BATCH_ID
                for item in expansion_attempts
            ),
            f"attempt_records={len(expansion_attempts)}",
        )
    else:
        check(
            "EXPANSION_AUTHORIZED_PENDING_RETRIEVAL",
            actual_expansion_selection is not None,
            f"{EXPANSION_BATCH_ID} is selected but has no retrieval ledger yet.",
        )

    hnn_resolution = read_jsonl(HNN_RESOLUTION_LEDGER)
    hnn_ledger = read_jsonl(HNN_RETRIEVAL_LEDGER)
    hnn_attempts = read_jsonl(HNN_RETRY_LEDGER)
    if hnn_resolution:
        resolution_ids = [item.get("source_id") for item in hnn_resolution]
        check(
            "HNN_ARCHIVE_RESOLUTION_COVERAGE",
            sorted(resolution_ids) == sorted(hnn_ids) and len(resolution_ids) == len(set(resolution_ids)),
            f"resolved_records={len(resolution_ids)} expected={len(hnn_ids)}",
        )
        check(
            "HNN_ARCHIVE_CARRIER_POLICY",
            all(
                not item.get("resolved_retrieval_url")
                or (
                    urllib.parse.urlsplit(item["resolved_retrieval_url"]).netloc.lower() == "web.archive.org"
                    and wayback_timestamp(item["resolved_retrieval_url"])
                )
                for item in hnn_resolution
            ),
            "Every resolved HNN carrier is an exact timestamped public Wayback URL.",
        )
    else:
        check("HNN_ARCHIVE_RESOLUTION_PENDING", True, "HNN selection exists but carrier resolution has not run.")

    if hnn_ledger:
        hnn_ledger_ids = [item.get("source_id") for item in hnn_ledger]
        hnn_resolution_by_id = {item["source_id"]: item for item in hnn_resolution}
        check(
            "HNN_TERMINAL_IDS",
            sorted(hnn_ledger_ids) == sorted(hnn_ids) and len(hnn_ledger_ids) == len(set(hnn_ledger_ids)),
            f"terminal_records={len(hnn_ledger_ids)} expected={len(hnn_ids)}",
        )
        hnn_raw_ok = True
        hnn_provenance_ok = True
        hnn_fields_ok = True
        hnn_live_fallback_ok = True
        required_hnn_fields = {
            "source_id", "original_url", "final_url", "retrieval_tier", "capture_utc",
            "http_status", "content_type", "byte_count", "headers", "redirect_chain",
            "raw_sha256", "snapshot_timestamp_or_git_sha", "identity_comparison",
            "temporal_qualifier", "retrieval_batch_id",
        }
        for item in hnn_ledger:
            if not item.get("body_path"):
                continue
            body_path = REPO_ROOT / item["body_path"]
            provenance_path = REPO_ROOT / item["provenance_path"]
            if not body_path.exists() or sha256_bytes(body_path.read_bytes()) != item["body_sha256"]:
                hnn_raw_ok = False
            if not provenance_path.exists():
                hnn_provenance_ok = False
                continue
            provenance = read_json(provenance_path)
            resolution = hnn_resolution_by_id.get(item["source_id"], {})
            tier = provenance.get("retrieval_tier")
            archive_carrier_ok = (
                tier == "PUBLIC_WEB_ARCHIVE_EXACT_URL"
                and bool(resolution.get("resolved_retrieval_url"))
            )
            live_carrier_ok = (
                tier in {"EXACT_PUBLIC_LIVE_CANONICAL", "PROVEN_FIRST_PARTY_REDIRECT_OR_REPLACEMENT"}
                and not resolution.get("resolved_retrieval_url")
                and provenance.get("request", {}).get("retrieval_url_basis")
                == "PUBLIC_LIVE_MEDIUM_FALLBACK_AFTER_NO_ARCHIVE_SNAPSHOT"
                and urllib.parse.urlsplit(provenance.get("final_url") or "").netloc.lower() == "medium.com"
            )
            if (
                provenance.get("source_id") != item["source_id"]
                or provenance.get("raw_body", {}).get("sha256") != item["body_sha256"]
                or provenance.get("retrieval_batch_id") != HNN_BATCH_ID
                or not (archive_carrier_ok or live_carrier_ok)
            ):
                hnn_provenance_ok = False
            if live_carrier_ok:
                body_text = body_path.read_bytes()[:500000].decode("utf-8", errors="ignore").lower()
                if not (
                    "article:published_time" in body_text
                    and ("application/ld+json" in body_text or '"paragraph"' in body_text)
                    and len(body_path.read_bytes()) >= 50000
                ):
                    hnn_live_fallback_ok = False
            if not required_hnn_fields.issubset(provenance):
                hnn_fields_ok = False
        check("HNN_RAW_BODY_CHECKSUMS", hnn_raw_ok, "Every recovered HNN body matches its ledger SHA-256.")
        check("HNN_PROVENANCE_RECONCILES", hnn_provenance_ok, "Every recovered HNN record uses its declared exact-archive or public-live fallback tier and reconciles to its batch.")
        check("HNN_LIVE_FALLBACK_COMPLETENESS", hnn_live_fallback_ok, "Every Medium live fallback contains article publication metadata and structured body evidence.")
        check("HNN_REQUIRED_PROVENANCE_FIELDS", hnn_fields_ok, "Every recovered HNN response has the complete provenance field set.")
        hnn_manual = read_jsonl(HNN_MANUAL_REVIEW_QUEUE)
        check(
            "HNN_MANUAL_REVIEW_QUEUE",
            sorted(item["source_id"] for item in hnn_manual)
            == sorted(item["source_id"] for item in hnn_ledger if item.get("manual_review_required")),
            "HNN manual-review queue equals its flagged terminal records.",
        )
        check(
            "HNN_RETRY_SCOPE",
            all(
                item.get("source_id") in set(hnn_ids)
                and item.get("retrieval_batch_id") == HNN_BATCH_ID
                for item in hnn_attempts
            ),
            f"attempt_records={len(hnn_attempts)}",
        )
    else:
        check("HNN_AUTHORIZED_PENDING_RETRIEVAL", actual_hnn_selection is not None, f"{HNN_BATCH_ID} has no retrieval ledger yet.")

    official_ledger = read_jsonl(OFFICIAL_RETRIEVAL_LEDGER)
    official_attempts = read_jsonl(OFFICIAL_RETRY_LEDGER)
    if official_ledger:
        official_ledger_ids = [item.get("source_id") for item in official_ledger]
        check(
            "OFFICIAL_TERMINAL_IDS",
            sorted(official_ledger_ids) == sorted(official_ids)
            and len(official_ledger_ids) == len(set(official_ledger_ids)),
            f"terminal_records={len(official_ledger_ids)} expected={len(official_ids)}",
        )
        official_raw_ok = True
        official_provenance_ok = True
        official_fields_ok = True
        official_git_ok = True
        required_official_fields = {
            "source_id", "original_url", "final_url", "retrieval_tier", "capture_utc",
            "http_status", "content_type", "byte_count", "headers", "redirect_chain",
            "raw_sha256", "snapshot_timestamp_or_git_sha", "identity_comparison",
            "temporal_qualifier", "retrieval_batch_id",
        }
        for item in official_ledger:
            if not item.get("body_path"):
                continue
            body_path = REPO_ROOT / item["body_path"]
            provenance_path = REPO_ROOT / item["provenance_path"]
            if not body_path.exists() or sha256_bytes(body_path.read_bytes()) != item["body_sha256"]:
                official_raw_ok = False
            if not provenance_path.exists():
                official_provenance_ok = False
                continue
            provenance = read_json(provenance_path)
            if (
                provenance.get("source_id") != item["source_id"]
                or provenance.get("raw_body", {}).get("sha256") != item["body_sha256"]
                or provenance.get("retrieval_batch_id") != OFFICIAL_BATCH_ID
            ):
                official_provenance_ok = False
            if not required_official_fields.issubset(provenance):
                official_fields_ok = False
            source_record = records_by_id.get(item["source_id"], {}) if actual else {}
            if urllib.parse.urlsplit(source_record.get("retrieval_url") or "").netloc.lower() == "api.github.com":
                git_sha = provenance.get("snapshot_timestamp_or_git_sha")
                if (
                    provenance.get("retrieval_tier") != "IMMUTABLE_GIT_COMMIT_OR_BLOB"
                    or not isinstance(git_sha, str)
                    or not re.fullmatch(r"[0-9a-f]{40}", git_sha)
                ):
                    official_git_ok = False
        check("OFFICIAL_RAW_BODY_CHECKSUMS", official_raw_ok, "Every official-source body matches its ledger SHA-256.")
        check("OFFICIAL_PROVENANCE_RECONCILES", official_provenance_ok, "Every official-source provenance record reconciles to its batch, Source ID, and body.")
        check("OFFICIAL_REQUIRED_PROVENANCE_FIELDS", official_fields_ok, "Every official-source response has the complete provenance field set.")
        check("OFFICIAL_GITHUB_IMMUTABILITY", official_git_ok, "Every GitHub README carrier resolves to a 40-character immutable commit target.")
        official_manual = read_jsonl(OFFICIAL_MANUAL_REVIEW_QUEUE)
        check(
            "OFFICIAL_MANUAL_REVIEW_QUEUE",
            sorted(item["source_id"] for item in official_manual)
            == sorted(item["source_id"] for item in official_ledger if item.get("manual_review_required")),
            "Official-source manual-review queue equals its flagged terminal records.",
        )
        check(
            "OFFICIAL_RETRY_SCOPE",
            all(
                item.get("source_id") in set(official_ids)
                and item.get("retrieval_batch_id") == OFFICIAL_BATCH_ID
                for item in official_attempts
            ),
            f"attempt_records={len(official_attempts)}",
        )
    else:
        check(
            "OFFICIAL_AUTHORIZED_PENDING_RETRIEVAL",
            actual_official_selection is not None,
            f"{OFFICIAL_BATCH_ID} has no retrieval ledger yet.",
        )

    check(
        "CROSS_BATCH_SOURCE_IDS_UNIQUE",
        not {item.get("source_id") for item in ledger}.intersection(
            item.get("source_id") for item in expansion_ledger
        ),
        f"pilot={len(ledger)} expansion={len(expansion_ledger)}",
    )
    hnn_pilot_overlap = {item.get("source_id") for item in ledger}.intersection(
        item.get("source_id") for item in hnn_ledger
    )
    expected_hnn_pilot_repairs = set((actual_hnn_selection or {}).get("pilot_source_ids_repaired", []))
    check(
        "HNN_PILOT_REPAIR_SCOPE",
        (not hnn_ledger and not hnn_pilot_overlap)
        or hnn_pilot_overlap == expected_hnn_pilot_repairs,
        (
            "retrieval_pending; overlap=0"
            if not hnn_ledger
            else f"overlap={len(hnn_pilot_overlap)} expected_repairs={len(expected_hnn_pilot_repairs)}"
        ),
    )
    official_pilot_overlap = {item.get("source_id") for item in ledger}.intersection(
        item.get("source_id") for item in official_ledger
    )
    expected_official_pilot_repairs = set(
        (actual_official_selection or {}).get("pilot_source_ids_repaired", [])
    )
    check(
        "OFFICIAL_PILOT_REPAIR_SCOPE",
        (not official_ledger and not official_pilot_overlap)
        or official_pilot_overlap == expected_official_pilot_repairs,
        (
            "retrieval_pending; overlap=0"
            if not official_ledger
            else (
                f"overlap={len(official_pilot_overlap)} "
                f"expected_repairs={len(expected_official_pilot_repairs)}"
            )
        ),
    )

    check(
        "PROTECTED_EVIDENCE_UNCHANGED",
        all(item["status"] == "PASS" for item in checks if item["check"] in {"EXTRACTION_CHECKSUMS", "SOURCE_RECORD_REFERENCES"}),
        "Frozen extraction and Source Record checksums are unchanged.",
    )
    effective_terminal_by_source: dict[str, dict[str, Any]] = {}
    for item in ledger + expansion_ledger + hnn_ledger + official_ledger:
        effective_terminal_by_source[item["source_id"]] = item
    all_terminal_ledger = [
        effective_terminal_by_source[source_id] for source_id in sorted(effective_terminal_by_source)
    ]
    declared_output_paths = [
        item.get(key)
        for item in all_terminal_ledger
        for key in ("body_path", "provenance_path")
        if item.get(key)
    ]
    check(
        "OUTPUT_SCOPE",
        all(
            path.startswith("archive/raw/legacy-written-recovery/")
            if key == "body_path"
            else path.startswith("archive/provenance/legacy-written-recovery/")
            for item in all_terminal_ledger
            for key in ("body_path", "provenance_path")
            for path in (item.get(key),)
            if path
        ),
        "Every declared raw and provenance output remains under its approved repository layer.",
    )
    declared_artifact_paths = set(declared_output_paths)
    actual_artifact_paths = {
        relative(path)
        for root in (RAW_ROOT, PROVENANCE_ROOT)
        if root.exists()
        for path in root.rglob("*")
        if path.is_file()
    }
    check(
        "NO_ORPHAN_RAW_OR_PROVENANCE",
        actual_artifact_paths == declared_artifact_paths,
        f"declared={len(declared_artifact_paths)} actual={len(actual_artifact_paths)}",
    )
    expected_archive_manifest = build_archive_manifest()
    actual_archive_manifest = read_json(ARCHIVE_MANIFEST) if ARCHIVE_MANIFEST.exists() else None
    check(
        "ARCHIVE_MANIFEST_RECONCILES",
        actual_archive_manifest == expected_archive_manifest,
        f"artifact_count={expected_archive_manifest['artifact_count']}",
    )
    allowed_dispositions = CAPTURED_DISPOSITIONS | {
        "NOT_FOUND_EXHAUSTED", "AMBIGUOUS_MANUAL_REVIEW", "BLOCKED_ACCESS_OR_POLICY"
    }
    check(
        "CONTROLLED_TERMINAL_DISPOSITIONS",
        all(item.get("terminal_disposition") in allowed_dispositions for item in all_terminal_ledger),
        "Every terminal record uses the frozen Phase 2 disposition vocabulary.",
    )
    summary = read_json(CAMPAIGN_SUMMARY_JSON)
    check(
        "CAMPAIGN_SUMMARY_RECONCILES",
        summary.get("urls_attempted") == len(all_terminal_ledger)
        and summary.get("urls_retrieved") == sum(bool(item.get("body_path")) for item in all_terminal_ledger)
        and summary.get("distinct_records_attempted")
        == len({item.get("source_id") for item in all_terminal_ledger}),
        f"terminal_records={len(all_terminal_ledger)}",
    )
    check(
        "PROTECTED_LAYERS_ABSENT_FROM_OUTPUTS",
        all(
            not path.startswith(("archive/normalized/", "archive/source-records/", "archive/semantic/", "knowledge/", "graph/", "publication/"))
            for path in declared_output_paths
        ),
        "No declared output enters a protected evidence, knowledge, graph, or publication layer.",
    )

    passed = all(item["status"] == "PASS" for item in checks)
    report = {
        "campaign_id": CAMPAIGN_ID,
        "checks": checks,
        "failed_checks": [item["check"] for item in checks if item["status"] == "FAIL"],
        "passed_checks": sum(item["status"] == "PASS" for item in checks),
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if passed else "FAIL",
        "total_checks": len(checks),
    }
    write_json(VALIDATION_REPORT_JSON, report)
    write_archive_manifest()
    lines = [
        "# Legacy Written Raw Recovery Validation",
        "",
        f"Status: **{report['status']}**",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| {item['check']} | {item['status']} | {item['detail'].replace('|', '/')} |"
        for item in checks
    )
    VALIDATION_REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Validation {report['status']}: {report['passed_checks']}/{report['total_checks']} checks passed.")
    return passed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("freeze", help="Freeze the 800-record Alpha–Delta extraction inventory.")
    retrieve_parser = subcommands.add_parser("retrieve", help="Retrieve exact public HTTP response bytes.")
    selection = retrieve_parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--pilot", action="store_true", help="Retrieve only the approved 20-record pilot.")
    selection.add_argument(
        "--batch",
        choices=[EXPANSION_BATCH_ID, HNN_BATCH_ID, OFFICIAL_BATCH_ID],
        help="Retrieve one explicitly authorized fixed expansion batch.",
    )
    retrieve_parser.add_argument("--retry-failures", action="store_true", help="Explicitly retry prior terminal access/failure records.")
    subcommands.add_parser("validate", help="Validate the frozen inventory and all captured recovery batches.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "freeze":
            freeze()
        elif args.command == "retrieve":
            if args.pilot:
                retrieve_pilot(args.retry_failures)
            elif args.batch == EXPANSION_BATCH_ID:
                retrieve_expansion(args.retry_failures)
            elif args.batch == HNN_BATCH_ID:
                retrieve_hnn_completion(args.retry_failures)
            elif args.batch == OFFICIAL_BATCH_ID:
                retrieve_official_completion(args.retry_failures)
        elif args.command == "validate":
            return 0 if validate() else 1
    except (RuntimeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
