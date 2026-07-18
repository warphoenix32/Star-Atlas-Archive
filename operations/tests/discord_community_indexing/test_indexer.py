import csv
import importlib.util
import json
from pathlib import Path
import sys


MODULE_PATH = Path(__file__).parents[2] / "campaigns" / "discord-community-indexing-001" / "build_index.py"
SPEC = importlib.util.spec_from_file_location("discord_community_index", MODULE_PATH)
indexer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = indexer
SPEC.loader.exec_module(indexer)


def test_parses_supported_structured_formats(tmp_path):
    root = tmp_path
    base = root / "archive" / "raw" / "discord-test"
    base.mkdir(parents=True)
    record = {"message_id": "1", "channel_id": "2", "author": {"id": "3", "username": "Alpha"}, "timestamp": "2025-01-01T00:00:00Z", "content": "hello"}
    (base / "messages.json").write_text(json.dumps({"messages": [record]}), encoding="utf-8")
    (base / "messages.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
    with (base / "messages.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["message_id", "channel_id", "author_id", "author", "timestamp", "content"])
        writer.writeheader()
        writer.writerow({"message_id": "4", "channel_id": "2", "author_id": "3", "author": "Alpha", "timestamp": "2025-01-02T00:00:00Z", "content": "csv"})
    messages, inventory = indexer.load_messages(root)
    assert len(messages) == 2  # JSON and JSONL copies collapse, CSV remains.
    copied = next(message for message in messages if message.message_id == "1")
    assert len(copied.source_paths) == 2
    assert copied.author_id == "3"
    assert len(inventory) == 3


def test_parses_markdown_text_and_html(tmp_path):
    root = tmp_path
    base = root / "archive" / "raw" / "discord-test"
    base.mkdir(parents=True)
    (base / "chat.md").write_text("### Alpha\n1/2/2025, 3:04:05 PM\n\nI am the founder of Guild One.\n\n---\n", encoding="utf-8")
    (base / "chat.html").write_text('<article class="message" data-message-id="9" data-channel-id="8" data-author-id="7"><span class="author">Beta</span><time datetime="2025-01-03T00:00:00Z"></time><div class="content">Hello HTML</div></article>', encoding="utf-8")
    messages, _ = indexer.load_messages(root)
    assert {message.display_name for message in messages} == {"Alpha", "Beta"}
    html_message = next(message for message in messages if message.display_name == "Beta")
    assert (html_message.message_id, html_message.channel_id, html_message.author_id) == ("9", "8", "7")


def test_does_not_merge_fuzzy_names_without_evidence(tmp_path):
    root = tmp_path
    base = root / "archive" / "normalized" / "discord-test"
    base.mkdir(parents=True)
    records = [
        {"source_id": "a", "author": "Bohdi", "timestamp": "2025-01-01T00:00:00", "content": "hello"},
        {"source_id": "b", "author": "Bodhi", "timestamp": "2025-01-02T00:00:00", "content": "hello"},
    ]
    (base / "messages.jsonl").write_text("".join(json.dumps(item) + "\n" for item in records), encoding="utf-8")
    messages, _ = indexer.load_messages(root)
    aliases, _ = indexer.build_alias_registry(messages)
    identities, _, _ = indexer.build_indexes(messages, aliases)
    observed = {record["canonical_handle"] for record in identities if record["canonical_handle"] in {"Bohdi", "Bodhi"}}
    assert observed == {"Bohdi", "Bodhi"}


def test_relationship_claims_resolve_and_are_dated(tmp_path):
    root = tmp_path
    base = root / "archive" / "normalized" / "discord-test"
    base.mkdir(parents=True)
    record = {
        "source_id": "council-1", "author": "Official", "timestamp": "2025-03-14T12:00:00",
        "content": "The first Council served six months:\n@[AEP] Funcracker\nMentions: @[AEP] Funcracker",
    }
    (base / "messages.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
    messages, inventory = indexer.load_messages(root)
    aliases, _ = indexer.build_alias_registry(messages)
    identities, guilds, relationships = indexer.build_indexes(messages, aliases)
    report = indexer.validate_outputs(messages, aliases, identities, guilds, relationships, inventory)
    assert report["status"] == "pass"
    assert any(rel["predicate"] == "served_as" and rel["valid_at"] for rel in relationships)


def test_build_is_deterministic_and_searches_aliases(tmp_path):
    root = tmp_path / "repo"
    base = root / "archive" / "normalized" / "discord-test"
    base.mkdir(parents=True)
    (base / "messages.jsonl").write_text(json.dumps({"source_id": "x", "author": "Official", "timestamp": "2025-01-01T00:00:00", "content": "Aephia won. Mentions: @[AEP] Funcracker"}) + "\n", encoding="utf-8")
    first = indexer.build(root)
    second = indexer.build(root)
    assert first == second
    output = tmp_path / "out"
    indexer.write_outputs(root, output)
    assert indexer.search(output, "AEP", 0.72)[0]["name"] == "Aephia"
