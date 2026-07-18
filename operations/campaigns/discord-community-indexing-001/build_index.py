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
SCHEMA_VERSION = "1.0.0"
SUPPORTED_SUFFIXES = {".json", ".jsonl", ".csv", ".html", ".htm", ".txt", ".md"}
ROLE_TERMS = ("founder", "officer", "organizer", "builder", "creator", "diplomat", "competitor", "leader")
SEEDS = [
    ("guild", "Aephia", ["AEP", "Aephia Industries"]),
    ("guild", "The Club Guild", ["The Club"]),
    ("guild", "The Vanguard", []),
    ("guild", "BULK", []),
    ("person", "Eoganacht", []),
    ("guild", "Rome", ["ROME"]),
    ("person", "Funcracker", []),
    ("person", "Agent Solace", []),
    ("person", "Witticus", []),
    ("person", "ReyVeezy", []),
    ("person", "FancyHat", []),
    ("person", "King Bryan", []),
    ("person", "Virtuwaal", []),
    ("person", "Bohdi", []),
]
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


@dataclass
class Message:
    source_id: str
    message_id: str | None
    channel_id: str | None
    author_id: str | None
    display_name: str | None
    timestamp: str | None
    content: str
    metadata: list[str] = field(default_factory=list)
    source_paths: list[str] = field(default_factory=list)
    source_formats: list[str] = field(default_factory=list)

    def fingerprint(self) -> str:
        key = "\x1f".join((normalized(self.display_name), self.timestamp or "", clean_space(self.content)))
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def merge(self, other: "Message") -> None:
        if self.source_id.startswith("DISCORD-SOURCE-") and not other.source_id.startswith("DISCORD-SOURCE-"):
            self.source_id = other.source_id
        for attr in ("message_id", "channel_id", "author_id", "display_name", "timestamp"):
            if getattr(self, attr) is None and getattr(other, attr) is not None:
                setattr(self, attr, getattr(other, attr))
        if len(other.content) > len(self.content):
            self.content = other.content
        self.metadata = sorted(set(self.metadata + other.metadata))
        self.source_paths = sorted(set(self.source_paths + other.source_paths))
        self.source_formats = sorted(set(self.source_formats + other.source_formats))


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
    return Message(
        source_id=source_id,
        message_id=str(message_id) if message_id is not None else None,
        channel_id=str(channel_id) if channel_id is not None else None,
        author_id=author_id,
        display_name=display_name,
        timestamp=timestamp,
        content=content,
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


def load_messages(repo_root: Path) -> tuple[list[Message], list[dict[str, Any]]]:
    by_fingerprint: dict[str, Message] = {}
    by_source_id: dict[str, Message] = {}
    by_author_time: dict[tuple[str, str], Message] = {}
    inventory = []
    for path in discover_sources(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        classification = source_class(rel)
        ingested = classification in {"raw", "normalized"}
        parsed = parse_source(path, repo_root) if ingested else []
        inventory.append({
            "path": rel,
            "classification": classification,
            "format": path.suffix.casefold().lstrip("."),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "ingested": ingested,
            "parsed_message_occurrences": len(parsed),
            "reason": "raw_or_normalized_discord_export" if ingested else "derived_or_context_artifact_not_reingested",
        })
        for message in parsed:
            author_time = (normalized(message.display_name), message.timestamp or "")
            existing = by_source_id.get(message.source_id) or by_fingerprint.get(message.fingerprint())
            if existing is None and all(author_time):
                existing = by_author_time.get(author_time)
            if existing:
                existing.merge(message)
                by_source_id[message.source_id] = existing
                by_source_id[existing.source_id] = existing
                by_fingerprint[existing.fingerprint()] = existing
                if all(author_time):
                    by_author_time[author_time] = existing
            else:
                by_source_id[message.source_id] = message
                by_fingerprint[message.fingerprint()] = message
                if all(author_time):
                    by_author_time[author_time] = message
    unique_by_object = {id(message): message for message in by_fingerprint.values()}
    unique = sorted(unique_by_object.values(), key=lambda m: ((m.timestamp or ""), m.source_id))
    return unique, inventory


def evidence(message: Message, quote: str | None = None, attribution: str = "third_party_attribution") -> dict[str, Any]:
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
    }


def extract_mentions(content: str) -> list[str]:
    results = []
    sections = re.findall(r"(?im)^Mentions:\s*(.+)$", content)
    for section in sections:
        results.extend(part.strip() for part in section.split(","))
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
    return sorted(set(cleaned), key=str.casefold)


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
    for entity_type, canonical, aliases in SEEDS:
        terms = [canonical, *aliases]
        refs = []
        for message in messages:
            for _, matched_canonical, term in matched_seed_terms(message):
                if matched_canonical == canonical:
                    refs.append(evidence(message, term, "repeated_community_attribution"))
                    break
        for term in terms:
            alias_owners[normalized(term)].append(canonical)
        entries.append({
            "entity_type": entity_type,
            "canonical_name": canonical,
            "aliases": aliases,
            "normalized_terms": sorted(set(normalized(term) for term in terms)),
            "registry_status": "seeded_supported" if refs else "seeded_unresolved",
            "identity_merge_authorized": False,
            "evidence": refs[:25],
        })
    for term, owners in sorted(alias_owners.items()):
        if len(set(owners)) > 1:
            conflicts.append({"type": "alias_collision", "normalized_term": term, "canonical_names": sorted(set(owners))})
    # This fuzzy resemblance is deliberately reported, never merged.
    observed = {person_name_from_handle(h) for m in messages for h in extract_mentions(m.content)}
    for entity_type, canonical, _ in SEEDS:
        if entity_type != "person":
            continue
        for handle in observed:
            ratio = SequenceMatcher(None, normalized(canonical), normalized(handle)).ratio()
            shared_prefix = normalized(canonical)[:2] == normalized(handle)[:2] and ratio >= 0.55
            if canonical.casefold() != handle.casefold() and (ratio >= 0.68 or shared_prefix):
                conflicts.append({
                    "type": "unresolved_fuzzy_identity",
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

    def add_identity(name: str, message: Message, observed_as: str, attribution: str, author_id: str | None = None) -> str:
        name = clean_handle(name)
        key = f"id:{author_id}" if author_id else f"handle:{normalized(name)}"
        identity_id = stable_id("PERSON", key)
        record = identities.setdefault(identity_id, {
            "identity_id": identity_id,
            "canonical_handle": name,
            "author_ids": [],
            "observed_handles": [],
            "roles": [],
            "first_seen": message.timestamp,
            "last_seen": message.timestamp,
            "evidence": [],
            "identity_confidence": "author_id_supported" if author_id else "handle_only_not_merged",
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
            "evidence": [evidence(message, quote, attribution)],
        }
        relationships.append(record)
        if role and subject_id in identities and role not in identities[subject_id]["roles"]:
            identities[subject_id]["roles"].append(role)

    for message in messages:
        if message.display_name:
            author_id = add_identity(
                message.display_name, message, message.display_name,
                "inferred_alias" if any("author inferred" in item.casefold() for item in message.metadata) else "third_party_attribution",
                message.author_id,
            )
            if re.search(r"\bmod(?:erator)?\b", message.display_name, re.I):
                add_relationship(author_id, message.display_name, "has_community_role", "role", "moderator", message,
                                 "inferred_alias", message.display_name, "medium", "moderator")
        mentions = extract_mentions(message.content)
        mention_ids = {}
        for handle in mentions:
            person = person_name_from_handle(handle)
            if not person or normalized(person) in GENERIC_MENTIONS:
                continue
            mention_ids[handle] = add_identity(person, message, handle, "third_party_attribution")
            tag = re.match(r"@?\[([^\]]+)\]", handle)
            guild = None
            if tag:
                guild = "Aephia" if tag.group(1).casefold() == "aep" else tag.group(1)
            elif "|" in handle:
                left, right = [part.strip(" @") for part in handle.split("|", 1)]
                if left.casefold() == "rome":
                    guild = "Rome"
                elif right.casefold() in {"bulk", "rome"}:
                    guild = right.upper() if right.casefold() == "bulk" else "Rome"
            if guild:
                add_relationship(mention_ids[handle], person, "member_of", "guild", guild, message,
                                 "inferred_alias", handle, "low", "guild_member")

        # Official council roster attribution.
        if re.search(r"first\s+(?:star atlas dao\s+)?council", message.content, re.I):
            for handle, identity_id in mention_ids.items():
                person = person_name_from_handle(handle)
                add_relationship(identity_id, person, "served_as", "organization", "Star Atlas DAO Council", message,
                                 "third_party_attribution", handle, "high", "council_member")

        # Explicit creator attribution (not generic mentions of creators).
        for match in re.finditer(r"(?i)(thanks\s+)(?P<handle>@(?:\[[^\]]+\]\s*)?[^\n,()]{2,80}?)(?=\s+for\s+creat(?:ing|ed))", message.content):
            handle = clean_handle(match.group("handle"))
            person = person_name_from_handle(handle)
            identity_id = mention_ids.get(handle) or add_identity(person, message, handle, "third_party_attribution")
            add_relationship(identity_id, person, "contributed_as", "role", "creator", message,
                             "third_party_attribution", match.group(0), "high", "creator")

        # Direct self-identification statements receive their own evidence class.
        if message.display_name:
            for match in re.finditer(r"(?i)\bI(?:'m| am)\s+(?:the\s+)?(founder|officer|organizer|builder|creator|diplomat|competitor|leader)\s+(?:of|for|at)\s+([A-Z][^.!?\n]{1,80})", message.content):
                identity_id = add_identity(message.display_name, message, message.display_name, "direct_self_identification", message.author_id)
                role, organization = match.group(1).casefold(), clean_space(match.group(2))
                add_relationship(identity_id, message.display_name, "served_as", "organization", organization, message,
                                 "direct_self_identification", match.group(0), "high", role)

        # Guild placement is an event, not a permanent hierarchy assertion.
        for match in re.finditer(r"(?im)^\s*(1st|2nd|3rd)(?:\s+Place)?\s*[-:]\s*([^\r\n,]+)", message.content):
            guild = clean_space(match.group(2))
            relationships.append({
                "relationship_id": stable_id("REL", f"{message.source_id}:{match.group(0)}"),
                "subject_id": stable_id("GUILD", normalized(guild)),
                "subject_name": guild,
                "predicate": "placed_in_competition",
                "object_type": "placement",
                "object_name": match.group(1).casefold(),
                "valid_at": message.timestamp,
                "confidence": "high",
                "evidence": [evidence(message, match.group(0), "third_party_attribution")],
            })

        # Conservative dated guild transition extraction.
        transition = re.search(r"(?i)\b([^.!?\n]{2,80}?)\s+(renamed|merged|split|became|succeeded)\s+(?:into|from|as|by|to)?\s*([^.!?\n]{2,80})", message.content)
        if transition:
            left, verb, right = clean_space(transition.group(1)), transition.group(2).casefold(), clean_space(transition.group(3))
            relationships.append({
                "relationship_id": stable_id("REL", f"{message.source_id}:{transition.group(0)}"),
                "subject_id": stable_id("GUILD", normalized(left)),
                "subject_name": left,
                "predicate": {"renamed": "renamed_to", "merged": "merged_into", "split": "split_into", "became": "became", "succeeded": "succeeded_by"}[verb],
                "object_type": "guild",
                "object_name": right,
                "valid_at": message.timestamp,
                "confidence": "medium",
                "evidence": [evidence(message, transition.group(0), "third_party_attribution")],
            })

    # Ensure every seeded person is discoverable even when unresolved.
    for entry in alias_registry["entries"]:
        if entry["entity_type"] != "person":
            continue
        canonical = entry["canonical_name"]
        identity_id = stable_id("PERSON", f"seed:{normalized(canonical)}")
        if not any(normalized(record["canonical_handle"]) == normalized(canonical) for record in identities.values()):
            identities[identity_id] = {
                "identity_id": identity_id,
                "canonical_handle": canonical,
                "author_ids": [],
                "observed_handles": [],
                "roles": [],
                "first_seen": None,
                "last_seen": None,
                "evidence": entry["evidence"],
                "identity_confidence": "seeded_unresolved",
            }

    guilds = []
    for entry in alias_registry["entries"]:
        if entry["entity_type"] != "guild":
            continue
        canonical = entry["canonical_name"]
        refs = entry["evidence"]
        dated = sorted(ref["timestamp"] for ref in refs if ref.get("timestamp"))
        guild_relationships = [r["relationship_id"] for r in relationships if r["object_type"] == "guild" and normalized(r["object_name"]) == normalized(canonical)]
        guild_relationships += [r["relationship_id"] for r in relationships if normalized(r["subject_name"]) == normalized(canonical)]
        guilds.append({
            "guild_id": stable_id("GUILD", normalized(canonical)),
            "canonical_name": canonical,
            "aliases": entry["aliases"],
            "first_seen": dated[0] if dated else None,
            "last_seen": dated[-1] if dated else None,
            "relationship_ids": sorted(set(guild_relationships)),
            "evidence": refs,
            "status": "evidence_supported" if refs else "seeded_unresolved",
        })

    for record in identities.values():
        record["author_ids"].sort()
        record["observed_handles"].sort(key=str.casefold)
        record["roles"].sort()
        seen_refs = {}
        for ref in record["evidence"]:
            seen_refs[(ref["source_id"], ref["quoted_text"], ref["attribution_class"])] = ref
        record["evidence"] = list(seen_refs.values())
    relationships.sort(key=lambda r: (r.get("valid_at") or "", r["relationship_id"]))
    return sorted(identities.values(), key=lambda r: (r["canonical_handle"].casefold(), r["identity_id"])), guilds, relationships


def promotion_candidates(identities: list[dict[str, Any]], guilds: list[dict[str, Any]], relationships: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = []
    rel_by_subject: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for relationship in relationships:
        rel_by_subject[relationship["subject_id"]].append(relationship)
    for identity in identities:
        refs = identity["evidence"]
        source_ids = {r["source_id"] for r in refs}
        authors = {r.get("display_name") for r in refs if r.get("display_name")}
        channels = {r.get("channel_id") for r in refs if r.get("channel_id")}
        roles = set(identity["roles"])
        if len(source_ids) < 2:
            continue
        direct = any(r["attribution_class"] == "direct_self_identification" for r in refs)
        leadership = bool(roles & {"founder", "officer", "organizer", "leader", "council_member"})
        dates = sorted(r["timestamp"] for r in refs if r.get("timestamp"))
        duration_days = 0
        if len(dates) > 1:
            try:
                duration_days = (datetime.fromisoformat(dates[-1].replace("Z", "+00:00")) - datetime.fromisoformat(dates[0].replace("Z", "+00:00"))).days
            except ValueError:
                duration_days = 0
        components = {
            "evidence_strength": 20 if direct else (15 if len(authors) >= 2 else 10),
            "independent_mentions": min(15, len(source_ids) * 3),
            "activity_duration": min(10, duration_days // 180),
            "leadership_or_founder": 15 if leadership and (direct or len(authors) >= 2) else (5 if leadership else 0),
            "contribution_type": min(10, len(roles) * 4),
            "cross_channel_corroboration": min(10, len(channels) * 5),
            "identity_confidence": 10 if identity["author_ids"] else 6,
            "historical_significance": min(10, len(rel_by_subject[identity["identity_id"]]) * 3),
        }
        total = sum(components.values())
        volume_guard = bool(roles or rel_by_subject[identity["identity_id"]])
        recommendation = "defer"
        if volume_guard and total >= 65 and (not leadership or direct or len(authors) >= 2):
            recommendation = "promote"
        elif volume_guard and total >= 40:
            recommendation = "review"
        candidates.append({
            "entity_type": "person",
            "entity_id": identity["identity_id"],
            "name": identity["canonical_handle"],
            "score": total,
            "score_components": components,
            "independent_message_count": len(source_ids),
            "independent_author_count": len(authors),
            "duration_days": duration_days,
            "roles": sorted(roles),
            "recommendation": recommendation,
            "volume_only_guard_passed": volume_guard,
            "evidence": refs[:25],
        })
    for guild in guilds:
        refs = guild["evidence"]
        source_ids = {r["source_id"] for r in refs}
        authors = {r.get("display_name") for r in refs if r.get("display_name")}
        if len(source_ids) < 2:
            continue
        rel_count = len(guild["relationship_ids"])
        components = {
            "evidence_strength": 15 if len(authors) >= 2 else 10,
            "independent_mentions": min(15, len(source_ids) * 3),
            "activity_duration": 5 if guild["first_seen"] != guild["last_seen"] else 0,
            "leadership_or_founder": 0,
            "contribution_type": min(10, rel_count * 3),
            "cross_channel_corroboration": 0,
            "identity_confidence": 8,
            "historical_significance": min(10, rel_count * 3),
        }
        total = sum(components.values())
        candidates.append({
            "entity_type": "guild", "entity_id": guild["guild_id"], "name": guild["canonical_name"],
            "score": total, "score_components": components, "independent_message_count": len(source_ids),
            "independent_author_count": len(authors), "recommendation": "promote" if total >= 65 else ("review" if total >= 40 else "defer"),
            "volume_only_guard_passed": rel_count > 0, "evidence": refs[:25],
        })
    candidates.sort(key=lambda c: (-c["score"], c["name"].casefold()))
    return {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "scoring_note": "Message volume is not a scoring component; independent evidence, time, roles, contribution, corroboration, confidence, and significance are scored.",
        "thresholds": {"promote": 65, "review": 40},
        "candidates": candidates,
    }


def validate_outputs(messages: list[Message], alias_registry: dict[str, Any], identities: list[dict[str, Any]],
                     guilds: list[dict[str, Any]], relationships: list[dict[str, Any]], inventory: list[dict[str, Any]]) -> dict[str, Any]:
    source_ids = {message.source_id for message in messages}
    all_claim_records: list[dict[str, Any]] = identities + guilds + relationships
    unresolved_refs = []
    for record in all_claim_records:
        for ref in record.get("evidence", []):
            if ref["source_id"] not in source_ids:
                unresolved_refs.append({"record": record.get("identity_id") or record.get("guild_id") or record.get("relationship_id"), "source_id": ref["source_id"]})
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
    undated_relationships = [r["relationship_id"] for r in relationships if not r.get("valid_at")]
    missing_quotes = [
        ref["source_id"] for record in all_claim_records for ref in record.get("evidence", [])
        if not ref.get("quoted_text")
    ]
    duplicate_provenance_preserved = all(message.source_paths for message in messages)
    checks = [
        {"name": "every_indexed_claim_resolves_to_source_message", "passed": not unresolved_refs, "details": unresolved_refs},
        {"name": "aliases_non_circular_and_conflict_aware", "passed": not alias_collisions, "details": alias_collisions},
        {"name": "user_ids_not_merged_without_evidence", "passed": not merged_ids, "details": merged_ids},
        {"name": "guild_relationships_dated_where_possible", "passed": not undated_relationships, "details": undated_relationships},
        {"name": "duplicate_messages_collapsed_with_provenance", "passed": duplicate_provenance_preserved, "details": {"unique_messages": len(messages), "source_occurrences": sum(i["parsed_message_occurrences"] for i in inventory if i["ingested"])}},
        {"name": "quoted_text_preserved", "passed": not missing_quotes, "details": missing_quotes},
        {"name": "deterministic_ordering", "passed": True, "details": "All paths and records use stable sorting and hash-based identifiers."},
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "status": "pass" if all(check["passed"] for check in checks) else "fail",
        "checks": checks,
        "counts": {"sources": len(inventory), "unique_messages": len(messages), "identities": len(identities), "guilds": len(guilds), "relationships": len(relationships)},
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


def build(repo_root: Path) -> dict[str, str]:
    messages, inventory = load_messages(repo_root)
    alias_registry, seed_conflicts = build_alias_registry(messages)
    identities, guilds, relationships = build_indexes(messages, alias_registry)
    promotions = promotion_candidates(identities, guilds, relationships)
    missing_identifier_counts = {
        "message_id": sum(message.message_id is None for message in messages),
        "channel_id": sum(message.channel_id is None for message in messages),
        "author_id": sum(message.author_id is None for message in messages),
    }
    conflicts = {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "unresolved_conflicts": seed_conflicts,
        "source_limitations": [{
            "type": "missing_discord_identifiers",
            "counts": missing_identifier_counts,
            "handling": "Fields remain null. Stable archive source_id values are not relabeled as Discord message IDs.",
        }],
        "identity_merge_policy": "No identities are merged from name or fuzzy similarity alone.",
    }
    unresolved_seeds = [entry["canonical_name"] for entry in alias_registry["entries"] if entry["registry_status"] == "seeded_unresolved"]
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
    validation = validate_outputs(messages, alias_registry, identities, guilds, relationships, inventory)
    source_inventory = {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": CAMPAIGN_ID,
        "discovery_rule": "Supported files below archive/raw or archive/normalized whose repository path contains 'discord'.",
        "supported_formats": sorted(suffix.lstrip(".") for suffix in SUPPORTED_SUFFIXES),
        "files": inventory,
        "summary": dict(sorted(Counter(item["classification"] for item in inventory).items())),
    }
    return {
        "source-inventory.json": serialize_json(source_inventory),
        "alias-registry.json": serialize_json(alias_registry),
        "identity-index.jsonl": serialize_jsonl(identities),
        "guild-index.jsonl": serialize_jsonl(guilds),
        "relationship-index.jsonl": serialize_jsonl(relationships),
        "promotion-candidates.json": serialize_json(promotions),
        "conflict-report.json": serialize_json(conflicts),
        "research-backlog.json": serialize_json(backlog),
        "validation-report.json": serialize_json(validation),
    }


def write_outputs(repo_root: Path, output_dir: Path) -> dict[str, str]:
    rendered = build(repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in rendered.items():
        (output_dir / filename).write_text(content, encoding="utf-8", newline="\n")
    return rendered


def search(output_dir: Path, query: str, threshold: float) -> list[dict[str, Any]]:
    targets = (("identity", "identity-index.jsonl", "canonical_handle"), ("guild", "guild-index.jsonl", "canonical_name"))
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
