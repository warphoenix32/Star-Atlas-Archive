from star_atlas_ingest.inventory import flatten_inventory


def test_flatten_deduplicates_and_preserves_provenance():
    document = {"creators": [{
        "canonical_name": "HNN",
        "aliases": ["The Hologram"],
        "classification": {"role": "ORIGINAL_REPORTER", "priority": 1},
        "platforms": {"website": {"urls": [
            {"url": "https://example.com/story?utm_source=a", "provenance_occurrences": [{"posted_at": "2024-02-01T00:00:00Z"}]},
            {"url": "https://example.com/story/", "provenance_occurrences": [{"posted_at": "2024-01-01T00:00:00Z"}]},
        ]}},
    }]}
    records = flatten_inventory(document)
    assert len(records) == 1
    assert records[0]["processing_status"] == "PENDING"
    assert records[0]["first_discord_posted_at"] == "2024-01-01T00:00:00Z"
    assert len(records[0]["provenance_occurrences"]) == 2


def test_audiovisual_content_is_retained_as_deferred_metadata():
    document = {"creators": [{
        "canonical_name": "HNN", "aliases": [], "classification": {},
        "platforms": {"youtube": {"urls": [{"url": "https://youtu.be/abc", "provenance_occurrences": []}]}},
    }]}
    assert flatten_inventory(document)[0]["processing_status"] == "DEFERRED"
