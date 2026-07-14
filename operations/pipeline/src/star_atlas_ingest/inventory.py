"""Load and flatten the preserved creator-grouped URL inventory."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from .normalize import canonicalize_url

WRITTEN_PLATFORMS = {"website", "medium", "reddit", "google_docs", "github"}


def manifest_provenance(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    document = json.loads(raw)
    occurrences = [
        occurrence.get("posted_at")
        for creator in document.get("creators", [])
        for platform in creator.get("platforms", {}).values()
        for item in platform.get("urls", [])
        for occurrence in item.get("provenance_occurrences", [])
        if occurrence.get("posted_at")
    ]
    return {
        "original_filename": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "file_size": len(raw),
        "schema_version": document.get("metadata", {}).get("schema_version", "unknown"),
        "source_date_range": {"first": min(occurrences, default=None), "last": max(occurrences, default=None)},
        "creator_count": len(document.get("creators", [])),
        "unique_creator_url_pairs": document.get("summary", {}).get("unique_creator_url_pairs"),
    }


def flatten_inventory(document: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for creator in document.get("creators", []):
        classification = creator.get("classification", {})
        for platform, bundle in creator.get("platforms", {}).items():
            for item in bundle.get("urls", []):
                canonical = canonicalize_url(item["url"])
                grouped[canonical].append({
                    "creator_name": creator.get("canonical_name"),
                    "creator_aliases": creator.get("aliases", []),
                    "platform": platform,
                    "role": classification.get("role", "UNCLASSIFIED"),
                    "priority": classification.get("priority", 3),
                    "original_url": item["url"],
                    "provenance": item.get("provenance_occurrences", []),
                })

    records = []
    for canonical, entries in grouped.items():
        occurrences = [o for entry in entries for o in entry["provenance"]]
        dates = sorted(o["posted_at"] for o in occurrences if o.get("posted_at"))
        digest = hashlib.sha256(canonical.encode()).hexdigest()[:16].upper()
        platforms = sorted({entry["platform"] for entry in entries})
        records.append({
            "url_id": f"URL-{digest}",
            "canonical_url": canonical,
            "original_urls": sorted({entry["original_url"] for entry in entries}),
            "creators": sorted({entry["creator_name"] for entry in entries if entry["creator_name"]}),
            "creator_aliases": sorted({alias for entry in entries for alias in entry["creator_aliases"]}),
            "platforms": platforms,
            "roles": sorted({entry["role"] for entry in entries}),
            "priority": min(entry["priority"] for entry in entries),
            "provenance_occurrences": sorted(occurrences, key=lambda item: item.get("posted_at", "")),
            "first_discord_posted_at": dates[0] if dates else None,
            "last_discord_posted_at": dates[-1] if dates else None,
            "network_status": "UNTESTED",
            "processing_status": "PENDING" if any(p in WRITTEN_PLATFORMS for p in platforms) else "DEFERRED",
        })
    return sorted(records, key=lambda record: record["url_id"])


def write_jsonl(records: Iterable[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
