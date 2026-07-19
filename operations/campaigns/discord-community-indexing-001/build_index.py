#!/usr/bin/env python3
"""Build and search a deterministic, evidence-linked Discord community index.

The module intentionally uses only the Python standard library. It supports
Discord-like JSON, JSONL, CSV, HTML, Markdown, and plain-text exports without
assuming a particular exporter. Generated claims always point back to a parsed
source message and missing Discord identifiers remain explicit null values.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
from html.parser import HTMLParser
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


CAMPAIGN_ID = "discord-community-indexing-001"
SCHEMA_VERSION = "2.0.0"
AS_OF = "2026-07-18"
SUPPORTED_SUFFIXES = {".json", ".jsonl", ".csv", ".html", ".htm", ".txt", ".md"}
ROLE_TERMS = ("founder", "officer", "organizer", "builder", "creator", "diplomat", "competitor", "leader")
EVIDENCE_CLASSES = {
    "observed_authorship", "direct_self_identification", "explicit_third_party_attribution",
    "repeated_independent_attribution", "display_name_guild_tag", "operator_confirmed_alias",
    "inferred_alias", "unresolved_similarity",
}
ORGANIZATION_TYPES = {
    "guild", "guild_alliance", "community_organization", "official_team",
    "informal_group", "community_meme", "software_agent", "unresolved_tag",
}
REVIEW_STATUSES = {
    "READY_FOR_HUMAN_PROMOTION_REVIEW", "EVIDENCE_SUPPORTED_PROFILE_CANDIDATE",
    "REQUIRES_IDENTITY_RESOLUTION", "REQUIRES_ROLE_CORROBORATION", "DISCOVERY_ONLY", "DEFERRED",
    "OPERATOR_APPROVED_FOR_PROMOTION",
}
COVERAGE_STATUSES = {
    "ACTIVE_PARTIAL", "ACTIVE_CURRENT_TO_LAST_CAPTURE", "HISTORICAL_PARTIAL",
    "HISTORICAL_COMPLETE_AS_CAPTURED", "UNRESOLVED_CHANNEL", "EMPTY_OR_UNPARSED",
}
CHANNEL_CATEGORIES = {
    "announcements", "general", "foundation-room", "foundation-room-chat",
    "economics", "dao-chat", "governance", "guild", "event", "product",
    "support", "uncategorized",
}
ENTITY_SEEDS = [
    {"entity_type": "guild", "canonical_name": "Aephia", "aliases": ["AEP", "Aephia Industries"], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "Guild co-founded by Funcracker and Prometheus."},
    {"entity_type": "guild", "canonical_name": "BULK", "aliases": ["Bulk"], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "Specialized armed-freighting guild founded and led by Eoganacht."},
    {"entity_type": "community_organization", "canonical_name": "Star Atlas Italia", "aliases": ["SAI"], "resolution_status": "OPERATOR_CONFIRMED"},
    {"entity_type": "guild_alliance", "canonical_name": "Intergalactic Alliance", "aliases": ["IA"], "resolution_status": "OPERATOR_CONFIRMED"},
    {"entity_type": "community_meme", "canonical_name": "426", "aliases": [], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "A community gag derived from ‘4 to 6 weeks,’ used in response to repeatedly missed product-delivery timelines."},
    {"entity_type": "guild", "canonical_name": "The Club Guild", "aliases": ["The Club"], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "One of the original Star Atlas guilds."},
    {"entity_type": "unresolved_tag", "canonical_name": "The Vanguard", "aliases": [], "resolution_status": "HUMAN_REVIEW_REQUIRED"},
    {"entity_type": "guild", "canonical_name": "Rome", "aliases": ["ROME"], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "Guild founded by Witticus, ReyVeezy, and FancyHat; associated with the Metaverse Nomads Show."},
    {"entity_type": "guild", "canonical_name": "Coexist", "aliases": ["COEX"], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "Turkish-based guild."},
    {"entity_type": "guild", "canonical_name": "Eclypse", "aliases": ["EC"], "resolution_status": "OPERATOR_CONFIRMED"},
    {"entity_type": "guild", "canonical_name": "Deep Profits", "aliases": ["DEEP"], "resolution_status": "OPERATOR_CONFIRMED"},
    {"entity_type": "community_organization", "canonical_name": "Polaris Fuel", "aliases": [], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "Organization focused on reducing fuel prices in Star Atlas."},
    {"entity_type": "community_organization", "canonical_name": "Star Atlas TV", "aliases": [], "resolution_status": "OPERATOR_CONFIRMED"},
    {"entity_type": "community_organization", "canonical_name": "Ryden Systems", "aliases": ["EveEye", "Eveeye"], "resolution_status": "OPERATOR_CONFIRMED"},
    {"entity_type": "software_agent", "canonical_name": "The Star Atlas AI App", "aliases": ["AIAPP", "Star Atlas AI App"], "resolution_status": "OPERATOR_CONFIRMED", "meaning": "In-Discord software bot; not a person and not eligible for promotion."},
]
PERSON_SEEDS = [
    {"preferred_display_name": "King Bryan", "confirmed_aliases": ["King Bryan-Titan Analytics"]},
    {"preferred_display_name": "Bohdi", "confirmed_aliases": ["Bodhi", "Bodhitree", "BodhiTree"]},
    {"preferred_display_name": "Michael Wagner", "confirmed_aliases": ["Wagner", "SW4GNER", "SW4GN3R", "SW4GN3R [STAR]"]},
    {"preferred_display_name": "Jose", "confirmed_aliases": ["Zesk", "ZeSKK", "⪛⦿⫺ZeSKK [STAR]"]},
    {"preferred_display_name": "Funcracker", "confirmed_aliases": []},
    {"preferred_display_name": "Eoganacht", "confirmed_aliases": []},
    {"preferred_display_name": "Santi", "confirmed_aliases": ["SantiMod"]},
    {"preferred_display_name": "Dom", "confirmed_aliases": ["Dominic", "DominicVain", "DominicVainMod"]},
    {"preferred_display_name": "Jindo", "confirmed_aliases": ["Jindo | Star Atlas Mod", "Jindo | Star Atlas Mod [STAR]"]},
    {"preferred_display_name": "Suhail", "confirmed_aliases": ["SuhailDebar", "SuhailDebar | Star Atlas Mod", "SuhailDebar | Star Atlas ModMod"]},
    {"preferred_display_name": "Prometheus", "confirmed_aliases": ["[AEP] Prometheus", "[AEP] Prometheus ⪛⦿⫺"]},
    {"preferred_display_name": "Hakmer", "confirmed_aliases": ["[COEX] Hakmer"]},
    {"preferred_display_name": "Lerinor", "confirmed_aliases": ["[AEP] Lerinor"]},
    {"preferred_display_name": "Neo_AArmstrong", "confirmed_aliases": ["[Λ] Neo_AArmstrong [EC]"]},
    {"preferred_display_name": "Atlas Theory", "confirmed_aliases": []},
    {"preferred_display_name": "DrumCarlos", "confirmed_aliases": ["DRUMCARL05", "DRUMCARL05 | Polaris Fuel"]},
    {"preferred_display_name": "Xcode", "confirmed_aliases": ["Xcode [STAR]"]},
    {"preferred_display_name": "BTH 2620", "confirmed_aliases": ["beyondthehorizon2620"]},
    {"preferred_display_name": "ODVB", "confirmed_aliases": ["odvb"]},
    {"preferred_display_name": "Ryden", "confirmed_aliases": []},
    {"preferred_display_name": "MagicPuncher", "confirmed_aliases": []},
    {"preferred_display_name": "Agent Solace", "confirmed_aliases": []},
    {"preferred_display_name": "Witticus", "confirmed_aliases": []},
    {"preferred_display_name": "ReyVeezy", "confirmed_aliases": []},
    {"preferred_display_name": "FancyHat", "confirmed_aliases": []},
    {"preferred_display_name": "Virtuwaal", "confirmed_aliases": []},
]
# Compatibility view used by term matching helpers.
SEEDS = [(entry["entity_type"], entry["canonical_name"], entry["aliases"]) for entry in ENTITY_SEEDS] + [
    ("person", entry["preferred_display_name"], entry["confirmed_aliases"]) for entry in PERSON_SEEDS
]
TAG_REGISTRY_SEEDS = [
    {"tag": "AEP", "canonical_entity": "Aephia", "entity_type": "guild", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "BULK", "canonical_entity": "BULK", "entity_type": "guild", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "IA", "canonical_entity": "Intergalactic Alliance", "entity_type": "guild_alliance", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "SAI", "canonical_entity": "Star Atlas Italia", "entity_type": "community_organization", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "426", "canonical_entity": "426", "entity_type": "community_meme", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "ROME", "canonical_entity": "Rome", "entity_type": "guild", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "COEX", "canonical_entity": "Coexist", "entity_type": "guild", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "EC", "canonical_entity": "Eclypse", "entity_type": "guild", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
    {"tag": "DEEP", "canonical_entity": "Deep Profits", "entity_type": "guild", "resolution_status": "OPERATOR_CONFIRMED", "resolution_basis": "repository_operator_confirmation"},
]
PUBLICLY_EXCLUDED_HANDLES = {"deleteduser"}
PROMOTION_IGNORED_HANDLES = {"diego", "diegodiaz08", "inti", "shaddix", "shaddix1", "shaddix1staratlasmod"}
PROMOTION_DEFERRED_HANDLES = {"chriz"}
NON_PERSON_HANDLES = {"aiapp", "thestaratlasaiapp", "staratlasaiapp"}
PROMOTION_APPROVED_HANDLES = {"funcracker"}
OPERATOR_CONFIRMED_PEOPLE = {
    "kingbryan", "bohdi", "michaelwagner", "jose", "funcracker", "eoganacht",
    "santi", "dom", "jindo", "suhail", "prometheus", "hakmer", "lerinor",
    "neoaarmstrong", "atlastheory", "drumcarlos", "xcode", "bth2620", "odvb",
    "ryden", "magicpuncher", "witticus", "reyveezy", "fancyhat",
}
GENERIC_MENTIONS = {
    "all", "atlas", "community", "communitymoderator", "deleted", "event",
    "everyone", "game", "governance", "here", "holosim", "metaverse", "mod",
    "sage", "sneak", "star", "staratlas", "the",
}


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:16].upper()}"


def normalized(value: Any) -> str:
    text = html.unescape(str(value or "")).casefold()
    return re.sub(r"[^a-z0-9]+", "", text)


def clean_space(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def clean_handle(value: Any) -> str:
    text = clean_space(value).strip("@,.;:()")
    return re.sub(r"\s+", " ", text)


def text_sort_key(value: Any) -> tuple[str, str]:
    text = str(value)
    return text.casefold(), text


def canonical_text_bytes(path: Path) -> bytes:
    """Return repository-stable UTF-8 bytes for supported text evidence.

    Git can materialize tracked JSON/JSONL/CSV text with platform-specific line
    endings.  The discovery inventory therefore checksums an explicitly
    declared LF-normalized UTF-8 view rather than making campaign output depend
    on checkout configuration.  Source evidence itself is never rewritten.
    """
    return path.read_text(encoding="utf-8-sig", errors="replace").encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(canonical_text_bytes(path)).hexdigest()


def first(mapping: dict[str, Any], names: Iterable[str]) -> Any:
    lowered = {str(k).casefold(): v for k, v in mapping.items()}
    for name in names:
        if name.casefold() in lowered and lowered[name.casefold()] not in (None, ""):
            return lowered[name.casefold()]
    return None


def author_fields(record: dict[str, Any]) -> tuple[str | None, str | None]:
    author = first(record, ("author", "user", "sender", "member", "username", "display_name", "name"))
    author_id = first(record, ("author_id", "user_id", "sender_id", "member_id"))
    if isinstance(author, dict):
        author_id = author_id or first(author, ("id", "user_id", "author_id"))
        author = first(author, ("display_name", "global_name", "nickname", "username", "name"))
    return (clean_handle(author) or None, str(author_id) if author_id is not None else None)


def normalize_timestamp(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    candidate = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(candidate).isoformat().replace("+00:00", "Z")
    except ValueError:
        pass
    for fmt in ("%m/%d/%Y, %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).isoformat()
        except ValueError:
            continue
    return text


def collection_context(path: str, record: dict[str, Any] | None = None) -> dict[str, Any]:
    record = record or {}
    lower = path.casefold()
    if "discord-announcements" in lower:
        inferred = {
            "server_or_community_name": "Star Atlas Discord",
            "canonical_channel_name": "announcements",
            "channel_category": "announcements",
        }
    else:
        inferred = {
            "server_or_community_name": None,
            "canonical_channel_name": None,
            "channel_category": "uncategorized",
        }
    return {
        "server_or_community_name": first(record, ("server_or_community_name", "server_name", "guild_name", "community_name")) or inferred["server_or_community_name"],
        "observed_channel_name": first(record, ("observed_channel_name", "channel_name", "conversation", "conversation_name")),
        "canonical_channel_name": first(record, ("canonical_channel_name",)) or inferred["canonical_channel_name"],
        "channel_category": first(record, ("channel_category",)) or inferred["channel_category"],
        "collection_complete": first(record, ("collection_complete",)),
        "collection_notes": first(record, ("collection_notes", "collection_warnings")) or [],
    }


@dataclass
class Message:
    source_id: str
    message_id: str | None
    channel_id: str | None
    author_id: str | None
    display_name: str | None
    timestamp: str | None
    content: str
    server_or_community_name: str | None = None
    observed_channel_name: str | None = None
    canonical_channel_name: str | None = None
    channel_category: str | None = None
    collection_complete: bool | None = None
    collection_notes: list[str] = field(default_factory=list)
    content_variants: list[dict[str, Any]] = field(default_factory=list)
    metadata: list[str] = field(default_factory=list)
    source_paths: list[str] = field(default_factory=list)
    source_formats: list[str] = field(default_factory=list)

    def fingerprint(self) -> str:
        key = "\x1f".join((normalized(self.display_name), self.timestamp or "", clean_space(self.content)))
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def merge(self, other: "Message") -> None:
        self_is_archive = not self.source_id.startswith("DISCORD-SOURCE-")
        other_is_archive = not other.source_id.startswith("DISCORD-SOURCE-")
        self.content_variants.append({"content_sha256": hashlib.sha256(other.content.encode("utf-8")).hexdigest(), "source_paths": other.source_paths})
        if self.source_id.startswith("DISCORD-SOURCE-") and not other.source_id.startswith("DISCORD-SOURCE-"):
            self.source_id = other.source_id
            self.content = other.content
        for attr in ("message_id", "channel_id", "author_id", "display_name", "timestamp", "server_or_community_name", "observed_channel_name", "canonical_channel_name", "channel_category", "collection_complete"):
            if getattr(self, attr) is None and getattr(other, attr) is not None:
                setattr(self, attr, getattr(other, attr))
        if not self_is_archive and other_is_archive:
            self.content = other.content
        self.metadata = sorted(set(self.metadata + other.metadata))
        self.source_paths = sorted(set(self.source_paths + other.source_paths))
        self.source_formats = sorted(set(self.source_formats + other.source_formats))
        self.collection_notes = sorted(set(self.collection_notes + other.collection_notes))
        variants = self.content_variants + other.content_variants
        self.content_variants = sorted({(item["content_sha256"], tuple(item["source_paths"])): item for item in variants}.values(), key=lambda item: (item["content_sha256"], item["source_paths"]))


def compatible_raw_normalized(left: Message, right: Message) -> bool:
    if normalized(left.display_name) != normalized(right.display_name) or left.timestamp != right.timestamp:
        return False
    left_raw = any(path.startswith("archive/raw/") for path in left.source_paths)
    right_raw = any(path.startswith("archive/raw/") for path in right.source_paths)
    left_normalized = any(path.startswith("archive/normalized/") for path in left.source_paths)
    right_normalized = any(path.startswith("archive/normalized/") for path in right.source_paths)
    if not ((left_raw and right_normalized) or (right_raw and left_normalized)):
        return False
    def representation_core(value: str) -> str:
        # Markdown exports can retain a terminal block delimiter that the
        # normalized record omits (or vice versa).  Removing only that framing
        # marker lets the two representations reconcile without using
        # author+timestamp as a deduplication key.
        return clean_space(re.sub(r"(?:\s*---\s*)+$", "", value))

    a, b = representation_core(left.content), representation_core(right.content)
    return a == b or (min(len(a), len(b)) >= 20 and (a in b or b in a))


def message_from_mapping(record: dict[str, Any], path: str, suffix: str, ordinal: int) -> Message | None:
    content = first(record, ("content", "message", "text", "body", "message_content"))
    timestamp = first(record, ("timestamp_iso", "timestamp", "created_at", "date", "datetime", "time"))
    display_name, author_id = author_fields(record)
    if content is None or not (display_name or timestamp or first(record, ("message_id", "id", "source_id"))):
        return None
    content = str(content).strip()
    if not content:
        return None
    message_id = first(record, ("message_id", "discord_message_id"))
    source_id = first(record, ("source_id",))
    channel_id = first(record, ("channel_id", "discord_channel_id"))
    # A generic `id` is accepted as a Discord message ID only when explicitly
    # message-shaped; source_id is an archive identifier, not a Discord ID.
    if message_id is None and "messages" in record and first(record, ("id",)):
        message_id = first(record, ("id",))
    timestamp = normalize_timestamp(timestamp)
    fallback = "\x1f".join((path, str(ordinal), display_name or "", timestamp or "", clean_space(content)))
    source_id = str(source_id or stable_id("DISCORD-SOURCE", fallback))
    metadata = first(record, ("metadata", "notes", "flags")) or []
    if not isinstance(metadata, list):
        metadata = [str(metadata)]
    context = collection_context(path, record)
    notes = context["collection_notes"]
    if not isinstance(notes, list):
        notes = [str(notes)]
    complete = context["collection_complete"]
    if isinstance(complete, str):
        complete = complete.strip().casefold() in {"yes", "true", "1", "complete"}
    return Message(
        source_id=source_id,
        message_id=str(message_id) if message_id is not None else None,
        channel_id=str(channel_id) if channel_id is not None else None,
        author_id=author_id,
        display_name=display_name,
        timestamp=timestamp,
        content=content,
        server_or_community_name=clean_space(context["server_or_community_name"]) or None,
        observed_channel_name=clean_space(context["observed_channel_name"]) or None,
        canonical_channel_name=clean_space(context["canonical_channel_name"]) or None,
        channel_category=clean_space(context["channel_category"]) or "uncategorized",
        collection_complete=complete if isinstance(complete, bool) else None,
        collection_notes=[clean_space(item) for item in notes if clean_space(item)],
        metadata=[str(item) for item in metadata],
        source_paths=[path],
        source_formats=[suffix.lstrip(".")],
    )


def walk_message_mappings(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        content = first(value, ("content", "message", "text", "body", "message_content"))
        if content is not None:
            yield value
            return
        for key, child in value.items():
            if str(key).casefold() in {"messages", "data", "items", "records", "chat", "conversation"}:
                yield from walk_message_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_message_mappings(child)


class DiscordHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.field: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value for key, value in attrs}
        classes = set((data.get("class") or "").split())
        if tag in {"article", "li", "div"} and (classes & {"message", "chatlog__message-group"} or data.get("data-message-id")):
            if self.current:
                self.records.append(self.current)
            self.current = {
                "message_id": data.get("data-message-id"),
                "channel_id": data.get("data-channel-id"),
                "author_id": data.get("data-author-id"),
            }
        if self.current is not None:
            if classes & {"author", "chatlog__author-name", "username"}:
                self.field = "author"
            elif classes & {"content", "chatlog__content", "message-content"}:
                self.field = "content"
            elif tag == "time" or classes & {"timestamp", "chatlog__timestamp"}:
                self.field = "timestamp"
                if data.get("datetime"):
                    self.current["timestamp"] = data["datetime"]
            elif tag == "br" and self.field == "content":
                self.current["content"] = self.current.get("content", "") + "\n"

    def handle_endtag(self, tag: str) -> None:
        if tag in {"article", "li"} and self.current:
            self.records.append(self.current)
            self.current = None
        if tag in {"span", "div", "time", "p"}:
            self.field = None

    def handle_data(self, data: str) -> None:
        if self.current is not None and self.field:
            self.current[self.field] = self.current.get(self.field, "") + data

    def close(self) -> None:
        super().close()
        if self.current:
            self.records.append(self.current)
            self.current = None


def parse_text_export(text: str, path: str, suffix: str) -> list[Message]:
    messages: list[Message] = []
    conversation = re.search(r"(?im)^Conversation:\s*(.+?)\s*$", text)
    complete_match = re.search(r"(?im)^Collection complete:\s*(yes|no|true|false)\s*$", text)
    warning_match = re.search(r"(?ms)^## Collection Warnings\s*\n\s*(.*?)(?=\n---|\n## )", text)
    context = {
        "server_or_community_name": "Star Atlas Discord" if "discord-announcements" in path.casefold() else None,
        # Preserve the export header verbatim after whitespace normalization.
        # The trailing comma is part of the observed value and is not silently
        # promoted into a canonical native channel name.
        "observed_channel_name": clean_space(conversation.group(1)) if conversation else None,
        "canonical_channel_name": "announcements" if "discord-announcements" in path.casefold() else None,
        "channel_category": "announcements" if "discord-announcements" in path.casefold() else "uncategorized",
        "collection_complete": complete_match.group(1).casefold() in {"yes", "true"} if complete_match else None,
        "collection_notes": [clean_space(line.lstrip("- ")) for line in warning_match.group(1).splitlines() if clean_space(line.lstrip("- "))] if warning_match else [],
    }
    # Markdown conversation exports used by the archive.
    block_pattern = re.compile(
        r"(?ms)^###\s+(?P<author>[^\r\n]+)\r?\n(?P<timestamp>\d{1,2}/\d{1,2}/\d{4},?\s+\d{1,2}:\d{2}:\d{2}\s+[AP]M)\r?\n(?P<body>.*?)(?=\r?\n---(?:\r?\n|$))"
    )
    for ordinal, match in enumerate(block_pattern.finditer(text), 1):
        body_lines = match.group("body").strip().splitlines()
        metadata = []
        while body_lines and body_lines[0].strip().startswith("_") and body_lines[0].strip().endswith("_"):
            metadata.append(body_lines.pop(0).strip())
        mapping = {
            "author": match.group("author"),
            "timestamp": match.group("timestamp"),
            "content": "\n".join(body_lines).strip(),
            "metadata": metadata,
            **context,
        }
        message = message_from_mapping(mapping, path, suffix, ordinal)
        if message:
            messages.append(message)
    if messages:
        return messages
    # Common one-message-per-line text exports.
    line_pattern = re.compile(
        r"^\[?(?P<timestamp>\d{4}-\d{2}-\d{2}[^\]]*|\d{1,2}/\d{1,2}/\d{4}[^\]]*)\]?\s*(?:-|\|)?\s*(?P<author>[^:]{1,80}):\s*(?P<content>.+)$"
    )
    for ordinal, line in enumerate(text.splitlines(), 1):
        match = line_pattern.match(line.strip())
        if match:
            message = message_from_mapping(match.groupdict(), path, suffix, ordinal)
            if message:
                messages.append(message)
    return messages


def parse_source(path: Path, repo_root: Path) -> list[Message]:
    rel = path.relative_to(repo_root).as_posix()
    suffix = path.suffix.casefold()
    try:
        if suffix == ".json":
            document = json.loads(path.read_text(encoding="utf-8-sig"))
            mappings = list(walk_message_mappings(document))
        elif suffix == ".jsonl":
            mappings = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        elif suffix == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as stream:
                mappings = list(csv.DictReader(stream))
        elif suffix in {".html", ".htm"}:
            parser = DiscordHTMLParser()
            parser.feed(path.read_text(encoding="utf-8-sig", errors="replace"))
            parser.close()
            mappings = parser.records
        else:
            return parse_text_export(path.read_text(encoding="utf-8-sig", errors="replace"), rel, suffix)
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error):
        return []
    messages = []
    for ordinal, mapping in enumerate(mappings, 1):
        if isinstance(mapping, dict):
            message = message_from_mapping(mapping, rel, suffix, ordinal)
            if message:
                messages.append(message)
    return messages


def source_class(rel: str) -> str:
    lower = rel.casefold()
    if lower.startswith("archive/raw/"):
        return "raw"
    if lower.startswith("archive/normalized/"):
        return "normalized"
    return "derived_or_context"


def discover_sources(repo_root: Path) -> list[Path]:
    paths = []
    for path in repo_root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in SUPPORTED_SUFFIXES:
            continue
        rel = path.relative_to(repo_root).as_posix()
        lower = rel.casefold()
        if "discord" in lower and (lower.startswith("archive/raw/") or lower.startswith("archive/normalized/")):
            paths.append(path)
    return sorted(paths, key=lambda p: p.relative_to(repo_root).as_posix().casefold())


def load_messages(repo_root: Path, include_duplicate_reviews: bool = False) -> tuple[Any, ...]:
    by_fingerprint: dict[str, Message] = {}
    by_source_id: defaultdict[str, list[Message]] = defaultdict(list)
    by_message_id: defaultdict[str, list[Message]] = defaultdict(list)
    unique: list[Message] = []
    duplicate_reviews: list[dict[str, Any]] = []
    inventory = []
    for path in discover_sources(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        classification = source_class(rel)
        if rel.endswith("announcement-index.csv"):
            classification = "derived_index"
        ingested = classification in {"raw", "normalized"}
        parsed = parse_source(path, repo_root) if ingested else []
        representation_role = "raw_aggregate_export" if classification == "raw" else ("normalized_aggregate" if rel.endswith("messages.jsonl") else ("normalized_per_message" if "/messages/" in rel else "derived_index"))
        inventory.append({
            "path": rel,
            "classification": classification,
            "format": path.suffix.casefold().lstrip("."),
            "bytes": len(canonical_text_bytes(path)),
            "sha256": sha256_file(path),
            "checksum_basis": "UTF8_TEXT_LF_NORMALIZED",
            "byte_count_basis": "UTF8_TEXT_LF_NORMALIZED",
            "ingested": ingested,
            "representation_role": representation_role,
            "parsed_message_occurrences": len(parsed),
            "reason": "raw_or_normalized_discord_export" if ingested else "derived_index_not_reingested_as_messages",
        })
        for message in parsed:
            candidates = list(by_source_id.get(message.source_id, []))
            if message.message_id:
                candidates.extend(by_message_id.get(message.message_id, []))
            fingerprint_match = by_fingerprint.get(message.fingerprint())
            if fingerprint_match:
                candidates.append(fingerprint_match)
            candidates = list({id(item): item for item in candidates}.values())
            existing = next((item for item in candidates if item.fingerprint() == message.fingerprint() or compatible_raw_normalized(item, message)), None)
            if existing is None:
                # Author/time is only a compatibility lead for an exact raw-vs-
                # normalized representation; it is never a deduplication key.
                existing = next((item for item in unique if compatible_raw_normalized(item, message)), None)
            if existing:
                existing.merge(message)
                if existing not in by_source_id[message.source_id]:
                    by_source_id[message.source_id].append(existing)
                if message.message_id and existing not in by_message_id[message.message_id]:
                    by_message_id[message.message_id].append(existing)
                by_fingerprint[existing.fingerprint()] = existing
            else:
                incompatible = [item for item in candidates if item.source_id == message.source_id or (message.message_id and item.message_id == message.message_id)]
                for item in incompatible:
                    duplicate_reviews.append({
                        "review_id": stable_id("DUP-REVIEW", "\x1f".join(sorted((item.fingerprint(), message.fingerprint())))),
                        "review_type": "likely_duplicate_message",
                        "source_id": message.source_id,
                        "native_message_id": message.message_id,
                        "author": message.display_name,
                        "timestamp": message.timestamp,
                        "observed_contents": sorted({clean_space(item.content), clean_space(message.content)}),
                        "reason_human_review_required": "A shared source or native message ID has incompatible normalized content; both records were retained.",
                    })
                unique.append(message)
                by_source_id[message.source_id].append(message)
                if message.message_id:
                    by_message_id[message.message_id].append(message)
                by_fingerprint[message.fingerprint()] = message
    unique = sorted({id(message): message for message in unique}.values(), key=lambda m: ((m.timestamp or ""), m.source_id, m.fingerprint()))
    duplicate_reviews = sorted({item["review_id"]: item for item in duplicate_reviews}.values(), key=lambda item: item["review_id"])
    return (unique, inventory, duplicate_reviews) if include_duplicate_reviews else (unique, inventory)


def evidence(message: Message, quote: str | None = None, attribution: str = "observed_authorship") -> dict[str, Any]:
    excerpt = clean_space(quote if quote is not None else message.content)[:500]
    return {
        "source_id": message.source_id,
        "message_id": message.message_id,
        "channel_id": message.channel_id,
        "timestamp": message.timestamp,
        "author_id": message.author_id,
        "display_name": message.display_name,
        "source_paths": message.source_paths,
        "quoted_text": excerpt,
        "attribution_class": attribution,
        "evidence_location": "display_name" if attribution in {"observed_authorship", "inferred_alias"} else "message_content",
        "evidence_channel": "archive_evidence",
        "operator_assertion": False,
    }


def operator_evidence(note: str, attribution: str = "operator_confirmed_alias") -> dict[str, Any]:
    return {
        "source_id": None, "message_id": None, "channel_id": None, "timestamp": None,
        "author_id": None, "display_name": None, "source_paths": [], "quoted_text": None,
        "attribution_class": attribution, "evidence_channel": "operator_confirmation",
        "evidence_location": "operator_review_record",
        "operator_assertion": True, "review_note": note,
    }


def extract_mentions(content: str) -> list[str]:
    results = []
    sections = re.findall(r"(?im)^Mentions:\s*(.+)$", content)
    for section in sections:
        # Exporters commonly delimit footer handles with commas, while some
        # use an ``and @next`` join.  Split only at explicit mention
        # boundaries so pipe components remain attached to their handle.
        results.extend(part.strip() for part in re.split(r",\s*|\s+and\s+(?=@)", section))
    if not sections:
        # Conservative inline fallback for exporters without a Mentions footer.
        # It intentionally avoids consuming prose after @everyone/@here.
        results.extend(re.findall(r"@(?:\[[^\]]+\]\s*)?[\w.-]{2,40}", content, re.UNICODE))
        results.extend(re.findall(r"@[\w.-]{2,32}\s*\|\s*[\w. -]{2,40}(?=\s{2,}|,|\n|$)", content, re.UNICODE))
    cleaned = []
    for value in results:
        handle = clean_handle(value)
        if handle and normalized(handle) not in GENERIC_MENTIONS and len(handle) <= 100:
            cleaned.append(handle)
    return sorted(set(cleaned), key=text_sort_key)


def person_name_from_handle(handle: str) -> str:
    value = handle.lstrip("@").strip()
    value = re.sub(r"^\[[^\]]+\]\s*", "", value)
    if "|" in value:
        parts = [part.strip() for part in value.split("|")]
        # ROME|King Bryan uses guild first; Eoganacht | BULK uses guild last.
        if parts[0].casefold() == "rome":
            value = parts[1]
        else:
            value = parts[0]
    return clean_handle(value)


def matched_seed_terms(message: Message) -> list[tuple[str, str, str]]:
    result = []
    lower = message.content.casefold()
    for entity_type, canonical, aliases in SEEDS:
        for term in [canonical, *aliases]:
            if re.search(rf"(?<![\w]){re.escape(term.casefold())}(?![\w])", lower):
                result.append((entity_type, canonical, term))
                break
    return result


def build_alias_registry(messages: list[Message]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    entries = []
    conflicts = []
    alias_owners: defaultdict[str, list[str]] = defaultdict(list)
    for seed in ENTITY_SEEDS:
        entity_type, canonical, aliases = seed["entity_type"], seed["canonical_name"], seed["aliases"]
        terms = [canonical, *aliases]
        refs = [
            evidence(message, term, "explicit_third_party_attribution")
            for message in messages for term in terms
            if re.search(rf"(?<![\w]){re.escape(term)}(?![\w])", message.content, re.I)
        ]
        for term in terms:
            alias_owners[normalized(term)].append(canonical)
        entries.append({
            "entity_type": entity_type,
            "canonical_name": canonical,
            "aliases": aliases,
            "preferred_display_name": canonical,
            "observed_handles": sorted({ref["quoted_text"] for ref in refs if ref.get("quoted_text")}, key=text_sort_key),
            "confirmed_aliases": aliases,
            "alias_basis": "operator_confirmed" if aliases else None,
            "normalized_terms": sorted(set(normalized(term) for term in terms)),
            "registry_status": "operator_confirmed_with_archive_observations" if refs else seed["resolution_status"].casefold(),
            "resolution_status": seed["resolution_status"],
            "identity_merge_authorized": True,
            "meaning": seed.get("meaning"),
            "evidence": refs[:25],
            "operator_confirmation": operator_evidence("Confirmed by repository operator during PR review"),
        })
    for seed in PERSON_SEEDS:
        canonical, aliases = seed["preferred_display_name"], seed["confirmed_aliases"]
        operator_confirmed = normalized(canonical) in OPERATOR_CONFIRMED_PEOPLE
        terms = [canonical, *aliases]
        refs = []
        observed = set()
        for message in messages:
            if message.display_name and normalized(message.display_name) in {normalized(term) for term in terms}:
                refs.append(evidence(message, message.display_name, "observed_authorship"))
                observed.add(message.display_name)
            for handle in extract_mentions(message.content):
                if normalized(person_name_from_handle(handle)) in {normalized(term) for term in terms}:
                    refs.append(evidence(message, handle, "explicit_third_party_attribution"))
                    observed.add(handle)
        for term in terms:
            alias_owners[normalized(term)].append(canonical)
        entries.append({
            "entity_type": "person", "canonical_name": canonical,
            "preferred_display_name": canonical, "aliases": aliases,
            "observed_handles": sorted(observed, key=text_sort_key),
            "confirmed_aliases": aliases, "alias_basis": "operator_confirmed" if aliases or operator_confirmed else None,
            "normalized_terms": sorted({normalized(term) for term in terms}),
            "registry_status": "operator_confirmed_with_archive_observations" if refs else "seeded_unresolved",
            "resolution_status": "OPERATOR_CONFIRMED" if operator_confirmed else "HUMAN_REVIEW_REQUIRED",
            "identity_merge_authorized": operator_confirmed, "meaning": None,
            "evidence": refs[:25],
            "operator_confirmation": operator_evidence("Confirmed by repository operator during PR review") if operator_confirmed else None,
        })
    for term, owners in sorted(alias_owners.items()):
        if len(set(owners)) > 1:
            conflicts.append({"type": "alias_collision", "normalized_term": term, "canonical_names": sorted(set(owners))})
    # This fuzzy resemblance is deliberately reported, never merged.
    observed = {person_name_from_handle(h) for m in messages for h in extract_mentions(m.content)} | {m.display_name for m in messages if m.display_name}
    confirmed_terms = {normalized(term) for seed in PERSON_SEEDS for term in [seed["preferred_display_name"], *seed["confirmed_aliases"]]}
    for seed in PERSON_SEEDS:
        canonical = seed["preferred_display_name"]
        for handle in observed:
            ratio = SequenceMatcher(None, normalized(canonical), normalized(handle)).ratio()
            shared_prefix = normalized(canonical)[:2] == normalized(handle)[:2] and ratio >= 0.55
            if normalized(handle) not in confirmed_terms and canonical.casefold() != handle.casefold() and (ratio >= 0.68 or shared_prefix):
                conflicts.append({
                    "type": "unresolved_similarity",
                    "attribution_class": "unresolved_similarity",
                    "seeded_name": canonical,
                    "observed_handle": handle,
                    "similarity": round(ratio, 3),
                    "merge_performed": False,
                })
    return {"schema_version": SCHEMA_VERSION, "campaign_id": CAMPAIGN_ID, "entries": entries}, conflicts


def build_indexes(messages: list[Message], alias_registry: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    identities: dict[str, dict[str, Any]] = {}
    relationships: list[dict[str, Any]] = []
    relationship_keys = set()
    person_aliases = {
        term: entry for entry in alias_registry["entries"] if entry["entity_type"] == "person"
        for term in entry["normalized_terms"]
    }
    organization_entries = {entry["canonical_name"]: entry for entry in alias_registry["entries"] if entry["entity_type"] != "person"}
    organization_by_term = {term: entry for entry in organization_entries.values() for term in entry["normalized_terms"]}
    tag_registry = {entry["tag"].casefold(): entry for entry in TAG_REGISTRY_SEEDS}

    def add_identity(name: str, message: Message, observed_as: str, attribution: str, author_id: str | None = None) -> str:
        name = clean_handle(name)
        alias_entry = person_aliases.get(normalized(name))
        preferred = alias_entry["preferred_display_name"] if alias_entry and alias_entry["identity_merge_authorized"] else name
        key = f"confirmed:{normalized(preferred)}" if alias_entry and alias_entry["identity_merge_authorized"] else (f"id:{author_id}" if author_id else f"handle:{normalized(name)}")
        identity_id = stable_id("PERSON", key)
        record = identities.setdefault(identity_id, {
            "identity_id": identity_id,
            "record_type": "resolved_person_identity" if alias_entry and alias_entry["identity_merge_authorized"] else ("observed_author_identity" if author_id else "observed_handle_cluster"),
            "canonical_handle": preferred,
            "preferred_display_name": preferred,
            "author_ids": [],
            "observed_handles": [],
            "confirmed_aliases": list(alias_entry["confirmed_aliases"]) if alias_entry else [],
            "alias_basis": "operator_confirmed" if alias_entry and alias_entry["identity_merge_authorized"] else None,
            "roles": [],
            "operator_confirmed_roles": [],
            "first_seen": message.timestamp,
            "last_seen": message.timestamp,
            "evidence": [],
            "operator_confirmations": [alias_entry["operator_confirmation"]] if alias_entry and alias_entry.get("operator_confirmation") else [],
            "identity_confidence": "operator_confirmed_alias" if alias_entry and alias_entry["identity_merge_authorized"] else ("author_id_supported" if author_id else "handle_only_not_merged"),
        })
        if author_id and author_id not in record["author_ids"]:
            record["author_ids"].append(author_id)
        if observed_as not in record["observed_handles"]:
            record["observed_handles"].append(observed_as)
        record["evidence"].append(evidence(message, observed_as, attribution))
        dates = [d for d in (record["first_seen"], record["last_seen"], message.timestamp) if d]
        if dates:
            record["first_seen"], record["last_seen"] = min(dates), max(dates)
        return identity_id

    def add_relationship(subject_id: str, subject_name: str, predicate: str, object_type: str, object_name: str,
                         message: Message, attribution: str, quote: str, confidence: str, role: str | None = None) -> None:
        key = (subject_id, predicate, normalized(object_name), message.source_id, clean_space(quote))
        if key in relationship_keys:
            return
        relationship_keys.add(key)
        record = {
            "relationship_id": stable_id("REL", "\x1f".join(key)),
            "subject_id": subject_id,
            "subject_name": subject_name,
            "predicate": predicate,
            "object_type": object_type,
            "object_name": object_name,
            "valid_at": message.timestamp,
            "confidence": confidence,
            "evidence_channel": "archive_evidence",
            "evidence": [evidence(message, quote, attribution)],
        }
        relationships.append(record)
        if role and confidence in {"high", "operator_confirmed"} and attribution != "display_name_guild_tag" and subject_id in identities and role not in identities[subject_id]["roles"]:
            identities[subject_id]["roles"].append(role)

    for message in messages:
        if message.display_name and normalized(message.display_name) not in PUBLICLY_EXCLUDED_HANDLES | NON_PERSON_HANDLES:
            author_id = add_identity(
                message.display_name, message, message.display_name,
                "inferred_alias" if any("author inferred" in item.casefold() for item in message.metadata) else "observed_authorship",
                message.author_id,
            )
            if re.search(r"\bmod(?:erator)?\b", message.display_name, re.I):
                add_relationship(author_id, message.display_name, "has_community_role", "role", "moderator", message,
                                 "inferred_alias", message.display_name, "medium", "moderator")
        mentions = extract_mentions(message.content)
        mention_ids = {}
        for handle in mentions:
            person = person_name_from_handle(handle)
            if not person or normalized(person) in GENERIC_MENTIONS | PUBLICLY_EXCLUDED_HANDLES | NON_PERSON_HANDLES:
                continue
            mention_ids[handle] = add_identity(person, message, handle, "explicit_third_party_attribution")
            observed_components: list[tuple[str, str]] = []
            tag = re.match(r"@?\[([^\]]+)\]", handle)
            if tag:
                observed_components.append((tag.group(1), "bracket_tag"))
            if "|" in handle:
                observed_components.extend((part.strip(" @[]"), "pipe_component") for part in handle.split("|")[1:] if part.strip(" @[]"))
            for component, component_context in observed_components:
                resolved = tag_registry.get(component.casefold())
                if not resolved:
                    add_relationship(mention_ids[handle], person, "has_display_tag", "unresolved_tag", component, message,
                                     "display_name_guild_tag", handle, "low")
                    continue
                entity_type = resolved["entity_type"]
                if entity_type == "guild":
                    # A pipe-separated guild token (for example
                    # ``[IA] Dodger | BULK``) is association evidence only.
                    # A leading bracket tag may enter the membership-review
                    # queue, but it is never accepted as membership directly.
                    predicate, role = ("associated_with_guild", "guild_association") if component_context == "pipe_component" else ("possible_member_of", "guild_member_candidate")
                elif entity_type == "guild_alliance":
                    predicate, role = "associated_with_alliance", "alliance_association"
                elif entity_type == "community_organization":
                    predicate, role = "associated_with_organization", "community_organization_association"
                else:
                    predicate, role = "has_display_tag", None
                add_relationship(mention_ids[handle], person, predicate, entity_type, resolved["canonical_entity"], message,
                                 "display_name_guild_tag", handle, "low", role)

        # Official council roster attribution.
        if re.search(r"first\s+(?:star atlas dao\s+)?council", message.content, re.I):
            for handle, identity_id in mention_ids.items():
                person = person_name_from_handle(handle)
                add_relationship(identity_id, person, "served_as", "organization", "Star Atlas DAO Council", message,
                                 "explicit_third_party_attribution", handle, "high", "dao_council_service")

        # Explicit creator attribution (not generic mentions of creators).
        for match in re.finditer(r"(?i)(thanks\s+)(?P<handle>@(?:\[[^\]]+\]\s*)?[^\n,()]{2,80}?)(?=\s+for\s+creat(?:ing|ed))", message.content):
            handle = clean_handle(match.group("handle"))
            person = person_name_from_handle(handle)
            identity_id = mention_ids.get(handle) or add_identity(person, message, handle, "explicit_third_party_attribution")
            add_relationship(identity_id, person, "contributed_as", "role", "creator", message,
                             "explicit_third_party_attribution", match.group(0), "high", "creator_or_builder")

        # Direct self-identification statements receive their own evidence class.
        if message.display_name:
            for match in re.finditer(r"(?i)\bI(?:'m| am)\s+(?:the\s+)?(founder|officer|organizer|builder|creator|diplomat|competitor|leader)\s+(?:of|for|at)\s+([A-Z][^.!?\n]{1,80})", message.content):
                identity_id = add_identity(message.display_name, message, message.display_name, "direct_self_identification", message.author_id)
                role, organization = match.group(1).casefold(), clean_space(match.group(2))
                add_relationship(identity_id, message.display_name, "served_as", "organization", organization, message,
                                 "direct_self_identification", match.group(0), "high", role)

        # Competition placements are parsed in a dedicated typed pass after
        # organization resolution. No generic placement line creates a guild.

        # Conservative dated guild transition extraction.
        transition = re.search(r"(?i)\b([^.!?\n]{2,80}?)\s+(renamed|merged|split|became|succeeded)\s+(?:into|from|as|by|to)?\s*([^.!?\n]{2,80})", message.content)
        if transition:
            left, verb, right = clean_space(transition.group(1)), transition.group(2).casefold(), clean_space(transition.group(3))
            left_entry, right_entry = organization_by_term.get(normalized(left)), organization_by_term.get(normalized(right))
            if not left_entry or not right_entry:
                continue
            relationships.append({
                "relationship_id": stable_id("REL", f"{message.source_id}:{transition.group(0)}"),
                "subject_id": stable_id("ORG", normalized(left_entry["canonical_name"])),
                "subject_name": left_entry["canonical_name"],
                "predicate": {"renamed": "renamed_to", "merged": "merged_into", "split": "split_into", "became": "became", "succeeded": "succeeded_by"}[verb],
                "object_type": right_entry["entity_type"],
                "object_name": right_entry["canonical_name"],
                "valid_at": message.timestamp,
                "confidence": "medium",
                "evidence_channel": "archive_evidence",
                "evidence": [evidence(message, transition.group(0), "explicit_third_party_attribution")],
            })

    # Ensure every seeded person is discoverable even when unresolved.
    for entry in alias_registry["entries"]:
        if entry["entity_type"] != "person":
            continue
        canonical = entry["canonical_name"]
        identity_id = stable_id("PERSON", f"confirmed:{normalized(canonical)}") if entry["identity_merge_authorized"] else stable_id("PERSON", f"seed:{normalized(canonical)}")
        if not any(normalized(record["canonical_handle"]) == normalized(canonical) for record in identities.values()):
            identities[identity_id] = {
                "identity_id": identity_id,
                "record_type": "resolved_person_identity" if entry["identity_merge_authorized"] else "seeded_unresolved_identity",
                "canonical_handle": canonical,
                "preferred_display_name": canonical,
                "author_ids": [],
                "observed_handles": [],
                "confirmed_aliases": entry["confirmed_aliases"],
                "alias_basis": entry["alias_basis"],
                "roles": [],
                "operator_confirmed_roles": [],
                "first_seen": None,
                "last_seen": None,
                "evidence": entry["evidence"],
                "operator_confirmations": [entry["operator_confirmation"]] if entry.get("operator_confirmation") else [],
                "identity_confidence": "operator_confirmed_alias" if entry["identity_merge_authorized"] else "seeded_unresolved",
            }

    operator_roles = {
        "Funcracker": [
            ("co-founder of Aephia", "co_founder_of", "guild", "Aephia", "guild_founder", None),
            ("community creator", "contributed_as", "role", "community creator", "creator_or_builder", None),
        ],
        "Prometheus": [
            ("co-founder of Aephia", "co_founder_of", "guild", "Aephia", "guild_founder", None),
        ],
        "Eoganacht": [
            ("founder of BULK", "founder_of", "guild", "BULK", "guild_founder", None),
            ("leader of BULK", "leader_of", "guild", "BULK", "guild_leader", AS_OF),
        ],
        "Santi": [
            ("Head of Star Atlas Community", "served_as", "official_team", "Head of Star Atlas Community", "official_team_member", None),
        ],
        "Jose": [
            ("creator and steward of Star Atlas lore", "contributed_as", "role", "Star Atlas lore creator", "creator_or_builder", None),
        ],
        "Dom": [
            ("Star Atlas team member responsible for community events", "served_as", "role", "community events team member", "community_organizer", None),
        ],
        "Jindo": [
            ("Star Atlas moderator", "served_as", "role", "Star Atlas moderator", "moderator", None),
        ],
        "Suhail": [
            ("Star Atlas moderator", "served_as", "role", "Star Atlas moderator", "moderator", None),
        ],
        "Bohdi": [
            ("member of Aephia", "member_of", "guild", "Aephia", "guild_member", None),
            ("major Ustur player", "contributed_as", "role", "major Ustur player", "competitor", None),
            ("mega-whale asset holder", "known_as", "role", "mega-whale", "historically_significant_member", None),
        ],
        "Witticus": [("co-founder of Rome", "co_founder_of", "guild", "Rome", "guild_founder", None)],
        "ReyVeezy": [("co-founder of Rome", "co_founder_of", "guild", "Rome", "guild_founder", None)],
        "FancyHat": [
            ("co-founder of Rome", "co_founder_of", "guild", "Rome", "guild_founder", None),
            ("former member of Rome", "former_member_of", "guild", "Rome", "guild_member", None),
        ],
        "King Bryan": [
            ("member of Rome", "member_of", "guild", "Rome", "guild_member", None),
            ("former member of Guardians of the Galaxy", "former_member_of", "guild", "Guardians of the Galaxy", "guild_member", None),
        ],
        "Hakmer": [("member of Coexist", "member_of", "guild", "Coexist", "guild_member", None)],
        "Lerinor": [("member of Aephia", "member_of", "guild", "Aephia", "guild_member", None)],
        "Atlas Theory": [("long-standing Star Atlas content creator", "contributed_as", "role", "Star Atlas content creator", "creator_or_builder", None)],
        "DrumCarlos": [
            ("member of Polaris Fuel", "affiliated_with", "community_organization", "Polaris Fuel", "community_organization_member", None),
            ("Star Atlas DAO Council member", "served_as", "organization", "Star Atlas DAO Council", "dao_council_service", None),
        ],
        "Xcode": [
            ("founder of Deep Profits", "founder_of", "guild", "Deep Profits", "guild_founder", None),
            ("Star Atlas Lead Project Manager", "served_as", "official_team", "Lead Project Manager", "official_team_member", AS_OF),
            ("Star Atlas developer", "contributed_as", "role", "developer", "creator_or_builder", AS_OF),
        ],
        "BTH 2620": [("Star Atlas YouTube content creator", "contributed_as", "role", "YouTube content creator", "creator_or_builder", None)],
        "ODVB": [
            ("creator of Star Atlas TV", "creator_of", "community_organization", "Star Atlas TV", "creator_or_builder", None),
            ("recorder of Star Atlas community events", "contributed_as", "role", "community event recorder", "creator_or_builder", None),
        ],
        "Ryden": [("creator of EveEye, now Ryden Systems", "creator_of", "community_organization", "Ryden Systems", "creator_or_builder", None)],
        "MagicPuncher": [("Star Atlas gameplay engineer", "served_as", "official_team", "Gameplay Engineer", "official_team_member", None)],
    }
    for preferred, roles in operator_roles.items():
        identity = next(record for record in identities.values() if normalized(record["canonical_handle"]) == normalized(preferred))
        confirmation = operator_evidence("Confirmed by repository operator during PR review", "operator_confirmed_alias")
        for label, predicate, object_type, object_name, role_dimension, valid_at in roles:
            if role_dimension not in identity["operator_confirmed_roles"]:
                identity["operator_confirmed_roles"].append(role_dimension)
            relationships.append({
                "relationship_id": stable_id("REL", f"operator:{preferred}:{predicate}:{object_name}"),
                "subject_id": identity["identity_id"], "subject_name": preferred,
                "predicate": predicate, "object_type": object_type, "object_name": object_name,
                "valid_at": valid_at, "confidence": "operator_confirmed",
                "evidence_channel": "operator_confirmation", "evidence": [],
                "operator_confirmation": confirmation, "operator_assertion": True,
                "review_note": f"Operator-confirmed role: {label}. Archive corroboration remains separate.",
            })

    # Public community awards are archive-backed claims from the 2025 Joni
    # announcement. They remain distinct from operator-confirmed context.
    award_message = next((message for message in messages if message.source_id == "SA-DISCORD-ANN-7B4E108B64E5B830"), None)
    award_claims = {
        "Jindo": ("Community Helper of the Year", "Community Helper of the Year: @Jindo | Star Atlas Mod"),
        "Neo_AArmstrong": ("Community Member of the Year", "COMMUNITY MEMBER OF THE YEAR: @[Λ] Neo_AArmstrong [EC]"),
        "BTH 2620": ("Content Creator of the Year", "Content Creator of the Year: @beyondthehorizon2620"),
        "Hakmer": ("Best Gunplay Player of the Year", "Best Gunplay Player of the Year @[COEX] Hakmer"),
        "Lerinor": ("Most Knowledgeable Member of the Year", "Most Knowledgeable Member of the Year: @[AEP] Lerinor"),
        "Ryden": ("Best Community Tool of the Year (EveEye)", "Best Community Tool of the Year: Eveeye ( @Ryden )"),
        "ODVB": ("Star Atlas IP Project / Business of the Year (Star Atlas TV)", "Star Atlas IP Project / Business of the Year: Star Atlas TV ( @odvb )"),
        "Atlas Theory": ("Most Entertaining Video of the Year (The Star Atlas Summit Experience)", "Most Entertaining Video of the Year: The Star Atlas Summit Experience ( @Atlas Theory @Shaddix1 | Star Atlas Mod )"),
    }
    if award_message:
        for preferred, (award, quote) in award_claims.items():
            identity = next(record for record in identities.values() if normalized(record["canonical_handle"]) == normalized(preferred))
            relationships.append({
                "relationship_id": stable_id("REL", f"{award_message.source_id}:{preferred}:{award}"),
                "subject_id": identity["identity_id"], "subject_name": preferred,
                "predicate": "received_award", "object_type": "community_award", "object_name": award,
                "valid_at": award_message.timestamp, "confidence": "high",
                "evidence_channel": "archive_evidence",
                "evidence": [evidence(award_message, quote, "explicit_third_party_attribution")],
            })

    archive_context_claims = [
        ("SA-DISCORD-ANN-4680CBB3330347DA", "Jose", "contributed_to", "creative_domain", "Star Atlas lore", "Our next episode of Atlas Brew will be about LORE!", "explicit_third_party_attribution", "medium", "creator_or_builder"),
        ("SA-DISCORD-ANN-68752D6112C7FC1D", "Dom", "announced_event", "community_event", "Council of Peace Assembly (COPA)", "CALLING ALL GUILDS AND GUILD LEADERS", "observed_authorship", "medium", None),
        ("SA-DISCORD-ANN-2380EB26CAD5D8DA", "MagicPuncher", "served_as", "official_team", "Gameplay Engineer", "gameplay engineer, @MagicPuncher", "explicit_third_party_attribution", "high", "official_team_member"),
    ]
    message_by_source = {message.source_id: message for message in messages}
    for source_id, preferred, predicate, object_type, object_name, quote, attribution, confidence, role in archive_context_claims:
        message = message_by_source.get(source_id)
        if not message:
            continue
        identity = next(record for record in identities.values() if normalized(record["canonical_handle"]) == normalized(preferred))
        relationships.append({
            "relationship_id": stable_id("REL", f"{source_id}:{preferred}:{predicate}:{object_name}"),
            "subject_id": identity["identity_id"], "subject_name": preferred,
            "predicate": predicate, "object_type": object_type, "object_name": object_name,
            "valid_at": message.timestamp, "confidence": confidence,
            "evidence_channel": "archive_evidence", "evidence": [evidence(message, quote, attribution)],
        })
        if role and confidence == "high" and role not in identity["roles"]:
            identity["roles"].append(role)

    operator_context = [
        ("Rome", "guild", "produced", "community_show", "Metaverse Nomads Show", "Rome produced the Metaverse Nomads Show."),
        ("Rome", "guild", "had_dispute_over", "negotiation", "MUD Empire negotiations", "A disagreement over Rome negotiations with MUD Empire preceded deletion of the show and original Rome Discord."),
        ("Rome", "guild", "succeeded_community_space_with", "community_space", "new Rome Discord", "A new Rome Discord succeeded the deleted original community space; exact dates remain unresolved."),
        ("Bohdi", "person", "had_public_community_conflict_with", "guild", "Rome", "Operator-confirmed community conflict; archive corroboration and dates remain unresolved."),
        ("Bohdi", "person", "had_public_community_conflict_with", "person", "King Bryan", "Operator-confirmed community conflict; archive corroboration and dates remain unresolved."),
        ("Witticus", "person", "has_public_activity_status", "status", "out of the public eye", "Operator-reported current public activity status; no private information is added."),
        ("ReyVeezy", "person", "has_public_activity_status", "status", "out of the public eye", "Operator-reported current public activity status; no private information is added."),
        ("BTH 2620", "person", "has_activity_status", "status", "inactive", "Currently inactive; operator reports the creator's YouTube content was copyright restricted."),
        ("Xcode", "person", "transitioned_from", "community_role", "Star Atlas community member", "Career progression context: community member and DEEP founder before joining the Star Atlas team."),
    ]
    for subject_name, subject_type, predicate, object_type, object_name, note in operator_context:
        if subject_type == "person":
            subject = next(record for record in identities.values() if normalized(record["canonical_handle"]) == normalized(subject_name))
            subject_id = subject["identity_id"]
        else:
            subject_id = stable_id("ORG", normalized(subject_name))
        relationships.append({
            "relationship_id": stable_id("REL", f"operator:{subject_name}:{predicate}:{object_name}"),
            "subject_id": subject_id, "subject_name": subject_name,
            "predicate": predicate, "object_type": object_type, "object_name": object_name,
            "valid_at": None, "confidence": "operator_confirmed",
            "evidence_channel": "operator_confirmation", "evidence": [],
            "operator_confirmation": operator_evidence("Confirmed by repository operator during PR review"),
            "operator_assertion": True, "review_note": note,
        })

    organizations = []
    for entry in alias_registry["entries"]:
        if entry["entity_type"] == "person":
            continue
        canonical = entry["canonical_name"]
        refs = entry["evidence"]
        dated = sorted(ref["timestamp"] for ref in refs if ref.get("timestamp"))
        organization_relationships = [r["relationship_id"] for r in relationships if normalized(r["object_name"]) == normalized(canonical)]
        organization_relationships += [r["relationship_id"] for r in relationships if normalized(r["subject_name"]) == normalized(canonical)]
        organizations.append({
            "organization_id": stable_id("ORG", normalized(canonical)),
            "guild_id": stable_id("GUILD", normalized(canonical)) if entry["entity_type"] == "guild" else None,
            "canonical_name": canonical,
            "entity_type": entry["entity_type"],
            "aliases": entry["aliases"],
            "meaning": entry.get("meaning"),
            "first_seen": dated[0] if dated else None,
            "last_seen": dated[-1] if dated else None,
            "relationship_ids": sorted(set(organization_relationships)),
            "evidence": refs,
            "operator_confirmation": entry.get("operator_confirmation"),
            "status": "evidence_supported" if refs else entry["resolution_status"].casefold(),
        })

    for record in identities.values():
        record["author_ids"].sort()
        record["observed_handles"].sort(key=text_sort_key)
        record["confirmed_aliases"].sort(key=text_sort_key)
        record["roles"].sort()
        record["operator_confirmed_roles"].sort()
        seen_refs = {}
        for ref in record["evidence"]:
            seen_refs[(ref["source_id"], ref["quoted_text"], ref["attribution_class"])] = ref
        record["evidence"] = list(seen_refs.values())
    relationships.sort(key=lambda r: (r.get("valid_at") or "", r["relationship_id"]))
    organizations.sort(key=lambda item: (item["canonical_name"].casefold(), item["organization_id"]))
    return sorted(identities.values(), key=lambda r: (r["canonical_handle"].casefold(), r["identity_id"])), organizations, relationships


def promotion_candidates(identities: list[dict[str, Any]], organizations: list[dict[str, Any]], relationships: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = []
    rel_by_subject: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for relationship in relationships:
        rel_by_subject[relationship["subject_id"]].append(relationship)
    for identity in identities:
        identity_key = normalized(identity["canonical_handle"])
        if identity_key in PROMOTION_IGNORED_HANDLES | PUBLICLY_EXCLUDED_HANDLES | NON_PERSON_HANDLES:
            continue
        refs = identity["evidence"]
        source_ids = {ref["source_id"] for ref in refs if ref.get("source_id")}
        authors = {ref.get("display_name") for ref in refs if ref.get("display_name")}
        rels = rel_by_subject[identity["identity_id"]]
        archive_roles = set(identity["roles"])
        operator_roles = set(identity["operator_confirmed_roles"])
        role_set = archive_roles | operator_roles
        dimensions = {
            "guild_founder": int("guild_founder" in role_set),
            "guild_leader": int("guild_leader" in role_set),
            "guild_officer": int("guild_officer" in role_set or "officer" in role_set),
            "alliance_leader": int("alliance_leader" in role_set),
            "dao_council_service": int("dao_council_service" in role_set),
            "official_team_member": int("official_team_member" in role_set),
            "creator_or_builder": int(bool(role_set & {"creator_or_builder", "builder", "creator"})),
            "community_organizer": int(bool(role_set & {"community_organizer", "organizer"})),
            "historical_significance": min(5, len(rels)),
            "identity_confidence": 3 if identity["alias_basis"] == "operator_confirmed" else (2 if identity["author_ids"] else 1),
            "evidence_strength": 3 if any(ref["attribution_class"] == "direct_self_identification" for ref in refs) else (2 if len(authors) >= 2 else (1 if source_ids else 0)),
        }
        substantive = bool(role_set or rels)
        if identity_key in PROMOTION_APPROVED_HANDLES:
            status = "OPERATOR_APPROVED_FOR_PROMOTION"
        elif identity_key in PROMOTION_DEFERRED_HANDLES:
            status = "DEFERRED"
        elif identity["identity_confidence"] == "seeded_unresolved":
            status = "REQUIRES_IDENTITY_RESOLUTION"
        elif substantive and (dimensions["evidence_strength"] >= 2 or operator_roles):
            status = "READY_FOR_HUMAN_PROMOTION_REVIEW"
        elif substantive:
            status = "REQUIRES_ROLE_CORROBORATION"
        elif source_ids:
            status = "EVIDENCE_SUPPORTED_PROFILE_CANDIDATE"
        else:
            status = "DISCOVERY_ONLY"
        candidates.append({
            "entity_type": "person", "entity_id": identity["identity_id"], "name": identity["canonical_handle"],
            "review_status": status, "score_dimensions": dimensions,
            "archive_roles": sorted(archive_roles), "operator_confirmed_roles": sorted(operator_roles),
            "operator_decision": "promotion_approved" if identity_key in PROMOTION_APPROVED_HANDLES else ("deferred_pending_identity_resolution" if identity_key in PROMOTION_DEFERRED_HANDLES else None),
            "independent_message_count": len(source_ids), "independent_author_count": len(authors),
            "council_service_excluded_from_guild_leadership": True,
            "evidence": refs[:25], "operator_confirmations": identity["operator_confirmations"],
        })
    for organization in organizations:
        if organization["entity_type"] == "software_agent":
            continue
        refs = organization["evidence"]
        source_ids = {ref["source_id"] for ref in refs if ref.get("source_id")}
        status = "EVIDENCE_SUPPORTED_PROFILE_CANDIDATE" if len(source_ids) >= 2 and organization["entity_type"] != "unresolved_tag" else ("REQUIRES_IDENTITY_RESOLUTION" if organization["entity_type"] == "unresolved_tag" else "DISCOVERY_ONLY")
        candidates.append({
            "entity_type": organization["entity_type"], "entity_id": organization["organization_id"],
            "name": organization["canonical_name"], "review_status": status,
            "score_dimensions": {"historical_significance": min(5, len(organization["relationship_ids"])), "identity_confidence": 3 if organization.get("operator_confirmation") else 1, "evidence_strength": 2 if len(source_ids) >= 2 else (1 if source_ids else 0)},
            "independent_message_count": len(source_ids), "evidence": refs[:25],
            "operator_confirmation": organization.get("operator_confirmation"),
        })
    candidates.sort(key=lambda item: (item["review_status"], item["name"].casefold(), item["entity_id"]))
    return {
        "schema_version": SCHEMA_VERSION, "campaign_id": CAMPAIGN_ID,
        "decision_boundary": "Review-oriented discovery only; no automated candidate is promoted into canonical knowledge.",
        "allowed_review_statuses": sorted(REVIEW_STATUSES), "candidates": candidates,
    }


def tag_registry(messages: list[Message]) -> dict[str, Any]:
    entries = {entry["tag"].casefold(): dict(entry) for entry in TAG_REGISTRY_SEEDS}
    for message in messages:
        for handle in extract_mentions(message.content):
            match = re.match(r"@?\[([^\]]+)\]", handle)
            if match and match.group(1).casefold() not in entries:
                tag = match.group(1)
                entries[tag.casefold()] = {
                    "tag": tag, "canonical_entity": tag, "entity_type": "unresolved_tag",
                    "resolution_status": "HUMAN_REVIEW_REQUIRED", "resolution_basis": "observed_display_tag_only",
                }
    return {"schema_version": SCHEMA_VERSION, "campaign_id": CAMPAIGN_ID, "entries": sorted(entries.values(), key=lambda item: item["tag"].casefold())}


def event_name(content: str) -> str | None:
    if re.search(r"\bCOPA\b|Council of Peace Assembly", content, re.I):
        return "Council of Peace Assembly (COPA)"
    if re.search(r"Color The Stars", content, re.I):
        return "Color The Stars"
    if re.search(r"Tufa Attack", content, re.I):
        return "Tufa Attack Tournament"
    if re.search(r"CORE Trivia", content, re.I):
        return "CORE Trivia"
    return None


def extract_competition_records(messages: list[Message], alias_registry: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    organization_terms = {
        term: entry for entry in alias_registry["entries"] if entry["entity_type"] != "person"
        for term in entry["normalized_terms"]
    }
    person_terms = {
        term: entry for entry in alias_registry["entries"] if entry["entity_type"] == "person"
        for term in entry["normalized_terms"]
    }
    records, relationships, reviews = [], [], []
    pattern = re.compile(r"(?i)(?<!\w)(1st|2nd|3rd)(?:\s+Place)?\s*[-:]\s*([^,\r\n]+)")
    for message in messages:
        for match in pattern.finditer(message.content):
            placement = {"1st": 1, "2nd": 2, "3rd": 3}[match.group(1).casefold()]
            raw_value = clean_space(match.group(2)).strip(" .")
            participant = re.sub(r"\s*\([^)]*\)\s*$", "", raw_value).strip()
            looks_like_prize = bool(re.search(r"\$|\b(?:prize|tier|origination price|receive|poster|land)\b", raw_value, re.I)) and not re.search(r"\b(?:winner|congratulations)\b", message.content, re.I)
            organization = organization_terms.get(normalized(participant))
            person = person_terms.get(normalized(participant))
            if looks_like_prize:
                participant_type, status, category, prize = "unresolved", "REVIEW_REQUIRED_PRIZE_OR_CATEGORY", raw_value, raw_value
            elif organization:
                participant_type, status, category, prize = organization["entity_type"], "RESOLVED", None, None
            elif person:
                participant_type, status, category, prize = "individual", "RESOLVED", None, None
            else:
                participant_type, status, category, prize = "unresolved", "REVIEW_REQUIRED_PARTICIPANT_TYPE", None, None
            competition_id = stable_id("COMP", f"{message.source_id}:{match.start()}:{raw_value}")
            record = {
                "competition_record_id": competition_id, "source_id": message.source_id,
                "event": event_name(message.content), "placement": placement,
                "participant": participant if not looks_like_prize else None,
                "participant_type": participant_type, "category": category, "prize": prize,
                "unresolved_text": raw_value if status != "RESOLVED" else None,
                "resolution_status": status, "timestamp": message.timestamp,
                "evidence": [evidence(message, match.group(0), "explicit_third_party_attribution")],
            }
            records.append(record)
            if status == "RESOLVED":
                entity_name = organization["canonical_name"] if organization else person["preferred_display_name"]
                entity_id = stable_id("ORG", normalized(entity_name)) if organization else stable_id("PERSON", f"confirmed:{normalized(entity_name)}")
                relationships.append({
                    "relationship_id": stable_id("REL", f"competition:{competition_id}"),
                    "subject_id": entity_id, "subject_name": entity_name,
                    "predicate": "placed_in_competition", "object_type": "event",
                    "object_name": record["event"] or "UNRESOLVED_EVENT", "valid_at": message.timestamp,
                    "confidence": "high" if record["event"] else "medium", "evidence_channel": "archive_evidence",
                    "evidence": record["evidence"], "placement": placement,
                })
            else:
                reviews.append({
                    "review_type": "malformed_competition_result" if looks_like_prize else "unresolved_participant_type",
                    "subject": participant or raw_value, "observed_values": [raw_value],
                    "candidate_resolution": None, "confidence": "LOW", "evidence": record["evidence"],
                    "reason_human_review_required": "Placement-like text is a prize/category fragment." if looks_like_prize else "Participant is not a resolved person or reviewed organization.",
                    "allowed_decisions": ["RESOLVE_PARTICIPANT", "CLASSIFY_AS_PRIZE_OR_CATEGORY", "REJECT_EXTRACTION", "DEFER"],
                })
    records.sort(key=lambda item: (item["timestamp"] or "", item["competition_record_id"]))
    relationships.sort(key=lambda item: (item["valid_at"] or "", item["relationship_id"]))
    return records, relationships, reviews


def month_range(first_month: str, last_month: str) -> list[str]:
    year, month = map(int, first_month.split("-"))
    end_year, end_month = map(int, last_month.split("-"))
    values = []
    while (year, month) <= (end_year, end_month):
        values.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            year, month = year + 1, 1
    return values


def build_channel_coverage(messages: list[Message], inventory: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    dated = sorted((message for message in messages if message.timestamp and re.match(r"^\d{4}-\d{2}", message.timestamp)), key=lambda item: (item.timestamp or "", item.source_id))
    timestamps = [message.timestamp for message in dated]
    represented_months = sorted({value[:7] for value in timestamps})
    expected_months = month_range(represented_months[0], represented_months[-1]) if represented_months else []
    missing_months = sorted(set(expected_months) - set(represented_months))
    years = sorted({month[:4] for month in represented_months})
    observed_names = sorted({message.observed_channel_name for message in messages if message.observed_channel_name}, key=text_sort_key)
    all_paths = sorted({path for message in messages for path in message.source_paths})
    anchor_paths = [path for path in all_paths if path.endswith("star-atlas-discord-announcements.md") or path.endswith("messages.jsonl")]
    anchor_paths.append("archive/normalized/discord-announcements/messages/")
    collection_notes = sorted({note for message in messages for note in message.collection_notes})
    no_text_count = sum(clean_space(message.content).casefold() == "[no text content]" for message in messages)
    coverage_id = stable_id("DISCORD-COVERAGE", "archive/raw/discord-announcements/star-atlas-discord-announcements.md")
    entry = {
        "coverage_id": coverage_id,
        "server_or_community_name": "Star Atlas Discord (repository-designated; native server unresolved)",
        "native_server_id": None, "server_identity_status": "REPOSITORY_DESIGNATED_NATIVE_IDENTITY_UNRESOLVED",
        "canonical_channel_name": None, "repository_designated_channel_name": "announcements",
        "observed_channel_names": observed_names, "channel_category": "announcements",
        "channel_identity_basis": "repository collection path plus raw export header; no native channel ID",
        "source_paths": anchor_paths, "formats": ["json", "jsonl", "md"],
        "earliest_message_timestamp": timestamps[0] if timestamps else None,
        "earliest_message_source_id": dated[0].source_id if dated else None,
        "latest_message_timestamp": timestamps[-1] if timestamps else None,
        "latest_message_source_id": dated[-1].source_id if dated else None,
        "message_count": len(messages), "months_present": represented_months,
        "years_present": years, "missing_months": missing_months,
        "missing_month_interpretation": "INDETERMINATE_NO_EXPORT_EVIDENCE" if missing_months else "NO_INTERNAL_MONTH_GAPS_OBSERVED_NOT_A_COMPLETENESS_CLAIM",
        "coverage_status": "UNRESOLVED_CHANNEL", "temporal_freshness": "ACTIVE_CURRENT_TO_LAST_CAPTURE",
        "historical_completeness": "PARTIAL_ACQUISITION_RUNTIME_LIMIT_REACHED",
        "last_ingested_archive_message": {"source_id": dated[-1].source_id, "timestamp": timestamps[-1]} if dated else None,
        "native_channel_id": None, "native_message_ids_present": False, "native_author_ids_present": False,
        "timezone_status": "OFFSET_NOT_CAPTURED", "collection_complete": False,
        "notes": collection_notes + ["All represented months contain at least one message; this does not prove complete monthly history."],
    }
    parsed_occurrences = sum(item["parsed_message_occurrences"] for item in inventory if item["ingested"])
    representations = {
        "raw_aggregate_exports": sum(item["path"].startswith("archive/raw/") and item["parsed_message_occurrences"] > 1 for item in inventory),
        "normalized_aggregate_exports": sum(item["path"].endswith("messages.jsonl") for item in inventory),
        "normalized_per_message_files": sum("/messages/" in item["path"] and item["format"] == "json" for item in inventory),
        "derived_indexes": sum(item["path"].endswith("announcement-index.csv") for item in inventory),
    }
    coverage = {
        "schema_version": SCHEMA_VERSION, "campaign_id": CAMPAIGN_ID,
        "scope_statement": "Rolling coverage ledger for imported exports; not a completed Discord corpus declaration.",
        "supported_coverage_statuses": sorted(COVERAGE_STATUSES),
        "supported_channel_categories": sorted(CHANNEL_CATEGORIES),
        "summary": {
            "source_files_inventoried": len(inventory), "independent_export_units": 1,
            "parsed_message_occurrences": parsed_occurrences, "unique_messages": len(messages),
            "repository_designated_communities": 1, "native_servers_identified": 0,
            "canonical_native_channels_identified": 0, "unresolved_channel_exports": 1,
            "earliest_message_timestamp": timestamps[0] if timestamps else None,
            "latest_message_timestamp": timestamps[-1] if timestamps else None,
            "internal_month_gaps": len(missing_months), "representation_counts": representations,
        },
        "channels": [entry],
    }
    gap_report = {
        "schema_version": SCHEMA_VERSION, "campaign_id": CAMPAIGN_ID,
        "channel_gap_count": len(missing_months), "unresolved_channel_exports": 1,
        "gaps": [{
            "coverage_id": coverage_id, "missing_months": missing_months,
            "partial_years": [years[0], years[-1]] if years else [],
            "zero_message_months": [], "months_without_available_export": missing_months,
            "findings": [
                "Native channel and server identity are unresolved.",
                "Historical acquisition reached its 180-minute limit before the requested start time.",
                "All native message, channel, and author IDs are absent.",
                "Message timestamps contain no captured timezone offset.",
                f"{no_text_count} no-text placeholders and attachment-only records require review.",
            ],
        }],
    }
    backlog = {
        "schema_version": SCHEMA_VERSION, "campaign_id": CAMPAIGN_ID,
        "items": [
            {"priority": "P0", "type": "missing_channel_identification", "target": "Imported announcements export", "required_artifact": "Native server/channel IDs and official channel-name export"},
            {"priority": "P0", "type": "historical_backfill", "target": "Imported announcements export before 2021-03-16", "required_artifact": "Completed history export reaching the requested start"},
        ] + [
            {"priority": "P1", "type": "mentioned_channel_not_imported", "target": name, "required_artifact": "Native channel export with message timestamps and IDs"}
            for name in ["Foundation Room", "Foundation Room Chat", "Foudnation Room", "Atlas Amphitheater", "Atlas Brew Lounge", "dao-announcements", "guild channels", "faction channels", "economics", "governance", "general", "support"]
        ] + [
            {"priority": "P1", "type": "empty_or_attachment_only_records", "target": f"{no_text_count} no-text placeholders", "required_artifact": "Attachment metadata or corrected export"},
            {"priority": "P2", "type": "native_identifiers", "target": "All imported messages", "required_artifact": "Privacy-reviewed ID-bearing export"},
        ],
    }
    backlog["items"] = sorted(backlog["items"], key=lambda item: (item["priority"], item["type"], item["target"].casefold()))
    return coverage, gap_report, backlog


def build_human_resolution_queue(duplicate_reviews: list[dict[str, Any]], alias_conflicts: list[dict[str, Any]], tags: dict[str, Any], organizations: list[dict[str, Any]], relationships: list[dict[str, Any]], competition_reviews: list[dict[str, Any]], coverage: dict[str, Any]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    def add(review_type: str, subject: str, observed_values: list[Any], candidate: Any, confidence: str, evidence_refs: list[dict[str, Any]], reason: str, decisions: list[str]) -> None:
        items.append({
            "review_id": stable_id("REVIEW", f"{review_type}:{subject}:{json.dumps(observed_values, sort_keys=True, ensure_ascii=False)}"),
            "review_type": review_type, "subject": subject, "observed_values": observed_values,
            "candidate_resolution": candidate, "confidence": confidence, "evidence": evidence_refs,
            "reason_human_review_required": reason, "allowed_decisions": decisions,
            "operator_decision": None, "decision_status": "OPEN",
        })
    for item in duplicate_reviews:
        add("likely_duplicate_message", item["source_id"], item["observed_contents"], None, "LOW", [], item["reason_human_review_required"], ["MERGE_AS_SAME_MESSAGE", "KEEP_DISTINCT", "DEFER"])
    for item in alias_conflicts:
        if item.get("type") == "unresolved_similarity":
            add("possible_alias", item["observed_handle"], [item["seeded_name"], item["observed_handle"]], item["seeded_name"], "LOW", [], "Fuzzy resemblance is not identity evidence.", ["CONFIRM_ALIAS", "REJECT_ALIAS", "DEFER"])
    for entry in tags["entries"]:
        if entry["resolution_status"] == "HUMAN_REVIEW_REQUIRED":
            add("unknown_display_tag", entry["tag"], [entry["tag"]], None, "LOW", [], "Display tag has no confirmed organization classification.", ["RESOLVE_TAG", "MARK_INFORMAL", "REJECT_ORGANIZATION", "DEFER"])
    for organization in organizations:
        if organization["entity_type"] == "unresolved_tag":
            add("uncertain_organization_type", organization["canonical_name"], [organization["canonical_name"], *organization["aliases"]], None, "LOW", organization["evidence"][:5], "Organization type is not confirmed.", ["GUILD", "GUILD_ALLIANCE", "COMMUNITY_ORGANIZATION", "INFORMAL_GROUP", "NOT_AN_ORGANIZATION", "DEFER"])
    confirmed_memberships = {
        (normalized(relation["subject_name"]), normalized(relation["object_name"]))
        for relation in relationships if relation["predicate"] == "member_of" and relation.get("evidence_channel") == "operator_confirmation"
    }
    for relation in relationships:
        if relation["predicate"] == "possible_member_of":
            if (normalized(relation["subject_name"]), normalized(relation["object_name"])) in confirmed_memberships:
                continue
            add("possible_guild_membership", relation["subject_name"], [relation["object_name"]], relation["object_name"], "LOW", relation["evidence"], "Display-name tag is association evidence, not confirmed membership.", ["CONFIRM_MEMBERSHIP", "ASSOCIATION_ONLY", "REJECT", "DEFER"])
    for item in competition_reviews:
        add(item["review_type"], item["subject"], item["observed_values"], item["candidate_resolution"], item["confidence"], item["evidence"], item["reason_human_review_required"], item["allowed_decisions"])
    for target in ["Agent Solace", "The Vanguard", "Virtuwaal"]:
        add("seeded_unresolved_identity_or_organization", target, [target], None, "UNKNOWN", [], "Seeded by operator for the next resolution pass; no resolution is manufactured.", ["RESOLVE", "REJECT", "DEFER"])
    add("deferred_identity_resolution", "Chri.z", ["Chri.z", "Chris"], None, "LOW", [], "Operator reported insufficient context; the economics-team identity hypothesis remains unresolved.", ["RESOLVE_WITH_EVIDENCE", "REJECT", "DEFER"])
    add("deferred_promotion", "Shaddix", ["Shaddix1 | Star Atlas Mod"], None, "UNKNOWN", [], "Operator explicitly deferred this candidate.", ["RESOLVE", "REJECT", "DEFER"])
    add("spelling_conflict", "Virtuwaal / Virtuwuul", ["Virtuwaal", "Virtuwuul"], None, "LOW", [], "The supplied Rome-conflict context used a spelling that differs from the seeded handle; no alias merge is made from similarity alone.", ["CONFIRM_ALIAS", "KEEP_DISTINCT", "DEFER"])
    add("temporal_relationship_dates", "Rome guild history", ["original Discord deleted", "new Discord founded", "FancyHat left", "King Bryan joined"], None, "UNKNOWN", [], "Operator confirmed the sequence, but exact dates are not yet established from the available archive.", ["ADD_DATED_EVIDENCE", "ACCEPT_UNDATED_OPERATOR_CONTEXT", "DEFER"])
    if coverage["summary"]["unresolved_channel_exports"]:
        add("unresolved_channel_name", "Imported announcements export", coverage["channels"][0]["observed_channel_names"], "announcements", "MEDIUM", [], "Repository designation exists but native channel identity is absent.", ["CONFIRM_CANONICAL_CHANNEL", "RENAME", "DEFER"])
    add("source_gap", "Announcements historical lower bound", [coverage["summary"]["earliest_message_timestamp"]], None, "HIGH", [], "Acquisition runtime limit prevented complete historical backfill.", ["ACQUIRE_BACKFILL", "ACCEPT_PARTIAL", "DEFER"])
    items = sorted({item["review_id"]: item for item in items}.values(), key=lambda item: (item["review_type"], item["subject"].casefold(), item["review_id"]))
    return {"schema_version": SCHEMA_VERSION, "campaign_id": CAMPAIGN_ID, "item_count": len(items), "items": items}


def validate_outputs(messages: list[Message], alias_registry: dict[str, Any], identities: list[dict[str, Any]],
                     organizations: list[dict[str, Any]], relationships: list[dict[str, Any]], inventory: list[dict[str, Any]],
                     promotions: dict[str, Any] | None = None, tags: dict[str, Any] | None = None,
                     competition_records: list[dict[str, Any]] | None = None, coverage: dict[str, Any] | None = None,
                     human_queue: dict[str, Any] | None = None) -> dict[str, Any]:
    source_ids = {message.source_id for message in messages}
    all_claim_records: list[dict[str, Any]] = identities + organizations + relationships + (competition_records or [])
    unresolved_refs = []
    evidence_class_failures = []
    operator_channel_failures = []
    for record in all_claim_records:
        for ref in record.get("evidence", []):
            if ref.get("evidence_channel") == "archive_evidence" and ref.get("source_id") not in source_ids:
                unresolved_refs.append({"record": record.get("identity_id") or record.get("guild_id") or record.get("relationship_id"), "source_id": ref["source_id"]})
            if ref.get("attribution_class") not in EVIDENCE_CLASSES:
                evidence_class_failures.append(ref.get("attribution_class"))
            if ref.get("evidence_channel") == "operator_confirmation" and (ref.get("source_id") is not None or not ref.get("operator_assertion")):
                operator_channel_failures.append(record.get("identity_id") or record.get("relationship_id"))
        confirmation = record.get("operator_confirmation")
        if confirmation and (confirmation.get("evidence_channel") != "operator_confirmation" or confirmation.get("source_id") is not None or not confirmation.get("operator_assertion")):
            operator_channel_failures.append(record.get("identity_id") or record.get("organization_id") or record.get("relationship_id"))
    terms = defaultdict(list)
    for entry in alias_registry["entries"]:
        for term in entry["normalized_terms"]:
            terms[term].append(entry["canonical_name"])
    alias_collisions = {term: owners for term, owners in terms.items() if len(set(owners)) > 1}
    id_owners = defaultdict(set)
    for identity in identities:
        for author_id in identity["author_ids"]:
            id_owners[author_id].add(identity["identity_id"])
    merged_ids = {key: sorted(value) for key, value in id_owners.items() if len(value) > 1}
    undated_relationships = [r["relationship_id"] for r in relationships if r.get("evidence_channel") == "archive_evidence" and not r.get("valid_at")]
    missing_quotes = [
        ref["source_id"] for record in all_claim_records for ref in record.get("evidence", [])
        if not ref.get("quoted_text")
    ]
    duplicate_provenance_preserved = all(message.source_paths for message in messages)
    relationship_426 = [r["relationship_id"] for r in relationships if normalized(r.get("object_name")) == "426" and r.get("predicate") in {"member_of", "possible_member_of"}]
    bad_tag_memberships = [r["relationship_id"] for r in relationships if r.get("predicate") in {"member_of", "possible_member_of"} and r.get("object_type") != "guild"]
    ia_bad = [r["relationship_id"] for r in relationships if normalized(r.get("object_name")) == "ia" or (r.get("object_name") == "Intergalactic Alliance" and r.get("predicate") != "associated_with_alliance")]
    prize_false_positives = [r["relationship_id"] for r in relationships if "csstier" in normalized(r.get("subject_name"))]
    bare_promotions = [item["entity_id"] for item in (promotions or {}).get("candidates", []) if item.get("recommendation") == "promote" or item.get("review_status") not in REVIEW_STATUSES]
    council_score_failures = [item["entity_id"] for item in (promotions or {}).get("candidates", []) if item.get("score_dimensions", {}).get("dao_council_service") and any(item.get("score_dimensions", {}).get(key) for key in ("guild_founder", "guild_leader", "guild_officer")) and not set(item.get("operator_confirmed_roles", [])) & {"guild_founder", "guild_leader", "guild_officer"}]
    organization_types = [item["entity_type"] for item in organizations if item["entity_type"] not in ORGANIZATION_TYPES]
    coverage_dates_ok = True
    coverage_taxonomy_ok = True
    if coverage and messages:
        dated = sorted(message.timestamp for message in messages if message.timestamp and re.match(r"^\d{4}-\d{2}", message.timestamp))
        coverage_dates_ok = coverage["summary"]["earliest_message_timestamp"] == dated[0] and coverage["summary"]["latest_message_timestamp"] == dated[-1]
        coverage_taxonomy_ok = (
            set(coverage.get("supported_coverage_statuses", [])) == COVERAGE_STATUSES
            and set(coverage.get("supported_channel_categories", [])) == CHANNEL_CATEGORIES
            and all(item.get("coverage_status") in COVERAGE_STATUSES and item.get("channel_category") in CHANNEL_CATEGORIES for item in coverage.get("channels", []))
        )
    source_record_dir = Path(__file__).resolve().parents[3] / "archive/source-records/discord-announcements"
    source_record_reconciliation = True
    if source_record_dir.exists() and all(source_id.startswith("SA-DISCORD-ANN-") for source_id in source_ids):
        record_ids = {path.stem for path in source_record_dir.glob("*.json")}
        source_record_reconciliation = source_ids == record_ids
    checks = [
        {"name": "every_indexed_claim_resolves_to_source_message", "passed": not unresolved_refs, "details": unresolved_refs},
        {"name": "controlled_evidence_taxonomy", "passed": not evidence_class_failures, "details": sorted(set(evidence_class_failures))},
        {"name": "operator_confirmation_separate_from_archive_evidence", "passed": not operator_channel_failures, "details": operator_channel_failures},
        {"name": "aliases_non_circular_and_conflict_aware", "passed": not alias_collisions, "details": alias_collisions},
        {"name": "user_ids_not_merged_without_evidence", "passed": not merged_ids, "details": merged_ids},
        {"name": "archive_relationships_are_dated", "passed": not undated_relationships, "details": undated_relationships},
        {"name": "duplicate_messages_collapsed_with_provenance", "passed": duplicate_provenance_preserved, "details": {"unique_messages": len(messages), "source_occurrences": sum(i["parsed_message_occurrences"] for i in inventory if i["ingested"])}},
        {"name": "quoted_text_preserved", "passed": not missing_quotes, "details": missing_quotes},
        {"name": "organization_types_controlled", "passed": not organization_types, "details": organization_types},
        {"name": "community_meme_426_never_membership", "passed": not relationship_426, "details": relationship_426},
        {"name": "non_guild_tags_never_guild_membership", "passed": not bad_tag_memberships, "details": bad_tag_memberships},
        {"name": "ia_is_alliance_association", "passed": not ia_bad, "details": ia_bad},
        {"name": "competition_prize_fragments_not_participants", "passed": not prize_false_positives, "details": prize_false_positives},
        {"name": "review_oriented_promotion_statuses_only", "passed": not bare_promotions, "details": bare_promotions},
        {"name": "council_service_not_guild_leadership_evidence", "passed": not council_score_failures, "details": council_score_failures},
        {"name": "coverage_dates_derive_from_messages", "passed": coverage_dates_ok, "details": None},
        {"name": "coverage_status_and_channel_category_taxonomies", "passed": coverage_taxonomy_ok, "details": None},
        {"name": "source_ids_reconcile_to_source_records", "passed": source_record_reconciliation, "details": None},
        {"name": "human_resolution_queue_present", "passed": human_queue is None or human_queue.get("item_count", 0) > 0, "details": human_queue.get("item_count") if human_queue else "fixture_not_supplied"},
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "status": "pass" if all(check["passed"] for check in checks) else "fail",
        "checks": checks,
        "counts": {"sources": len(inventory), "unique_messages": len(messages), "identities": len(identities), "organizations": len(organizations), "guilds": sum(item["entity_type"] == "guild" for item in organizations), "relationships": len(relationships), "competition_records": len(competition_records or [])},
        "external_validation": {
            "json_and_jsonl_parse": "run validate_campaign.py",
            "regeneration_determinism": "run validate_campaign.py",
            "tests": "run validate_campaign.py",
            "git_diff_check": "run validate_campaign.py",
        },
    }


def serialize_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def serialize_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)


def curator_decisions() -> dict[str, Any]:
    """Return the durable human adjudications supplied for PR 21."""
    decisions = [
        (1, "Michael Wagner", "CONFIRMED", "SW4GNER/SW4GN3R variants resolve to Michael Wagner."),
        (2, "Santi", "CONFIRMED", "Santi was Head of Star Atlas Community."),
        (3, "Jose / ZeSKK", "CONFIRMED", "Jose, known as ZeSKK, created and expanded Star Atlas lore."),
        (4, "Dom / DominicVain", "CONFIRMED", "Dom was a Star Atlas team member responsible for community events."),
        (5, "Jindo", "CONFIRMED", "Star Atlas moderator; retain the archive-backed Community Helper of the Year award."),
        (6, "Suhail", "CONFIRMED", "SuhailDebar handle variants resolve to Suhail."),
        (7, "Funcracker", "PROMOTION_APPROVED", "Operator approved promotion."),
        (8, "Aephia", "CONFIRMED", "Aephia and AEP are the same guild; Funcracker and Prometheus are co-founders."),
        (9, "BULK", "CONFIRMED", "BULK is an armed-freighting guild founded and currently led by Eoganacht."),
        (10, "Bohdi", "CONFIRMED", "Bodhi/Bodhitree resolve to Bohdi; AEP member, major Ustur player, and mega-whale. Community-conflict claims remain operator-sourced."),
        (11, "Deleted User", "EXCLUDE_PUBLIC_ENTITY", "Exclude deleted-user tags and identity references; retain messages only as context for other public users."),
        (12, "Rome", "CONFIRMED", "Guild founded by Witticus, ReyVeezy, and FancyHat; preserve supplied show, Discord succession, departure, and membership history as operator context pending dates."),
        (13, "Hakmer / Coexist", "CONFIRMED", "Hakmer is associated with COEX, shorthand for the Turkish-based Coexist guild."),
        (14, "Lerinor", "CONFIRMED", "Lerinor is an AEP member."),
        (15, "Neo_AArmstrong / Eclypse", "CONFIRMED", "EC means Eclypse; retain the archive-backed Community Member of the Year award."),
        (16, "Atlas Theory", "CONFIRMED", "Long-standing Star Atlas content creator; supplied identity and role details confirmed."),
        (17, "Chri.z", "DEFERRED", "Insufficient context to resolve the possible Star Atlas economics-team identity."),
        (18, "DrumCarlos / Polaris Fuel", "CONFIRMED", "Use DrumCarlos; Polaris Fuel seeks to reduce fuel prices; DAO Council service confirmed."),
        (19, "The Club Guild", "CONFIRMED", "The Club is an alias for one of the original Star Atlas guilds."),
        (20, "Diego_Diaz08", "IGNORE", "Exclude from promotion review."),
        (21, "Prometheus", "CONFIRMED", "Co-founder of Aephia/AEP."),
        (22, "inti", "IGNORE", "Exclude from promotion review."),
        (23, "The Star Atlas AI App", "NOT_PROMOTABLE", "In-Discord software bot, not a person."),
        (24, "Xcode", "CONFIRMED", "Founder of Deep Profits [DEEP]; later hired by Star Atlas and now Lead Project Manager and Developer."),
        (25, "BTH 2620", "CONFIRMED_INACTIVE", "YouTube creator beyondthehorizon2620; Content Creator of the Year; currently inactive after copyright restrictions."),
        (26, "ODVB", "CONFIRMED", "Creator of Star Atlas TV and recorder of events represented by repository transcripts."),
        (27, "Ryden", "CONFIRMED", "Creator of EveEye, now Ryden Systems."),
        (28, "Shaddix", "DEFERRED", "Skipped for now."),
        (29, "MagicPuncher", "CONFIRMED", "Star Atlas gameplay engineer."),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "decision_date": AS_OF,
        "evidence_policy": "Operator decisions authorize identity resolution and review disposition but remain separate from archive evidence.",
        "item_count": len(decisions),
        "items": [
            {"item": number, "subject": subject, "decision": decision, "operator_note": note}
            for number, subject, decision, note in decisions
        ],
    }


def build(repo_root: Path) -> dict[str, str]:
    messages, inventory, duplicate_reviews = load_messages(repo_root, include_duplicate_reviews=True)
    alias_registry, seed_conflicts = build_alias_registry(messages)
    identities, organizations, relationships = build_indexes(messages, alias_registry)
    competition_records, competition_relationships, competition_reviews = extract_competition_records(messages, alias_registry)
    relationships.extend(competition_relationships)
    relationships = sorted({item["relationship_id"]: item for item in relationships}.values(), key=lambda item: (item.get("valid_at") or "", item["relationship_id"]))
    promotions = promotion_candidates(identities, organizations, relationships)
    tags = tag_registry(messages)
    coverage, gap_report, collection_backlog = build_channel_coverage(messages, inventory)
    human_queue = build_human_resolution_queue(duplicate_reviews, seed_conflicts, tags, organizations, relationships, competition_reviews, coverage)
    missing_identifier_counts = {
        "message_id": sum(message.message_id is None for message in messages),
        "channel_id": sum(message.channel_id is None for message in messages),
        "author_id": sum(message.author_id is None for message in messages),
    }
    conflicts = {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "unresolved_conflicts": seed_conflicts,
        "duplicate_review_candidates": duplicate_reviews,
        "source_limitations": [{
            "type": "missing_discord_identifiers",
            "counts": missing_identifier_counts,
            "handling": "Fields remain null. Stable archive source_id values are not relabeled as Discord message IDs.",
        }],
        "identity_merge_policy": "No identities are merged from name or fuzzy similarity alone.",
    }
    unresolved_seeds = [entry["canonical_name"] for entry in alias_registry["entries"] if entry["resolution_status"] == "HUMAN_REVIEW_REQUIRED"]
    transition_count = sum(r["predicate"] in {"renamed_to", "merged_into", "split_into", "became", "succeeded_by"} for r in relationships)
    backlog = {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "items": [
            {"priority": "high", "topic": "Discord native identifiers", "reason": "Current exports omit message IDs, channel IDs, and author IDs.", "next_evidence": "Acquire a privacy-reviewed export retaining public Discord identifiers."},
            {"priority": "medium", "topic": "Unresolved seeded identities", "entities": unresolved_seeds, "reason": "No exact primary-source match exists in the current corpus.", "next_evidence": "Locate self-identification or repeated independent community attribution."},
            {"priority": "medium", "topic": "Guild succession and structural events", "reason": f"Only {transition_count} explicit rename, merge, split, or successor statements were found.", "next_evidence": "Index guild channels and dated public guild announcements."},
            {"priority": "medium", "topic": "Leadership corroboration", "reason": "A single official announcement is still one independent reference.", "next_evidence": "Require direct self-identification or a second independently authored message before promotion."},
        ],
    }
    validation = validate_outputs(messages, alias_registry, identities, organizations, relationships, inventory, promotions, tags, competition_records, coverage, human_queue)
    parsed_occurrences = sum(item["parsed_message_occurrences"] for item in inventory if item["ingested"])
    source_inventory = {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "discovery_rule": "Supported files below archive/raw or archive/normalized whose repository path contains 'discord'.",
        "supported_formats": sorted(suffix.lstrip(".") for suffix in SUPPORTED_SUFFIXES),
        "files": inventory,
        "summary": {
            "source_files_inventoried": len(inventory),
            "parsed_message_occurrences": parsed_occurrences,
            "unique_messages": len(messages),
            "independent_export_units": 1,
            "channels_represented_native_confirmed": 0,
            "servers_represented_native_confirmed": 0,
            "repository_designated_communities": 1,
            "date_range": {"earliest": coverage["summary"]["earliest_message_timestamp"], "latest": coverage["summary"]["latest_message_timestamp"]},
            "classification_counts": dict(sorted(Counter(item["classification"] for item in inventory).items())),
            "representation_counts": dict(sorted(Counter(item["representation_role"] for item in inventory).items())),
        },
    }
    guilds = [item for item in organizations if item["entity_type"] == "guild"]
    return {
        "source-inventory.json": serialize_json(source_inventory),
        "alias-registry.json": serialize_json(alias_registry),
        "identity-index.jsonl": serialize_jsonl(identities),
        "guild-index.jsonl": serialize_jsonl(guilds),
        "organization-index.jsonl": serialize_jsonl(organizations),
        "relationship-index.jsonl": serialize_jsonl(relationships),
        "competition-index.jsonl": serialize_jsonl(competition_records),
        "tag-registry.json": serialize_json(tags),
        "promotion-candidates.json": serialize_json(promotions),
        "conflict-report.json": serialize_json(conflicts),
        "research-backlog.json": serialize_json(backlog),
        "discord-channel-coverage.json": serialize_json(coverage),
        "discord-channel-gap-report.json": serialize_json(gap_report),
        "discord-collection-backlog.json": serialize_json(collection_backlog),
        "human-resolution-queue.json": serialize_json(human_queue),
        "curator-decisions.json": serialize_json(curator_decisions()),
        "validation-report.json": serialize_json(validation),
    }


def write_outputs(repo_root: Path, output_dir: Path) -> dict[str, str]:
    rendered = build(repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in rendered.items():
        (output_dir / filename).write_text(content, encoding="utf-8", newline="\n")
    return rendered


def search(output_dir: Path, query: str, threshold: float) -> list[dict[str, Any]]:
    targets = (("identity", "identity-index.jsonl", "canonical_handle"), ("organization", "organization-index.jsonl", "canonical_name"))
    needle = normalized(query)
    results = []
    for kind, filename, name_field in targets:
        path = output_dir / filename
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            names = [record.get(name_field, ""), *record.get("aliases", []), *record.get("observed_handles", [])]
            exact = any(normalized(name) == needle for name in names)
            contains = any(needle and needle in normalized(name) for name in names)
            fuzzy = max((SequenceMatcher(None, needle, normalized(name)).ratio() for name in names if name), default=0.0)
            if exact or contains or fuzzy >= threshold:
                results.append({"kind": kind, "name": record.get(name_field), "exact": exact, "contains": contains, "fuzzy_score": round(fuzzy, 3), "record": record})
    return sorted(results, key=lambda item: (not item["exact"], -item["fuzzy_score"], item["name"].casefold()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build", help="discover sources and regenerate all campaign indexes")
    build_parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    build_parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    search_parser = subparsers.add_parser("search", help="search exact names, aliases, abbreviations, or fuzzy matches")
    search_parser.add_argument("query")
    search_parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    search_parser.add_argument("--threshold", type=float, default=0.72)
    args = parser.parse_args()
    if args.command == "build":
        rendered = write_outputs(args.repo_root.resolve(), args.output_dir.resolve())
        print(json.dumps({"campaign_id": CAMPAIGN_ID, "outputs": sorted(rendered), "status": "built"}, sort_keys=True))
    else:
        # ASCII escaping keeps search reliable in Windows consoles with legacy
        # code pages while JSON consumers still recover the exact Unicode text.
        print(json.dumps(search(args.output_dir.resolve(), args.query, args.threshold), ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
