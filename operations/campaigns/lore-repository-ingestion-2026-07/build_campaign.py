#!/usr/bin/env python3
"""Build the deterministic Star Atlas Lore Repository ingestion campaign."""

from __future__ import annotations

import hashlib
import html
import json
import mimetypes
import posixpath
import re
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_ID = "lore-repository-ingestion-2026-07"
CAMPAIGN_REL = Path("operations/campaigns") / CAMPAIGN_ID
CAMPAIGN_DIR = ROOT / CAMPAIGN_REL
RAW_REL = Path("archive/raw/lore-repository")
RAW_ZIP_REL = RAW_REL / "star-atlas-lore-22555f277eb1496e34c0839c8f1f382842bd1d2b.zip"
RAW_HOME_REL = RAW_REL / "live-site-home-2026-07-19.html"
RAW_SITEMAP_REL = RAW_REL / "live-site-sitemap-2026-07-19.xml"
PROVENANCE_REL = Path("archive/provenance/lore-repository")
NORMALIZED_REL = Path("archive/normalized/lore")
SOURCE_RECORDS_REL = Path("archive/source-records/lore-repository")
PACKAGE_REL = Path("archive/ingestion-packages/lore-repository")
ARCHIVE_MANIFEST_REL = Path("archive/manifests") / f"{CAMPAIGN_ID}.json"

UPSTREAM_REPOSITORY = "JoseEduardonoot/star-atlas-lore"
UPSTREAM_REPOSITORY_URL = "https://github.com/JoseEduardonoot/star-atlas-lore"
UPSTREAM_SITE_URL = "https://joseeduardonoot.github.io/star-atlas-lore/"
UPSTREAM_BRANCH = "main"
UPSTREAM_COMMIT = "22555f277eb1496e34c0839c8f1f382842bd1d2b"
UPSTREAM_TREE = "f4b6c4121447887ff2b12b7c23a11307f3e81093"
UPSTREAM_COMMIT_DATE = "2026-06-29T00:36:35Z"
UPSTREAM_COMMIT_MESSAGE = "docs(c4): preserve crew/gear/mission/encounter design artifacts"
DEFAULT_BRANCH_AT_CAPTURE = "master"
DEFAULT_BRANCH_COMMIT = "d138c60a210e2afc2d898806ecf9b032a4f8c3a1"
DEPLOYMENT_BRANCH = "gh-pages"
DEPLOYMENT_COMMIT = "abf1c5852935c1607901b8953f241801e264f573"
DEPLOYED_SOURCE_COMMIT = "e1d87b0"
DEPLOYMENT_DATE = "2026-06-04T19:29:23Z"
CAPTURED_AT = "2026-07-19T15:26:28Z"
EXPECTED_ZIP_SHA256 = "08061a661f47a8d55d233a79ba5cdadbbd98c471f50b171d2d56ea583f2a04a1"
EXPECTED_ZIP_BYTES = 11118506
CURATOR_DECISION_DATE = "2026-07-19"
HISTORICAL_CANON_SOURCE_PATH = "canon/geography/oni_css_lore_layer.md"
WORKSTATION_PATH_REDACTION = "[REDACTED_UPSTREAM_WORKSTATION_PATH]"

SITE_PREFIX = "https://joseeduardonoot.github.io/star-atlas-lore/"
MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".mp4", ".webm", ".mp3", ".wav"}
INDEX_NAMES = {"index.md"}
SUPPORTED_REPOSITORY_TYPES = {
    "PERSON", "ORGANIZATION", "DAO", "CORPORATION", "TOKEN", "FEATURE",
    "TECHNOLOGY", "GAME_SYSTEM", "GAME_MODE", "SHIP", "LOCATION",
    "RESOURCE", "EVENT", "DOCUMENT", "PRODUCT", "COMMUNITY", "GUILD",
}

LORE_TYPE_HIERARCHY = {
    "AGENT": ["CHARACTER", "SPECIES", "FACTION", "ORGANIZATION", "INSTITUTION", "CORPORATION", "MANUFACTURER"],
    "PLACE": ["REGION", "SECTOR", "STAR_SYSTEM", "WORLD", "PLANET", "MOON", "STATION", "LOCATION"],
    "CONCEPT": ["TECHNOLOGY", "GAME_SYSTEM", "COSMOLOGY"],
    "OBJECT": ["ARTIFACT", "RESOURCE"],
    "OCCURRENCE": ["LORE_EVENT"],
    "DOCUMENTARY": ["NARRATIVE", "QUEST", "TAXONOMY", "REFERENCE", "REGISTRY_AUDIT"],
}

LORE_TO_REPOSITORY_TYPE = {
    "CHARACTER": "PERSON",
    "SPECIES": "COMMUNITY",
    "FACTION": "ORGANIZATION",
    "ORGANIZATION": "ORGANIZATION",
    "INSTITUTION": "ORGANIZATION",
    "CORPORATION": "CORPORATION",
    "MANUFACTURER": "CORPORATION",
    "REGION": "LOCATION",
    "SECTOR": "LOCATION",
    "STAR_SYSTEM": "LOCATION",
    "WORLD": "LOCATION",
    "PLANET": "LOCATION",
    "MOON": "LOCATION",
    "STATION": "LOCATION",
    "LOCATION": "LOCATION",
    "TECHNOLOGY": "TECHNOLOGY",
    "GAME_SYSTEM": "GAME_SYSTEM",
    "COSMOLOGY": "DOCUMENT",
    "ARTIFACT": "RESOURCE",
    "RESOURCE": "RESOURCE",
    "LORE_EVENT": "EVENT",
    "NARRATIVE": "DOCUMENT",
    "QUEST": "DOCUMENT",
    "TAXONOMY": "DOCUMENT",
    "REFERENCE": "DOCUMENT",
    "REGISTRY_AUDIT": "DOCUMENT",
}

EXISTING_LORE_MAPPINGS = [
    {"existing_id": "LORE-GALIA", "existing_name": "Galia Expanse", "candidates": ["canon/reference/atlas/galia_expanse_atlas.md", "canon/geography/galactic_regions.md"]},
    {"existing_id": "LORE-CATACLYSM", "existing_name": "The Cataclysm", "candidates": ["canon/geography/the_cataclysm.md"]},
    {"existing_id": "LORE-COUNCIL-PEACE", "existing_name": "Council of Peace", "candidates": ["canon/institutions/council_of_peace.md", "canon/factions/council_of_peace.md"]},
    {"existing_id": "LORE-FACTION-MUD", "existing_name": "MUD — Manus Ultima Divina", "candidates": ["canon/factions/mud.md"]},
    {"existing_id": "LORE-FACTION-ONI", "existing_name": "ONI Consortium", "candidates": ["canon/factions/oni.md"]},
    {"existing_id": "LORE-FACTION-USTUR", "existing_name": "Ustur Sector", "candidates": ["canon/factions/ustur.md", "canon/species/ustur.md"]},
    {"existing_id": "LORE-TUFA", "existing_name": "Tufa", "candidates": ["canon/species/tufa.md"]},
    {"existing_id": "LORE-NARRATIVE-CORE", "existing_name": "Star Atlas: CORE", "candidates": []},
    {"existing_id": "LORE-VOICE-OF-IRIS", "existing_name": "The Voice of Iris", "candidates": []},
]

CURATOR_DECISIONS = {
    "LRH-001": {
        "accepted_disposition": "RECOGNIZE_PERSONAL_REPOSITORY_AS_ATMTA_AFFILIATED_CANONICAL_LORE_AUTHORITY",
        "decision_note": "Operator confirms Jose is a Star Atlas team member responsible for lore; his personal repository is treated as ATMTA-affiliated and canonical for lore taxonomy and nomenclature.",
    },
    "LRH-002": {
        "accepted_disposition": "MAP_TO_REGION_AND_RETAIN_ATLAS_DOCUMENT_AS_REFERENCE",
    },
    "LRH-003": {
        "accepted_disposition": "KEEP_DISTINCT_INSTITUTION_AND_FACTION_ENTITIES_WITH_SHARED_ALIAS",
    },
    "LRH-004": {
        "accepted_disposition": "KEEP_DISTINCT_SPECIES_AND_FACTION_ENTITIES_WITH_SHARED_NAME",
    },
    "LRH-005": {
        "accepted_disposition": "PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING",
    },
    "LRH-006": {
        "accepted_disposition": "PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING",
    },
    "LRH-007": {
        "accepted_disposition": "KEEP_CURRENT_MAIN_AS_SOURCE_AND_PRESERVE_LIVE_SITE_AS_SEPARATE_SNAPSHOT",
    },
    "LRH-008": {
        "accepted_disposition": "CANON_CONTROLS_TAXONOMY_AND_BOTH_TEXT_VARIANTS_REMAIN_PRESERVED",
    },
    "LRH-009": {
        "accepted_disposition": "PRESERVE_SOURCE_AND_STAGE_SEPARATE_LINK_REPAIR_CAMPAIGN",
    },
    "LRH-010": {
        "accepted_disposition": "CLASSIFY_AS_HISTORICAL_CANONICAL_SOURCE_SNAPSHOT_NOT_CURRENT_TAXONOMY",
        "decision_note": "The ONI/CSS page is canonical-source evidence for its captured historical state, not current canonical taxonomy.",
    },
    "LRH-011": {
        "accepted_disposition": "DEFER_INDIVIDUAL_CORRECTIONS_UNTIL_OFFICIAL_PRIMARY_EVIDENCE_IS_ATTACHED",
    },
    "LRH-012": {
        "accepted_disposition": "TREAT_AS_RESEARCH_CANDIDATES_NOT_CONFIRMED_CONTRADICTIONS",
    },
    "LRH-013": {
        "accepted_disposition": "PRESERVE_AS_RESEARCH_GAPS_PENDING_TIMELINE_EVIDENCE_REVIEW",
    },
    "LRH-014": {
        "accepted_disposition": "PRESERVE_RAW_REDACT_NORMALIZED_AND_PUBLIC_OUTPUTS",
        "decision_note": "Absolute workstation paths remain only in immutable raw evidence and are redacted from normalized records and public-facing derivatives.",
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repository_text_bytes(path: Path) -> bytes:
    """Return a stable UTF-8/LF representation for tracked text files."""
    text = path.read_bytes().decode("utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def dump_jsonl(values: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values)


def normalize_text(data: bytes) -> str:
    text = data.decode("utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return text.rstrip("\n") + "\n"


def redact_normalized_workstation_paths(text: str) -> tuple[str, int]:
    """Redact upstream workstation paths from derivatives without changing raw evidence."""
    return re.subn(r"`[A-Za-z]:\\Users\\[^`\r\n]+`", f"`{WORKSTATION_PATH_REDACTION}`", text)


def stable_id(prefix: str, *parts: str, length: int = 12) -> str:
    payload = "\x00".join(parts).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(payload).hexdigest()[:length].upper()}"


def strip_markdown(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "").replace("__", "").replace("`", "").replace("*", "")
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def clean_title(value: str) -> str:
    value = strip_markdown(value)
    value = re.sub(r"^(?:Canon\s+(?:Document|Registry)\s*:\s*)", "", value, flags=re.I)
    value = value.lstrip()
    while value and (unicodedata.category(value[0]).startswith("S") or value[0] in "⚖⚔⏳"):
        value = value[1:].lstrip()
    return value.strip()


def aliases_from_title(title: str) -> list[str]:
    aliases: set[str] = set()
    for part in re.findall(r"\(([^)]+)\)", title):
        candidate = strip_markdown(part)
        if re.fullmatch(r"[A-Z][A-Z0-9.'/-]{1,14}", candidate):
            aliases.add(candidate)
        elif re.fullmatch(r"[A-Za-z][A-Za-z .'-]{5,80}", candidate) and re.match(r"^[A-Z0-9.'/-]{2,14}\s+\(", title):
            aliases.add(candidate)
    prefix_match = re.match(r"^([A-Z][A-Z0-9.'/-]{1,14})\s+\(([^)]+)\)", title)
    if prefix_match:
        aliases.add(prefix_match.group(1))
        aliases.add(prefix_match.group(2))
    return sorted(alias for alias in aliases if alias.casefold() != title.casefold())


def get_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return clean_title(line[2:])
    return "UNTITLED"


def headings(text: str) -> list[dict[str, Any]]:
    result = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            result.append({"level": len(match.group(1)), "line": line_number, "text": clean_title(match.group(2))})
    return result


def taxonomy_for_path(path: str) -> tuple[str, str, list[str]]:
    rel = path.split("/", 1)[1] if path.startswith(("canon/", "docs/")) else path
    parts = rel.split("/")
    top = parts[0]
    filename = parts[-1]
    if top == "species":
        lore_type = "TAXONOMY" if filename in {"species_master_guide.md", "species_encyclopedia.md", "naming_conventions.md"} else "SPECIES"
    elif top == "factions":
        lore_type = "FACTION"
    elif top == "geography" and len(parts) > 2 and parts[1] == "sectors":
        lore_type = "SECTOR"
    elif top == "geography" and len(parts) > 2 and parts[1] == "worlds":
        lore_type = "WORLD"
    elif rel == "geography/eternity_system.md":
        lore_type = "STAR_SYSTEM"
    elif rel == "geography/the_cataclysm.md":
        lore_type = "LORE_EVENT"
    elif top == "geography":
        lore_type = "REGION"
    elif top == "history":
        lore_type = "LORE_EVENT"
    elif top == "institutions":
        lore_type = "INSTITUTION"
    elif top == "manufacturers":
        lore_type = "MANUFACTURER"
    elif top == "narratives":
        lore_type = "NARRATIVE"
    elif top == "quests":
        lore_type = "QUEST"
    elif top == "cosmology":
        lore_type = "COSMOLOGY"
    elif top == "systems":
        lore_type = "GAME_SYSTEM"
    elif top == "technology":
        lore_type = "TECHNOLOGY"
    elif top == "meta":
        lore_type = "REGISTRY_AUDIT"
    elif top == "reference":
        lore_type = "REFERENCE"
    else:
        lore_type = "REFERENCE"
    return LORE_TO_REPOSITORY_TYPE[lore_type], lore_type, parts[:-1]


def zip_members() -> tuple[str, dict[str, bytes]]:
    with zipfile.ZipFile(ROOT / RAW_ZIP_REL) as archive:
        files = {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
    prefixes = {name.split("/", 1)[0] for name in files}
    if len(prefixes) != 1:
        raise ValueError(f"unexpected archive roots: {sorted(prefixes)}")
    prefix = next(iter(prefixes)) + "/"
    return prefix, {name[len(prefix):]: data for name, data in files.items()}


def classify_file(path: str) -> tuple[str, str]:
    suffix = PurePosixPath(path).suffix.lower()
    if path.startswith("canon/"):
        return ("CANON_AUTHORING_SOURCE", "INCLUDED")
    if path.startswith("docs/"):
        return ("PUBLICATION_PRESENTATION", "INVENTORIED")
    if path.startswith("c4-internal/"):
        return ("WORKING_DESIGN_MATERIAL", "EXCLUDED_FROM_CANONICAL_LORE_NORMALIZATION")
    if path.startswith("tools/") or path.startswith(".github/"):
        return ("UPSTREAM_OPERATIONAL", "PRESERVED_NOT_NORMALIZED")
    if suffix in MEDIA_EXTENSIONS:
        return ("UPSTREAM_MEDIA", "PRESERVED_AND_INVENTORIED")
    return ("UPSTREAM_REPOSITORY_SUPPORT", "PRESERVED_NOT_NORMALIZED")


def resolve_link(source_path: str, target: str, members: set[str]) -> tuple[str | None, str]:
    target = unquote(target.strip().strip("<>"))
    split = urlsplit(target)
    if split.scheme or target.startswith("//"):
        return None, "EXTERNAL"
    path = split.path
    if not path:
        return source_path, "SAME_PAGE_ANCHOR"
    if path.startswith("canon/") or path.startswith("docs/"):
        resolved = posixpath.normpath(path)
    else:
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), path))
    if resolved in members:
        return resolved, "RESOLVED"
    if not PurePosixPath(resolved).suffix and f"{resolved}.md" in members:
        return f"{resolved}.md", "RESOLVED"
    if resolved.endswith("/") and f"{resolved}index.md" in members:
        return f"{resolved}index.md", "RESOLVED"
    return resolved, "UNRESOLVED"


def extract_links(source_path: str, text: str, member_paths: set[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    links: list[dict[str, Any]] = []
    media: list[dict[str, Any]] = []
    pattern = re.compile(r"(!?)\[([^]]*)\]\(([^)]+)\)")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in pattern.finditer(line):
            is_media = bool(match.group(1))
            label = strip_markdown(match.group(2))
            original_target = match.group(3).strip()
            resolved, status = resolve_link(source_path, original_target, member_paths)
            item = {
                "line": line_number,
                "label": label or None,
                "original_target": original_target,
                "resolved_path": resolved,
                "resolution_status": status,
            }
            (media if is_media else links).append(item)
    return links, media


def table_rows(text: str, required_header: str) -> list[tuple[int, dict[str, str]]]:
    lines = text.splitlines()
    rows: list[tuple[int, dict[str, str]]] = []
    index = 0
    while index + 1 < len(lines):
        if lines[index].lstrip().startswith("|") and required_header in lines[index]:
            headers = [strip_markdown(cell.strip()) for cell in lines[index].strip().strip("|").split("|")]
            separator = lines[index + 1]
            if not separator.lstrip().startswith("|") or not re.search(r"---", separator):
                index += 1
                continue
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if len(cells) == len(headers):
                    rows.append((index + 1, dict(zip(headers, cells))))
                index += 1
            continue
        index += 1
    return rows


def page_markdown(page: dict[str, Any], source_text: str) -> str:
    frontmatter = [
        "---",
        f"source_id: {page['source_id']}",
        f"preferred_name: {json.dumps(page['preferred_name'], ensure_ascii=False)}",
        f"lore_type: {page['lore_type']}",
        f"repository_entity_type: {page['repository_entity_type']}",
        f"upstream_commit: {UPSTREAM_COMMIT}",
        f"upstream_path: {page['upstream_path']}",
        f"authority_scope: {page['authority_scope']}",
        "---",
        "",
        f"# {page['preferred_name']}",
        "",
        "## Normalization Note",
        "",
        "The text below is a line-ending-normalized derivative of the preserved upstream page. No source wording was rewritten. Taxonomy and link metadata are stored in the paired JSON record.",
        "",
        "## Preserved Source Text",
        "",
    ]
    return "\n".join(frontmatter) + source_text


def source_record_markdown(page: dict[str, Any]) -> str:
    aliases = ", ".join(page["aliases"]) if page["aliases"] else "None captured"
    limitations = "\n".join(f"- {item}" for item in page["limitations"])
    return f"""---
source_id: {page['source_id']}
title: {json.dumps(page['preferred_name'], ensure_ascii=False)}
publisher: {json.dumps(UPSTREAM_REPOSITORY)}
source_type: lore_repository
captured: {CAPTURED_AT}
access: public
authenticity: repository_commit_verified
url: {page['canonical_url']}
---

# {page['preferred_name']}

## Metadata

- Source ID: `{page['source_id']}`
- Upstream Path: `{page['upstream_path']}`
- Upstream Commit: `{UPSTREAM_COMMIT}`
- Lore Type: `{page['lore_type']}`
- Repository Entity Type: `{page['repository_entity_type']}`
- Preferred Name: {page['preferred_name']}
- Aliases: {aliases}
- Published Mirror Status: `{page['published_mirror_status']}`
- Extraction Confidence: `{page['extraction_confidence']}`

## Source Lineage

- Publication: `{UPSTREAM_REPOSITORY}`
- Publication Role: `ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_SOURCE`
- Relationship: `PRESERVED_FROM_COMMIT`
- Primary Source: `{UPSTREAM_REPOSITORY_URL}/blob/{UPSTREAM_COMMIT}/{page['upstream_path']}`
- Original Creator: `JoseEduardonoot` (repository account; page-level authorship not independently established)
- Lineage Confidence: `HIGH` for repository path and commit; `UNKNOWN` for underlying claim authorship

## Archival Abstract

This Source Record inventories one lore repository page and its normalized artifact chain. By operator confirmation, Jose is a Star Atlas team member responsible for lore and this personal repository is ATMTA-affiliated canonical authority for lore nomenclature and taxonomy. Page-level authorship and narrative claims remain separately attributed evidence.

## Provenance

- Immutable snapshot: `{RAW_ZIP_REL.as_posix()}`
- Snapshot member: `{page['upstream_path']}`
- Raw member SHA-256: `{page['raw_sha256']}`
- Normalized JSON: `{page['normalized_json_path']}`
- Normalized Markdown: `{page['normalized_markdown_path']}`
- Normalized text SHA-256: `{page['normalized_sha256']}`

## Limitations

{limitations}

## Review Status

- Canonical knowledge promoted: `NO`
- Graph facts promoted: `NO`
- Manual review required: `{str(page['manual_review_required']).upper()}`
"""


def build() -> dict[str, bytes]:
    prefix, members = zip_members()
    member_paths = set(members)
    raw_zip = ROOT / RAW_ZIP_REL
    home_bytes = (ROOT / RAW_HOME_REL).read_bytes()
    sitemap_bytes = (ROOT / RAW_SITEMAP_REL).read_bytes()
    sitemap_root = ElementTree.fromstring(sitemap_bytes.decode("utf-8-sig"))
    sitemap_urls = sorted(node.text.strip() for node in sitemap_root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if node.text)

    file_inventory = []
    for path in sorted(members):
        role, disposition = classify_file(path)
        data = members[path]
        file_inventory.append({
            "path": path,
            "archive_member": prefix + path,
            "byte_length": len(data),
            "sha256": sha256_bytes(data),
            "extension": PurePosixPath(path).suffix.lower(),
            "role": role,
            "disposition": disposition,
        })

    canon_paths = sorted(path for path in members if path.startswith("canon/") and path.endswith(".md"))
    docs_paths = sorted(path for path in members if path.startswith("docs/") and path.endswith(".md"))
    internal_paths = sorted(path for path in members if path.startswith("c4-internal/") and path.endswith(".md"))
    canon_rel = {path[len("canon/"):]: path for path in canon_paths}
    docs_rel = {path[len("docs/"):]: path for path in docs_paths}
    docs_only = sorted(set(docs_rel) - set(canon_rel))
    canon_only = sorted(set(canon_rel) - set(docs_rel))
    docs_only_content = [docs_rel[rel] for rel in docs_only if PurePosixPath(rel).name not in INDEX_NAMES]

    page_inventory: list[dict[str, Any]] = []
    mirror_divergences = []
    for path in canon_paths:
        rel = path[len("canon/"):]
        mirror = docs_rel.get(rel)
        if mirror is None:
            status = "CANON_ONLY"
        elif normalize_text(members[path]) == normalize_text(members[mirror]):
            status = "TEXT_IDENTICAL"
        else:
            status = "TEXT_DIVERGENT"
            mirror_divergences.append({
                "canon_path": path,
                "docs_path": mirror,
                "canon_sha256": sha256_bytes(members[path]),
                "docs_sha256": sha256_bytes(members[mirror]),
            })
        page_inventory.append({
            "path": path,
            "scope": "CANON_AUTHORING_SOURCE",
            "disposition": "NORMALIZED",
            "published_mirror_path": mirror,
            "published_mirror_status": status,
            "sha256": sha256_bytes(members[path]),
        })
    for path in docs_paths:
        rel = path[len("docs/"):]
        if rel in canon_rel:
            disposition = "MIRROR_INVENTORIED"
        elif PurePosixPath(rel).name in INDEX_NAMES:
            disposition = "NAVIGATION_PAGE_INVENTORIED"
        else:
            disposition = "PUBLISHED_ONLY_NORMALIZED_MANUAL_REVIEW"
        page_inventory.append({
            "path": path,
            "scope": "PUBLICATION_PRESENTATION",
            "disposition": disposition,
            "canon_source_path": canon_rel.get(rel),
            "sha256": sha256_bytes(members[path]),
        })
    for path in internal_paths:
        page_inventory.append({
            "path": path,
            "scope": "WORKING_DESIGN_MATERIAL",
            "disposition": "PRESERVED_EXCLUDED_FROM_CANONICAL_LORE_NORMALIZATION",
            "sha256": sha256_bytes(members[path]),
        })
    page_inventory.sort(key=lambda item: item["path"])

    selected_paths = canon_paths + docs_only_content
    source_ids_by_path = {path: stable_id("SRC-LORE-REPO", path) for path in selected_paths}
    pages: list[dict[str, Any]] = []
    normalized_page_text: dict[str, str] = {}
    page_entities: dict[str, str] = {}
    entity_store: dict[tuple[str, str], dict[str, Any]] = {}

    def add_entity(
        name: str,
        lore_type: str,
        repository_type: str,
        source_id: str,
        source_path: str,
        aliases: list[str] | None = None,
        attributes: dict[str, Any] | None = None,
        extraction_basis: str = "PAGE_SUBJECT",
    ) -> str:
        canonical_name = strip_markdown(name)
        key = (lore_type, canonical_name.casefold())
        entity_id = stable_id(f"LRTX-{lore_type}", canonical_name.casefold())
        if key not in entity_store:
            entity_store[key] = {
                "entity_id": entity_id,
                "canonical_name": canonical_name,
                "aliases": sorted(set(aliases or [])),
                "repository_entity_type": repository_type,
                "lore_type": lore_type,
                "source_ids": [source_id],
                "source_paths": [source_path],
                "extraction_basis": [extraction_basis],
                "authority_scope": "ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_AND_NOMENCLATURE",
                "resolution_confidence": "HIGH" if extraction_basis == "PAGE_SUBJECT" else "MEDIUM",
                "attributes": [attributes] if attributes else [],
                "id_scope": "SOURCE_LOCAL_CANONICAL_TAXONOMY",
            }
        else:
            record = entity_store[key]
            record["aliases"] = sorted(set(record["aliases"]) | set(aliases or []))
            record["source_ids"] = sorted(set(record["source_ids"]) | {source_id})
            record["source_paths"] = sorted(set(record["source_paths"]) | {source_path})
            record["extraction_basis"] = sorted(set(record["extraction_basis"]) | {extraction_basis})
            if attributes and attributes not in record["attributes"]:
                record["attributes"].append(attributes)
        return entity_id

    for path in selected_paths:
        source_text_raw = normalize_text(members[path])
        source_text, redaction_count = redact_normalized_workstation_paths(source_text_raw)
        source_id = source_ids_by_path[path]
        repository_type, lore_type, taxonomy_path = taxonomy_for_path(path)
        title = get_heading(source_text)
        alias_values = aliases_from_title(title)
        links, media_refs = extract_links(path, source_text, member_paths)
        is_published_only = path.startswith("docs/")
        is_historical_canonical_snapshot = path == HISTORICAL_CANON_SOURCE_PATH
        rel = path.split("/", 1)[1]
        mirror_path = docs_rel.get(rel) if path.startswith("canon/") else path
        if path.startswith("canon/"):
            if mirror_path is None:
                mirror_status = "CANON_ONLY"
            elif normalize_text(members[path]) == normalize_text(members[mirror_path]):
                mirror_status = "TEXT_IDENTICAL"
            else:
                mirror_status = "TEXT_DIVERGENT"
        else:
            mirror_status = "PUBLISHED_ONLY_NO_CANON_COUNTERPART"
        if mirror_path:
            site_rel = mirror_path[len("docs/"):]
            if site_rel == "index.md":
                canonical_url = SITE_PREFIX
            elif site_rel.endswith("/index.md"):
                canonical_url = SITE_PREFIX + site_rel[:-len("index.md")]
            else:
                canonical_url = SITE_PREFIX + site_rel[:-3] + "/"
        else:
            candidate_url = SITE_PREFIX + rel[:-3] + "/"
            canonical_url = candidate_url if candidate_url in sitemap_urls else f"{UPSTREAM_REPOSITORY_URL}/blob/{UPSTREAM_COMMIT}/{path}"
        limitations = []
        if is_historical_canonical_snapshot:
            limitations.append("This page is preserved as a historical canonical-source snapshot and is excluded from current canonical taxonomy authority.")
        else:
            limitations.append("ATMTA-affiliated canonical authority is limited to lore taxonomy and preferred nomenclature; page-level authorship and narrative claims remain separately attributed evidence.")
        if mirror_status == "TEXT_DIVERGENT":
            limitations.append("The published docs mirror differs from the canon authoring page and requires source-level reconciliation.")
        if mirror_status == "CANON_ONLY":
            limitations.append("No same-path published docs mirror exists in the captured repository.")
        if is_published_only:
            limitations.append("This public docs page has no same-path canon authoring source and is retained as an unreconciled publication-only page.")
        if any(item["resolution_status"] == "UNRESOLVED" for item in links + media_refs):
            limitations.append("One or more upstream relative references do not resolve inside the pinned repository snapshot.")
        if redaction_count:
            limitations.append("Absolute upstream workstation paths are preserved in immutable raw evidence and redacted from this normalized derivative by curator decision LRH-014.")
        normalized_json_path = (NORMALIZED_REL / "pages" / f"{source_id}.json").as_posix()
        normalized_markdown_path = (NORMALIZED_REL / "pages" / f"{source_id}.md").as_posix()
        page = {
            "source_id": source_id,
            "preferred_name": title,
            "aliases": alias_values,
            "upstream_path": path,
            "upstream_repository": UPSTREAM_REPOSITORY,
            "upstream_commit": UPSTREAM_COMMIT,
            "canonical_url": canonical_url,
            "source_scope": "HISTORICAL_CANONICAL_SOURCE_SNAPSHOT" if is_historical_canonical_snapshot else ("PUBLISHED_ONLY" if is_published_only else "CANON"),
            "authority_scope": "HISTORICAL_LORE_EVIDENCE_NOT_CURRENT_TAXONOMY" if is_historical_canonical_snapshot else "ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_AND_NOMENCLATURE",
            "taxonomy_status": "HISTORICAL_SNAPSHOT_EXCLUDED_FROM_CURRENT_CANONICAL_TAXONOMY" if is_historical_canonical_snapshot else "CURRENT_SOURCE_TAXONOMY",
            "claim_authority": "SOURCE_ASSERTION_REQUIRES_INDEPENDENT_EVIDENCE_FOR_PROMOTION",
            "repository_entity_type": repository_type,
            "lore_type": lore_type,
            "taxonomy_path": taxonomy_path,
            "headings": headings(source_text),
            "internal_links": [item for item in links if item["resolution_status"] != "EXTERNAL"],
            "outbound_links": [item for item in links if item["resolution_status"] == "EXTERNAL"],
            "media_references": media_refs,
            "raw_sha256": sha256_bytes(members[path]),
            "raw_byte_length": len(members[path]),
            "normalized_sha256": sha256_bytes(source_text.encode("utf-8")),
            "normalized_json_path": normalized_json_path,
            "normalized_markdown_path": normalized_markdown_path,
            "published_mirror_path": mirror_path,
            "published_mirror_status": mirror_status,
            "extraction_confidence": "HIGH",
            "manual_review_required": is_published_only or (mirror_status != "TEXT_IDENTICAL" and not is_historical_canonical_snapshot) or any(item["resolution_status"] == "UNRESOLVED" for item in links + media_refs),
            "limitations": limitations,
            "redactions": {
                "count": redaction_count,
                "policy": "PRESERVE_RAW_REDACT_NORMALIZED_AND_PUBLIC_OUTPUTS" if redaction_count else "NONE",
                "curator_decision_id": "LRH-014" if redaction_count else None,
            },
            "provenance": {
                "snapshot_path": RAW_ZIP_REL.as_posix(),
                "snapshot_sha256": EXPECTED_ZIP_SHA256,
                "snapshot_member": prefix + path,
                "captured_at": CAPTURED_AT,
            },
        }
        entity_id = add_entity(title, lore_type, repository_type, source_id, path, alias_values)
        if is_historical_canonical_snapshot:
            entity_record = entity_store[(lore_type, strip_markdown(title).casefold())]
            entity_record["authority_scope"] = "HISTORICAL_LORE_EVIDENCE_NOT_CURRENT_TAXONOMY"
            entity_record["id_scope"] = "SOURCE_LOCAL_HISTORICAL_TAXONOMY_SNAPSHOT"
            entity_record["resolution_confidence"] = "HIGH"
            entity_record["attributes"].append({
                "taxonomy_status": "HISTORICAL_SNAPSHOT_EXCLUDED_FROM_CURRENT_CANONICAL_TAXONOMY",
                "curator_decision_id": "LRH-010",
            })
        page["primary_entity_id"] = entity_id
        page_entities[path] = entity_id
        pages.append(page)
        normalized_page_text[path] = source_text

    page_by_path = {page["upstream_path"]: page for page in pages}

    named_path = "canon/meta/named_characters.md"
    named_page = page_by_path[named_path]
    for line, row in table_rows(normalized_page_text[named_path], "Name"):
        if not {"Name", "Species", "Role", "Allegiance"}.issubset(row):
            continue
        observed_name = strip_markdown(row["Name"])
        if not observed_name or observed_name.casefold() == "name":
            continue
        alias_values = []
        match = re.match(r"^(.+?)\s+\(([^)]+)\)$", observed_name)
        canonical_name = observed_name
        if match and len(match.group(2)) < 40:
            canonical_name = match.group(1).strip()
            alias_values = [match.group(2).strip()]
        add_entity(
            canonical_name,
            "CHARACTER",
            "PERSON",
            named_page["source_id"],
            named_path,
            alias_values,
            {
                "line": line,
                "species_observed": strip_markdown(row.get("Species", "")) or None,
                "role_observed": strip_markdown(row.get("Role", "")) or None,
                "allegiance_observed": strip_markdown(row.get("Allegiance", "")) or None,
                "source_cell_observed": strip_markdown(row.get("Source", "")) or None,
            },
            "NAMED_CHARACTER_REGISTRY_ROW",
        )

    planets_path = "canon/reference/atlas/planets.md"
    planets_page = page_by_path[planets_path]
    planet_text = normalized_page_text[planets_path]
    parent_heading = None
    heading_by_line = {item["line"]: item for item in headings(planet_text) if item["level"] in {2, 3}}
    table_planet_rows = table_rows(planet_text, "Planet/Location")
    for line, row in table_planet_rows:
        for heading_line in sorted((value for value in heading_by_line if value < line), reverse=True):
            parent_heading = heading_by_line[heading_line]["text"]
            break
        name = strip_markdown(row.get("Planet/Location", ""))
        if not name or "unnamed" in name.casefold():
            continue
        type_observed = strip_markdown(row.get("Type", ""))
        lower = type_observed.casefold()
        if "station" in lower:
            lore_type = "STATION"
        elif "moon" in lower:
            lore_type = "MOON"
        elif "planet" in lower or "world" in lower or "capital" in lower:
            lore_type = "PLANET"
        elif "system" in lower:
            lore_type = "STAR_SYSTEM"
        else:
            lore_type = "LOCATION"
        add_entity(
            name,
            lore_type,
            "LOCATION",
            planets_page["source_id"],
            planets_path,
            attributes={
                "line": line,
                "type_observed": type_observed or None,
                "parent_heading_observed": parent_heading,
                "description_observed": strip_markdown(row.get("Description", "")) or None,
            },
            extraction_basis="PLANET_LOCATION_REGISTRY_ROW",
        )

    resources_path = "canon/reference/resources/galia_expanse_resources.md"
    resources_page = page_by_path[resources_path]
    active_family = None
    active_tier = None
    for line_number, line in enumerate(normalized_page_text[resources_path].splitlines(), start=1):
        if line.startswith("## "):
            active_family = clean_title(line[3:])
        elif line.startswith("### "):
            active_tier = clean_title(line[4:])
        elif re.match(r"^\*\s+\S", line):
            name = strip_markdown(re.sub(r"^\*\s+", "", line))
            add_entity(
                name,
                "RESOURCE",
                "RESOURCE",
                resources_page["source_id"],
                resources_path,
                attributes={"line": line_number, "family_observed": active_family, "tier_observed": active_tier},
                extraction_basis="RESOURCE_REGISTRY_BULLET",
            )

    artifacts_path = "canon/reference/crafting/crafted_items_descriptions.md"
    artifacts_page = page_by_path[artifacts_path]
    active_family = None
    for line_number, line in enumerate(normalized_page_text[artifacts_path].splitlines(), start=1):
        if line.startswith("## "):
            active_family = clean_title(line[3:])
        elif line.startswith("### "):
            raw_name = clean_title(line[4:])
            if raw_name.casefold() == "summary":
                continue
            name = re.sub(r"\s+\([^)]*Tier[^)]*\)\s*$", "", raw_name, flags=re.I).strip()
            add_entity(
                name,
                "ARTIFACT",
                "RESOURCE",
                artifacts_page["source_id"],
                artifacts_path,
                attributes={"line": line_number, "family_observed": active_family, "heading_observed": raw_name},
                extraction_basis="CRAFTED_ITEM_HEADING",
            )

    entities = sorted(entity_store.values(), key=lambda item: item["entity_id"])

    relationships: list[dict[str, Any]] = []
    unresolved_links: list[dict[str, Any]] = []
    for page in pages:
        for item in page["internal_links"]:
            target_path = item["resolved_path"]
            target_page = page_by_path.get(target_path or "")
            status = item["resolution_status"]
            if status == "RESOLVED" and target_page is None:
                status = "RESOLVED_NON_SOURCE_PAGE"
            relationship = {
                "relationship_id": stable_id("LREL", page["source_id"], str(item["line"]), item["original_target"], item.get("label") or ""),
                "source_id": page["source_id"],
                "source_entity_id": page["primary_entity_id"],
                "target_source_id": target_page["source_id"] if target_page else None,
                "target_entity_id": target_page["primary_entity_id"] if target_page else None,
                "relationship_type": "REFERENCES",
                "label_observed": item["label"],
                "target_observed": item["original_target"],
                "target_path": target_path,
                "resolution_status": status,
                "provenance": {"source_id": page["source_id"], "line": item["line"], "confidence": "HIGH"},
                "semantic_scope": "DOCUMENT_REFERENCE_NOT_ASSERTED_FACT_RELATIONSHIP",
            }
            relationships.append(relationship)
            if status == "UNRESOLVED":
                unresolved_links.append(relationship)
    relationships.sort(key=lambda item: item["relationship_id"])

    media_records = []
    for path in sorted(path for path in members if PurePosixPath(path).suffix.lower() in MEDIA_EXTENSIONS):
        referenced_by = []
        for page in pages:
            for reference in page["media_references"]:
                if reference["resolved_path"] == path:
                    referenced_by.append({"source_id": page["source_id"], "line": reference["line"], "alt_text": reference["label"]})
        in_canon = path.startswith("canon/")
        output_path = (RAW_REL / "media" / path).as_posix() if in_canon else None
        media_records.append({
            "media_id": stable_id("LMEDIA", path),
            "upstream_path": path,
            "sha256": sha256_bytes(members[path]),
            "byte_length": len(members[path]),
            "media_type": mimetypes.guess_type(path)[0] or "application/octet-stream",
            "referenced_by": referenced_by,
            "disposition": "EXTRACTED_CANON_MEDIA" if in_canon else "PRESERVED_IN_SNAPSHOT_EXCLUDED_WORKING_MATERIAL",
            "extracted_path": output_path,
        })

    nav_text = normalize_text(members["mkdocs.yml"])
    nav_entries = []
    for line_number, line in enumerate(nav_text.splitlines(), start=1):
        match = re.match(r"^(\s*)-\s+(?:(.+?):\s+)?([^\s]+\.md)\s*$", line)
        if not match:
            continue
        nav_path = "docs/" + match.group(3).strip("'\"")
        nav_entries.append({
            "line": line_number,
            "depth": len(match.group(1)) // 2,
            "label": strip_markdown(match.group(2) or PurePosixPath(nav_path).stem),
            "docs_path": nav_path,
            "resolution_status": "RESOLVED" if nav_path in members else "UNRESOLVED",
        })

    expected_urls = []
    for path in docs_paths:
        rel = path[len("docs/"):]
        if rel == "index.md":
            url = SITE_PREFIX
        elif rel.endswith("/index.md"):
            url = SITE_PREFIX + rel[:-len("index.md")]
        else:
            url = SITE_PREFIX + rel[:-3] + "/"
        expected_urls.append(url)
    expected_urls = sorted(expected_urls)
    navigation = {
        "campaign_id": CAMPAIGN_ID,
        "upstream_commit": UPSTREAM_COMMIT,
        "mkdocs_navigation": nav_entries,
        "live_sitemap_urls": sitemap_urls,
        "expected_urls_from_docs": expected_urls,
        "sitemap_missing_expected_urls": sorted(set(expected_urls) - set(sitemap_urls)),
        "sitemap_extra_urls": sorted(set(sitemap_urls) - set(expected_urls)),
        "unresolved_navigation_targets": [item for item in nav_entries if item["resolution_status"] == "UNRESOLVED"],
        "deployment": {
            "branch": DEPLOYMENT_BRANCH,
            "deployment_commit": DEPLOYMENT_COMMIT,
            "declared_source_commit": DEPLOYED_SOURCE_COMMIT,
            "deployment_date": DEPLOYMENT_DATE,
            "current_main_commit": UPSTREAM_COMMIT,
            "status": "LIVE_SITE_DEPLOYMENT_PRECEDES_CAPTURED_MAIN_COMMIT",
        },
    }

    migration_mappings = []
    for mapping in EXISTING_LORE_MAPPINGS:
        targets = []
        for path in mapping["candidates"]:
            page = page_by_path.get(path)
            if page:
                targets.append({
                    "source_id": page["source_id"],
                    "entity_id": page["primary_entity_id"],
                    "preferred_name": page["preferred_name"],
                    "lore_type": page["lore_type"],
                    "path": path,
                })
        if len(targets) == 1:
            status = "MAPPED_ONE_TO_ONE"
        elif len(targets) > 1:
            status = "AMBIGUOUS_MULTIPLE_TARGETS"
        else:
            status = "UNRESOLVED_NO_DIRECT_PAGE"
        mapping_record = {
            "existing_id": mapping["existing_id"],
            "legacy_name": mapping["existing_name"],
            "status": status,
            "targets": targets,
            "legacy_name_preservation": "PRESERVE_AS_ALIAS_OR_LEGACY_LABEL_AFTER_REVIEW",
            "automatic_rewrite_allowed": False,
            "manual_review_required": status != "MAPPED_ONE_TO_ONE",
        }
        if mapping["existing_id"] == "LORE-GALIA":
            mapping_record.update({
                "status": "MAPPED_TO_REGION_WITH_REFERENCE_DOCUMENT_RETAINED",
                "canonical_targets": [item for item in targets if item["lore_type"] == "REGION"],
                "reference_targets": [item for item in targets if item["lore_type"] == "REFERENCE"],
                "manual_review_required": False,
                "curator_decision_id": "LRH-002",
            })
        elif mapping["existing_id"] == "LORE-COUNCIL-PEACE":
            mapping_record.update({
                "status": "MAPPED_TO_INSTITUTION_WITH_DISTINCT_RELATED_FACTION",
                "canonical_targets": [item for item in targets if item["lore_type"] == "INSTITUTION"],
                "related_targets": [item for item in targets if item["lore_type"] == "FACTION"],
                "manual_review_required": False,
                "curator_decision_id": "LRH-003",
            })
        elif mapping["existing_id"] == "LORE-FACTION-USTUR":
            mapping_record.update({
                "status": "MAPPED_TO_FACTION_WITH_DISTINCT_RELATED_SPECIES",
                "canonical_targets": [item for item in targets if item["lore_type"] == "FACTION"],
                "related_targets": [item for item in targets if item["lore_type"] == "SPECIES"],
                "manual_review_required": False,
                "curator_decision_id": "LRH-004",
            })
        elif mapping["existing_id"] in {"LORE-NARRATIVE-CORE", "LORE-VOICE-OF-IRIS"}:
            mapping_record.update({
                "status": "PRESERVED_LEGACY_ENTITY_NEW_MAPPING_DEFERRED",
                "manual_review_required": False,
                "curator_decision_id": "LRH-005" if mapping["existing_id"] == "LORE-NARRATIVE-CORE" else "LRH-006",
            })
        migration_mappings.append(mapping_record)

    lore_type_counts = Counter(entity["lore_type"] for entity in entities)
    taxonomy = {
        "taxonomy_id": "STAR-ATLAS-LORE-TAXONOMY-22555F2",
        "version_basis": UPSTREAM_COMMIT,
        "authority": {
            "designation": "ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_AND_NOMENCLATURE",
            "scope": "IN_UNIVERSE_LORE_ONLY",
            "does_not_establish": [
                "page-level authorship for every source file",
                "independent truth of every narrative claim",
                "governance, operational, provenance, or historical authority outside lore",
            ],
            "precedence": [
                "STAR_ATLAS_LORE_REPOSITORY_FOR_LORE_TAXONOMY_AND_PREFERRED_NAMES",
                "OFFICIAL_STAR_ATLAS_PUBLICATIONS_FOR_NEWER_LORE_NOT_YET_REPRESENTED",
                "ARCHIVE_HISTORICAL_SOURCES_FOR_HISTORICAL_EVIDENCE",
                "OPERATOR_CONFIRMATIONS_FOR_ARCHIVAL_AMBIGUITY",
                "DERIVED_KNOWLEDGE_FOR_DISCOVERY_ONLY",
            ],
        },
        "hierarchy": LORE_TYPE_HIERARCHY,
        "repository_schema_compatibility": LORE_TO_REPOSITORY_TYPE,
        "compatibility_limitations": {
            "SPECIES": "Repository Schema v2.1 has no SPECIES type; COMMUNITY is retained as the broad compatibility type and lore_type=SPECIES is authoritative.",
            "ARTIFACT": "Repository Schema v2.1 has no ARTIFACT type; RESOURCE is retained as the broad compatibility type and lore_type=ARTIFACT is authoritative.",
            "place_subtypes": "PLANET, WORLD, MOON, STATION, STAR_SYSTEM, SECTOR, and REGION refine Repository Schema v2.1 LOCATION.",
        },
        "adopted_lore_types": sorted({item for values in LORE_TYPE_HIERARCHY.values() for item in values}),
        "entity_counts": dict(sorted(lore_type_counts.items())),
        "historical_snapshot_entity_count": sum(entity["authority_scope"] == "HISTORICAL_LORE_EVIDENCE_NOT_CURRENT_TAXONOMY" for entity in entities),
        "identifier_policy": "LRTX identifiers are deterministic source-taxonomy IDs and do not replace registry-assigned repository canonical IDs.",
    }

    embedded_local_paths = []
    for path in canon_paths:
        for line_number, line in enumerate(normalize_text(members[path]).splitlines(), start=1):
            if re.search(r"[A-Za-z]:\\Users\\", line):
                embedded_local_paths.append({"path": path, "line": line_number, "text_sha256": sha256_bytes(line.encode("utf-8"))})

    upstream_verification = json.loads(normalize_text(members["canon/meta/_verification_report.json"]))
    conflicts = [
        {
            "conflict_id": "LRC-001-AUTHORITY-LABEL",
            "severity": "HIGH",
            "topic": "Upstream identity and authority labeling",
            "finding": "Repository API/default-branch metadata describes a fan-created encyclopedia, while main-branch and deployed-site metadata use an Official Star Atlas Lore Encyclopedia description.",
            "disposition": "CURATOR ADJUDICATED: Jose is a Star Atlas team member responsible for lore; the personal repository is ATMTA-affiliated canonical lore authority. Page-level authorship remains separately attributed.",
            "manual_review_required": False,
        },
        {
            "conflict_id": "LRC-003-BRANCH-AUTHORITY",
            "severity": "MEDIUM",
            "topic": "Default branch differs from active content branch",
            "finding": f"Default branch {DEFAULT_BRANCH_AT_CAPTURE} points to {DEFAULT_BRANCH_COMMIT}; current content and deployment workflow use main at {UPSTREAM_COMMIT}.",
            "disposition": "MAIN_COMMIT_SELECTED_AND_ALL_BRANCH_IDENTITIES_PRESERVED.",
            "manual_review_required": False,
        },
        {
            "conflict_id": "LRC-004-DEPLOYMENT-STALE",
            "severity": "MEDIUM",
            "topic": "Live deployment does not match current main",
            "finding": f"The live gh-pages deployment declares source {DEPLOYED_SOURCE_COMMIT}, preceding captured main {UPSTREAM_COMMIT}.",
            "disposition": "SOURCE_COMMIT_AND_LIVE_SITE_PROVENANCE_REMAIN_DISTINCT.",
            "manual_review_required": False,
        },
        {
            "conflict_id": "LRC-005-MIRROR-DIVERGENCE",
            "severity": "HIGH" if mirror_divergences else "LOW",
            "topic": "Canon authoring pages versus docs publication mirrors",
            "finding": f"{len(mirror_divergences)} same-path Markdown mirrors differ after UTF-8/LF normalization; {len(canon_only)} canon pages have no same-path docs mirror; {len(docs_only_content)} non-index docs pages have no same-path canon source.",
            "disposition": "CURATOR_ADJUDICATED: CANON CONTROLS TAXONOMY; BOTH TEXT VARIANTS REMAIN PRESERVED.",
            "manual_review_required": False,
        },
        {
            "conflict_id": "LRC-006-UPSTREAM-LINKS",
            "severity": "MEDIUM",
            "topic": "Unresolved upstream relative links",
            "finding": f"{len(unresolved_links)} relative Markdown links do not resolve to a member of the pinned snapshot.",
            "disposition": "CURATOR_ADJUDICATED: SOURCE PRESERVED; REPAIR DEFERRED TO A SEPARATE LINK-REPAIR CAMPAIGN.",
            "manual_review_required": False,
        },
        {
            "conflict_id": "LRC-007-NAVIGATION",
            "severity": "MEDIUM",
            "topic": "MkDocs navigation resolution",
            "finding": f"{len(navigation['unresolved_navigation_targets'])} configured navigation targets are absent from the pinned docs tree; sitemap has {len(navigation['sitemap_missing_expected_urls'])} missing expected and {len(navigation['sitemap_extra_urls'])} extra URLs.",
            "disposition": "CURATOR_ADJUDICATED: LIVE SITEMAP AND SOURCE NAVIGATION PRESERVED SEPARATELY; ONI/CSS PAGE CLASSIFIED AS A HISTORICAL CANONICAL-SOURCE SNAPSHOT.",
            "manual_review_required": False,
        },
        {
            "conflict_id": "LRC-008-UPSTREAM-VERIFICATION",
            "severity": "HIGH",
            "topic": "Upstream self-reported chronology and consistency findings",
            "finding": f"The upstream verification artifact reports {len(upstream_verification.get('chrono_errors', []))} chronology errors, {len(upstream_verification.get('contradictions', []))} possible contradictions, and {len(upstream_verification.get('orphaned_years', []))} orphaned years.",
            "disposition": "PRESERVED_AS_UPSTREAM SELF-ASSESSMENT; NO CLAIM CORRECTIONS APPLIED.",
            "manual_review_required": False,
        },
        {
            "conflict_id": "LRC-009-LOCAL-PATHS",
            "severity": "LOW",
            "topic": "Embedded workstation paths",
            "finding": f"{len(embedded_local_paths)} canon lines contain absolute Windows user paths.",
            "disposition": "CURATOR_ADJUDICATED: PRESERVED IN IMMUTABLE RAW EVIDENCE; REDACTED FROM NORMALIZED RECORDS AND PUBLIC-FACING DERIVATIVES.",
            "manual_review_required": False,
        },
    ]

    migration_report = {
        "campaign_id": CAMPAIGN_ID,
        "authority_scope": taxonomy["authority"],
        "adopted_classifications": taxonomy["adopted_lore_types"],
        "classification_counts": taxonomy["entity_counts"],
        "migration_mappings": migration_mappings,
        "renamed_entities": [],
        "renamed_entities_note": "No rename was asserted solely from lexical similarity. Ambiguous candidates remain unresolved.",
        "aliases": [
            {"entity_id": entity["entity_id"], "preferred_name": entity["canonical_name"], "aliases": entity["aliases"]}
            for entity in entities if entity["aliases"]
        ],
        "deprecated_names": [],
        "deprecated_names_note": "No source-native deprecation statement was identified by the structural extractor; legacy Archive names remain preserved pending review.",
        "hierarchy_changes": [
            {
                "legacy_id": "LORE-FACTION-USTUR",
                "legacy_classification": "Major faction / Ustur Sector",
                "proposed_taxonomy": ["SPECIES: Ustur", "FACTION: Ustur"],
                "status": "CURATOR_ADJUDICATED_DISTINCT_ENTITIES",
                "curator_decision_id": "LRH-004",
                "reason": "The upstream taxonomy contains distinct species and faction pages with the same preferred name.",
            },
            {
                "legacy_id": "LORE-COUNCIL-PEACE",
                "legacy_classification": "Political institution",
                "proposed_taxonomy": ["INSTITUTION: Council of Peace", "FACTION: Council of Peace"],
                "status": "CURATOR_ADJUDICATED_DISTINCT_ENTITIES",
                "curator_decision_id": "LRH-003",
                "reason": "The upstream taxonomy contains distinct institution and faction pages.",
            },
        ],
        "unresolved_conflicts": [item["conflict_id"] for item in conflicts if item["manual_review_required"]],
        "automatic_historical_rewrites": 0,
    }

    research_backlog = {
        "campaign_id": CAMPAIGN_ID,
        "items": [
            {"priority": 1, "topic": "Page-level authorship granularity", "required_artifact": "Optional per-page bylines or commit attribution if future work needs authorship beyond Jose's operator-confirmed institutional lore role.", "related_conflicts": ["LRC-001-AUTHORITY-LABEL"], "blocking": False},
            {"priority": 2, "topic": "Canon/docs narrative reconciliation", "required_artifact": "Upstream-generated diff or maintainer adjudication for narrative differences; canon already controls taxonomy under LRH-008.", "related_conflicts": ["LRC-005-MIRROR-DIVERGENCE"], "blocking": False},
            {"priority": 3, "topic": "Deferred legacy lore mapping", "required_artifact": "Direct upstream pages or official evidence for Star Atlas: CORE and The Voice of Iris.", "related_conflicts": [], "blocking": False},
            {"priority": 4, "topic": "Chronology and contradiction review", "required_artifact": "Primary official lore citations resolving each upstream self-reported chronology error and contradiction.", "related_conflicts": ["LRC-008-UPSTREAM-VERIFICATION"]},
            {"priority": 5, "topic": "Broken upstream references", "required_artifact": "Replacement target paths or source pages for unresolved Markdown links and MkDocs navigation entries.", "related_conflicts": ["LRC-006-UPSTREAM-LINKS", "LRC-007-NAVIGATION"]},
            {"priority": 6, "topic": "Live deployment freshness", "required_artifact": "A gh-pages deployment from the selected main commit or an upstream declaration that the older deployment is intentional.", "related_conflicts": ["LRC-004-DEPLOYMENT-STALE"]},
        ],
    }

    human_review = {
        "campaign_id": CAMPAIGN_ID,
        "operator_directives_applied": [
            "Licensing status is excluded from campaign requirements, restrictions, validation, conflicts, and review queues."
        ],
        "decision_items": [
            {
                "review_id": "LRH-001",
                "topic": "Upstream identity label",
                "decision_needed": "Choose how the Archive should describe the upstream repository without inferring ATMTA authorship.",
                "recommended_disposition": "KEEP_OPERATOR_DESIGNATED_TAXONOMY_AUTHORITY_WITH_OFFICIAL_AFFILIATION_UNVERIFIED",
                "allowed_dispositions": ["KEEP_OPERATOR_DESIGNATED_TAXONOMY_AUTHORITY_WITH_OFFICIAL_AFFILIATION_UNVERIFIED", "DESCRIBE_AS_OFFICIAL_STAR_ATLAS_SOURCE", "DESCRIBE_AS_FAN_CURATED_SOURCE"],
                "evidence": ["LRC-001-AUTHORITY-LABEL", "archive/provenance/lore-repository/authority-assessment.json"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-002",
                "topic": "Galia Expanse legacy mapping",
                "decision_needed": "Map LORE-GALIA to the region, the atlas reference document, both, or neither.",
                "recommended_disposition": "MAP_TO_REGION_AND_RETAIN_ATLAS_DOCUMENT_AS_REFERENCE",
                "allowed_dispositions": ["MAP_TO_REGION_AND_RETAIN_ATLAS_DOCUMENT_AS_REFERENCE", "MAP_TO_ATLAS_DOCUMENT", "MAP_TO_BOTH", "DEFER"],
                "evidence": ["canon/geography/galactic_regions.md", "canon/reference/atlas/galia_expanse_atlas.md"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-003",
                "topic": "Council of Peace entity split",
                "decision_needed": "Decide whether the institution and faction pages represent distinct canonical entities or two views of one entity.",
                "recommended_disposition": "KEEP_DISTINCT_INSTITUTION_AND_FACTION_ENTITIES_WITH_SHARED_ALIAS",
                "allowed_dispositions": ["KEEP_DISTINCT_INSTITUTION_AND_FACTION_ENTITIES_WITH_SHARED_ALIAS", "MERGE_AS_ONE_INSTITUTION", "MERGE_AS_ONE_FACTION", "DEFER"],
                "evidence": ["canon/institutions/council_of_peace.md", "canon/factions/council_of_peace.md"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-004",
                "topic": "Ustur entity split",
                "decision_needed": "Decide whether Ustur species and Ustur faction remain distinct canonical entities.",
                "recommended_disposition": "KEEP_DISTINCT_SPECIES_AND_FACTION_ENTITIES_WITH_SHARED_NAME",
                "allowed_dispositions": ["KEEP_DISTINCT_SPECIES_AND_FACTION_ENTITIES_WITH_SHARED_NAME", "MAP_LEGACY_ID_TO_FACTION_ONLY", "MAP_LEGACY_ID_TO_SPECIES_ONLY", "DEFER"],
                "evidence": ["canon/species/ustur.md", "canon/factions/ustur.md"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-005",
                "topic": "Star Atlas: CORE legacy entity",
                "decision_needed": "Choose whether to preserve the unmatched legacy entity or defer it until a direct upstream page is acquired.",
                "recommended_disposition": "PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING",
                "allowed_dispositions": ["PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING", "DEPRECATE_LEGACY_ENTITY", "RESEARCH_FOR_DIRECT_PAGE"],
                "evidence": ["LORE-NARRATIVE-CORE", "operations/campaigns/lore-repository-ingestion-2026-07/taxonomy-migration-report.json"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-006",
                "topic": "The Voice of Iris legacy entity",
                "decision_needed": "Choose whether to preserve the unmatched legacy entity or defer it until a direct upstream page is acquired.",
                "recommended_disposition": "PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING",
                "allowed_dispositions": ["PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING", "DEPRECATE_LEGACY_ENTITY", "RESEARCH_FOR_DIRECT_PAGE"],
                "evidence": ["LORE-VOICE-OF-IRIS", "operations/campaigns/lore-repository-ingestion-2026-07/taxonomy-migration-report.json"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-007",
                "topic": "Source branch and live deployment",
                "decision_needed": "Confirm whether current main remains the ingestion authority even though the live gh-pages deployment is older.",
                "recommended_disposition": "KEEP_CURRENT_MAIN_AS_SOURCE_AND_PRESERVE_LIVE_SITE_AS_SEPARATE_SNAPSHOT",
                "allowed_dispositions": ["KEEP_CURRENT_MAIN_AS_SOURCE_AND_PRESERVE_LIVE_SITE_AS_SEPARATE_SNAPSHOT", "USE_LIVE_DEPLOYMENT_TEXT", "WAIT_FOR_REDEPLOYMENT"],
                "evidence": ["LRC-003-BRANCH-AUTHORITY", "LRC-004-DEPLOYMENT-STALE"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-008",
                "topic": "Canon/docs mirror divergence policy",
                "decision_needed": "Choose the standing rule for 86 divergent canon/docs page pairs.",
                "recommended_disposition": "CANON_CONTROLS_TAXONOMY_AND_BOTH_TEXT_VARIANTS_REMAIN_PRESERVED",
                "allowed_dispositions": ["CANON_CONTROLS_TAXONOMY_AND_BOTH_TEXT_VARIANTS_REMAIN_PRESERVED", "DOCS_CONTROLS_PUBLISHED_TEXT", "REQUIRE_PAGE_BY_PAGE_ADJUDICATION"],
                "evidence": ["operations/campaigns/lore-repository-ingestion-2026-07/mirror-divergence-ledger.json"],
                "evidence_count": len(mirror_divergences),
                "status": "OPEN",
            },
            {
                "review_id": "LRH-009",
                "topic": "Unresolved upstream links",
                "decision_needed": "Choose whether 252 broken source-local links remain preserved defects or receive a later repair campaign.",
                "recommended_disposition": "PRESERVE_SOURCE_AND_STAGE_SEPARATE_LINK_REPAIR_CAMPAIGN",
                "allowed_dispositions": ["PRESERVE_SOURCE_AND_STAGE_SEPARATE_LINK_REPAIR_CAMPAIGN", "LEAVE_PERMANENTLY_UNRESOLVED", "REPAIR_NORMALIZED_LINKS_NOW"],
                "evidence": ["operations/campaigns/lore-repository-ingestion-2026-07/unresolved-reference-ledger.json"],
                "evidence_count": len(unresolved_links),
                "status": "OPEN",
            },
            {
                "review_id": "LRH-010",
                "topic": "Live sitemap-only ONI/CSS lore page",
                "decision_needed": "Classify the live sitemap URL that is absent from current docs but present in the canon source tree.",
                "recommended_disposition": "KEEP_AS_CANON_SOURCE_WITH_STALE_DEPLOYMENT_PROVENANCE",
                "allowed_dispositions": ["KEEP_AS_CANON_SOURCE_WITH_STALE_DEPLOYMENT_PROVENANCE", "TREAT_AS_LIVE_SITE_ONLY", "DEFER"],
                "evidence": ["canon/geography/oni_css_lore_layer.md", "https://joseeduardonoot.github.io/star-atlas-lore/geography/oni_css_lore_layer/"],
                "status": "OPEN",
            },
            {
                "review_id": "LRH-011",
                "topic": "Self-reported chronology ordering errors",
                "decision_needed": "Adjudicate or defer each of the 12 source-reported chronology ordering errors.",
                "recommended_disposition": "DEFER_INDIVIDUAL_CORRECTIONS_UNTIL_OFFICIAL_PRIMARY_EVIDENCE_IS_ATTACHED",
                "allowed_dispositions": ["DEFER_INDIVIDUAL_CORRECTIONS_UNTIL_OFFICIAL_PRIMARY_EVIDENCE_IS_ATTACHED", "ACCEPT_UPSTREAM_ORDER", "CORRECT_SELECTED_ITEMS_WITH_CITATIONS"],
                "evidence": upstream_verification.get("chrono_errors", []),
                "evidence_count": len(upstream_verification.get("chrono_errors", [])),
                "status": "OPEN",
            },
            {
                "review_id": "LRH-012",
                "topic": "Possible contradiction clusters",
                "decision_needed": "Adjudicate or dismiss each of the 20 machine-flagged lexical contradiction clusters.",
                "recommended_disposition": "TREAT_AS_RESEARCH_CANDIDATES_NOT_CONFIRMED_CONTRADICTIONS",
                "allowed_dispositions": ["TREAT_AS_RESEARCH_CANDIDATES_NOT_CONFIRMED_CONTRADICTIONS", "REVIEW_CLUSTER_BY_CLUSTER", "ACCEPT_AS_CONTRADICTIONS"],
                "evidence": upstream_verification.get("contradictions", []),
                "evidence_count": len(upstream_verification.get("contradictions", [])),
                "status": "OPEN",
            },
            {
                "review_id": "LRH-013",
                "topic": "Orphaned timeline years",
                "decision_needed": "Decide whether seven unindexed years require timeline additions or should remain source-local references.",
                "recommended_disposition": "PRESERVE_AS_RESEARCH_GAPS_PENDING_TIMELINE_EVIDENCE_REVIEW",
                "allowed_dispositions": ["PRESERVE_AS_RESEARCH_GAPS_PENDING_TIMELINE_EVIDENCE_REVIEW", "ADD_TO_LORE_TIMELINE_INDEX", "DISMISS_AS_NON_EVENT_REFERENCES"],
                "evidence": upstream_verification.get("orphaned_years", []),
                "evidence_count": len(upstream_verification.get("orphaned_years", [])),
                "status": "OPEN",
            },
            {
                "review_id": "LRH-014",
                "topic": "Embedded workstation paths",
                "decision_needed": "Choose whether normalized display copies should redact two upstream absolute workstation paths while raw evidence remains immutable.",
                "recommended_disposition": "PRESERVE_RAW_AND_REDACT_ONLY_IN_FUTURE_PUBLICATION_OUTPUTS",
                "allowed_dispositions": ["PRESERVE_RAW_AND_REDACT_ONLY_IN_FUTURE_PUBLICATION_OUTPUTS", "PRESERVE_EVERYWHERE", "REDACT_NORMALIZED_DISPLAY_COPIES"],
                "evidence": embedded_local_paths,
                "evidence_count": len(embedded_local_paths),
                "status": "OPEN",
            },
        ],
    }
    for item in human_review["decision_items"]:
        decision = CURATOR_DECISIONS[item["review_id"]]
        item.update({
            "status": "ACCEPTED",
            "accepted_disposition": decision["accepted_disposition"],
            "decided_by": "REPOSITORY_OPERATOR",
            "decided_at": CURATOR_DECISION_DATE,
        })
        if "decision_note" in decision:
            item["decision_note"] = decision["decision_note"]

    source_records_json: dict[str, str] = {}
    source_records_md: dict[str, str] = {}
    normalized_pages_json: dict[str, str] = {}
    normalized_pages_md: dict[str, str] = {}
    for page in sorted(pages, key=lambda item: item["source_id"]):
        source_id = page["source_id"]
        normalized_pages_json[(NORMALIZED_REL / "pages" / f"{source_id}.json").as_posix()] = dump_json(page)
        normalized_pages_md[(NORMALIZED_REL / "pages" / f"{source_id}.md").as_posix()] = page_markdown(page, normalized_page_text[page["upstream_path"]])
        source_record = {
            "source_id": source_id,
            "title": page["preferred_name"],
            "publisher": UPSTREAM_REPOSITORY,
            "creator": ["JoseEduardonoot"],
            "creator_scope": "REPOSITORY_ACCOUNT; PAGE_LEVEL_AUTHORSHIP_UNKNOWN",
            "source_type": "lore_repository",
            "document_type": "HISTORICAL_LORE_REPOSITORY_SNAPSHOT" if page["source_scope"] == "HISTORICAL_CANONICAL_SOURCE_SNAPSHOT" else "LORE_REPOSITORY_PAGE",
            "canonical_url": page["canonical_url"],
            "published_at_original": None,
            "published_at_normalized": None,
            "updated_at_original": None,
            "updated_at_normalized": None,
            "captured_at": CAPTURED_AT,
            "access": "public",
            "authenticity": "repository_commit_verified",
            "source_lineage": {
                "publication": UPSTREAM_REPOSITORY,
                "publication_role": "HISTORICAL_CANONICAL_SOURCE_SNAPSHOT" if page["source_scope"] == "HISTORICAL_CANONICAL_SOURCE_SNAPSHOT" else "ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_SOURCE",
                "relationship": "PRESERVED_FROM_COMMIT",
                "primary_sources": [f"{UPSTREAM_REPOSITORY_URL}/blob/{UPSTREAM_COMMIT}/{page['upstream_path']}"],
                "original_creators": ["JoseEduardonoot (repository account; page-level authorship unknown)"],
                "lineage_confidence": "HIGH_FOR_REPOSITORY_PATH_AND_COMMIT; UNKNOWN_FOR_UNDERLYING_CLAIM_AUTHORSHIP",
            },
            "taxonomy": {
                "preferred_name": page["preferred_name"],
                "aliases": page["aliases"],
                "lore_type": page["lore_type"],
                "repository_entity_type": page["repository_entity_type"],
                "primary_entity_id": page["primary_entity_id"],
                "taxonomy_status": page["taxonomy_status"],
                "authority_scope": page["authority_scope"],
            },
            "quality": {
                "extraction_confidence": page["extraction_confidence"],
                "manual_review_required": page["manual_review_required"],
                "limitations": page["limitations"],
                "redactions": page["redactions"],
            },
            "provenance": page["provenance"],
            "artifact_chain": {
                "normalized_json": page["normalized_json_path"],
                "normalized_markdown": page["normalized_markdown_path"],
                "source_record_json": (SOURCE_RECORDS_REL / f"{source_id}.json").as_posix(),
                "source_record_markdown": (SOURCE_RECORDS_REL / f"{source_id}.md").as_posix(),
            },
        }
        source_records_json[(SOURCE_RECORDS_REL / f"{source_id}.json").as_posix()] = dump_json(source_record)
        source_records_md[(SOURCE_RECORDS_REL / f"{source_id}.md").as_posix()] = source_record_markdown(page)

    package = {
        "metadata": {
            "repository_schema": "2.1",
            "artifact_type": "INGESTION_PACKAGE",
            "ingestion_id": "INGEST-LORE-REPOSITORY-22555F2",
            "campaign_id": CAMPAIGN_ID,
            "promotion_status": "ARCHIVED_NOT_KNOWLEDGE_OR_GRAPH_PROMOTED",
        },
        "sources": [
            {
                "source_id": page["source_id"],
                "title": page["preferred_name"],
                "type": "LORE_REPOSITORY_PAGE",
                "tier": page["authority_scope"],
                "url": page["canonical_url"],
                "language": "English",
                "source_lineage": {
                    "publication": UPSTREAM_REPOSITORY,
                    "relationship": "PRESERVED_FROM_COMMIT",
                    "authority_scope": page["authority_scope"],
                },
            }
            for page in sorted(pages, key=lambda item: item["source_id"])
        ],
        "entities": [
            {
                "entity_id": entity["entity_id"],
                "canonical_name": entity["canonical_name"],
                "entity_type": entity["repository_entity_type"],
                "lore_type": entity["lore_type"],
                "aliases": entity["aliases"],
                "role": None,
                "confidence": entity["resolution_confidence"],
                "source_ids": entity["source_ids"],
                "id_scope": entity["id_scope"],
            }
            for entity in entities
        ],
        "claims": [],
        "events": [],
        "quotes": [],
        "relationships": relationships,
        "timeline_updates": [],
        "research_tasks": research_backlog["items"],
        "knowledge_delta": {},
        "repository_health": {
            "manual_review_required": False,
            "curator_adjudication_complete": True,
            "conflict_count": len(conflicts),
            "unresolved_link_count": len(unresolved_links),
            "taxonomy_mappings_requiring_review": sum(item["manual_review_required"] for item in migration_mappings),
        },
    }

    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "captured_at": CAPTURED_AT,
        "custody": {
            "retrieval_method": "PUBLIC_GITHUB_COMMIT_ARCHIVE_OVER_HTTPS",
            "retrieved_by": "Star Atlas Archive ingestion campaign",
            "repository": UPSTREAM_REPOSITORY,
            "repository_url": UPSTREAM_REPOSITORY_URL,
            "live_site_url": UPSTREAM_SITE_URL,
            "selected_branch": UPSTREAM_BRANCH,
            "selection_reason": "main is the active content branch and deployment workflow source; default master is older",
            "commit": UPSTREAM_COMMIT,
            "tree": UPSTREAM_TREE,
            "commit_date": UPSTREAM_COMMIT_DATE,
            "commit_message": UPSTREAM_COMMIT_MESSAGE,
            "default_branch_at_capture": DEFAULT_BRANCH_AT_CAPTURE,
            "default_branch_commit": DEFAULT_BRANCH_COMMIT,
            "deployment_branch": DEPLOYMENT_BRANCH,
            "deployment_commit": DEPLOYMENT_COMMIT,
            "deployed_source_commit": DEPLOYED_SOURCE_COMMIT,
        },
        "raw_artifacts": [
            {"path": RAW_ZIP_REL.as_posix(), "sha256": sha256_bytes(raw_zip.read_bytes()), "byte_length": raw_zip.stat().st_size, "role": "IMMUTABLE_COMMIT_SNAPSHOT"},
            {"path": RAW_HOME_REL.as_posix(), "sha256": sha256_bytes(home_bytes), "byte_length": len(home_bytes), "role": "LIVE_SITE_IDENTITY_CAPTURE"},
            {"path": RAW_SITEMAP_REL.as_posix(), "sha256": sha256_bytes(sitemap_bytes), "byte_length": len(sitemap_bytes), "role": "LIVE_SITE_URL_INVENTORY_CAPTURE"},
        ],
        "authority_assessment": taxonomy["authority"],
        "identity_observations": {
            "repository_api_description": "Fan-created encyclopedia of Star Atlas lore — factions, species, history, and more",
            "default_master_description": "Fan-created encyclopedia of Star Atlas lore — factions, species, history, and more",
            "main_branch_description": "Official Star Atlas Lore Encyclopedia — factions, species, history, and more (Alpha)",
            "atmta_affiliation_independently_verified": False,
            "atmta_affiliation_operator_confirmed": True,
            "operator_confirmed_repository_owner_role": "STAR_ATLAS_TEAM_MEMBER_RESPONSIBLE_FOR_LORE",
            "repository_treatment": "ATMTA_AFFILIATED_CANONICAL_LORE_AUTHORITY",
            "operator_designation_applied": True,
        },
        "immutability": {"historical_source_rewrites": 0, "raw_snapshot_modified": False},
    }

    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "ARCHIVED_NORMALIZED_CURATOR_ADJUDICATED",
        "upstream_commit": UPSTREAM_COMMIT,
        "repository_files_preserved": len(file_inventory),
        "markdown_pages_inventoried": len(page_inventory),
        "canon_pages": len(canon_paths),
        "published_docs_pages": len(docs_paths),
        "working_material_pages_preserved_excluded": len(internal_paths),
        "normalized_source_pages": len(pages),
        "source_records_json": len(pages),
        "source_records_markdown": len(pages),
        "entities_extracted": len(entities),
        "relationships_extracted": len(relationships),
        "media_inventoried": len(media_records),
        "canon_media_extracted": sum(item["disposition"] == "EXTRACTED_CANON_MEDIA" for item in media_records),
        "mirror_divergences": len(mirror_divergences),
        "unresolved_internal_links": len(unresolved_links),
        "unresolved_navigation_targets": len(navigation["unresolved_navigation_targets"]),
        "migration_mappings": len(migration_mappings),
        "migration_mappings_requiring_review": sum(item["manual_review_required"] for item in migration_mappings),
        "manual_review_conflicts": sum(item["manual_review_required"] for item in conflicts),
        "curator_decisions_accepted": len(CURATOR_DECISIONS),
        "normalized_workstation_path_redactions": sum(page["redactions"]["count"] for page in pages),
        "historical_sources_rewritten": 0,
        "knowledge_files_modified": 0,
        "graph_files_modified": 0,
        "publication_files_modified": 0,
    }

    conflict_md = "# Lore Repository Conflict Report\n\n" + "\n\n".join(
        f"## {item['conflict_id']} — {item['topic']}\n\n- Severity: `{item['severity']}`\n- Manual review: `{str(item['manual_review_required']).upper()}`\n- Finding: {item['finding']}\n- Disposition: {item['disposition']}"
        for item in conflicts
    ) + "\n"
    migration_md = f"""# Lore Taxonomy Migration Report

## Authority

By operator confirmation, Jose is a Star Atlas team member responsible for lore and the pinned personal repository is ATMTA-affiliated canonical authority for in-universe taxonomy and preferred nomenclature. This does not establish page-level authorship for every source file or independently verify every narrative claim.

## Results

- Adopted lore classifications: {len(taxonomy['adopted_lore_types'])}
- Extracted taxonomy entities: {len(entities)}
- Existing Archive lore IDs reviewed: {len(migration_mappings)}
- One-to-one mappings: {sum(item['status'] == 'MAPPED_ONE_TO_ONE' for item in migration_mappings)}
- Ambiguous mappings: {sum(item['status'] == 'AMBIGUOUS_MULTIPLE_TARGETS' for item in migration_mappings)}
- Missing direct pages: {sum(item['status'] == 'UNRESOLVED_NO_DIRECT_PAGE' for item in migration_mappings)}
- Explicit source-native renames asserted automatically: 0
- Explicit source-native deprecated names asserted automatically: 0

## Compatibility rule

Historical source material and existing Archive Lore IDs remain unchanged. One-to-one mappings connect legacy IDs to source-taxonomy entities. Ambiguous or missing mappings require curator review.

## Curator adjudication

- `LORE-FACTION-USTUR` maps to the faction; the identically named species remains a distinct related entity.
- `LORE-COUNCIL-PEACE` maps to the institution; the identically named faction remains a distinct related entity.
- `LORE-GALIA` maps to the region; the Galia Expanse Atlas remains a reference document.
- Star Atlas: CORE and The Voice of Iris remain preserved legacy entities with new mappings deferred.
- Canon controls taxonomy while divergent docs text remains preserved as separate evidence.
- The ONI/CSS page is a historical canonical-source snapshot, not current canonical taxonomy.
"""
    summary_md = f"""# Lore Repository Ingestion Campaign Summary

## Outcome

The public lore repository was preserved at immutable `main` commit `{UPSTREAM_COMMIT}` and normalized into the Archive evidence layer. No canonical knowledge, graph, or publication content was modified.

## Counts

- Repository files preserved: {summary['repository_files_preserved']}
- Markdown pages inventoried: {summary['markdown_pages_inventoried']}
- Canon authoring pages: {summary['canon_pages']}
- Published docs pages: {summary['published_docs_pages']}
- C4 working-material pages preserved but excluded: {summary['working_material_pages_preserved_excluded']}
- Normalized source pages and paired Source Records: {summary['normalized_source_pages']}
- Entities extracted: {summary['entities_extracted']}
- Reference relationships extracted: {summary['relationships_extracted']}
- Media artifacts inventoried: {summary['media_inventoried']}

## Preserved findings and curator dispositions

- Divergent canon/docs mirrors: {summary['mirror_divergences']}
- Unresolved internal links: {summary['unresolved_internal_links']}
- Unresolved navigation targets: {summary['unresolved_navigation_targets']}
- Existing lore ID mappings requiring review: {summary['migration_mappings_requiring_review']}
- Manual-review conflict groups: {summary['manual_review_conflicts']}
- Curator decisions accepted: {summary['curator_decisions_accepted']}
- Normalized workstation-path redactions: {summary['normalized_workstation_path_redactions']}

All campaign-level curator decisions are recorded. The upstream identity label, stale deployment, divergent mirrors, self-reported chronology findings, broken references, and deferred legacy mappings remain explicit evidence or research gaps; they are not silently converted into canonical claims.
"""
    backlog_md = "# Lore Repository Research Backlog\n\n" + "\n".join(
        f"{item['priority']}. **{item['topic']}** — {item['required_artifact']}"
        for item in research_backlog["items"]
    ) + "\n"
    human_review_md = "# Lore Repository Human Review Items\n\n" + "\n\n".join(
        "\n".join([
            f"## {item['review_id']} — {item['topic']}",
            "",
            f"- Status: `{item['status']}`",
            f"- Original decision question: {item['decision_needed']}",
            f"- Recommended disposition: `{item['recommended_disposition']}`",
            f"- Accepted disposition: `{item['accepted_disposition']}`",
            f"- Decided by: `{item['decided_by']}`",
            f"- Decided at: `{item['decided_at']}`",
            *([f"- Decision note: {item['decision_note']}"] if "decision_note" in item else []),
            f"- Allowed dispositions: {', '.join(f'`{value}`' for value in item['allowed_dispositions'])}",
            f"- Evidence: {', '.join(f'`{value}`' if isinstance(value, str) else 'embedded structured evidence' for value in item['evidence'][:5])}",
            *([f"- Evidence count: {item['evidence_count']}"] if "evidence_count" in item else []),
        ])
        for item in human_review["decision_items"]
    ) + "\n"

    rendered: dict[str, bytes] = {}

    def add_text(path: Path | str, content: str) -> None:
        rendered[Path(path).as_posix()] = content.encode("utf-8")

    add_text(PROVENANCE_REL / "upstream-snapshot.json", dump_json(provenance))
    add_text(PROVENANCE_REL / "authority-assessment.json", dump_json(provenance["authority_assessment"] | {"identity_observations": provenance["identity_observations"]}))
    add_text(NORMALIZED_REL / "pages.jsonl", dump_jsonl(sorted(pages, key=lambda item: item["source_id"])))
    add_text(NORMALIZED_REL / "entities.jsonl", dump_jsonl(entities))
    add_text(NORMALIZED_REL / "relationships.jsonl", dump_jsonl(relationships))
    add_text(NORMALIZED_REL / "taxonomy.json", dump_json(taxonomy))
    add_text(NORMALIZED_REL / "navigation.json", dump_json(navigation))
    add_text(NORMALIZED_REL / "media.jsonl", dump_jsonl(media_records))
    add_text(NORMALIZED_REL / "alias-mappings.json", dump_json({"campaign_id": CAMPAIGN_ID, "mappings": migration_mappings}))
    for path, content in normalized_pages_json.items():
        add_text(path, content)
    for path, content in normalized_pages_md.items():
        add_text(path, content)
    for path, content in source_records_json.items():
        add_text(path, content)
    for path, content in source_records_md.items():
        add_text(path, content)
    add_text(PACKAGE_REL / "lore-repository-corpus.json", dump_json(package))
    add_text(CAMPAIGN_REL / "source-inventory.json", dump_json({"campaign_id": CAMPAIGN_ID, "files": file_inventory}))
    add_text(CAMPAIGN_REL / "page-inventory.json", dump_json({"campaign_id": CAMPAIGN_ID, "pages": page_inventory}))
    add_text(CAMPAIGN_REL / "mirror-divergence-ledger.json", dump_json({"campaign_id": CAMPAIGN_ID, "divergences": mirror_divergences, "canon_only": canon_only, "docs_only": docs_only}))
    add_text(CAMPAIGN_REL / "unresolved-reference-ledger.json", dump_json({"campaign_id": CAMPAIGN_ID, "relationships": unresolved_links, "navigation": navigation["unresolved_navigation_targets"]}))
    add_text(CAMPAIGN_REL / "taxonomy-migration-report.json", dump_json(migration_report))
    add_text(CAMPAIGN_REL / "taxonomy-migration-report.md", migration_md)
    add_text(CAMPAIGN_REL / "conflict-report.json", dump_json({"campaign_id": CAMPAIGN_ID, "conflicts": conflicts, "embedded_local_paths": embedded_local_paths}))
    add_text(CAMPAIGN_REL / "conflict-report.md", conflict_md)
    add_text(CAMPAIGN_REL / "research-backlog.json", dump_json(research_backlog))
    add_text(CAMPAIGN_REL / "research-backlog.md", backlog_md)
    add_text(CAMPAIGN_REL / "human-review-items.json", dump_json(human_review))
    add_text(CAMPAIGN_REL / "human-review-items.md", human_review_md)
    add_text(CAMPAIGN_REL / "campaign-summary.json", dump_json(summary))
    add_text(CAMPAIGN_REL / "campaign-summary.md", summary_md)

    for media in media_records:
        if media["extracted_path"]:
            rendered[media["extracted_path"]] = members[media["upstream_path"]]

    manifest_entries = [
        {"path": RAW_ZIP_REL.as_posix(), "role": "raw_commit_snapshot", "sha256": sha256_bytes(raw_zip.read_bytes()), "byte_length": raw_zip.stat().st_size},
        {"path": RAW_HOME_REL.as_posix(), "role": "raw_live_site_identity", "sha256": sha256_bytes(home_bytes), "byte_length": len(home_bytes)},
        {"path": RAW_SITEMAP_REL.as_posix(), "role": "raw_live_site_inventory", "sha256": sha256_bytes(sitemap_bytes), "byte_length": len(sitemap_bytes)},
    ]
    for static_path, role in [
        (RAW_REL / ".gitattributes", "raw_path_attributes"),
        (CAMPAIGN_REL / "README.md", "campaign_documentation"),
        (CAMPAIGN_REL / "build_campaign.py", "deterministic_generator"),
        (CAMPAIGN_REL / "validate_campaign.py", "campaign_validator"),
        (Path("operations/tests/lore_repository/test_lore_repository_campaign.py"), "campaign_test"),
        (Path("operations/ci/validate_repository.py"), "repository_ci_integration"),
    ]:
        static_data = repository_text_bytes(ROOT / static_path)
        manifest_entries.append({
            "path": static_path.as_posix(),
            "role": role,
            "hash_mode": "UTF8_LF",
            "sha256": sha256_bytes(static_data),
            "byte_length": len(static_data),
        })
    for path, data in sorted(rendered.items()):
        manifest_entries.append({"path": path, "role": "generated_artifact", "sha256": sha256_bytes(data), "byte_length": len(data)})
    manifest = {
        "campaign_id": CAMPAIGN_ID,
        "repository_schema": "2.1",
        "upstream_commit": UPSTREAM_COMMIT,
        "generated_at": CAPTURED_AT,
        "files": sorted(manifest_entries, key=lambda item: item["path"]),
    }
    manifest_text = dump_json(manifest)
    add_text(CAMPAIGN_REL / "manifest.json", manifest_text)
    add_text(ARCHIVE_MANIFEST_REL, manifest_text)
    return rendered


def write_outputs() -> None:
    for relative_path, data in build().items():
        path = ROOT / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


if __name__ == "__main__":
    write_outputs()
    result = json.loads((CAMPAIGN_DIR / "campaign-summary.json").read_text(encoding="utf-8"))
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": result["status"], "normalized_pages": result["normalized_source_pages"], "entities": result["entities_extracted"]}))
