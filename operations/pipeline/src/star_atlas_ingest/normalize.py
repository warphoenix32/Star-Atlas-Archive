"""URL canonicalization with conservative, platform-aware rules."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "source"}
YOUTUBE_KEYS = {"feature", "si", "t", "time_continue", "start", "lc"}


def canonicalize_url(value: str) -> str:
    """Return a canonical URL without collapsing distinct content pages."""
    parts = urlsplit(value.strip())
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    if not scheme or not host:
        raise ValueError(f"absolute HTTP(S) URL required: {value!r}")
    if scheme not in {"http", "https"}:
        raise ValueError(f"unsupported URL scheme: {scheme}")

    if host in {"youtu.be", "youtube.com", "www.youtube.com", "m.youtube.com"}:
        if host == "youtu.be":
            video_id = parts.path.strip("/")
        else:
            query = dict(parse_qsl(parts.query, keep_blank_values=True))
            video_id = query.get("v", "")
            if parts.path.startswith(("/live/", "/shorts/")):
                video_id = parts.path.split("/", 2)[2]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    port = parts.port
    netloc = host if port is None else f"{host}:{port}"
    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    query = []
    for key, val in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith("utm_") or lowered in TRACKING_KEYS:
            continue
        if "youtube.com" in host and lowered in YOUTUBE_KEYS:
            continue
        query.append((key, val))
    query.sort()
    return urlunsplit((scheme, netloc, path, urlencode(query), ""))
