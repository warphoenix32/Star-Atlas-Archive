#!/usr/bin/env python3
"""Publication-native ingestion for the official Star Atlas Medium corpus."""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError as exc:  # pragma: no cover - user-facing dependency gate
    raise SystemExit(
        "Beautiful Soup is required. Install operations/campaigns/"
        "star-atlas-medium-ingestion-2026-07/requirements.txt"
    ) from exc

CAMPAIGN_ID = "star-atlas-medium-ingestion-2026-07"
REPO_ROOT = Path(__file__).resolve().parents[3]
OPS = REPO_ROOT / "operations" / "campaigns" / CAMPAIGN_ID
DISCOVERY_CAPTURES = OPS / "discovery-captures"
IDENTITY_CAPTURES = OPS / "identity-captures"
RAW_ROOT = REPO_ROOT / "archive" / "raw" / "medium" / "star-atlas"
NORMALIZED_ROOT = REPO_ROOT / "archive" / "normalized" / "medium" / "star-atlas"
SOURCE_RECORD_ROOT = REPO_ROOT / "archive" / "source-records" / "medium" / "star-atlas"
PACKAGE_ROOT = REPO_ROOT / "archive" / "ingestion-packages" / "star-atlas-medium"
EXTRACTION_ROOT = PACKAGE_ROOT / "extractions"
ARCHIVE_MANIFEST = REPO_ROOT / "archive" / "manifests" / f"{CAMPAIGN_ID}.json"
SUMMARY_ROOT = REPO_ROOT / "archive" / "campaign-summaries" / CAMPAIGN_ID
URL_MANIFEST = OPS / "url-manifest.json"
DISCOVERY_LEDGER = OPS / "discovery-ledger.json"
EXCLUSION_LEDGER = OPS / "exclusion-ledger.json"
DUPLICATE_LEDGER = OPS / "redirect-duplicate-clusters.json"
RETRIEVAL_LEDGER = OPS / "retrieval-ledger.json"
RETRY_LEDGER = OPS / "retry-ledger.json"
MANUAL_REVIEW = OPS / "manual-review-queue.json"
ADJUDICATION_LEDGER = OPS / "manual-review-adjudication.json"
CAMPAIGN_MANIFEST = OPS / "campaign-manifest.json"
VALIDATION_JSON = OPS / "validation-report.json"
VALIDATION_MD = OPS / "validation-report.md"
SUMMARY_JSON = SUMMARY_ROOT / "campaign-summary.json"
SUMMARY_MD = SUMMARY_ROOT / "campaign-summary.md"
BROWSER_HELPER = OPS / "medium_browser.js"

USER_AGENT = (
    "Mozilla/5.0 (compatible; StarAtlasArchive/1.0; "
    "+https://github.com/warphoenix32/Star-Atlas-Archive)"
)
OFFICIAL_PUBLICATION = "Star Atlas"
OFFICIAL_PUBLICATION_ID = "a97f09b411f1"
OFFICIAL_PROFILE_ID = "5ed69ff9cfb0"
POST_ID_RE = re.compile(r"(?:/p/|[-/])([0-9a-f]{11,12})(?=[^0-9a-f]|$)", re.I)
URL_RE = re.compile(r"https?://[^\s<>\"'`]+", re.I)
TRACKING_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8", newline="\n")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def clean_url_tail(value: str) -> str:
    value = html.unescape(value)
    # Repository records sometimes contain HTML-escaped attribute fragments
    # immediately after a URL (for example ``&quot;&gt;published``). They are
    # markup, not part of the observed URL.
    value = re.split(r"[<>\"']", value, maxsplit=1)[0]
    return value.rstrip(".,;:!?)]}>'\"")


def canonicalize_url(value: str) -> str:
    value = clean_url_tail(value.strip())
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme.lower() not in {"http", "https"}:
        return value
    host = (parsed.hostname or "").lower()
    if host == "www.medium.com":
        host = "medium.com"
    port = parsed.port
    netloc = host if port in (None, 80, 443) else f"{host}:{port}"
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = []
    for key, item in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True):
        lower = key.lower()
        if lower.startswith("utm_") or lower in TRACKING_KEYS:
            continue
        query.append((key, item))
    return urllib.parse.urlunsplit(
        (parsed.scheme.lower(), netloc, path, urllib.parse.urlencode(sorted(query)), "")
    )


def post_id_from_url(value: str) -> str | None:
    # A Medium sign-in URL can embed an article URL in its query string. The
    # stable post identifier belongs to the article path, never to navigation
    # or authentication query parameters.
    path = urllib.parse.urlsplit(canonicalize_url(value)).path
    match = POST_ID_RE.search(urllib.parse.unquote(path))
    return match.group(1).lower() if match else None


def source_id(post_id: str | None, canonical_url: str) -> str:
    suffix = post_id.upper() if post_id else hashlib.sha256(canonical_url.encode()).hexdigest()[:16].upper()
    return f"SRC-MEDIUM-STARATLAS-{suffix}"


def normalize_date(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        number = float(value)
        if number > 10_000_000_000:
            number /= 1000
        return dt.datetime.fromtimestamp(number, tz=dt.timezone.utc).isoformat().replace("+00:00", "Z")
    text = str(value).strip()
    try:
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    except ValueError:
        try:
            from email.utils import parsedate_to_datetime

            parsed = parsedate_to_datetime(text)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
        except (TypeError, ValueError, OverflowError):
            return None


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[dict[str, Any]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        self.chain.append({"from": req.full_url, "to": newurl, "status": code})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def http_get(url: str, timeout: int = 60) -> dict[str, Any]:
    recorder = RedirectRecorder()
    opener = urllib.request.build_opener(recorder)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            data = response.read()
            return {
                "ok": 200 <= response.status < 400,
                "requested_url": url,
                "final_url": response.geturl(),
                "status": response.status,
                "headers": dict(response.headers.items()),
                "redirect_chain": recorder.chain,
                "body": data,
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return {
            "ok": False,
            "requested_url": url,
            "final_url": exc.geturl(),
            "status": exc.code,
            "headers": dict(exc.headers.items()) if exc.headers else {},
            "redirect_chain": recorder.chain,
            "body": body,
            "error": f"HTTP {exc.code}",
        }
    except Exception as exc:  # noqa: BLE001 - persistent retrieval ledger records exact error
        return {
            "ok": False,
            "requested_url": url,
            "final_url": url,
            "status": None,
            "headers": {},
            "redirect_chain": recorder.chain,
            "body": b"",
            "error": f"{type(exc).__name__}: {exc}",
        }


def decode_body(result: dict[str, Any]) -> str:
    body: bytes = result.get("body", b"")
    content_type = result.get("headers", {}).get("Content-Type", "")
    match = re.search(r"charset=([^;\s]+)", content_type, re.I)
    encodings = [match.group(1).strip('"\'')] if match else []
    encodings += ["utf-8", "windows-1252"]
    for encoding in encodings:
        try:
            return body.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return body.decode("utf-8", errors="replace")


def capture_http(label: str, url: str) -> tuple[dict[str, Any], str]:
    result = http_get(url)
    suffix = ".xml" if "xml" in result.get("headers", {}).get("Content-Type", "").lower() else ".html"
    body_path = DISCOVERY_CAPTURES / f"{label}{suffix}"
    metadata_path = DISCOVERY_CAPTURES / f"{label}.json"
    body_path.parent.mkdir(parents=True, exist_ok=True)
    if not body_path.exists() or body_path.read_bytes() != result["body"]:
        body_path.write_bytes(result["body"])
    previous = read_json(metadata_path, {}) or {}
    checksum = sha256_bytes(result["body"])
    captured_at = previous.get("captured_at") if previous.get("sha256") == checksum else now_iso()
    metadata = {
        "capture_label": label,
        "requested_url": url,
        "final_url": result["final_url"],
        "http_status": result["status"],
        "content_type": result.get("headers", {}).get("Content-Type"),
        "byte_count": len(result["body"]),
        "sha256": checksum,
        "redirect_chain": result["redirect_chain"],
        "captured_at": captured_at,
        "error": result["error"],
        "body_path": rel(body_path),
    }
    write_json(metadata_path, metadata)
    return metadata, decode_body(result)


def find_node() -> str | None:
    configured = os.environ.get("MEDIUM_NODE")
    if configured and Path(configured).exists():
        return configured
    return shutil.which("node") or shutil.which("node.exe")


def browser_capture(label: str, url: str, scroll: bool, output_dir: Path = DISCOVERY_CAPTURES) -> dict[str, Any]:
    node = find_node()
    if not node:
        return {"requested_url": url, "error": "Node.js not found", "anchors": [], "post_ids": []}
    metadata_path = output_dir / f"{label}.browser.json"
    html_path = output_dir / f"{label}.browser.html"
    command = [node, str(BROWSER_HELPER), url, str(metadata_path), str(html_path), "scroll" if scroll else "single"]
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=180)
    if completed.returncode != 0:
        return {
            "requested_url": url,
            "error": (completed.stderr or completed.stdout).strip(),
            "anchors": [],
            "post_ids": [],
        }
    data = read_json(metadata_path, {})
    data["rendered_html_path"] = rel(html_path)
    write_json(metadata_path, data)
    return data


def iter_urls(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield from (clean_url_tail(match.group(0)) for match in URL_RE.finditer(value))
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_urls(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_urls(item)


def is_medium_url(value: str) -> bool:
    host = (urllib.parse.urlsplit(value).hostname or "").lower()
    return host == "medium.com" or host.endswith(".medium.com") or host == "link.medium.com"


def official_story_namespace(value: str) -> bool:
    parsed = urllib.parse.urlsplit(canonicalize_url(value))
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()
    return (
        host == "staratlasgame.medium.com"
        or (host == "medium.com" and (path.startswith("/star-atlas/") or path.startswith("/@staratlasgame/")))
    ) and post_id_from_url(value) is not None


def landing_exclusion(value: str) -> str | None:
    parsed = urllib.parse.urlsplit(canonicalize_url(value))
    path = parsed.path.rstrip("/").lower()
    if not is_medium_url(value):
        return "NOT_MEDIUM"
    if post_id_from_url(value):
        return None
    if path in {"", "/", "/star-atlas", "/@staratlasgame", "/about", "/archive", "/latest"}:
        return "NAVIGATION_OR_PUBLICATION_LANDING_PAGE"
    if any(part in path for part in ("/tag/", "/lists/", "/me/", "/search", "/m/signin", "/responses")):
        return "NAVIGATION_OR_ACTIVITY_SURFACE"
    return None


def add_candidate(
    candidates: dict[str, dict[str, Any]],
    url: str,
    discovery_source: str,
    referrer_source_id: str | None = None,
    supplied: dict[str, Any] | None = None,
) -> None:
    if not url or not is_medium_url(url):
        return
    observed = clean_url_tail(url)
    canonical = canonicalize_url(observed)
    pid = post_id_from_url(canonical)
    key = pid or f"URL-{hashlib.sha256(canonical.encode()).hexdigest()[:20]}"
    record = candidates.setdefault(
        key,
        {
            "medium_post_id": pid,
            "canonical_url": canonical,
            "observed_urls": [],
            "title": None,
            "author": None,
            "publication": None,
            "published_at_original": None,
            "published_at_normalized": None,
            "updated_at_original": None,
            "updated_at_normalized": None,
            "discovery_sources": [],
            "referrer_source_ids": [],
            "identity_status": "UNRESOLVED",
            "inclusion_status": None,
            "exclusion_reason": None,
            "redirect_chain": [],
            "retrieval_status": "PENDING",
            "retrieval_method": None,
            "manual_review_required": False,
            "manual_review_reasons": [],
        },
    )
    if observed not in record["observed_urls"]:
        record["observed_urls"].append(observed)
    if discovery_source not in record["discovery_sources"]:
        record["discovery_sources"].append(discovery_source)
    if referrer_source_id and referrer_source_id not in record["referrer_source_ids"]:
        record["referrer_source_ids"].append(referrer_source_id)
    if supplied:
        for field in ("title", "author", "publication", "published_at_original", "updated_at_original"):
            if supplied.get(field) and not record.get(field):
                record[field] = supplied[field]
    record["observed_urls"].sort()
    record["discovery_sources"].sort()
    record["referrer_source_ids"].sort()


def parse_rss(xml_text: str) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    bodies: dict[str, dict[str, Any]] = {}
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items, bodies
    content_tag = "{http://purl.org/rss/1.0/modules/content/}encoded"
    creator_tag = "{http://purl.org/dc/elements/1.1/}creator"
    for node in root.findall("./channel/item"):
        link = (node.findtext("link") or "").strip()
        guid = (node.findtext("guid") or "").strip()
        pid = post_id_from_url(guid) or post_id_from_url(link)
        if not link or not pid:
            continue
        body = node.findtext(content_tag) or ""
        item = {
            "url": link,
            "medium_post_id": pid,
            "title": node.findtext("title"),
            "author": node.findtext(creator_tag),
            "publication": OFFICIAL_PUBLICATION,
            "published_at_original": node.findtext("pubDate"),
            "updated_at_original": None,
            "categories": [item.text for item in node.findall("category") if item.text],
            "guid": guid,
        }
        items.append(item)
        bodies[pid] = {**item, "content_encoded": body}
    return items, bodies


def parse_sitemap(xml_text: str) -> list[dict[str, str | None]]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    return [
        {"url": node.findtext(f"{namespace}loc"), "lastmod": node.findtext(f"{namespace}lastmod")}
        for node in root.findall(f"{namespace}url")
        if node.findtext(f"{namespace}loc")
    ]


def parse_apollo_urls(html_text: str) -> list[str]:
    decoded = html.unescape(html_text).replace("\\u002F", "/")
    urls = set(clean_url_tail(match.group(0).replace("\\/", "/")) for match in URL_RE.finditer(decoded))
    return sorted(url for url in urls if is_medium_url(url) and post_id_from_url(url))


def repository_discovery(candidates: dict[str, dict[str, Any]], ledger: list[dict[str, Any]]) -> None:
    targets = [
        REPO_ROOT / "archive" / "normalized" / "discord-announcements" / "messages.jsonl",
        REPO_ROOT
        / "archive"
        / "normalized"
        / "social-governance-semantic-enrichment"
        / "social-media"
        / "staratlas-posts.jsonl",
        REPO_ROOT / "archive" / "normalized" / "manifests" / "normalized-urls.jsonl",
    ]
    targets.extend(
        sorted((REPO_ROOT / "archive" / "ingestion-packages" / "campaign-delta-official" / "extractions").glob("*.json"))
    )
    for path in targets:
        if not path.exists():
            ledger.append({"surface": "repository", "path": rel(path), "status": "MISSING"})
            continue
        count = 0
        if path.suffix == ".jsonl":
            records = []
            for line in path.read_text(encoding="utf-8-sig").splitlines():
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        else:
            try:
                records = [json.loads(path.read_text(encoding="utf-8-sig"))]
            except json.JSONDecodeError:
                records = []
        for record in records:
            referrer = record.get("source_id") if isinstance(record, dict) else None
            for url in iter_urls(record):
                if is_medium_url(url):
                    add_candidate(candidates, url, f"repository:{rel(path)}", referrer)
                    count += 1
        ledger.append({"surface": "repository", "path": rel(path), "status": "QUERIED", "url_occurrences": count})


def discover_web_archive(candidates: dict[str, dict[str, Any]], ledger: list[dict[str, Any]]) -> None:
    queries = [
        (
            "wayback-custom-domain",
            "https://web.archive.org/cdx/search/cdx?url=staratlasgame.medium.com/*&output=json&"
            "filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,digest&collapse=urlkey",
        ),
        (
            "wayback-publication",
            "https://web.archive.org/cdx/search/cdx?url=medium.com/star-atlas/*&output=json&"
            "filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original,digest&collapse=urlkey",
        ),
    ]
    for label, url in queries:
        metadata, text = capture_http(label, url)
        rows: list[Any] = []
        try:
            payload = json.loads(text)
            rows = payload[1:] if isinstance(payload, list) and payload else []
        except json.JSONDecodeError:
            pass
        for row in rows:
            if not isinstance(row, list) or len(row) < 2:
                continue
            timestamp, original = row[0], row[1]
            add_candidate(
                candidates,
                original,
                f"web_archive:{label}",
                supplied={"updated_at_original": None},
            )
            pid = post_id_from_url(original)
            if pid:
                candidates[pid].setdefault("archived_snapshots", []).append(
                    {"timestamp": timestamp, "original_url": original, "digest": row[2] if len(row) > 2 else None}
                )
        ledger.append(
            {
                "surface": "web_archive",
                "label": label,
                "url": url,
                "status": "QUERIED" if metadata["http_status"] == 200 else "FAILED",
                "http_status": metadata["http_status"],
                "result_count": len(rows),
                "error": metadata["error"],
            }
        )


def disposition_candidates(candidates: dict[str, dict[str, Any]]) -> None:
    # Merge URL-only records into post-ID records when redirect/canonical evidence now exposes an ID.
    for key in list(candidates):
        record = candidates[key]
        if record["medium_post_id"]:
            continue
        exclusion = landing_exclusion(record["canonical_url"])
        if exclusion:
            record["identity_status"] = "NON_ARTICLE_SURFACE"
            record["inclusion_status"] = "EXCLUDED"
            record["exclusion_reason"] = exclusion
            continue
        result = http_get(record["canonical_url"], timeout=30)
        record["redirect_chain"] = result["redirect_chain"]
        final_url = canonicalize_url(result["final_url"])
        pid = post_id_from_url(final_url)
        if pid:
            add_candidate(candidates, final_url, "redirect_resolution")
            target = candidates[pid]
            for field in ("observed_urls", "discovery_sources", "referrer_source_ids"):
                target[field] = sorted(set(target[field]) | set(record[field]))
            target["redirect_chain"] = record["redirect_chain"]
            del candidates[key]
            continue
        record["identity_status"] = "UNRESOLVED_URL_WITHOUT_POST_ID"
        record["inclusion_status"] = "MANUAL_REVIEW"
        record["manual_review_required"] = True
        record["manual_review_reasons"].append("Medium post ID could not be resolved")

    for record in candidates.values():
        record["published_at_normalized"] = normalize_date(record.get("published_at_original"))
        record["updated_at_normalized"] = normalize_date(record.get("updated_at_original"))
        record["source_id"] = source_id(record.get("medium_post_id"), record["canonical_url"])
        if record.get("inclusion_status"):
            continue
        official_urls = [url for url in record["observed_urls"] if official_story_namespace(url)]
        publication_sources = [
            item
            for item in record["discovery_sources"]
            if item.startswith("rss:publication") or item.startswith("publication_archive")
        ]
        direct_publication_urls = [
            url
            for url in official_urls
            if urllib.parse.urlsplit(canonicalize_url(url)).path.lower().startswith("/star-atlas/")
        ]
        if direct_publication_urls or publication_sources:
            record["canonical_url"] = canonicalize_url(direct_publication_urls[0] if direct_publication_urls else official_urls[0])
            record["identity_status"] = (
                "OFFICIAL_PUBLICATION_URL_NAMESPACE" if direct_publication_urls else "OFFICIAL_PUBLICATION_RSS"
            )
            record["inclusion_status"] = "INCLUDED"
            record["publication"] = OFFICIAL_PUBLICATION
        elif official_urls:
            record["identity_status"] = "OFFICIAL_PROFILE_OR_CUSTOM_DOMAIN_PENDING_ARTICLE_CONFIRMATION"
            record["inclusion_status"] = "MANUAL_REVIEW"
            record["manual_review_required"] = True
            record["manual_review_reasons"].append("Profile/custom-domain story lacks captured publication membership")
        else:
            record["identity_status"] = "EXTERNAL_OR_UNRELATED_MEDIUM_STORY"
            record["inclusion_status"] = "EXCLUDED"
            record["exclusion_reason"] = "NOT_ESTABLISHED_AS_STAR_ATLAS_PUBLICATION"
        for field in ("observed_urls", "discovery_sources", "referrer_source_ids", "manual_review_reasons"):
            record[field] = sorted(set(record[field]))
        if "archived_snapshots" in record:
            record["archived_snapshots"] = sorted(
                {json.dumps(item, sort_keys=True): item for item in record["archived_snapshots"]}.values(),
                key=lambda item: (item.get("timestamp") or "", item.get("original_url") or ""),
            )


def discover() -> int:
    for directory in (OPS, DISCOVERY_CAPTURES, IDENTITY_CAPTURES, SUMMARY_ROOT):
        directory.mkdir(parents=True, exist_ok=True)
    old_manifest = read_json(URL_MANIFEST, {}) or {}
    old_by_id = {item.get("source_id"): item for item in old_manifest.get("records", [])}
    candidates: dict[str, dict[str, Any]] = {}
    ledger: list[dict[str, Any]] = []
    rss_bodies: dict[str, dict[str, Any]] = {}

    current_year = dt.datetime.now(dt.timezone.utc).year
    for year in range(2020, current_year + 1):
        url = f"https://medium.com/star-atlas/archive/{year}"
        label = f"publication-archive-{year}"
        metadata, text = capture_http(label, url)
        for article_url in parse_apollo_urls(text):
            if official_story_namespace(article_url):
                add_candidate(candidates, article_url, f"publication_archive:{year}")
        browser = browser_capture(label, metadata["final_url"] or url, scroll=True)
        for anchor in browser.get("anchors", []):
            article_url = anchor.get("href", "")
            if official_story_namespace(article_url):
                add_candidate(candidates, article_url, f"publication_archive_browser:{year}")
        ledger.append(
            {
                "surface": "publication_archive",
                "year": year,
                "requested_url": url,
                "http_status": metadata["http_status"],
                "final_url": metadata["final_url"],
                "direct_sha256": metadata["sha256"],
                "browser_sha256": browser.get("rendered_html_sha256"),
                "browser_item_count": browser.get("final_item_count", 0),
                "browser_scroll_passes": browser.get("scroll_passes", 0),
                "status": "QUERIED",
                "limitations": "Current Medium archive route may expose only a hydration shell; repository/social/archive discovery remains additive.",
            }
        )

    page_sources = [
        ("publication-page", "https://medium.com/star-atlas", "publication_page"),
        ("publication-all", "https://medium.com/star-atlas/all", "publication_page"),
        ("profile-page", "https://medium.com/@staratlasgame", "profile_page"),
        ("custom-profile-page", "https://staratlasgame.medium.com/", "profile_page"),
    ]
    for label, url, source in page_sources:
        metadata, text = capture_http(label, url)
        found = parse_apollo_urls(text)
        for article_url in found:
            add_candidate(candidates, article_url, source)
        browser = browser_capture(label, metadata["final_url"] or url, scroll=True)
        for anchor in browser.get("anchors", []):
            if post_id_from_url(anchor.get("href", "")):
                add_candidate(candidates, anchor["href"], f"{source}_browser")
        ledger.append(
            {
                "surface": source,
                "requested_url": url,
                "http_status": metadata["http_status"],
                "direct_item_count": len(found),
                "browser_item_count": browser.get("final_item_count", 0),
                "status": "QUERIED",
            }
        )

    rss_sources = [
        ("publication-rss", "https://medium.com/feed/star-atlas", "rss:publication"),
        ("profile-rss", "https://staratlasgame.medium.com/feed", "rss:profile"),
        ("profile-rss-medium", "https://medium.com/feed/@staratlasgame", "rss:profile"),
    ]
    for label, url, source in rss_sources:
        metadata, text = capture_http(label, url)
        items, bodies = parse_rss(text)
        for item in items:
            add_candidate(candidates, item["url"], source, supplied=item)
        for pid, item in bodies.items():
            existing = rss_bodies.get(pid)
            if not existing or len(item.get("content_encoded", "")) > len(existing.get("content_encoded", "")):
                rss_bodies[pid] = item
        ledger.append(
            {
                "surface": source,
                "requested_url": url,
                "http_status": metadata["http_status"],
                "item_count": len(items),
                "status": "QUERIED" if metadata["http_status"] == 200 else "FAILED",
            }
        )
    write_json(OPS / "rss-content-index.json", rss_bodies)

    sitemap_sources = [
        ("custom-sitemap", "https://staratlasgame.medium.com/sitemap/sitemap.xml"),
        ("publication-sitemap", "https://medium.com/star-atlas/sitemap.xml"),
    ]
    for label, url in sitemap_sources:
        metadata, text = capture_http(label, url)
        items = parse_sitemap(text)
        for item in items:
            add_candidate(
                candidates,
                item["url"] or "",
                f"sitemap:{label}",
                supplied={"updated_at_original": item.get("lastmod")},
            )
        ledger.append(
            {
                "surface": "sitemap",
                "label": label,
                "requested_url": url,
                "http_status": metadata["http_status"],
                "item_count": len(items),
                "status": "QUERIED",
                "limitations": "Sitemap is additive and not treated as exhaustive.",
            }
        )

    repository_discovery(candidates, ledger)
    discover_web_archive(candidates, ledger)
    disposition_candidates(candidates)

    records = sorted(candidates.values(), key=lambda item: (item["source_id"], item["canonical_url"]))
    for record in records:
        prior = old_by_id.get(record["source_id"])
        if prior:
            for field in ("retrieval_status", "retrieval_method", "manual_review_required", "manual_review_reasons"):
                if prior.get(field) not in (None, [], "PENDING"):
                    record[field] = prior[field]
    manifest_core = {
        "campaign_id": CAMPAIGN_ID,
        "schema_version": "1.0",
        "discovery_range": {"first_year": 2020, "last_year": current_year},
        "identity_rules": {
            "official_publication": OFFICIAL_PUBLICATION,
            "official_publication_id": OFFICIAL_PUBLICATION_ID,
            "official_profile_id": OFFICIAL_PROFILE_ID,
            "stable_key": "medium_post_id",
        },
        "records": records,
    }
    digest = sha256_bytes(json.dumps(manifest_core, ensure_ascii=False, sort_keys=True).encode())
    frozen_at = old_manifest.get("frozen_at") if old_manifest.get("manifest_sha256") == digest else now_iso()
    manifest = {**manifest_core, "frozen_at": frozen_at, "manifest_sha256": digest}
    write_json(URL_MANIFEST, manifest)
    write_json(DISCOVERY_LEDGER, {"campaign_id": CAMPAIGN_ID, "surfaces": ledger})
    write_json(
        EXCLUSION_LEDGER,
        {
            "campaign_id": CAMPAIGN_ID,
            "records": [item for item in records if item["inclusion_status"] == "EXCLUDED"],
        },
    )
    write_json(
        MANUAL_REVIEW,
        {
            "campaign_id": CAMPAIGN_ID,
            "records": [item for item in records if item["inclusion_status"] == "MANUAL_REVIEW"],
        },
    )
    clusters = [
        {
            "medium_post_id": item["medium_post_id"],
            "source_id": item["source_id"],
            "canonical_url": item["canonical_url"],
            "observed_urls": item["observed_urls"],
            "redirect_chain": item["redirect_chain"],
            "duplicate_basis": "MEDIUM_POST_ID" if len(item["observed_urls"]) > 1 else None,
        }
        for item in records
        if len(item["observed_urls"]) > 1 or item["redirect_chain"]
    ]
    write_json(DUPLICATE_LEDGER, {"campaign_id": CAMPAIGN_ID, "clusters": clusters})
    counts = collections.Counter(item["inclusion_status"] for item in records)
    print(f"Discovered {len(records)} candidates: {dict(sorted(counts.items()))}")
    return 0


MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif", ".ico", ".mp4", ".webm", ".mov", ".mp3", ".wav", ".m4a"}
AUXILIARY_SUFFIXES = {".xml", ".json", ".txt", ".rss", ".atom", ".pdf"}
NAVIGATION_PARTS = (
    "/tag/", "/tagged/", "/lists/", "/me/", "/search", "/m/signin", "/responses",
    "/followers", "/following", "/newsletter", "/verified-authors",
)


def deferred(record: dict[str, Any], reason: str, required_artifact: str, next_action: str) -> None:
    record["identity_status"] = "IDENTITY_OR_ARTICLE_STATUS_UNRESOLVED"
    record["inclusion_status"] = "DEFERRED"
    record["exclusion_reason"] = None
    record["manual_review_required"] = True
    record["adjudication_status"] = "DEFERRED"
    record["deferral_reason"] = reason
    record["required_artifact"] = required_artifact
    record["next_action"] = next_action
    record["last_attempt"] = "FROZEN_CAMPAIGN_REVIEW_2026-07-18"
    record["manual_review_reasons"] = [reason]


def excluded(record: dict[str, Any], reason: str) -> None:
    record["identity_status"] = "NON_INCLUDED_CANDIDATE"
    record["inclusion_status"] = "EXCLUDED"
    record["exclusion_reason"] = reason
    record["manual_review_required"] = False
    record["adjudication_status"] = "RESOLVED_EXCLUDED"
    record["manual_review_reasons"] = []
    for field in ("deferral_reason", "required_artifact", "next_action"):
        record.pop(field, None)


def adjudicate_candidate(record: dict[str, Any], included_by_post_id: dict[str, dict[str, Any]]) -> None:
    url = record["canonical_url"]
    decoded = urllib.parse.unquote(url)
    parsed = urllib.parse.urlsplit(decoded)
    host = (parsed.hostname or "").lower()
    path = parsed.path.rstrip("/").lower()
    suffix = Path(path).suffix.lower()
    recovered_post_id = post_id_from_url(url)
    if recovered_post_id:
        record["recovered_post_id"] = recovered_post_id

    if suffix in MEDIA_SUFFIXES or re.search(r"/1\*[^/]+\.(?:png|jpe?g|gif|webp|svg|avif)$", path, re.I):
        excluded(record, "ARTICLE_MEDIA_ASSET")
        return
    if suffix in AUXILIARY_SUFFIXES:
        excluded(record, "AUXILIARY_OR_NON_ARTICLE_DOCUMENT")
        return
    if path in {"", "/", "/star-atlas", "/@staratlasgame", "/about", "/archive", "/latest"} or any(part in path for part in NAVIGATION_PARTS):
        excluded(record, "NAVIGATION_OR_ACTIVITY_SURFACE")
        return
    if recovered_post_id and recovered_post_id in included_by_post_id:
        target = included_by_post_id[recovered_post_id]
        target["observed_urls"] = sorted(set(target.get("observed_urls", [])) | set(record.get("observed_urls", [])))
        record["duplicate_of_source_id"] = target["source_id"]
        excluded(record, "MALFORMED_OR_VARIANT_URL_DUPLICATES_INCLUDED_ARTICLE")
        return
    if host == "link.medium.com":
        deferred(
            record,
            "UNRESOLVED_MEDIUM_SHORTLINK",
            "A captured redirect chain resolving the shortlink to a stable article URL and publication identity.",
            "Resolve the shortlink in a network-enabled archival pass and preserve every redirect hop.",
        )
        return
    official_namespace = host == "staratlasgame.medium.com" or (host == "medium.com" and path.startswith("/star-atlas/"))
    if recovered_post_id and official_namespace:
        deferred(
            record,
            "OFFICIAL_NAMESPACE_LEAD_WITHOUT_CONFIRMED_ARTICLE_CAPTURE",
            "Live or archived article metadata proving title, author, publication membership, date, and complete body for the recovered 11- or 12-character Medium ID.",
            "Retrieve the candidate in a separate acquisition pass; do not include it from URL shape alone.",
        )
        return
    if recovered_post_id:
        excluded(record, "EXTERNAL_OR_UNRELATED_MEDIUM_POST_ID")
        return
    if host not in {"medium.com", "staratlasgame.medium.com"}:
        excluded(record, "EXTERNAL_OR_UNRELATED_MEDIUM_SURFACE")
        return
    if path.startswith("/@") and not path.startswith("/@staratlasgame"):
        excluded(record, "EXTERNAL_MEDIUM_PROFILE")
        return
    if official_namespace:
        deferred(
            record,
            "TRUNCATED_OR_MALFORMED_OFFICIAL_NAMESPACE_LEAD",
            "An original URL or archived index entry containing a stable Medium post ID, followed by article metadata proving publication membership.",
            "Recover an untruncated URL from source context or a web-archive index before retrieval.",
        )
        return
    excluded(record, "NAVIGATION_EXTERNAL_OR_NON_ARTICLE_SURFACE")


def adjudicate() -> int:
    manifest = read_json(URL_MANIFEST, {}) or {}
    records = manifest.get("records", [])
    if not records:
        raise SystemExit("Frozen URL manifest is missing")
    review_records = [item for item in records if item.get("inclusion_status") == "MANUAL_REVIEW"]
    if not review_records and all(item.get("inclusion_status") != "MANUAL_REVIEW" for item in records):
        print("Manual-review candidates are already adjudicated")
    included_by_post_id = {
        item["medium_post_id"]: item
        for item in records
        if item.get("inclusion_status") == "INCLUDED" and item.get("medium_post_id")
    }
    original = {
        item["source_id"]: {
            "source_id": item["source_id"],
            "canonical_url": item["canonical_url"],
            "prior_inclusion_status": item.get("inclusion_status"),
            "prior_identity_status": item.get("identity_status"),
        }
        for item in review_records
    }
    for record in review_records:
        adjudicate_candidate(record, included_by_post_id)

    # Collapse repeated unresolved post-ID leads to one deferred primary while retaining every candidate.
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for record in records:
        if record.get("inclusion_status") == "DEFERRED" and record.get("recovered_post_id"):
            groups[record["recovered_post_id"]].append(record)
    for recovered_post_id, members in sorted(groups.items()):
        ordered = sorted(members, key=lambda item: (item["canonical_url"], item["source_id"]))
        primary = ordered[0]
        primary["candidate_cluster_id"] = f"MEDIUM-LEAD-{recovered_post_id.upper()}"
        for duplicate in ordered[1:]:
            duplicate["duplicate_of_candidate_id"] = primary["source_id"]
            duplicate["candidate_cluster_id"] = primary["candidate_cluster_id"]
            excluded(duplicate, "DUPLICATE_OF_DEFERRED_IDENTITY_LEAD")

    records.sort(key=lambda item: (item["source_id"], item["canonical_url"]))
    core = {key: value for key, value in manifest.items() if key not in {"manifest_sha256", "adjudication"}}
    core["records"] = records
    digest = sha256_bytes(json.dumps(core, ensure_ascii=False, sort_keys=True).encode())
    previous_adjudication = manifest.get("adjudication", {})
    adjudicated_at = previous_adjudication.get("adjudicated_at") or now_iso()
    counts = collections.Counter(item.get("inclusion_status") for item in records)
    manifest.update(
        {
            "records": records,
            "manifest_sha256": digest,
            "adjudication": {
                "adjudicated_at": adjudicated_at,
                "review_candidates_received": len(review_records) or previous_adjudication.get("review_candidates_received", 329),
                "method": "DETERMINISTIC_OFFLINE_CANDIDATE_ADJUDICATION_V1",
                "counts": dict(sorted(counts.items())),
            },
        }
    )
    write_json(URL_MANIFEST, manifest)

    # The 2020 archive surface returned generic Medium navigation links during
    # browser discovery. Preserve the observed count, but do not let it imply
    # that a Star Atlas article was confirmed for that year.
    discovery = read_json(DISCOVERY_LEDGER, {}) or {}
    for surface in discovery.get("surfaces", []):
        if surface.get("surface") == "publication_archive" and surface.get("year") == 2020:
            surface["confirmed_article_count"] = 0
            surface["browser_item_interpretation"] = (
                "GENERIC_MEDIUM_NAVIGATION_LINKS_NOT_CONFIRMED_STAR_ATLAS_ARTICLES"
            )
            surface["coverage_note"] = (
                "The 2020 publication archive was queried, but no candidate could be "
                "confirmed as a Star Atlas publication article."
            )
    write_json(DISCOVERY_LEDGER, discovery)

    write_json(EXCLUSION_LEDGER, {"campaign_id": CAMPAIGN_ID, "records": [item for item in records if item.get("inclusion_status") == "EXCLUDED"]})
    deferred_records = [item for item in records if item.get("inclusion_status") == "DEFERRED"]
    write_json(
        MANUAL_REVIEW,
        {
            "campaign_id": CAMPAIGN_ID,
            "queue_status": "EXPLICITLY_DEFERRED",
            "records": deferred_records,
        },
    )
    decisions = []
    for source_id, prior in sorted(original.items()):
        current = next(item for item in records if item["source_id"] == source_id)
        decisions.append(
            {
                **prior,
                "final_inclusion_status": current.get("inclusion_status"),
                "adjudication_status": current.get("adjudication_status"),
                "reason": current.get("exclusion_reason") or current.get("deferral_reason"),
                "recovered_post_id": current.get("recovered_post_id"),
                "duplicate_of_source_id": current.get("duplicate_of_source_id"),
                "duplicate_of_candidate_id": current.get("duplicate_of_candidate_id"),
                "required_artifact": current.get("required_artifact"),
                "next_action": current.get("next_action"),
                "last_attempt": current.get("last_attempt"),
            }
        )
    if not decisions:
        decisions = (read_json(ADJUDICATION_LEDGER, {}) or {}).get("decisions", [])
    write_json(
        ADJUDICATION_LEDGER,
        {
            "campaign_id": CAMPAIGN_ID,
            "review_candidates_received": len(decisions),
            "resolved_excluded": sum(item.get("final_inclusion_status") == "EXCLUDED" for item in decisions),
            "explicitly_deferred": sum(item.get("final_inclusion_status") == "DEFERRED" for item in decisions),
            "decisions": decisions,
        },
    )
    clusters = [
        {
            "medium_post_id": item.get("medium_post_id") or item.get("recovered_post_id"),
            "source_id": item["source_id"],
            "canonical_url": item["canonical_url"],
            "observed_urls": item.get("observed_urls", []),
            "redirect_chain": item.get("redirect_chain", []),
            "duplicate_basis": (
                "INCLUDED_ARTICLE_VARIANT_URL" if item.get("duplicate_of_source_id")
                else "DEFERRED_IDENTITY_LEAD" if item.get("candidate_cluster_id")
                else "MEDIUM_POST_ID" if len(item.get("observed_urls", [])) > 1
                else None
            ),
            "duplicate_of_source_id": item.get("duplicate_of_source_id"),
            "duplicate_of_candidate_id": item.get("duplicate_of_candidate_id"),
            "candidate_cluster_id": item.get("candidate_cluster_id"),
        }
        for item in records
        if len(item.get("observed_urls", [])) > 1
        or item.get("redirect_chain")
        or item.get("duplicate_of_source_id")
        or item.get("candidate_cluster_id")
    ]
    write_json(DUPLICATE_LEDGER, {"campaign_id": CAMPAIGN_ID, "clusters": clusters})
    results = (read_json(RETRIEVAL_LEDGER, {}) or {}).get("results", [])
    generate_reports(manifest, results)
    print(f"Adjudicated {len(decisions)} review candidates: {dict(sorted(counts.items()))}")
    return 0


def json_ld_objects(soup: BeautifulSoup) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for node in soup.select('script[type="application/ld+json"]'):
        try:
            value = json.loads(node.get_text())
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(value, dict):
            values.append(value)
            if isinstance(value.get("@graph"), list):
                values.extend(item for item in value["@graph"] if isinstance(item, dict))
        elif isinstance(value, list):
            values.extend(item for item in value if isinstance(item, dict))
    return values


def article_ld(soup: BeautifulSoup) -> dict[str, Any]:
    for item in json_ld_objects(soup):
        kind = item.get("@type")
        kinds = kind if isinstance(kind, list) else [kind]
        if any(value in {"Article", "NewsArticle", "BlogPosting", "SocialMediaPosting"} for value in kinds):
            return item
    return {}


def meta_value(soup: BeautifulSoup, *names: str) -> str | None:
    for name in names:
        node = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
        if node and node.get("content"):
            return str(node["content"]).strip()
    return None


def publisher_name(ld: dict[str, Any]) -> str | None:
    publisher = ld.get("publisher")
    if isinstance(publisher, dict):
        return publisher.get("name")
    return publisher if isinstance(publisher, str) else None


def author_names(ld: dict[str, Any], soup: BeautifulSoup) -> list[str]:
    value = ld.get("author") or ld.get("creator")
    values = value if isinstance(value, list) else [value]
    names: list[str] = []
    for item in values:
        if isinstance(item, dict) and item.get("name"):
            names.append(str(item["name"]).strip())
        elif isinstance(item, str):
            names.append(item.strip())
    fallback = meta_value(soup, "author")
    if fallback and not names:
        names.append(fallback)
    return sorted(set(name for name in names if name))


def complete_article_html(html_text: str) -> tuple[bool, str, dict[str, Any]]:
    soup = BeautifulSoup(html_text, "html.parser")
    article = soup.find("article")
    if not article:
        return False, "ARTICLE_ELEMENT_MISSING", {}
    text = article.get_text(" ", strip=True)
    if len(text) < 500:
        return False, "ARTICLE_TEXT_TOO_SHORT", {"text_length": len(text)}
    lower = text.lower()
    if "sign in to continue" in lower or "create an account to read" in lower:
        return False, "LOGIN_OR_PREVIEW_WRAPPER", {"text_length": len(text)}
    ld = article_ld(soup)
    return True, "COMPLETE_ARTICLE_DOM", {"text_length": len(text), "json_ld": ld}


def retrieve_browser(record: dict[str, Any]) -> dict[str, Any]:
    label = record["source_id"]
    data = browser_capture(label, record["canonical_url"], scroll=False, output_dir=IDENTITY_CAPTURES)
    html_path_value = data.get("rendered_html_path")
    body = (REPO_ROOT / html_path_value).read_bytes() if html_path_value else b""
    return {
        "ok": bool(body),
        "requested_url": record["canonical_url"],
        "final_url": data.get("final_url", record["canonical_url"]),
        "status": data.get("http_status"),
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "redirect_chain": [],
        "body": body,
        "error": data.get("error"),
        "browser_metadata": data,
    }


def best_archive_snapshot(record: dict[str, Any]) -> dict[str, Any] | None:
    snapshots = record.get("archived_snapshots") or []
    if not snapshots:
        return None
    snapshot = sorted(snapshots, key=lambda item: item.get("timestamp") or "")[-1]
    replay = f"https://web.archive.org/web/{snapshot['timestamp']}id_/{snapshot['original_url']}"
    result = http_get(replay, timeout=90)
    result["snapshot"] = snapshot
    return result


def select_article(record: dict[str, Any], rss_bodies: dict[str, Any]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    direct = http_get(record["canonical_url"], timeout=60)
    direct_text = decode_body(direct)
    complete, reason, details = complete_article_html(direct_text)
    attempts.append(
        {
            "tier": "LIVE_DIRECT_HTML",
            "requested_url": direct["requested_url"],
            "final_url": direct["final_url"],
            "http_status": direct["status"],
            "byte_count": len(direct["body"]),
            "sha256": sha256_bytes(direct["body"]),
            "complete": complete,
            "decision": reason,
            "details": details,
            "error": direct["error"],
            "redirect_chain": direct["redirect_chain"],
        }
    )
    if complete:
        direct["retrieval_tier"] = "LIVE_DIRECT_HTML"
        return direct, attempts

    browser = retrieve_browser(record)
    browser_text = decode_body(browser)
    complete, reason, details = complete_article_html(browser_text)
    attempts.append(
        {
            "tier": "LIVE_PLAYWRIGHT_DOM",
            "requested_url": browser["requested_url"],
            "final_url": browser["final_url"],
            "http_status": browser["status"],
            "byte_count": len(browser["body"]),
            "sha256": sha256_bytes(browser["body"]),
            "complete": complete,
            "decision": reason,
            "details": details,
            "error": browser["error"],
            "redirect_chain": browser["redirect_chain"],
        }
    )
    if complete:
        browser["retrieval_tier"] = "LIVE_PLAYWRIGHT_DOM"
        return browser, attempts

    pid = record.get("medium_post_id")
    rss = rss_bodies.get(pid) if pid else None
    if rss and rss.get("content_encoded"):
        rss_html = f"<html><body><article>{rss['content_encoded']}</article></body></html>"
        complete, reason, details = complete_article_html(rss_html)
        truncated_markers = ("continue reading on medium", "read the full story on medium")
        if any(marker in rss_html.lower() for marker in truncated_markers):
            complete, reason = False, "RSS_TRUNCATION_MARKER"
        attempts.append(
            {
                "tier": "RSS_CONTENT_ENCODED",
                "requested_url": record["canonical_url"],
                "final_url": record["canonical_url"],
                "http_status": 200,
                "byte_count": len(rss_html.encode()),
                "sha256": sha256_bytes(rss_html.encode()),
                "complete": complete,
                "decision": reason,
                "details": details,
                "error": None,
                "redirect_chain": [],
            }
        )
        if complete:
            return (
                {
                    "ok": True,
                    "requested_url": record["canonical_url"],
                    "final_url": record["canonical_url"],
                    "status": 200,
                    "headers": {"Content-Type": "text/html; charset=utf-8"},
                    "redirect_chain": [],
                    "body": rss_html.encode(),
                    "error": None,
                    "retrieval_tier": "RSS_CONTENT_ENCODED",
                    "rss_metadata": rss,
                },
                attempts,
            )

    archived = best_archive_snapshot(record)
    if archived:
        archive_text = decode_body(archived)
        complete, reason, details = complete_article_html(archive_text)
        attempts.append(
            {
                "tier": "WEB_ARCHIVE_SNAPSHOT",
                "requested_url": archived["requested_url"],
                "final_url": archived["final_url"],
                "http_status": archived["status"],
                "byte_count": len(archived["body"]),
                "sha256": sha256_bytes(archived["body"]),
                "complete": complete,
                "decision": reason,
                "details": details,
                "error": archived["error"],
                "redirect_chain": archived["redirect_chain"],
                "snapshot": archived.get("snapshot"),
            }
        )
        if complete:
            archived["retrieval_tier"] = "WEB_ARCHIVE_SNAPSHOT"
            return archived, attempts
    return None, attempts


def node_text(node: Tag) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()


def best_image_url(node: Tag) -> str | None:
    srcset = node.get("srcset")
    if srcset:
        choices: list[tuple[int, str]] = []
        for item in srcset.split(","):
            parts = item.strip().split()
            if not parts:
                continue
            size = 0
            if len(parts) > 1:
                match = re.match(r"(\d+)", parts[-1])
                size = int(match.group(1)) if match else 0
            choices.append((size, parts[0]))
        if choices:
            return max(choices)[1]
    return node.get("src") or node.get("data-src")


def extract_article(html_text: str, record: dict[str, Any], selected: dict[str, Any]) -> dict[str, Any]:
    soup = BeautifulSoup(html_text, "html.parser")
    article = soup.find("article")
    if not article:
        raise ValueError("Article element missing")
    for unwanted in article.select("nav, aside, footer, script, style, noscript, form"):
        unwanted.decompose()
    ld = article_ld(soup)
    canonical_node = soup.find("link", rel=lambda value: value and "canonical" in value)
    canonical = canonicalize_url(
        (canonical_node.get("href") if canonical_node else None)
        or ld.get("url")
        or selected.get("final_url")
        or record["canonical_url"]
    )
    title = ld.get("headline") or ld.get("name") or meta_value(soup, "og:title", "twitter:title") or record.get("title")
    subtitle = meta_value(soup, "description", "og:description")
    authors = author_names(ld, soup) or ([record["author"]] if record.get("author") else [])
    publisher = publisher_name(ld) or record.get("publication")
    published_original = ld.get("datePublished") or ld.get("dateCreated") or record.get("published_at_original")
    updated_original = ld.get("dateModified") or record.get("updated_at_original")
    tags = []
    keywords = ld.get("keywords") or meta_value(soup, "keywords", "news_keywords")
    if isinstance(keywords, str):
        tags = [item.strip() for item in keywords.split(",") if item.strip()]
    elif isinstance(keywords, list):
        tags = [str(item).strip() for item in keywords if str(item).strip()]

    blocks: list[dict[str, Any]] = []
    images: list[dict[str, Any]] = []
    embeds: list[dict[str, Any]] = []
    outbound_links: list[dict[str, Any]] = []
    seen_text_nodes: set[int] = set()
    for node in article.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "pre", "figure", "iframe"]):
        if any(id(parent) in seen_text_nodes for parent in node.parents if isinstance(parent, Tag)):
            continue
        name = node.name.lower()
        if name == "figure":
            for image_index, image_node in enumerate(node.find_all("img")):
                url = best_image_url(image_node)
                if url:
                    images.append(
                        {
                            "article_order": len(images) + 1,
                            "original_url": urllib.parse.urljoin(canonical, url),
                            "alt_text": image_node.get("alt") or None,
                            "caption": node_text(node.find("figcaption")) if node.find("figcaption") else None,
                            "placement_block": len(blocks),
                            "figure_image_index": image_index,
                        }
                    )
            caption = node.find("figcaption")
            if caption and node_text(caption):
                blocks.append({"type": "caption", "text": node_text(caption), "level": None})
            for frame in node.find_all(["iframe", "video", "audio"]):
                url = frame.get("src")
                if url:
                    embeds.append(
                        {
                            "article_order": len(embeds) + 1,
                            "url": urllib.parse.urljoin(canonical, url),
                            "kind": frame.name.lower(),
                            "placement_block": len(blocks),
                        }
                    )
            seen_text_nodes.add(id(node))
            continue
        if name == "iframe":
            if node.get("src"):
                embeds.append(
                    {
                        "article_order": len(embeds) + 1,
                        "url": urllib.parse.urljoin(canonical, node["src"]),
                        "kind": "iframe",
                        "placement_block": len(blocks),
                    }
                )
            continue
        text = node_text(node)
        if not text:
            continue
        lower_text = text.casefold()
        if lower_text in {
            "listen",
            "share",
            "follow",
            "sign in",
            "get started",
            "open in app",
            "--",
        } or re.fullmatch(r"\d+", text):
            continue
        if name == "h1" and title and text.strip() == str(title).strip():
            continue
        if name.startswith("h"):
            block_type, level = "heading", int(name[1])
        elif name == "li":
            block_type, level = "list_item", None
        elif name == "blockquote":
            block_type, level = "quotation", None
        elif name == "pre":
            block_type, level = "code", None
        else:
            block_type, level = "paragraph", None
        blocks.append({"type": block_type, "text": text, "level": level})
        seen_text_nodes.add(id(node))

    for image_node in article.find_all("img"):
        url = best_image_url(image_node)
        if not url:
            continue
        absolute = urllib.parse.urljoin(canonical, url)
        if any(item["original_url"] == absolute for item in images):
            continue
        images.append(
            {
                "article_order": len(images) + 1,
                "original_url": absolute,
                "alt_text": image_node.get("alt") or None,
                "caption": None,
                "placement_block": None,
                "figure_image_index": 0,
            }
        )
    images = [
        item
        for item in images
        if not any(marker in item["original_url"].lower() for marker in ("avatar", "stat?", "tracking", "favicon"))
    ]
    for link in article.find_all("a", href=True):
        url = urllib.parse.urljoin(canonical, link["href"])
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme not in {"http", "https"}:
            continue
        outbound_links.append(
            {
                "url": canonicalize_url(url),
                "text": node_text(link) or None,
                "placement_block": None,
            }
        )
    outbound_links = list(
        {json.dumps(item, sort_keys=True): item for item in outbound_links}.values()
    )
    article_text = "\n\n".join(block["text"] for block in blocks)
    reading_time = meta_value(soup, "twitter:data1")
    return {
        "source": {
            "source_id": record["source_id"],
            "medium_post_id": record["medium_post_id"],
            "url": canonical,
            "canonical_url": canonical,
            "observed_urls": record["observed_urls"],
            "title": title,
            "subtitle": subtitle,
            "authors": authors,
            "publisher": publisher,
            "publication_identity": ld.get("publisher") if isinstance(ld.get("publisher"), dict) else None,
            "published_at_original": published_original,
            "published_at_normalized": normalize_date(published_original),
            "updated_at_original": updated_original,
            "updated_at_normalized": normalize_date(updated_original),
            "retrieved_at": None,
            "document_type": "WRITTEN_PUBLICATION",
            "source_role": "OFFICIAL_MEDIUM_ARTICLE",
            "language": "English",
            "tags": sorted(set(tags)),
            "reading_time_original": reading_time,
        },
        "source_lineage": {
            "publication": OFFICIAL_PUBLICATION,
            "publication_role": "OFFICIAL_PUBLICATION",
            "relationship": "PUBLISHED_BY",
            "primary_sources": [],
            "original_creators": authors,
            "attribution_chain": [
                {"role": "AUTHOR", "name": name, "url": None, "organization": None} for name in authors
            ],
            "lineage_confidence": "HIGH" if publisher == OFFICIAL_PUBLICATION and authors else "MEDIUM",
            "limitations": ["Article-level cited-source lineage requires later semantic review."],
        },
        "blocks": blocks,
        "article_text": article_text,
        "content_sha256": sha256_bytes(article_text.encode()),
        "outbound_links": outbound_links,
        "images": images,
        "embeds": embeds,
        "quality": {
            "extraction_confidence": "HIGH" if len(article_text) >= 1000 and title and publisher else "MEDIUM",
            "date_confidence": "HIGH" if normalize_date(published_original) else "UNKNOWN",
            "author_confidence": "HIGH" if authors else "UNKNOWN",
            "completeness": "COMPLETE_ARTICLE_DOM",
            "manual_review_reasons": [],
        },
    }


def retrieve_images(article: dict[str, Any], article_dir: Path) -> list[dict[str, Any]]:
    del article_dir  # retained in the signature to keep call sites stable
    return [
        {
            "article_order": image.get("article_order"),
            "original_url": image.get("original_url"),
            "alt_text": image.get("alt_text"),
            "caption": image.get("caption"),
            "placement_block": image.get("placement_block"),
            "figure_image_index": image.get("figure_image_index"),
            "retrieval_status": "URL_ONLY_OPERATOR_SCOPE",
        }
        for image in article.get("images", [])
    ]


def normalized_markdown(article: dict[str, Any], media: list[dict[str, Any]]) -> str:
    source = article["source"]
    lines = [
        "---",
        f"source_id: {source['source_id']}",
        f"medium_post_id: {source['medium_post_id']}",
        f"title: {json.dumps(source['title'], ensure_ascii=False)}",
        f"publisher: {json.dumps(source['publisher'], ensure_ascii=False)}",
        f"published_at: {source['published_at_normalized'] or 'null'}",
        f"updated_at: {source['updated_at_normalized'] or 'null'}",
        f"canonical_url: {source['canonical_url']}",
        "document_type: WRITTEN_PUBLICATION",
        "---",
        "",
        f"# {source['title']}",
    ]
    if source.get("subtitle"):
        lines += ["", source["subtitle"]]
    lines += [
        "",
        f"- Author: {', '.join(source['authors']) if source['authors'] else 'UNKNOWN'}",
        f"- Publisher: {source['publisher'] or 'UNKNOWN'}",
        f"- Published: {source['published_at_original'] or 'UNKNOWN'}",
        f"- Updated: {source['updated_at_original'] or 'UNKNOWN'}",
        f"- Canonical URL: {source['canonical_url']}",
        "",
        "## Preserved Article",
        "",
    ]
    for block in article["blocks"]:
        if block["type"] == "heading":
            level = max(2, min(6, block.get("level") or 2))
            lines += ["", f"{'#' * level} {block['text']}", ""]
        elif block["type"] == "list_item":
            lines.append(f"- {block['text']}")
        elif block["type"] == "quotation":
            lines += [f"> {part}" for part in block["text"].splitlines()]
            lines.append("")
        elif block["type"] == "code":
            lines += ["```text", block["text"], "```", ""]
        elif block["type"] == "caption":
            lines += [f"*{block['text']}*", ""]
        else:
            lines += [block["text"], ""]
    if media:
        lines += ["## Referenced Article Images", ""]
        for item in media:
            label = item.get("alt_text") or item.get("caption") or f"Article image {item['article_order']}"
            lines.append(f"- {label}: {item['original_url']} (URL only; binary not downloaded)")
        lines.append("")
    if article["embeds"]:
        lines += ["## Referenced Embeds", ""]
        lines += [f"- {item['kind']}: {item['url']}" for item in article["embeds"]]
    return "\n".join(lines)


def source_record_json(article: dict[str, Any], retrieval: dict[str, Any], media: list[dict[str, Any]]) -> dict[str, Any]:
    source = article["source"]
    return {
        "source_id": source["source_id"],
        "title": source["title"],
        "creator": source["authors"],
        "publisher": source["publisher"],
        "source_type": "official",
        "document_type": source["document_type"],
        "published_at_original": source["published_at_original"],
        "published_at_normalized": source["published_at_normalized"],
        "updated_at_original": source["updated_at_original"],
        "updated_at_normalized": source["updated_at_normalized"],
        "collected": retrieval["captured_at"],
        "access": "public",
        "completeness": "complete",
        "authenticity": "confirmed",
        "publication_restriction": "attribute",
        "canonical_url": source["canonical_url"],
        "observed_urls": source["observed_urls"],
        "raw_path": retrieval["selected_raw_path"],
        "normalized_json_path": rel(NORMALIZED_ROOT / f"{source['source_id']}.json"),
        "normalized_markdown_path": rel(NORMALIZED_ROOT / f"{source['source_id']}.md"),
        "raw_sha256": retrieval["raw_sha256"],
        "normalized_content_sha256": article["content_sha256"],
        "media_count": len(media),
        "media_successes": 0,
        "source_lineage": article["source_lineage"],
        "quality": article["quality"],
        "provenance": {
            "retrieval_tier": retrieval["selected_tier"],
            "retrieval_attempts": retrieval["attempts"],
            "discovery_sources": retrieval["discovery_sources"],
            "referrer_source_ids": retrieval["referrer_source_ids"],
        },
        "limitations": [
            "Current live content may reflect edits made after original publication.",
            "Cited-source lineage requires separate semantic enrichment.",
        ],
    }


def source_record_markdown(record: dict[str, Any], article: dict[str, Any]) -> str:
    lineage = record["source_lineage"]
    sources = lineage["primary_sources"] or ["UNKNOWN"]
    creators = lineage["original_creators"] or ["UNKNOWN"]
    return f"""---
source_id: {record['source_id']}
title: {json.dumps(record['title'], ensure_ascii=False)}
creator: {json.dumps(record['creator'], ensure_ascii=False)}
publisher: {json.dumps(record['publisher'], ensure_ascii=False)}
source_type: official
published: {record['published_at_normalized'] or 'null'}
updated: {record['updated_at_normalized'] or 'null'}
collected: {record['collected']}
access: public
completeness: complete
authenticity: confirmed
publication_restriction: attribute
url: {record['canonical_url']}
---

# {record['title']}

## Metadata

- Source ID: `{record['source_id']}`
- Medium Post ID: `{article['source']['medium_post_id']}`
- Author: {', '.join(record['creator']) if record['creator'] else 'UNKNOWN'}
- Publisher: {record['publisher'] or 'UNKNOWN'}
- Publication Date: {record['published_at_original'] or 'UNKNOWN'}
- Normalized Publication Date: {record['published_at_normalized'] or 'UNKNOWN'}
- Updated Date: {record['updated_at_original'] or 'UNKNOWN'}
- Canonical URL: {record['canonical_url']}
- Retrieval Tier: `{record['provenance']['retrieval_tier']}`

## Source Lineage

- Publication: {lineage['publication']}
- Publication Role: `{lineage['publication_role']}`
- Relationship: `{lineage['relationship']}`
- Primary Sources: {', '.join(sources)}
- Original Creators: {', '.join(creators)}
- Lineage Confidence: `{lineage['lineage_confidence']}`

## Source Summary

This record preserves the complete captured text and article-body media of an official Star Atlas Medium publication. It does not convert the article into canonical knowledge or semantic claims.

## What This Source Establishes

- Star Atlas published this written article at the captured canonical Medium URL.
- The preserved article text and media are available through the linked archive artifacts.

## Reliability and Limitations

The captured publication is authoritative for what Star Atlas publicly stated, not automatic proof that every announced plan, result, partnership outcome, or historical claim occurred as described. Current live content may include later edits. Article-level citations and republished-source lineage require separate semantic review.

## Provenance

- Raw evidence: `{record['raw_path']}`
- Raw SHA-256: `{record['raw_sha256']}`
- Normalized JSON: `{record['normalized_json_path']}`
- Normalized Markdown: `{record['normalized_markdown_path']}`
- Normalized content SHA-256: `{record['normalized_content_sha256']}`
- Discovery sources: {', '.join(record['provenance']['discovery_sources']) or 'UNKNOWN'}

## Processing Notes

- Article image and embed URLs are preserved as references; media binaries were not downloaded by operator instruction.
- Medium navigation, recommendation cards, avatars, and tracking/UI assets were excluded from normalized content.
- Publisher and author identities remain separate fields.

## Extraction Confidence

- Extraction: `{article['quality']['extraction_confidence']}`
- Date: `{article['quality']['date_confidence']}`
- Author: `{article['quality']['author_confidence']}`

## Open Verification Tasks

- Review outbound citations and quotations during the follow-on semantic campaign.
- Reconcile any post-publication edits against archived captures when historically material.
"""


def ingestion_package(article: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    source = article["source"]
    return {
        "metadata": {
            "repository_schema": "2.1",
            "artifact_type": "INGESTION_PACKAGE",
            "ingestion_id": f"INGEST-MEDIUM-STARATLAS-{source['medium_post_id'].upper()}",
            "campaign_id": CAMPAIGN_ID,
            "promotion_status": "ARCHIVED_NOT_PROMOTED",
        },
        "sources": [
            {
                "source_id": source["source_id"],
                "title": source["title"],
                "type": "OFFICIAL_MEDIUM_ARTICLE",
                "tier": "OFFICIAL",
                "language": source["language"],
                "url": source["canonical_url"],
                "artifact_chain": {
                    "raw_html": record["raw_path"],
                    "normalized_json": record["normalized_json_path"],
                    "normalized_markdown": record["normalized_markdown_path"],
                    "source_record_json": rel(SOURCE_RECORD_ROOT / f"{source['source_id']}.json"),
                    "source_record_markdown": rel(SOURCE_RECORD_ROOT / f"{source['source_id']}.md"),
                },
                "source_lineage": article["source_lineage"],
            }
        ],
        "entities": [],
        "events": [],
        "claims": [],
        "quotes": [],
        "relationships": [],
        "timeline_updates": [],
        "research_tasks": [],
        "knowledge_delta": {},
        "search_log": {
            "discovery_sources": record["provenance"]["discovery_sources"],
            "referrer_source_ids": record["provenance"]["referrer_source_ids"],
        },
        "repository_health": {"manual_review_required": bool(article["quality"]["manual_review_reasons"])},
        "transcript": [],
        "article": {
            "published_at_original": source["published_at_original"],
            "published_at_normalized": source["published_at_normalized"],
            "updated_at_original": source["updated_at_original"],
            "updated_at_normalized": source["updated_at_normalized"],
            "content_sha256": article["content_sha256"],
            "block_count": len(article["blocks"]),
            "outbound_links": article["outbound_links"],
            "embeds": article["embeds"],
        },
    }


def retrieve_one(record: dict[str, Any], rss_bodies: dict[str, Any]) -> dict[str, Any]:
    sid = record["source_id"]
    normalized_path = NORMALIZED_ROOT / f"{sid}.json"
    retrieval_path = RAW_ROOT / sid / "retrieval.json"
    previous_retrieval = read_json(retrieval_path, {}) or {}
    if normalized_path.exists() and previous_retrieval:
        raw_value = previous_retrieval.get("selected_raw_path")
        cached_raw = REPO_ROOT / raw_value if raw_value else None
        if cached_raw and cached_raw.exists() and sha256_file(cached_raw) == previous_retrieval.get("raw_sha256"):
            selected = {
                "final_url": previous_retrieval.get("final_url", record["canonical_url"]),
                "requested_url": previous_retrieval.get("requested_url", record["canonical_url"]),
                "status": previous_retrieval.get("http_status"),
                "retrieval_tier": previous_retrieval.get("selected_tier"),
            }
            refreshed = extract_article(cached_raw.read_text(encoding="utf-8"), record, selected)
            refreshed["source"]["retrieved_at"] = previous_retrieval.get("captured_at")
            refreshed["images"] = retrieve_images(refreshed, RAW_ROOT / sid)
            refreshed["retrieval"] = previous_retrieval
            write_json(normalized_path, refreshed)
    if normalized_path.exists():
        cached_article = read_json(normalized_path, {}) or {}
        text_only_media = retrieve_images(cached_article, RAW_ROOT / sid)
        if cached_article.get("images") != text_only_media:
            cached_article["images"] = text_only_media
            write_json(normalized_path, cached_article)
            write_json(
                RAW_ROOT / sid / "media-manifest.json",
                {
                    "source_id": sid,
                    "canonical_url": cached_article.get("source", {}).get("canonical_url"),
                    "media": text_only_media,
                    "mode": "URL_ONLY_OPERATOR_SCOPE",
                },
            )
        if previous_retrieval:
            write_text(NORMALIZED_ROOT / f"{sid}.md", normalized_markdown(cached_article, text_only_media))
            cached_sr = source_record_json(cached_article, previous_retrieval, text_only_media)
            write_json(SOURCE_RECORD_ROOT / f"{sid}.json", cached_sr)
            write_text(SOURCE_RECORD_ROOT / f"{sid}.md", source_record_markdown(cached_sr, cached_article))
            write_json(EXTRACTION_ROOT / f"{sid}.json", ingestion_package(cached_article, cached_sr))
    if normalized_path.exists() and not previous_retrieval:
        cached_article = read_json(normalized_path, {}) or {}
        cached_retrieval = cached_article.get("retrieval", {})
        raw_value = cached_retrieval.get("selected_raw_path")
        cached_raw = REPO_ROOT / raw_value if raw_value else None
        if cached_raw and cached_raw.exists() and sha256_file(cached_raw) == cached_retrieval.get("raw_sha256"):
            cached_media = (read_json(RAW_ROOT / sid / "media-manifest.json", {}) or {}).get("media", [])
            write_text(NORMALIZED_ROOT / f"{sid}.md", normalized_markdown(cached_article, cached_media))
            cached_sr = source_record_json(cached_article, cached_retrieval, cached_media)
            write_json(SOURCE_RECORD_ROOT / f"{sid}.json", cached_sr)
            write_text(SOURCE_RECORD_ROOT / f"{sid}.md", source_record_markdown(cached_sr, cached_article))
            write_json(EXTRACTION_ROOT / f"{sid}.json", ingestion_package(cached_article, cached_sr))
            write_json(retrieval_path, cached_retrieval)
            previous_retrieval = cached_retrieval
    if normalized_path.exists() and previous_retrieval:
        raw_value = previous_retrieval.get("selected_raw_path")
        raw_path = REPO_ROOT / raw_value if raw_value else None
        if raw_path and raw_path.exists() and sha256_file(raw_path) == previous_retrieval.get("raw_sha256"):
            return {"source_id": sid, "status": "SKIPPED_CHECKSUM_IDENTICAL_SUCCESS", "retrieval": previous_retrieval}

    delay = max(0.0, float(os.environ.get("MEDIUM_REQUEST_DELAY", "0")))
    if delay:
        time.sleep(delay)
    selected, attempts = select_article(record, rss_bodies)
    if not selected:
        failure = {
            "source_id": sid,
            "status": "FAILED",
            "canonical_url": record["canonical_url"],
            "attempted_at": now_iso(),
            "attempts": attempts,
        }
        return failure
    html_text = decode_body(selected)
    article = extract_article(html_text, record, selected)
    publisher = article["source"].get("publisher")
    canonical_path = urllib.parse.urlsplit(article["source"]["canonical_url"]).path.lower()
    publication_confirmed = publisher == OFFICIAL_PUBLICATION or canonical_path.startswith("/star-atlas/")
    if not publication_confirmed:
        return {
            "source_id": sid,
            "status": "FAILED_IDENTITY_MISMATCH",
            "canonical_url": record["canonical_url"],
            "attempted_at": now_iso(),
            "publisher_found": publisher,
            "attempts": attempts,
        }
    if publisher != OFFICIAL_PUBLICATION:
        article["quality"]["manual_review_reasons"].append("Publisher inferred from canonical publication path")
        article["source"]["publisher"] = OFFICIAL_PUBLICATION
        article["source_lineage"]["lineage_confidence"] = "MEDIUM"

    raw_dir = RAW_ROOT / sid
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_sha = sha256_bytes(selected["body"])
    raw_path = raw_dir / "article.html"
    if raw_path.exists() and sha256_file(raw_path) != raw_sha:
        raw_path = raw_dir / f"article-{raw_sha[:12]}.html"
    if not raw_path.exists():
        raw_path.write_bytes(selected["body"])
    captured_at = now_iso()
    article["source"]["retrieved_at"] = captured_at
    media = retrieve_images(article, raw_dir)
    media_manifest_path = raw_dir / "media-manifest.json"
    write_json(
        media_manifest_path,
        {
            "source_id": sid,
            "canonical_url": article["source"]["canonical_url"],
            "media": media,
            "mode": "URL_ONLY_OPERATOR_SCOPE",
        },
    )
    article["images"] = media
    article["retrieval"] = {
        "selected_tier": selected["retrieval_tier"],
        "selected_raw_path": rel(raw_path),
        "requested_url": selected["requested_url"],
        "final_url": selected["final_url"],
        "http_status": selected["status"],
        "content_type": selected.get("headers", {}).get("Content-Type"),
        "raw_sha256": raw_sha,
        "raw_byte_count": len(selected["body"]),
        "captured_at": captured_at,
        "attempts": attempts,
        "discovery_sources": record["discovery_sources"],
        "referrer_source_ids": record["referrer_source_ids"],
        "redirect_chain": selected.get("redirect_chain", []),
    }
    write_json(normalized_path, article)
    write_text(NORMALIZED_ROOT / f"{sid}.md", normalized_markdown(article, media))
    sr_json = source_record_json(article, article["retrieval"], media)
    write_json(SOURCE_RECORD_ROOT / f"{sid}.json", sr_json)
    write_text(SOURCE_RECORD_ROOT / f"{sid}.md", source_record_markdown(sr_json, article))
    write_json(EXTRACTION_ROOT / f"{sid}.json", ingestion_package(article, sr_json))
    write_json(retrieval_path, article["retrieval"])
    return {
        "source_id": sid,
        "medium_post_id": record["medium_post_id"],
        "status": "SUCCESS",
        "canonical_url": article["source"]["canonical_url"],
        "title": article["source"]["title"],
        "authors": article["source"]["authors"],
        "publisher": article["source"]["publisher"],
        "published_at": article["source"]["published_at_normalized"],
        "updated_at": article["source"]["updated_at_normalized"],
        "retrieval_tier": selected["retrieval_tier"],
        "extraction_confidence": article["quality"]["extraction_confidence"],
        "raw_sha256": raw_sha,
        "content_sha256": article["content_sha256"],
        "media_count": len(media),
        "media_successes": 0,
        "manual_review_reasons": article["quality"]["manual_review_reasons"],
        "retrieval": article["retrieval"],
    }


def update_manifest_retrieval(records: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    result_by_id = {item["source_id"]: item for item in results}
    for record in records:
        result = result_by_id.get(record["source_id"])
        if not result:
            continue
        if result["status"] in {"SUCCESS", "SKIPPED_CHECKSUM_IDENTICAL_SUCCESS"}:
            record["retrieval_status"] = "SUCCESS"
            record["retrieval_method"] = result.get("retrieval_tier") or result.get("retrieval", {}).get("selected_tier")
            # The retrieved article is the final identity and quality evidence. Do
            # not retain discovery-time cautions after its structured metadata has
            # established official publication membership.
            record["manual_review_reasons"] = list(result.get("manual_review_reasons", []))
            record["manual_review_required"] = bool(record["manual_review_reasons"])
        else:
            record["retrieval_status"] = result["status"]
            record["manual_review_required"] = True
            reason = f"Retrieval result: {result['status']}"
            if reason not in record["manual_review_reasons"]:
                record["manual_review_reasons"].append(reason)


def retrieve() -> int:
    manifest = read_json(URL_MANIFEST)
    if not manifest:
        raise SystemExit("Run discover before retrieve: frozen URL manifest is missing")
    records = manifest.get("records", [])
    unresolved = [item for item in records if item.get("inclusion_status") not in {"INCLUDED", "EXCLUDED", "DEFERRED"}]
    if unresolved:
        raise SystemExit(f"Discovery manifest is not frozen: {len(unresolved)} candidates lack dispositions")
    rss_bodies = read_json(OPS / "rss-content-index.json", {}) or {}
    included = [item for item in records if item["inclusion_status"] == "INCLUDED"]
    previous = read_json(RETRIEVAL_LEDGER, {}) or {}
    previous_results = {item["source_id"]: item for item in previous.get("results", [])}
    results_by_id: dict[str, dict[str, Any]] = {}
    workers = max(1, min(6, int(os.environ.get("MEDIUM_WORKERS", "3"))))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_record = {executor.submit(retrieve_one, record, rss_bodies): record for record in included}
        completed_count = 0
        for future in concurrent.futures.as_completed(future_to_record):
            record = future_to_record[future]
            completed_count += 1
            try:
                result = future.result()
            except Exception as exc:  # noqa: BLE001 - campaign must checkpoint unexpected per-article defects
                result = {
                    "source_id": record["source_id"],
                    "status": "FAILED_INTERNAL_ERROR",
                    "canonical_url": record["canonical_url"],
                    "attempted_at": now_iso(),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            if result["status"] == "SKIPPED_CHECKSUM_IDENTICAL_SUCCESS":
                prior = previous_results.get(record["source_id"])
                if prior and prior.get("status") == "SUCCESS":
                    result = prior
                else:
                    normalized = read_json(NORMALIZED_ROOT / f"{record['source_id']}.json", {}) or {}
                    source = normalized.get("source", {})
                    retrieval = result["retrieval"]
                    media = (read_json(RAW_ROOT / record["source_id"] / "media-manifest.json", {}) or {}).get("media", [])
                    result = {
                        "source_id": record["source_id"],
                        "medium_post_id": record["medium_post_id"],
                        "status": "SUCCESS",
                        "canonical_url": source.get("canonical_url", record["canonical_url"]),
                        "title": source.get("title"),
                        "authors": source.get("authors", []),
                        "publisher": source.get("publisher"),
                        "published_at": source.get("published_at_normalized"),
                        "updated_at": source.get("updated_at_normalized"),
                        "retrieval_tier": retrieval.get("selected_tier"),
                        "extraction_confidence": normalized.get("quality", {}).get("extraction_confidence"),
                        "raw_sha256": retrieval.get("raw_sha256"),
                        "content_sha256": normalized.get("content_sha256"),
                        "media_count": len(media),
                        "media_successes": 0,
                        "manual_review_reasons": normalized.get("quality", {}).get("manual_review_reasons", []),
                        "retrieval": retrieval,
                    }
            results_by_id[record["source_id"]] = result
            print(
                f"[{completed_count}/{len(included)}] {record['source_id']} -> {result['status']}",
                flush=True,
            )
            ordered_results = [results_by_id[item["source_id"]] for item in included if item["source_id"] in results_by_id]
            write_json(RETRIEVAL_LEDGER, {"campaign_id": CAMPAIGN_ID, "results": ordered_results})
            write_json(
                RETRY_LEDGER,
                {
                    "campaign_id": CAMPAIGN_ID,
                    "records": [item for item in ordered_results if item["status"] != "SUCCESS"],
                },
            )
    results = [results_by_id[item["source_id"]] for item in included]
    update_manifest_retrieval(records, results)
    manifest["records"] = records
    manifest["retrieval_updated_at"] = now_iso()
    write_json(URL_MANIFEST, manifest)
    write_json(
        MANUAL_REVIEW,
        {
            "campaign_id": CAMPAIGN_ID,
            "queue_status": "EXPLICITLY_DEFERRED_OR_ARTICLE_QUALITY_REVIEW",
            "records": [item for item in records if item["manual_review_required"]],
        },
    )
    generate_reports(manifest, results)
    successes = sum(item["status"] == "SUCCESS" for item in results)
    print(f"Retrieved {successes}/{len(included)} included articles")
    return 0 if successes == len(included) else 2


def artifact_entry(path: Path) -> dict[str, Any]:
    return {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)}


def normalized_output_fingerprint() -> str:
    digest = hashlib.sha256()
    roots = (NORMALIZED_ROOT, SOURCE_RECORD_ROOT, PACKAGE_ROOT)
    for root in roots:
        for path in sorted(
            (item for item in root.rglob("*") if item.is_file() and item.name != ".gitattributes"),
            key=rel,
        ):
            digest.update(rel(path).encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
    return digest.hexdigest()


def campaign_artifacts() -> list[Path]:
    roots = [RAW_ROOT, NORMALIZED_ROOT, SOURCE_RECORD_ROOT, PACKAGE_ROOT, OPS, SUMMARY_ROOT]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file())
    excluded = {CAMPAIGN_MANIFEST.resolve(), ARCHIVE_MANIFEST.resolve(), VALIDATION_JSON.resolve(), VALIDATION_MD.resolve()}
    return sorted((path for path in files if path.resolve() not in excluded), key=rel)


def generate_reports(manifest: dict[str, Any], results: list[dict[str, Any]]) -> None:
    records = manifest["records"]
    included = [item for item in records if item["inclusion_status"] == "INCLUDED"]
    successful = [item for item in results if item["status"] == "SUCCESS"]
    failures = [item for item in results if item["status"] != "SUCCESS"]
    dates = sorted(item["published_at"] for item in successful if item.get("published_at"))
    by_year = collections.Counter(
        int(item["published_at"][:4]) for item in successful if item.get("published_at") and item["published_at"][:4].isdigit()
    )
    for year in range(2020, dt.datetime.now(dt.timezone.utc).year + 1):
        by_year.setdefault(year, 0)
    confirmed_complete = len(successful) == len(included) and not failures
    discovery_status = "INCOMPLETE"
    generated_at = manifest.get("adjudication", {}).get("adjudicated_at") or manifest.get("retrieval_updated_at") or now_iso()
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": (
            "CONFIRMED_ARTICLE_INGESTION_COMPLETE_PUBLICATION_DISCOVERY_INCOMPLETE"
            if confirmed_complete
            else "CONFIRMED_ARTICLE_INGESTION_HAS_RETRIEVAL_FAILURES_PUBLICATION_DISCOVERY_INCOMPLETE"
        ),
        "confirmed_article_ingestion_status": "COMPLETE" if confirmed_complete else "RETRIEVAL_FAILURES_REMAIN",
        "publication_discovery_status": discovery_status,
        "generated_at": generated_at,
        "urls_discovered": len(records),
        "urls_included": len(included),
        "urls_excluded": sum(item["inclusion_status"] == "EXCLUDED" for item in records),
        "urls_deferred_after_review": sum(item["inclusion_status"] == "DEFERRED" for item in records),
        "review_candidates_adjudicated": (read_json(ADJUDICATION_LEDGER, {}) or {}).get("review_candidates_received", 0),
        "urls_attempted": len(results),
        "successful_retrievals": len(successful),
        "retrieval_failures": len(failures),
        "articles_extracted": len(successful),
        "duplicate_or_redirect_clusters": len((read_json(DUPLICATE_LEDGER, {}) or {}).get("clusters", [])),
        "retrieval_tier_counts": dict(sorted(collections.Counter(item.get("retrieval_tier") for item in successful).items())),
        "extraction_confidence_counts": dict(
            sorted(collections.Counter(item.get("extraction_confidence") for item in successful).items())
        ),
        "coverage_dates": {"earliest": dates[0] if dates else None, "latest": dates[-1] if dates else None},
        "years_queried": list(range(2020, dt.datetime.now(dt.timezone.utc).year + 1)),
        "confirmed_articles_by_year": {str(year): by_year[year] for year in sorted(by_year)},
        "coverage_2020": "SURFACES_SEARCHED_NO_CONFIRMED_2020_ARTICLE_INCLUDED",
        "media": {
            "references": sum(item.get("media_count", 0) for item in successful),
            "downloads_succeeded": 0,
            "mode": "URL_ONLY_OPERATOR_SCOPE",
        },
        "determinism": read_json(OPS / "determinism-report.json", {}),
        "manual_review_count": sum(item.get("inclusion_status") == "DEFERRED" for item in records),
        "retrieval_failures_detail": failures,
        "completeness_limits": [
            f"Ingestion is complete for the {len(included)} confirmed included articles; publication-level discovery remains incomplete.",
            "The 2020 publication surfaces were searched, but no 2020 Star Atlas publication article was confirmed or included.",
            "Medium year archives currently expose hydration shells or incomplete rendered results.",
            "RSS exposes only a recent subset and sitemap coverage is non-exhaustive.",
            "Deleted or unindexed stories may remain undiscoverable when neither repository nor web-archive evidence survives.",
            "Current live article text may reflect edits made after original publication.",
        ],
    }
    write_json(SUMMARY_JSON, summary)
    lines = [
        "# Official Star Atlas Medium Campaign Summary",
        "",
        f"- Confirmed-article ingestion: **{summary['confirmed_article_ingestion_status']}** ({summary['successful_retrievals']}/{summary['urls_included']})",
        f"- Publication discovery: **{summary['publication_discovery_status']}**",
        f"- Campaign state: **{summary['status']}**",
        f"- URLs discovered: {summary['urls_discovered']}",
        f"- URLs included: {summary['urls_included']}",
        f"- URLs excluded: {summary['urls_excluded']}",
        f"- Review candidates adjudicated: {summary['review_candidates_adjudicated']}",
        f"- Explicitly deferred discovery leads: {summary['urls_deferred_after_review']}",
        f"- URLs attempted: {summary['urls_attempted']}",
        f"- Successful retrievals: {summary['successful_retrievals']}",
        f"- Articles extracted: {summary['articles_extracted']}",
        f"- Retrieval failures: {summary['retrieval_failures']}",
        f"- Duplicate/redirect clusters: {summary['duplicate_or_redirect_clusters']}",
        f"- Coverage: {summary['coverage_dates']['earliest'] or 'UNKNOWN'} through {summary['coverage_dates']['latest'] or 'UNKNOWN'}",
        "- 2020: surfaces searched; no confirmed 2020 publication article included",
        "",
        "## Retrieval tiers",
        "",
    ]
    lines += [f"- {key}: {value}" for key, value in summary["retrieval_tier_counts"].items()]
    lines += ["", "## Extraction confidence", ""]
    lines += [f"- {key}: {value}" for key, value in summary["extraction_confidence_counts"].items()]
    lines += ["", "## Completeness limits", ""]
    lines += [f"- {item}" for item in summary["completeness_limits"]]
    if failures:
        lines += ["", "## Retrieval failures", ""]
        lines += [f"- `{item['source_id']}`: {item['status']} — {item.get('canonical_url')}" for item in failures]
    write_text(SUMMARY_MD, "\n".join(lines))
    artifacts = campaign_artifacts()
    campaign = {
        "campaign_id": CAMPAIGN_ID,
        "repository_schema": "2.1",
        "status": summary["status"],
        "confirmed_article_ingestion_status": summary["confirmed_article_ingestion_status"],
        "publication_discovery_status": summary["publication_discovery_status"],
        "mappings": {
            "raw": rel(RAW_ROOT),
            "normalized": rel(NORMALIZED_ROOT),
            "source_records": rel(SOURCE_RECORD_ROOT),
            "ingestion_packages": rel(PACKAGE_ROOT),
            "operations": rel(OPS),
            "summary": rel(SUMMARY_ROOT),
        },
        "counts": {
            "discovered": len(records),
            "included": len(included),
            "excluded": summary["urls_excluded"],
            "deferred": summary["urls_deferred_after_review"],
            "review_candidates_adjudicated": summary["review_candidates_adjudicated"],
            "retrieved": len(successful),
            "failed": len(failures),
            "confirmed_2020_articles": summary["confirmed_articles_by_year"].get("2020", 0),
        },
        "artifacts": [artifact_entry(path) for path in artifacts],
    }
    write_json(CAMPAIGN_MANIFEST, campaign)
    outer_files = [path for path in campaign_artifacts() if path != CAMPAIGN_MANIFEST]
    outer_files.append(CAMPAIGN_MANIFEST)
    outer = {
        "campaign_id": CAMPAIGN_ID,
        "repository_base": "main",
        "artifact_count": len(outer_files),
        "total_size_bytes": sum(path.stat().st_size for path in outer_files),
        "mappings": campaign["mappings"],
        "artifacts": [artifact_entry(path) for path in sorted(outer_files, key=rel)],
    }
    write_json(ARCHIVE_MANIFEST, outer)


def validate_relative_links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = target.strip().split("#", 1)[0]
        if not target or urllib.parse.urlsplit(target).scheme or target.startswith("#"):
            continue
        if not (path.parent / urllib.parse.unquote(target)).resolve().exists():
            errors.append(f"Broken relative link in {rel(path)}: {target}")
    return errors


def repository_changed_paths() -> list[str]:
    paths: set[str] = set()
    base_name = os.environ.get("GITHUB_BASE_REF", "main")
    for base in (f"origin/{base_name}", base_name):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", base], cwd=REPO_ROOT, capture_output=True, text=True
        )
        if result.returncode:
            continue
        committed = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"], cwd=REPO_ROOT, capture_output=True, text=True
        )
        if not committed.returncode:
            paths.update(line.strip().replace("\\", "/") for line in committed.stdout.splitlines() if line.strip())
            break
    status = subprocess.run(
        ["git", "status", "--porcelain", "-uall"], cwd=REPO_ROOT, capture_output=True, text=True
    )
    for line in status.stdout.splitlines():
        if len(line) >= 4:
            path = line[3:].replace("\\", "/")
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            paths.add(path)
    return sorted(paths)


def validate() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}
    manifest = read_json(URL_MANIFEST)
    if not manifest:
        errors.append("Frozen URL manifest missing or invalid")
        records = []
    else:
        records = manifest.get("records", [])
    dispositions = {"INCLUDED", "EXCLUDED", "DEFERRED"}
    invalid_dispositions = [item.get("source_id") for item in records if item.get("inclusion_status") not in dispositions]
    if invalid_dispositions:
        errors.append(f"Candidates without valid disposition: {invalid_dispositions[:10]}")
    checks["candidate_dispositions"] = {"total": len(records), "invalid": len(invalid_dispositions)}

    if any(item.get("inclusion_status") == "MANUAL_REVIEW" for item in records):
        errors.append("Bare MANUAL_REVIEW disposition remains after adjudication")
    deferred_records = [item for item in records if item.get("inclusion_status") == "DEFERRED"]
    required_deferred_fields = {"adjudication_status", "deferral_reason", "required_artifact", "next_action", "last_attempt"}
    incomplete_deferred = [
        item.get("source_id")
        for item in deferred_records
        if any(not item.get(field) for field in required_deferred_fields)
        or item.get("adjudication_status") != "DEFERRED"
    ]
    if incomplete_deferred:
        errors.append(f"Deferred candidates lack explicit adjudication metadata: {incomplete_deferred[:10]}")
    obvious_deferred = [
        item.get("source_id")
        for item in deferred_records
        if Path(urllib.parse.urlsplit(urllib.parse.unquote(item.get("canonical_url", ""))).path).suffix.lower()
        in MEDIA_SUFFIXES | AUXILIARY_SUFFIXES
    ]
    if obvious_deferred:
        errors.append(f"Obvious asset/document candidates remain deferred: {obvious_deferred[:10]}")
    adjudication = read_json(ADJUDICATION_LEDGER, {}) or {}
    decisions = adjudication.get("decisions", [])
    review_candidates_received = adjudication.get("review_candidates_received", len(decisions))
    if len(decisions) != review_candidates_received:
        errors.append(
            "Manual-review adjudication ledger decision count does not reconcile "
            f"({len(decisions)} decisions for {review_candidates_received} received candidates)"
        )
    decision_ids = [item.get("source_id") for item in decisions]
    if len(decision_ids) != len(set(decision_ids)):
        errors.append("Manual-review adjudication ledger contains duplicate candidate IDs")
    unresolved_decisions = [
        item.get("source_id") for item in decisions if item.get("final_inclusion_status") not in {"EXCLUDED", "DEFERRED"}
    ]
    if unresolved_decisions:
        errors.append(f"Adjudication decisions remain unresolved: {unresolved_decisions[:10]}")
    checks["manual_review_adjudication"] = {
        "received": adjudication.get("review_candidates_received"),
        "resolved_excluded": adjudication.get("resolved_excluded"),
        "explicitly_deferred": adjudication.get("explicitly_deferred"),
        "incomplete_deferred": len(incomplete_deferred),
    }

    included = [item for item in records if item.get("inclusion_status") == "INCLUDED"]
    post_ids = [item.get("medium_post_id") for item in included]
    source_ids = [item.get("source_id") for item in included]
    if None in post_ids:
        errors.append("Included record lacks Medium post ID")
    if len(post_ids) != len(set(post_ids)):
        errors.append("Duplicate Medium post IDs in included manifest")
    if len(source_ids) != len(set(source_ids)):
        errors.append("Duplicate Source IDs in included manifest")
    checks["included_identity"] = {"included": len(included), "unique_post_ids": len(set(post_ids)), "unique_source_ids": len(set(source_ids))}

    discovery = read_json(DISCOVERY_LEDGER, {}) or {}
    years = sorted(
        item.get("year")
        for item in discovery.get("surfaces", [])
        if item.get("surface") == "publication_archive" and item.get("status") == "QUERIED"
    )
    expected_years = list(range(2020, dt.datetime.now(dt.timezone.utc).year + 1))
    if years != expected_years:
        errors.append(f"Archive year coverage mismatch: expected {expected_years}, found {years}")
    required_surfaces = {"publication_archive", "publication_page", "profile_page", "rss:publication", "rss:profile", "sitemap", "repository", "web_archive"}
    found_surfaces = {item.get("surface") for item in discovery.get("surfaces", [])}
    missing_surfaces = sorted(required_surfaces - found_surfaces)
    if missing_surfaces:
        errors.append(f"Discovery surfaces missing: {missing_surfaces}")
    checks["discovery_coverage"] = {"years": years, "surfaces": sorted(str(item) for item in found_surfaces)}
    confirmed_2020 = [item.get("source_id") for item in included if str(item.get("published_at_normalized") or "").startswith("2020-")]
    if 2020 not in years or confirmed_2020:
        errors.append(f"2020 boundary failed: queried={2020 in years}, confirmed_included={len(confirmed_2020)}")
    checks["coverage_2020"] = {"surface_queried": 2020 in years, "confirmed_articles_included": len(confirmed_2020)}

    success_count = 0
    for item in included:
        sid = item["source_id"]
        if item.get("retrieval_status") != "SUCCESS":
            warnings.append(f"Included record not successfully retrieved: {sid} ({item.get('retrieval_status')})")
            continue
        paths = [
            RAW_ROOT / sid / "retrieval.json",
            RAW_ROOT / sid / "media-manifest.json",
            NORMALIZED_ROOT / f"{sid}.json",
            NORMALIZED_ROOT / f"{sid}.md",
            SOURCE_RECORD_ROOT / f"{sid}.json",
            SOURCE_RECORD_ROOT / f"{sid}.md",
            EXTRACTION_ROOT / f"{sid}.json",
        ]
        missing = [rel(path) for path in paths if not path.exists()]
        if missing:
            errors.append(f"Incomplete artifact set for {sid}: {missing}")
            continue
        try:
            normalized = read_json(paths[2])
            source_record = read_json(paths[4])
            package = read_json(paths[6])
            retrieval = read_json(paths[0])
            media_manifest = read_json(paths[1])
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"Invalid JSON/UTF-8 for {sid}: {exc}")
            continue
        if normalized["source"]["source_id"] != sid or source_record["source_id"] != sid:
            errors.append(f"Source ID mismatch in artifact set for {sid}")
        if package.get("metadata", {}).get("repository_schema") != "2.1":
            errors.append(f"Schema v2.1 metadata missing for {sid}")
        raw_path = REPO_ROOT / retrieval["selected_raw_path"]
        if not raw_path.exists() or sha256_file(raw_path) != retrieval["raw_sha256"]:
            errors.append(f"Raw checksum mismatch for {sid}")
        article_text = normalized.get("article_text", "")
        if sha256_bytes(article_text.encode()) != normalized.get("content_sha256"):
            errors.append(f"Normalized content checksum mismatch for {sid}")
        lower = article_text.lower()
        too_short = len(article_text) < 400 or (
            len(article_text) < 500 and len(normalized.get("blocks", [])) < 3
        )
        if too_short or "sign in to continue" in lower or "create an account to read" in lower:
            errors.append(f"Incomplete/login wrapper accepted for {sid}")
        if normalized["source"].get("publisher") != OFFICIAL_PUBLICATION:
            errors.append(f"Publisher identity is not Star Atlas for {sid}")
        if "authors" not in normalized["source"] or "publisher" not in normalized["source"]:
            errors.append(f"Author/publisher fields not separated for {sid}")
        if not normalized.get("source_lineage"):
            errors.append(f"Source lineage missing for {sid}")
        for media in media_manifest.get("media", []):
            if media.get("retrieval_status") == "SUCCESS":
                media_path = REPO_ROOT / media["local_path"]
                if not media_path.exists() or sha256_file(media_path) != media["sha256"]:
                    errors.append(f"Media checksum mismatch for {sid}: {media.get('local_path')}")
        success_count += 1
    checks["artifact_sets"] = {"included": len(included), "validated_successes": success_count}

    for path in sorted(set(NORMALIZED_ROOT.glob("*.md")) | set(SOURCE_RECORD_ROOT.glob("*.md"))):
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"Invalid UTF-8 Markdown {rel(path)}: {exc}")
        errors.extend(validate_relative_links(path))

    campaign_manifest = read_json(CAMPAIGN_MANIFEST, {}) or {}
    for artifact in campaign_manifest.get("artifacts", []):
        path = REPO_ROOT / artifact["path"]
        if not path.exists():
            errors.append(f"Manifest orphan/missing artifact: {artifact['path']}")
        elif path.stat().st_size != artifact["size_bytes"] or sha256_file(path) != artifact["sha256"]:
            errors.append(f"Manifest checksum mismatch: {artifact['path']}")
    checks["campaign_manifest_artifacts"] = len(campaign_manifest.get("artifacts", []))

    summary = read_json(SUMMARY_JSON, {}) or {}
    expected_status = "CONFIRMED_ARTICLE_INGESTION_COMPLETE_PUBLICATION_DISCOVERY_INCOMPLETE"
    if summary.get("status") != expected_status:
        errors.append(f"Campaign status must distinguish confirmed ingestion from incomplete discovery: {summary.get('status')}")
    if summary.get("confirmed_article_ingestion_status") != "COMPLETE":
        errors.append("Confirmed-article ingestion is not marked COMPLETE")
    if summary.get("publication_discovery_status") != "INCOMPLETE":
        errors.append("Publication discovery must remain INCOMPLETE")
    if summary.get("confirmed_articles_by_year", {}).get("2020") != 0:
        errors.append("Summary must record zero confirmed 2020 articles")
    if summary.get("urls_included") != len(included) or summary.get("successful_retrievals") != len(included):
        errors.append(
            "Confirmed article set must reconcile between manifest inclusion and successful retrievals "
            f"({len(included)} manifest records, {summary.get('urls_included')} summarized inclusions, "
            f"{summary.get('successful_retrievals')} successful retrievals)"
        )
    if summary.get("review_candidates_adjudicated") != review_candidates_received:
        errors.append(
            "Summary does not reconcile the adjudication ledger's received-candidate count "
            f"({summary.get('review_candidates_adjudicated')} summarized, {review_candidates_received} ledgered)"
        )
    if campaign_manifest.get("status") != expected_status:
        errors.append("Campaign manifest contains a corpus-level COMPLETE or inconsistent status")
    checks["corpus_status_boundary"] = {
        "confirmed_article_ingestion_status": summary.get("confirmed_article_ingestion_status"),
        "publication_discovery_status": summary.get("publication_discovery_status"),
        "confirmed_2020": summary.get("confirmed_articles_by_year", {}).get("2020"),
    }

    determinism = read_json(OPS / "determinism-report.json", {}) or {}
    current_fingerprint = normalized_output_fingerprint()
    expected_fingerprint = determinism.get("after_sha256")
    if not determinism.get("match") or expected_fingerprint != current_fingerprint:
        errors.append(
            "Deterministic normalized-output fingerprint does not match the verified cached-rerun baseline"
        )
    checks["deterministic_outputs"] = {
        "verified_rerun_match": bool(determinism.get("match")),
        "expected_sha256": expected_fingerprint,
        "current_sha256": current_fingerprint,
        "match": expected_fingerprint == current_fingerprint,
    }

    status = repository_changed_paths()
    prohibited = []
    allowed_prefixes = (
        "archive/raw/medium/star-atlas/",
        "archive/normalized/medium/star-atlas/",
        "archive/source-records/medium/star-atlas/",
        "archive/ingestion-packages/star-atlas-medium/",
        f"archive/manifests/{CAMPAIGN_ID}.json",
        f"archive/campaign-summaries/{CAMPAIGN_ID}/",
        f"operations/campaigns/{CAMPAIGN_ID}/",
        "operations/tests/star_atlas_medium/",
        ".github/workflows/",
        "operations/ci/",
    )
    for path in status:
        if not any(path.startswith(prefix) for prefix in allowed_prefixes):
            prohibited.append(path)
    if prohibited:
        errors.append(f"Prohibited or unrelated paths changed: {sorted(set(prohibited))}")
    checks["scope"] = {"changed_paths": len(status), "prohibited": sorted(set(prohibited))}

    base_name = os.environ.get("GITHUB_BASE_REF", "main")
    diff_worktree = subprocess.run(["git", "diff", "--check"], cwd=REPO_ROOT, capture_output=True, text=True)
    diff_committed = subprocess.run(["git", "diff", "--check", f"origin/{base_name}...HEAD"], cwd=REPO_ROOT, capture_output=True, text=True)
    if diff_worktree.returncode or (diff_committed.returncode and (REPO_ROOT / ".git").exists()):
        errors.append(f"git diff --check failed: {diff_worktree.stdout or diff_worktree.stderr}{diff_committed.stdout or diff_committed.stderr}")
    checks["git_diff_check"] = diff_worktree.returncode == 0 and diff_committed.returncode == 0

    report_core = {
        "campaign_id": CAMPAIGN_ID,
        "result": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "documented_external_warning": (
            "operations/migrations/validate_wave_1_5.py contains hard-coded legacy artifact counts and is not an additive-campaign gate."
        ),
    }
    report_digest = sha256_bytes(json.dumps(report_core, ensure_ascii=False, sort_keys=True).encode())
    previous_report = read_json(VALIDATION_JSON, {}) or {}
    validated_at = previous_report.get("validated_at") if previous_report.get("validation_content_sha256") == report_digest else now_iso()
    report = {**report_core, "validated_at": validated_at, "validation_content_sha256": report_digest}
    write_json(VALIDATION_JSON, report)
    lines = [
        "# Official Star Atlas Medium Validation Report",
        "",
        f"**Result: {report['result']}**",
        "",
        f"- Included records: {len(included)}",
        f"- Successfully validated artifact sets: {success_count}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
        "## Checks",
        "",
        "```json",
        json.dumps(checks, ensure_ascii=False, indent=2, sort_keys=True),
        "```",
    ]
    if errors:
        lines += ["", "## Errors", ""] + [f"- {item}" for item in errors]
    if warnings:
        lines += ["", "## Warnings", ""] + [f"- {item}" for item in warnings]
    lines += ["", "## Preserved legacy warning", "", f"- {report['documented_external_warning']}"]
    write_text(VALIDATION_MD, "\n".join(lines))
    print(f"Validation {report['result']}: {len(errors)} errors, {len(warnings)} warnings")
    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("discover", "adjudicate", "retrieve", "validate"))
    args = parser.parse_args()
    if args.command == "discover":
        return discover()
    if args.command == "retrieve":
        return retrieve()
    if args.command == "adjudicate":
        return adjudicate()
    return validate()


if __name__ == "__main__":
    raise SystemExit(main())
