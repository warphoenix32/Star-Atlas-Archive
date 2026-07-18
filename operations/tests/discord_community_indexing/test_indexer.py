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


def write_jsonl(root, records):
    base = root / "archive" / "normalized" / "discord-test"
    base.mkdir(parents=True, exist_ok=True)
    (base / "messages.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records),
        encoding="utf-8",
    )


def test_author_and_timestamp_are_not_a_deduplication_key(tmp_path):
    records = [
        {"source_id": "same-time-a", "author": "Alpha", "timestamp": "2025-01-01T00:00:00", "content": "First substantive statement."},
        {"source_id": "same-time-b", "author": "Alpha", "timestamp": "2025-01-01T00:00:00", "content": "Second and distinct statement."},
    ]
    write_jsonl(tmp_path, records)
    messages, _ = indexer.load_messages(tmp_path)
    assert {message.source_id for message in messages} == {"same-time-a", "same-time-b"}


def test_representation_wrapper_reconciles_by_content_not_author_time(tmp_path):
    raw = tmp_path / "archive" / "raw" / "discord-test"
    normalized = tmp_path / "archive" / "normalized" / "discord-test"
    raw.mkdir(parents=True)
    normalized.mkdir(parents=True)
    body = "A sufficiently long institutional announcement about a named system and its status."
    (raw / "chat.md").write_text(
        f"### Official\n1/1/2025, 12:00:00 AM\n\n_Reply context:_ Earlier statement.\n\n{body}\n\n---\n",
        encoding="utf-8",
    )
    (normalized / "messages.jsonl").write_text(
        json.dumps({"source_id": "canonical", "author": "Official", "timestamp": "2025-01-01T00:00:00", "content": body + "\n\n---"}) + "\n",
        encoding="utf-8",
    )
    messages, _ = indexer.load_messages(tmp_path)
    assert len(messages) == 1
    assert messages[0].source_id == "canonical"
    assert len(messages[0].source_paths) == 2


def test_operator_confirmed_aliases_are_explicit_and_separate(tmp_path):
    write_jsonl(tmp_path, [{"source_id": "alias-1", "author": "SW4GN3R [STAR]", "timestamp": "2025-01-01T00:00:00", "content": "Official update."}])
    messages, _ = indexer.load_messages(tmp_path)
    aliases, _ = indexer.build_alias_registry(messages)
    identities, _, _ = indexer.build_indexes(messages, aliases)
    michael = next(item for item in identities if item["canonical_handle"] == "Michael Wagner")
    assert michael["record_type"] == "resolved_person_identity"
    assert "SW4GN3R [STAR]" in michael["confirmed_aliases"]
    confirmation = michael["operator_confirmations"][0]
    assert confirmation["source_id"] is None
    assert confirmation["evidence_channel"] == "operator_confirmation"
    assert confirmation["operator_assertion"] is True


def test_observed_authorship_is_not_mislabeled_third_party(tmp_path):
    write_jsonl(tmp_path, [{"source_id": "authored-1", "author": "Alpha", "timestamp": "2025-01-01T00:00:00", "content": "I am speaking."}])
    messages, _ = indexer.load_messages(tmp_path)
    aliases, _ = indexer.build_alias_registry(messages)
    identities, _, _ = indexer.build_indexes(messages, aliases)
    alpha = next(item for item in identities if item["canonical_handle"] == "Alpha")
    assert {ref["attribution_class"] for ref in alpha["evidence"]} == {"observed_authorship"}
    assert alpha["record_type"] == "observed_handle_cluster"


def test_tag_context_keeps_alliance_meme_and_pipe_guild_distinct(tmp_path):
    write_jsonl(tmp_path, [{
        "source_id": "tags-1", "author": "Official", "timestamp": "2025-01-01T00:00:00",
        "content": "Mentions: @[IA] Dodger | BULK and @[426] MemeUser and @[SAI] ItaliaUser",
    }])
    messages, _ = indexer.load_messages(tmp_path)
    aliases, _ = indexer.build_alias_registry(messages)
    _, _, relationships = indexer.build_indexes(messages, aliases)
    simplified = {(item["subject_name"], item["predicate"], item["object_name"]) for item in relationships}
    assert ("Dodger", "associated_with_alliance", "Intergalactic Alliance") in simplified
    assert ("Dodger", "associated_with_guild", "BULK") in simplified
    assert ("MemeUser", "has_display_tag", "426") in simplified
    assert ("ItaliaUser", "associated_with_organization", "Star Atlas Italia") in simplified
    assert not any(item["predicate"] in {"member_of", "possible_member_of"} and item["object_name"] in {"426", "Intergalactic Alliance", "Star Atlas Italia", "BULK"} for item in relationships)


def test_competition_parser_does_not_make_prize_text_a_participant(tmp_path):
    write_jsonl(tmp_path, [
        {"source_id": "competition-1", "author": "Official", "timestamp": "2025-01-01T00:00:00", "content": "COPA results: 1st - Aephia"},
        {"source_id": "competition-2", "author": "Official", "timestamp": "2025-01-02T00:00:00", "content": "COPA prizes: 3rd - CSS Tier 3 ($17)"},
    ])
    messages, _ = indexer.load_messages(tmp_path)
    aliases, _ = indexer.build_alias_registry(messages)
    records, relationships, reviews = indexer.extract_competition_records(messages, aliases)
    assert any(item["participant"] == "Aephia" and item["resolution_status"] == "RESOLVED" for item in records)
    assert any(item["resolution_status"] == "REVIEW_REQUIRED_PRIZE_OR_CATEGORY" for item in records)
    assert not any("CSS Tier" in item["subject_name"] for item in relationships)
    assert any(item["review_type"] == "malformed_competition_result" for item in reviews)


def test_council_service_is_not_guild_leadership(tmp_path):
    write_jsonl(tmp_path, [{
        "source_id": "council-2", "author": "Official", "timestamp": "2025-01-01T00:00:00",
        "content": "The first Star Atlas DAO Council included @CouncilPerson.",
    }])
    messages, _ = indexer.load_messages(tmp_path)
    aliases, _ = indexer.build_alias_registry(messages)
    identities, organizations, relationships = indexer.build_indexes(messages, aliases)
    council = next(item for item in identities if item["canonical_handle"] == "CouncilPerson")
    assert "dao_council_service" in council["roles"]
    assert not set(council["roles"]) & {"guild_founder", "guild_leader", "guild_officer"}
    candidates = indexer.promotion_candidates(identities, organizations, relationships)
    entry = next(item for item in candidates["candidates"] if item["entity_id"] == council["identity_id"])
    assert entry["score_dimensions"]["dao_council_service"] == 1
    assert entry["score_dimensions"]["guild_leader"] == 0


def test_coverage_is_export_scoped_and_preserves_observed_header(tmp_path):
    raw = tmp_path / "archive" / "raw" / "discord-announcements"
    normalized = tmp_path / "archive" / "normalized" / "discord-announcements"
    raw.mkdir(parents=True)
    normalized.mkdir(parents=True)
    (raw / "star-atlas-discord-announcements.md").write_text(
        "Conversation: Compromised Discord Account of EX Team Member,\nCollection complete: no\n\n"
        "### Official\n1/1/2025, 12:00:00 AM\n\nOne message.\n\n---\n",
        encoding="utf-8",
    )
    (normalized / "messages.jsonl").write_text(
        json.dumps({"source_id": "coverage-1", "author": "Official", "timestamp": "2025-01-01T00:00:00", "content": "One message."}) + "\n",
        encoding="utf-8",
    )
    messages, inventory = indexer.load_messages(tmp_path)
    coverage, gaps, backlog = indexer.build_channel_coverage(messages, inventory)
    assert coverage["summary"]["independent_export_units"] == 1
    assert coverage["summary"]["native_servers_identified"] == 0
    assert coverage["summary"]["canonical_native_channels_identified"] == 0
    assert coverage["channels"][0]["observed_channel_names"] == ["Compromised Discord Account of EX Team Member,"]
    assert coverage["channels"][0]["coverage_status"] == "UNRESOLVED_CHANNEL"
    assert gaps["gaps"][0]["zero_message_months"] == []
    assert any(item["target"] == "Foudnation Room" for item in backlog["items"])


def test_human_queue_retains_required_seeded_unresolved_items(tmp_path):
    write_jsonl(tmp_path, [{"source_id": "queue-1", "author": "Official", "timestamp": "2025-01-01T00:00:00", "content": "Hello."}])
    messages, inventory, duplicate_reviews = indexer.load_messages(tmp_path, include_duplicate_reviews=True)
    aliases, conflicts = indexer.build_alias_registry(messages)
    identities, organizations, relationships = indexer.build_indexes(messages, aliases)
    tags = indexer.tag_registry(messages)
    coverage, _, _ = indexer.build_channel_coverage(messages, inventory)
    queue = indexer.build_human_resolution_queue(duplicate_reviews, conflicts, tags, organizations, relationships, [], coverage)
    subjects = {item["subject"] for item in queue["items"]}
    assert {"Agent Solace", "The Vanguard", "The Club Guild / The Club", "Rome", "Witticus", "ReyVeezy", "FancyHat", "Virtuwaal"} <= subjects
    assert all(item["decision_status"] == "OPEN" and item["operator_decision"] is None for item in queue["items"])


def test_repository_corpus_reconciles_all_representations():
    repo_root = MODULE_PATH.parents[3]
    messages, inventory, duplicate_reviews = indexer.load_messages(repo_root, include_duplicate_reviews=True)
    assert len(messages) == 1071
    assert all(message.source_id.startswith("SA-DISCORD-ANN-") for message in messages)
    assert not duplicate_reviews
    assert sum(item["parsed_message_occurrences"] for item in inventory if item["ingested"]) == 3213
    source_record_ids = {path.stem for path in (repo_root / "archive" / "source-records" / "discord-announcements").glob("*.json")}
    assert {message.source_id for message in messages} == source_record_ids
