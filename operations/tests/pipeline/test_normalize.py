from star_atlas_ingest.normalize import canonicalize_url


def test_removes_tracking_and_fragment_and_sorts_query():
    assert canonicalize_url("https://Example.com/post/?utm_source=x&b=2&a=1#section") == "https://example.com/post?a=1&b=2"


def test_normalizes_youtube_variants():
    expected = "https://www.youtube.com/watch?v=abc123"
    assert canonicalize_url("https://youtu.be/abc123?si=tracking") == expected
    assert canonicalize_url("https://youtube.com/live/abc123?t=8") == expected


def test_does_not_merge_http_and_https_without_evidence():
    assert canonicalize_url("http://example.com/a") != canonicalize_url("https://example.com/a")
