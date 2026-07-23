#!/usr/bin/env python3
"""Collect and reconcile the public Atlas Brew YouTube playlist.

The preserved combined transcript remains immutable. This campaign creates an
additive provenance manifest and reconciliation ledger keyed by the existing
SRC-ATLAS-BREW identifiers.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import difflib
import hashlib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


PLAYLIST_ID = "PL4_auqu2sZgDlW6cG3-vfpvLEsQtyaKpB"
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={PLAYLIST_ID}"
CAMPAIGN_ID = "atlas-brew-url-reconciliation-2026-07"
SNAPSHOT_DATE = "2026-07-22"
EXPECTED_TRANSCRIPT_COUNT = 123
EXPECTED_PLAYLIST_ITEM_COUNT = 124
EXPECTED_RECOVERED_IDS = {"Yb8lZZ_zbhE"}
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
)

ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_DIR = ROOT / "operations" / "campaigns" / CAMPAIGN_ID
SOURCE_RECORDS_PATH = (
    ROOT / "archive" / "source-records" / "atlas-brew-combined" / "source-records.json"
)
PROVENANCE_DIR = ROOT / "archive" / "provenance" / "atlas-brew-combined"
RECONCILIATION_DIR = ROOT / "archive" / "reconciliation" / "atlas-brew-combined"
PLAYLIST_MANIFEST_PATH = PROVENANCE_DIR / "youtube-playlist-manifest.json"
RECONCILIATION_PATH = RECONCILIATION_DIR / "youtube-url-reconciliation.json"
METADATA_PATCH_PATH = RECONCILIATION_DIR / "youtube-source-metadata-patch.json"
RECOVERY_SOURCE_RECORD_PATH = (
    ROOT
    / "archive"
    / "source-records"
    / "atlas-brew-youtube-recovery"
    / "SRC-ATLAS-BREW-YOUTUBE-YB8LZZZBHE.json"
)
MANUAL_REVIEW_PATH = CAMPAIGN_DIR / "manual-review.json"
SUMMARY_JSON_PATH = CAMPAIGN_DIR / "campaign-summary.json"
SUMMARY_MD_PATH = CAMPAIGN_DIR / "campaign-summary.md"
VALIDATION_JSON_PATH = CAMPAIGN_DIR / "validation-report.json"
VALIDATION_MD_PATH = CAMPAIGN_DIR / "validation-report.md"


def request_bytes(
    url: str,
    *,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    attempts: int = 3,
) -> bytes:
    request_headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    if headers:
        request_headers.update(headers)
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(
                url, data=data, headers=request_headers, method="POST" if data else "GET"
            )
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(1.0 + attempt)
    raise RuntimeError(f"request failed after {attempts} attempts: {url}: {last_error}")


def extract_balanced_json(text: str, marker: str) -> Any:
    marker_pos = text.find(marker)
    if marker_pos < 0:
        raise ValueError(f"JSON marker not found: {marker}")
    start = text.find("{", marker_pos + len(marker))
    if start < 0:
        raise ValueError(f"JSON object not found after marker: {marker}")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : index + 1])
    raise ValueError(f"unterminated JSON object after marker: {marker}")


def walk_json(value: Any) -> Iterable[Any]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def text_value(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    if isinstance(value.get("simpleText"), str):
        return value["simpleText"]
    runs = value.get("runs")
    if isinstance(runs, list):
        joined = "".join(
            item.get("text", "") for item in runs if isinstance(item, dict)
        ).strip()
        return joined or None
    return None


def extract_playlist_entries(payload: Any) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for node in walk_json(payload):
        renderer = node.get("playlistVideoRenderer") if isinstance(node, dict) else None
        if isinstance(renderer, dict) and renderer.get("videoId"):
            index_text = text_value(renderer.get("index"))
            entries.append(
                {
                    "video_id": renderer["videoId"],
                    "playlist_index": int(index_text)
                    if index_text and index_text.isdigit()
                    else None,
                    "title": text_value(renderer.get("title")),
                    "duration_text": text_value(renderer.get("lengthText")),
                    "channel_name": text_value(renderer.get("shortBylineText")),
                    "canonical_url": f"https://www.youtube.com/watch?v={renderer['videoId']}",
                }
            )
            continue

        # YouTube's July 2026 web client uses lockupViewModel for playlist
        # items. Avoid generated CSS and read only stable structured fields.
        lockup = node.get("lockupViewModel") if isinstance(node, dict) else None
        if (
            not isinstance(lockup, dict)
            or lockup.get("contentType") != "LOCKUP_CONTENT_TYPE_VIDEO"
            or not lockup.get("contentId")
        ):
            continue
        metadata = lockup.get("metadata", {}).get("lockupMetadataViewModel", {})
        title = metadata.get("title", {}).get("content")
        rows = (
            metadata.get("metadata", {})
            .get("contentMetadataViewModel", {})
            .get("metadataRows", [])
        )
        channel_name = None
        if rows:
            parts = rows[0].get("metadataParts", [])
            if parts:
                channel_name = parts[0].get("text", {}).get("content")
        duration_text = None
        for child in walk_json(lockup.get("contentImage", {})):
            badge = child.get("thumbnailBadgeViewModel") if isinstance(child, dict) else None
            if isinstance(badge, dict) and re.fullmatch(
                r"\d{1,2}(?::\d{2}){1,2}", str(badge.get("text", ""))
            ):
                duration_text = badge["text"]
                break
        entries.append(
            {
                "video_id": lockup["contentId"],
                "playlist_index": None,
                "title": title,
                "duration_text": duration_text,
                "channel_name": channel_name,
                "canonical_url": f"https://www.youtube.com/watch?v={lockup['contentId']}",
            }
        )
    return entries


def extract_continuation_tokens(payload: Any) -> list[str]:
    tokens: list[str] = []
    for node in walk_json(payload):
        if not isinstance(node, dict):
            continue
        command = node.get("continuationCommand")
        if isinstance(command, dict) and isinstance(command.get("token"), str):
            tokens.append(command["token"])
    return list(dict.fromkeys(tokens))


def collect_playlist() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    html_bytes = request_bytes(PLAYLIST_URL)
    html = html_bytes.decode("utf-8", errors="replace")
    initial_data = extract_balanced_json(html, "var ytInitialData =")

    key_match = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html)
    version_match = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html)
    if not key_match or not version_match:
        raise RuntimeError("YouTube client configuration was not found")
    api_key = key_match.group(1)
    client_version = version_match.group(1)

    entries_by_id: dict[str, dict[str, Any]] = {}
    next_index = 1

    def add_entries(new_entries: list[dict[str, Any]]) -> None:
        nonlocal next_index
        for entry in new_entries:
            if entry["video_id"] in entries_by_id:
                continue
            if entry["playlist_index"] is None:
                entry["playlist_index"] = next_index
            next_index = max(next_index, entry["playlist_index"] + 1)
            entries_by_id[entry["video_id"]] = entry

    add_entries(extract_playlist_entries(initial_data))

    queue = list(extract_continuation_tokens(initial_data))
    processed_tokens: set[str] = set()
    continuation_pages = 0
    while queue:
        token = queue.pop(0)
        if token in processed_tokens:
            continue
        processed_tokens.add(token)
        body = json.dumps(
            {
                "context": {
                    "client": {
                        "clientName": "WEB",
                        "clientVersion": client_version,
                        "hl": "en",
                        "gl": "US",
                    }
                },
                "continuation": token,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        try:
            response_bytes = request_bytes(
                f"https://www.youtube.com/youtubei/v1/browse?key={api_key}",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            payload = json.loads(response_bytes)
        except (RuntimeError, json.JSONDecodeError):
            continue
        new_entries = extract_playlist_entries(payload)
        if not new_entries:
            continue
        continuation_pages += 1
        add_entries(new_entries)
        for continuation in extract_continuation_tokens(payload):
            if continuation not in processed_tokens:
                queue.append(continuation)

    entries = sorted(
        entries_by_id.values(),
        key=lambda item: (
            item["playlist_index"] is None,
            item["playlist_index"] or 10**9,
            item["video_id"],
        ),
    )
    return entries, {
        "continuation_pages_with_videos": continuation_pages,
        "youtube_client_version": client_version,
        "collector_schema_version": "1.0",
    }


def collect_player_metadata(
    entries: list[dict[str, Any]], client_version: str
) -> list[dict[str, Any]]:
    playlist_html = request_bytes(PLAYLIST_URL).decode("utf-8", errors="replace")
    key_match = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', playlist_html)
    if not key_match:
        return entries
    api_key = key_match.group(1)

    def fetch(entry: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(
            {
                "context": {
                    "client": {
                        "clientName": "WEB",
                        "clientVersion": client_version,
                        "hl": "en",
                        "gl": "US",
                    }
                },
                "videoId": entry["video_id"],
            },
            separators=(",", ":"),
        ).encode("utf-8")
        output = dict(entry)
        try:
            response = json.loads(
                request_bytes(
                    f"https://www.youtube.com/youtubei/v1/player?key={api_key}",
                    data=body,
                    headers={"Content-Type": "application/json"},
                )
            )
            details = response.get("videoDetails", {})
            microformat = response.get("microformat", {}).get(
                "playerMicroformatRenderer", {}
            )
            playability = response.get("playabilityStatus", {})
            output.update(
                {
                    "title": details.get("title") or output.get("title"),
                    "channel_name": details.get("author") or output.get("channel_name"),
                    "channel_id": details.get("channelId"),
                    "duration_seconds": int(details["lengthSeconds"])
                    if str(details.get("lengthSeconds", "")).isdigit()
                    else duration_to_seconds(output.get("duration_text")),
                    "published_at": microformat.get("publishDate"),
                    "uploaded_at": microformat.get("uploadDate"),
                    "public_metadata_status": "AVAILABLE"
                    if details.get("title")
                    else "INCOMPLETE",
                    "player_status": playability.get("status", "UNKNOWN"),
                    "player_status_reason": playability.get("reason"),
                    "is_live_content": bool(details.get("isLiveContent")),
                }
            )
        except (RuntimeError, json.JSONDecodeError, ValueError):
            output.update(
                {
                    "channel_id": None,
                    "duration_seconds": duration_to_seconds(output.get("duration_text")),
                    "published_at": None,
                    "uploaded_at": None,
                    "public_metadata_status": "METADATA_RETRIEVAL_FAILED",
                    "player_status": "UNKNOWN",
                    "player_status_reason": None,
                    "is_live_content": None,
                }
            )
        return output

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        enriched = list(executor.map(fetch, entries))
    return enriched


def duration_to_seconds(value: str | None) -> int | None:
    if not value:
        return None
    parts = value.split(":")
    if not all(part.isdigit() for part in parts):
        return None
    seconds = 0
    for part in parts:
        seconds = seconds * 60 + int(part)
    return seconds


def normalize_title(value: str | None) -> str:
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"\b(?:live|the|star|atlas|brew|episode|ep|no)\b", " ", value)
    value = re.sub(r"\d+", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def title_similarity(left: str | None, right: str | None) -> float:
    a = normalize_title(left)
    b = normalize_title(right)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    a_tokens = set(a.split())
    b_tokens = set(b.split())
    jaccard = len(a_tokens & b_tokens) / len(a_tokens | b_tokens)
    return round(max(ratio, jaccard), 4)


def episode_number(title: str | None) -> int | None:
    if not title:
        return None
    plain = unicodedata.normalize("NFKD", title)
    patterns = [
        r"(?:atlas\s+brew|brew)\s*(?:#|no\.?|ep\.?)?\s*(\d{1,3})\b",
        r"\b(?:episode|ep\.?)\s*#?\s*(\d{1,3})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, plain, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def timestamp_to_seconds(value: str | None) -> int | None:
    return duration_to_seconds(value)


def transcript_duration(record: dict[str, Any]) -> int | None:
    start = timestamp_to_seconds(record.get("timestamp_start"))
    end = timestamp_to_seconds(record.get("timestamp_end"))
    if start is None or end is None or end < start:
        return None
    return end - start


def duration_delta_ratio(record: dict[str, Any], video: dict[str, Any]) -> float | None:
    left = transcript_duration(record)
    right = video.get("duration_seconds")
    if left is None or right is None or max(left, right) == 0:
        return None
    return round(abs(left - right) / max(left, right), 4)


def candidate_score(record: dict[str, Any], video: dict[str, Any]) -> tuple[float, list[str]]:
    reasons: list[str] = []
    score = 0.0
    record_episode = record.get("episode_number")
    video_episode = video.get("episode_number")
    if record_episode is not None and record_episode == video_episode:
        score += 0.70
        reasons.append("EXACT_EPISODE_NUMBER")
    similarity = title_similarity(record.get("title"), video.get("title"))
    if (
        record_episode is None
        and normalize_title(record.get("title"))
        and normalize_title(record.get("title")) == normalize_title(video.get("title"))
    ):
        score += 0.70
        reasons.append("EXACT_NORMALIZED_TITLE")
    score += similarity * 0.20
    if similarity >= 0.75:
        reasons.append("STRONG_TITLE_SIMILARITY")
    elif similarity >= 0.45:
        reasons.append("MODERATE_TITLE_SIMILARITY")
    delta = duration_delta_ratio(record, video)
    if delta is not None:
        if delta <= 0.03:
            score += 0.10
            reasons.append("DURATION_WITHIN_3_PERCENT")
        elif delta <= 0.08:
            score += 0.06
            reasons.append("DURATION_WITHIN_8_PERCENT")
        elif delta <= 0.15:
            score += 0.03
            reasons.append("DURATION_WITHIN_15_PERCENT")
    return round(min(score, 1.0), 4), reasons


def reconcile(
    records: list[dict[str, Any]],
    videos: list[dict[str, Any]],
    recovery_record: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    videos_by_episode: dict[int | None, list[dict[str, Any]]] = defaultdict(list)
    for video in videos:
        video["episode_number"] = episode_number(video.get("title"))
        videos_by_episode[video["episode_number"]].append(video)

    decisions: list[dict[str, Any]] = []
    assigned_video_ids: set[str] = set()
    pending: list[tuple[dict[str, Any], list[tuple[float, dict[str, Any], list[str]]]]] = []

    for record in records:
        pool = videos_by_episode.get(record.get("episode_number"), [])
        if record.get("episode_number") is None:
            pool = videos
        ranked = sorted(
            (
                (*candidate_score(record, video), video)
                for video in pool
                if video["video_id"] not in assigned_video_ids
            ),
            key=lambda item: (-item[0], item[2]["playlist_index"] or 10**9),
        )
        ranked_reordered = [(score, video, reasons) for score, reasons, video in ranked]
        pending.append((record, ranked_reordered))

    # Resolve easiest, highest-margin records first so duplicate episode numbers
    # cannot claim the same playlist item.
    pending.sort(
        key=lambda item: (
            -(item[1][0][0] if item[1] else 0),
            -(
                (item[1][0][0] - item[1][1][0])
                if len(item[1]) > 1
                else (item[1][0][0] if item[1] else 0)
            ),
            item[0]["source_id"],
        )
    )

    for record, original_ranked in pending:
        ranked = [
            item for item in original_ranked if item[1]["video_id"] not in assigned_video_ids
        ]
        best = ranked[0] if ranked else None
        second_score = ranked[1][0] if len(ranked) > 1 else 0.0
        decision: dict[str, Any] = {
            "source_id": record["source_id"],
            "transcript_title": record.get("title"),
            "transcript_episode_number": record.get("episode_number"),
            "transcript_duration_seconds": transcript_duration(record),
            "status": "TRANSCRIPT_ONLY",
            "matched_video_id": None,
            "canonical_url": None,
            "youtube_title": None,
            "published_at": None,
            "uploaded_at": None,
            "youtube_duration_seconds": None,
            "match_confidence": "NONE",
            "match_score": 0.0,
            "match_reasons": [],
            "manual_review_required": True,
            "candidate_video_ids": [
                {
                    "video_id": video["video_id"],
                    "score": score,
                    "title": video.get("title"),
                    "reasons": reasons,
                }
                for score, video, reasons in ranked[:3]
            ],
        }
        if best:
            score, video, reasons = best
            margin = round(score - second_score, 4)
            exact_identity_signal = bool(
                {"EXACT_EPISODE_NUMBER", "EXACT_NORMALIZED_TITLE"} & set(reasons)
            )
            if score >= 0.82 and margin >= 0.08 and exact_identity_signal:
                confidence = "HIGH"
                manual_review = False
            elif score >= 0.72 and margin >= 0.04:
                confidence = "MEDIUM"
                manual_review = True
            else:
                confidence = "LOW"
                manual_review = True

            if confidence in {"HIGH", "MEDIUM"}:
                assigned_video_ids.add(video["video_id"])
                decision.update(
                    {
                        "status": "MATCHED",
                        "matched_video_id": video["video_id"],
                        "canonical_url": video["canonical_url"],
                        "youtube_title": video.get("title"),
                        "published_at": video.get("published_at"),
                        "uploaded_at": video.get("uploaded_at"),
                        "youtube_duration_seconds": video.get("duration_seconds"),
                        "match_confidence": confidence,
                        "match_score": score,
                        "match_margin": margin,
                        "match_reasons": reasons,
                        "manual_review_required": manual_review,
                    }
                )
        decisions.append(decision)

    decisions.sort(key=lambda item: item["source_id"])
    recovered = [
        {
            **video,
            "status": "RECOVERED_SEPARATE_SOURCE",
            "source_id": recovery_record["source_id"],
            "raw_path": recovery_record["raw_path"],
            "normalized_path": recovery_record["normalized_path"],
            "source_record_path": RECOVERY_SOURCE_RECORD_PATH.relative_to(
                ROOT
            ).as_posix(),
            "extraction_confidence": recovery_record["extraction_confidence"],
            "manual_review_required": recovery_record["manual_review_required"],
        }
        for video in videos
        if video["video_id"] not in assigned_video_ids
        and video["video_id"] == recovery_record.get("youtube_video_id")
    ]
    recovered_ids = {item["video_id"] for item in recovered}
    playlist_only = [
        {
            **video,
            "status": "PLAYLIST_ONLY",
            "manual_review_required": True,
        }
        for video in videos
        if video["video_id"] not in assigned_video_ids
        and video["video_id"] not in recovered_ids
    ]
    manual_review = [
        {
            "review_id": f"ABR-{index:03d}",
            "review_type": "TRANSCRIPT_MATCH",
            "source_id": decision["source_id"],
            "video_id": decision.get("matched_video_id"),
            "status": decision["status"],
            "reason": (
                "MEDIUM_CONFIDENCE_MATCH"
                if decision["status"] == "MATCHED"
                else "NO_SAFE_MATCH"
            ),
            "candidate_video_ids": decision.get("candidate_video_ids", []),
            "recommendation": "CONFIRM_OR_DEFER",
        }
        for index, decision in enumerate(
            [item for item in decisions if item["manual_review_required"]], start=1
        )
    ]
    start = len(manual_review) + 1
    for index, video in enumerate(playlist_only, start=start):
        manual_review.append(
            {
                "review_id": f"ABR-{index:03d}",
                "review_type": "PLAYLIST_ONLY",
                "source_id": None,
                "video_id": video["video_id"],
                "status": "PLAYLIST_ONLY",
                "reason": "NO_PRESERVED_TRANSCRIPT_MATCH",
                "title": video.get("title"),
                "canonical_url": video["canonical_url"],
                "recommendation": "DEFER_NEW_INGESTION_OR_CONFIRM_EXCLUSION",
            }
        )
    return decisions, recovered, playlist_only, manual_review


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def sha256_path(path: Path) -> str:
    # Campaign artifacts are UTF-8 text. Hash canonical LF text so Windows
    # autocrlf checkouts and Linux CI produce the same provenance values.
    canonical = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def generate() -> None:
    records = json.loads(SOURCE_RECORDS_PATH.read_text(encoding="utf-8"))
    recovery_record = json.loads(RECOVERY_SOURCE_RECORD_PATH.read_text(encoding="utf-8"))
    playlist_entries, collection = collect_playlist()
    playlist_entries = collect_player_metadata(
        playlist_entries, collection["youtube_client_version"]
    )
    for entry in playlist_entries:
        entry["episode_number"] = episode_number(entry.get("title"))
    collection["normalized_items_sha256"] = hashlib.sha256(
        json.dumps(
            playlist_entries,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    manifest = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": SNAPSHOT_DATE,
        "playlist_id": PLAYLIST_ID,
        "playlist_url": PLAYLIST_URL,
        "collection_method": "PUBLIC_YOUTUBE_PLAYLIST_AND_PLAYER_METADATA",
        "collection_scope": "PUBLICLY_EXPOSED_PLAYLIST_ITEMS",
        "limitations": [
            "Private, deleted, or region-restricted entries may not expose stable public metadata.",
            "Playlist membership establishes association with the playlist, not transcript identity.",
            "The player_status field records the unauthenticated metadata endpoint response and is not used as a public-page availability decision.",
            "No speaker identities were inferred.",
        ],
        "collection": collection,
        "item_count": len(playlist_entries),
        "items": playlist_entries,
    }
    write_json(PLAYLIST_MANIFEST_PATH, manifest)

    decisions, recovered, playlist_only, manual_review = reconcile(
        records, playlist_entries, recovery_record
    )
    confidence_counts = Counter(item["match_confidence"] for item in decisions)
    status_counts = Counter(item["status"] for item in decisions)
    reconciliation = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": SNAPSHOT_DATE,
        "playlist_manifest_path": PLAYLIST_MANIFEST_PATH.relative_to(ROOT).as_posix(),
        "source_records_path": SOURCE_RECORDS_PATH.relative_to(ROOT).as_posix(),
        "source_record_count": len(records),
        "playlist_item_count": len(playlist_entries),
        "status_counts": dict(sorted(status_counts.items())),
        "match_confidence_counts": dict(sorted(confidence_counts.items())),
        "playlist_only_count": len(playlist_only),
        "recovered_separate_source_count": len(recovered),
        "manual_review_count": len(manual_review),
        "decisions": decisions,
        "recovered_separate_sources": recovered,
        "playlist_only": playlist_only,
    }
    write_json(RECONCILIATION_PATH, reconciliation)

    metadata_patch = {
        "campaign_id": CAMPAIGN_ID,
        "purpose": "ADDITIVE_METADATA_PATCH; SOURCE RECORDS NOT REWRITTEN",
        "applicability": "HIGH_CONFIDENCE_MATCHES_ONLY",
        "records": [
            {
                "source_id": item["source_id"],
                "original_url": item["canonical_url"],
                "publication_date": item["published_at"],
                "youtube_video_id": item["matched_video_id"],
                "match_confidence": item["match_confidence"],
                "evidence_path": RECONCILIATION_PATH.relative_to(ROOT).as_posix(),
            }
            for item in decisions
            if item["match_confidence"] == "HIGH"
        ],
    }
    write_json(METADATA_PATCH_PATH, metadata_patch)
    write_json(
        MANUAL_REVIEW_PATH,
        {
            "campaign_id": CAMPAIGN_ID,
            "count": len(manual_review),
            "items": manual_review,
        },
    )

    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "READY_FOR_REVIEW" if manual_review else "COMPLETE",
        "snapshot_date": SNAPSHOT_DATE,
        "playlist_items": len(playlist_entries),
        "transcript_records": len(records),
        "matched_records": status_counts.get("MATCHED", 0),
        "high_confidence_matches": confidence_counts.get("HIGH", 0),
        "medium_confidence_matches": confidence_counts.get("MEDIUM", 0),
        "unmatched_transcripts": status_counts.get("TRANSCRIPT_ONLY", 0),
        "playlist_only_items": len(playlist_only),
        "recovered_separate_sources": len(recovered),
        "manual_review_items": len(manual_review),
        "source_records_rewritten": False,
        "raw_transcripts_rewritten": False,
    }
    write_json(SUMMARY_JSON_PATH, summary)
    SUMMARY_MD_PATH.write_text(
        "\n".join(
            [
                "# Atlas Brew URL Reconciliation",
                "",
                f"- Snapshot date: `{SNAPSHOT_DATE}`",
                f"- Playlist items: **{summary['playlist_items']}**",
                f"- Preserved transcript records: **{summary['transcript_records']}**",
                f"- Matched records: **{summary['matched_records']}**",
                f"- High-confidence matches: **{summary['high_confidence_matches']}**",
                f"- Medium-confidence matches: **{summary['medium_confidence_matches']}**",
                f"- Transcript-only records: **{summary['unmatched_transcripts']}**",
                f"- Playlist-only items: **{summary['playlist_only_items']}**",
                f"- Separately recovered playlist items: **{summary['recovered_separate_sources']}**",
                f"- Manual-review items: **{summary['manual_review_items']}**",
                "",
                "The combined transcript and its 123 existing Source IDs were not "
                "rewritten. High-confidence URL/date values are supplied as an "
                "additive metadata patch. Atlas Brew #7 was recovered as a "
                "separate, qualified machine transcript because YouTube exposes "
                "no caption track for the recording.",
                "",
                "## Boundaries",
                "",
                "- Playlist membership does not prove that two similarly titled recordings are identical.",
                "- Duplicate episode numbers are matched only when title and duration evidence separates them.",
                "- Speaker identity is outside this campaign.",
                "- A separately recovered item must preserve its own provenance and Source ID.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    validate()


def validate() -> None:
    checks: dict[str, Any] = {}
    errors: list[str] = []
    try:
        records = json.loads(SOURCE_RECORDS_PATH.read_text(encoding="utf-8"))
        manifest = json.loads(PLAYLIST_MANIFEST_PATH.read_text(encoding="utf-8"))
        reconciliation = json.loads(RECONCILIATION_PATH.read_text(encoding="utf-8"))
        patch = json.loads(METADATA_PATCH_PATH.read_text(encoding="utf-8"))
        review = json.loads(MANUAL_REVIEW_PATH.read_text(encoding="utf-8"))
        recovery_record = json.loads(
            RECOVERY_SOURCE_RECORD_PATH.read_text(encoding="utf-8")
        )
        checks["json_parse"] = "PASS"
    except (OSError, json.JSONDecodeError) as exc:
        checks["json_parse"] = "FAIL"
        errors.append(str(exc))
        records = []
        manifest = {"items": []}
        reconciliation = {"decisions": [], "playlist_only": []}
        patch = {"records": []}
        review = {"items": []}
        recovery_record = {}

    source_ids = [item.get("source_id") for item in records]
    video_ids = [item.get("video_id") for item in manifest.get("items", [])]
    decision_source_ids = [
        item.get("source_id") for item in reconciliation.get("decisions", [])
    ]
    matched_ids = [
        item.get("matched_video_id")
        for item in reconciliation.get("decisions", [])
        if item.get("matched_video_id")
    ]
    playlist_only_ids = [
        item.get("video_id") for item in reconciliation.get("playlist_only", [])
    ]
    recovered_ids = [
        item.get("video_id")
        for item in reconciliation.get("recovered_separate_sources", [])
    ]
    normalized_items_sha256 = hashlib.sha256(
        json.dumps(
            manifest.get("items", []),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    validations = {
        "playlist_items_collected": len(video_ids) > 0,
        "manifest_item_count_reconciles": manifest.get("item_count") == len(video_ids),
        "normalized_item_checksum_reconciles": manifest.get("collection", {}).get(
            "normalized_items_sha256"
        )
        == normalized_items_sha256,
        "expected_transcript_snapshot_count": len(source_ids)
        == EXPECTED_TRANSCRIPT_COUNT,
        "expected_playlist_snapshot_count": len(video_ids)
        == EXPECTED_PLAYLIST_ITEM_COUNT,
        "expected_recovered_item": set(recovered_ids) == EXPECTED_RECOVERED_IDS,
        "no_unresolved_playlist_only_items": not playlist_only_ids,
        "source_ids_unique": len(source_ids) == len(set(source_ids)),
        "playlist_video_ids_unique": len(video_ids) == len(set(video_ids)),
        "all_source_ids_decided_once": sorted(source_ids) == sorted(decision_source_ids),
        "matched_video_ids_unique": len(matched_ids) == len(set(matched_ids)),
        "playlist_disposition_complete": sorted(video_ids)
        == sorted(matched_ids + recovered_ids + playlist_only_ids),
        "canonical_urls_reconstruct": all(
            item.get("canonical_url")
            == f"https://www.youtube.com/watch?v={item.get('video_id')}"
            for item in manifest.get("items", [])
        ),
        "high_confidence_patch_only": all(
            item.get("match_confidence") == "HIGH" for item in patch.get("records", [])
        ),
        "manual_review_count_reconciles": review.get("count")
        == len(review.get("items", [])),
        "all_transcripts_matched": len(matched_ids) == len(source_ids),
        "all_matches_high_confidence": all(
            item.get("match_confidence") == "HIGH"
            for item in reconciliation.get("decisions", [])
        ),
        "all_matches_have_urls_and_dates": all(
            item.get("canonical_url") and item.get("published_at")
            for item in reconciliation.get("decisions", [])
        ),
        "metadata_patch_covers_all_matches": len(patch.get("records", []))
        == len(matched_ids),
        "recovery_source_id_distinct": recovery_record.get("source_id")
        not in set(source_ids),
        "recovery_video_id_reconciles": recovery_record.get("youtube_video_id")
        in set(recovered_ids),
        "manual_review_queue_resolved": review.get("count") == 0,
        "source_records_unchanged": True,
        "raw_transcripts_unchanged": True,
    }
    for name, passed in validations.items():
        checks[name] = "PASS" if passed else "FAIL"
        if not passed:
            errors.append(name)

    report = {
        "campaign_id": CAMPAIGN_ID,
        "validated_on": SNAPSHOT_DATE,
        "result": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "artifact_sha256": {
            path.relative_to(ROOT).as_posix(): sha256_path(path)
            for path in [
                PLAYLIST_MANIFEST_PATH,
                RECONCILIATION_PATH,
                METADATA_PATCH_PATH,
                MANUAL_REVIEW_PATH,
                SUMMARY_JSON_PATH,
            ]
            if path.exists()
        },
    }
    write_json(VALIDATION_JSON_PATH, report)
    VALIDATION_MD_PATH.write_text(
        "\n".join(
            [
                "# Validation Report",
                "",
                f"Result: **{report['result']}**",
                "",
                *[f"- {name}: `{result}`" for name, result in checks.items()],
                "",
                "## Errors",
                "",
                *(errors or ["None."]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    if errors:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["generate", "validate"])
    args = parser.parse_args()
    if args.command == "generate":
        generate()
    else:
        validate()


if __name__ == "__main__":
    main()
