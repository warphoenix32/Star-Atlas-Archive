#!/usr/bin/env python3
"""Freeze, retrieve, and validate legacy written-source raw evidence.

This campaign is intentionally narrow. It reads the 800 successful extraction
records promoted by Campaigns Alpha through Delta, but it never rewrites those
extractions or their Source Records. The pilot retrieves only an approved set
of 20 records and stores the exact public HTTP response bytes plus provenance.
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
RETRIEVAL_LEDGER = CAMPAIGN_DIR / "retrieval-ledger.jsonl"
RETRY_LEDGER = CAMPAIGN_DIR / "retry-ledger.jsonl"
MANUAL_REVIEW_QUEUE = CAMPAIGN_DIR / "manual-review-queue.jsonl"
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


def freeze() -> None:
    manifest = build_frozen_manifest()
    write_json(FROZEN_MANIFEST, manifest)
    write_archive_manifest()
    print(
        f"Frozen {manifest['frozen_record_count']} records; "
        f"approved pilot contains {manifest['pilot_record_count']} records."
    )


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[dict[str, Any]] = []

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        self.chain.append({"from": req.full_url, "http_status": code, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


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
    if record["source_id"] == "SRC-OFF-076F496F0A6CA989" and "raw.githubusercontent.com/staratlasmeta/factory/" in final_url:
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
    api_url = "https://api.github.com/repos/staratlasmeta/factory/commits?path=README.md&per_page=1"
    request = urllib.request.Request(
        api_url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
    )
    with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, list) or not payload or not isinstance(payload[0].get("sha"), str):
        raise ValueError("GITHUB_COMMIT_SHA_NOT_RESOLVED")
    git_sha = payload[0]["sha"]
    return f"https://raw.githubusercontent.com/staratlasmeta/factory/{git_sha}/README.md", git_sha


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
    markers = ("cf-chl-", "just a moment...", "captcha", "verify you are human")
    return any(marker in sample for marker in markers)


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
    return provenance


def ledger_from_provenance(record: dict[str, Any], provenance: dict[str, Any], checkpoint: bool) -> dict[str, Any]:
    return {
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


def build_archive_manifest() -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = []
    for root in (RAW_ROOT, PROVENANCE_ROOT):
        if not root.exists():
            continue
        for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: relative(item)):
            data = path.read_bytes()
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
        "frozen_manifest_path": relative(FROZEN_MANIFEST),
        "frozen_manifest_sha256": sha256_bytes(FROZEN_MANIFEST.read_bytes()) if FROZEN_MANIFEST.exists() else None,
        "pilot_record_count": len(PILOT_SOURCE_IDS),
        "pilot_selection_path": relative(PILOT_SELECTION),
        "pilot_selection_sha256": sha256_bytes(PILOT_SELECTION.read_bytes()) if PILOT_SELECTION.exists() else None,
        "schema_version": SCHEMA_VERSION,
    }


def write_archive_manifest() -> None:
    write_json(ARCHIVE_MANIFEST, build_archive_manifest())


def retrieve_record(record: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
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
        if record["source_id"] == "SRC-OFF-076F496F0A6CA989":
            retrieval_url, git_sha = github_immutable_target(record, opener)
        request = urllib.request.Request(
            retrieval_url,
            headers={"Accept": "text/html,application/json,application/xhtml+xml;q=0.9,*/*;q=0.5", "User-Agent": USER_AGENT},
        )
        try:
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
                "redirect_chain": redirects.chain,
                "retrieval_tier": retrieval_tier,
                "response": {
                    "content_type": content_type,
                    "final_url": final_url,
                    "headers": headers,
                    "http_status": http_status,
                    "redirect_chain": redirects.chain,
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


def write_summary(ledger: list[dict[str, Any]]) -> None:
    dispositions = Counter(item["terminal_disposition"] for item in ledger)
    identity = Counter(item["identity_status"] for item in ledger)
    manual = [item for item in ledger if item["manual_review_required"]]
    preserved = [item for item in ledger if item.get("body_path")]
    captured = [item for item in ledger if item["terminal_disposition"] in CAPTURED_DISPOSITIONS]
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "frozen_records": 800,
        "identity_status_counts": dict(sorted(identity.items())),
        "manual_review_count": len(manual),
        "pilot_records": len(PILOT_SOURCE_IDS),
        "raw_bodies_preserved": len(preserved),
        "schema_version": SCHEMA_VERSION,
        "status": "PILOT_COMPLETE" if len(ledger) == len(PILOT_SOURCE_IDS) and len(captured) == len(ledger) else "PILOT_COMPLETE_WITH_EXCEPTIONS",
        "terminal_disposition_counts": dict(sorted(dispositions.items())),
        "urls_attempted": len(ledger),
        "urls_retrieved": len(preserved),
    }
    write_json(CAMPAIGN_SUMMARY_JSON, summary)
    lines = [
        "# Legacy Written Raw Recovery — Pilot Summary",
        "",
        f"- Frozen records: {summary['frozen_records']}",
        f"- Pilot records: {summary['pilot_records']}",
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
    CAMPAIGN_SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def retrieve_pilot(retry_failures: bool = False) -> None:
    if not FROZEN_MANIFEST.exists():
        raise RuntimeError("Run `freeze` before retrieval.")
    manifest = read_json(FROZEN_MANIFEST)
    records_by_id = {record["source_id"]: record for record in manifest["records"]}
    existing_ledger = {item["source_id"]: item for item in read_jsonl(RETRIEVAL_LEDGER)}
    existing_attempts: dict[str, list[dict[str, Any]]] = {}
    for attempt in read_jsonl(RETRY_LEDGER):
        existing_attempts.setdefault(attempt["source_id"], []).append(attempt)
    ledger: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    blocked_hosts: dict[str, str] = {}
    for source_id in PILOT_SOURCE_IDS:
        record = records_by_id[source_id]
        previous = existing_ledger.get(source_id)
        checkpoint = verified_checkpoint(record)
        if previous and ((previous.get("body_path") and checkpoint) or (not previous.get("body_path") and not retry_failures)):
            ledger.append(previous)
            attempts.extend(existing_attempts.get(source_id, []))
            print(f"Reusing terminal checkpoint {source_id}: {previous['terminal_disposition']}", flush=True)
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
        item, item_attempts = retrieve_record(record)
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
    ledger.sort(key=lambda item: item["source_id"])
    attempts.sort(key=lambda item: (item["source_id"], item["attempt"]))
    manual = [item for item in ledger if item["manual_review_required"]]
    write_jsonl(RETRIEVAL_LEDGER, ledger)
    write_jsonl(RETRY_LEDGER, attempts)
    write_jsonl(MANUAL_REVIEW_QUEUE, manual)
    write_summary(ledger)
    write_archive_manifest()


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

    check(
        "PROTECTED_EVIDENCE_UNCHANGED",
        all(item["status"] == "PASS" for item in checks if item["check"] in {"EXTRACTION_CHECKSUMS", "SOURCE_RECORD_REFERENCES"}),
        "Frozen extraction and Source Record checksums are unchanged.",
    )
    declared_output_paths = [
        item.get(key)
        for item in ledger
        for key in ("body_path", "provenance_path")
        if item.get(key)
    ]
    check(
        "OUTPUT_SCOPE",
        all(
            path.startswith("archive/raw/legacy-written-recovery/")
            if key == "body_path"
            else path.startswith("archive/provenance/legacy-written-recovery/")
            for item in ledger
            for key in ("body_path", "provenance_path")
            for path in (item.get(key),)
            if path
        ),
        "Every declared raw and provenance output remains under its approved repository layer.",
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
        all(item.get("terminal_disposition") in allowed_dispositions for item in ledger),
        "Every pilot record uses the frozen Phase 2 disposition vocabulary.",
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
    retrieve_parser.add_argument("--pilot", action="store_true", help="Retrieve only the approved 20-record pilot.")
    retrieve_parser.add_argument("--retry-failures", action="store_true", help="Explicitly retry prior terminal access/failure records.")
    subcommands.add_parser("validate", help="Validate the frozen inventory and any captured pilot artifacts.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "freeze":
            freeze()
        elif args.command == "retrieve":
            if not args.pilot:
                raise RuntimeError("Full-corpus retrieval is not authorized. Use `retrieve --pilot`.")
            retrieve_pilot(args.retry_failures)
        elif args.command == "validate":
            return 0 if validate() else 1
    except (RuntimeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
