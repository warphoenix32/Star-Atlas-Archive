# Discord Community Indexing 001

This campaign builds a deterministic local discovery index from the repository's primary-source Discord exports. It inventories every supported file below `archive/raw` or `archive/normalized` whose path contains `discord`, parses those exports, collapses duplicate messages while retaining all provenance paths, and emits evidence-linked identity, guild, and relationship records. It does not promote records into `knowledge/` or `graph/`.

## Evidence policy

- Discord messages are primary evidence for community handles and guild relationships.
- Every claim carries the archive `source_id`, Discord identifiers when available, timestamp, display name, source paths, and an exact quoted excerpt.
- Missing message, channel, or author IDs remain `null`; archive IDs are never relabeled as Discord IDs.
- Name similarity alone never merges identities. Guild tags such as `[AEP]` are recorded as low-confidence inferred membership.
- Leadership and founder promotion requires direct self-identification or at least two independently authored references.
- Guild renames, mergers, splits, and successor statements are retained as dated relationship events when explicitly stated.
- Only public handles and community roles already present in the archive are indexed.

## Build, validate, and search

From the repository root:

```powershell
python operations/campaigns/discord-community-indexing-001/build_index.py build
python operations/campaigns/discord-community-indexing-001/validate_campaign.py
python operations/campaigns/discord-community-indexing-001/build_index.py search "AEP"
python operations/campaigns/discord-community-indexing-001/build_index.py search "Funcraker" --threshold 0.70
```

The search command supports exact canonical names, aliases and abbreviations, substring matching, and fuzzy matching. All build dependencies are in the Python standard library; validation uses the repository's existing `pytest` workflow.

## Outputs

- `source-inventory.json`: file-level raw and normalized export inventory with digests and parse counts.
- `alias-registry.json`: seeded canonical names, aliases, conflict-aware status, and primary evidence.
- `identity-index.jsonl`: public handles, observed variants, roles, dates, confidence, and evidence.
- `guild-index.jsonl`: seeded guild records, aliases, dates, relationships, and evidence.
- `relationship-index.jsonl`: dated membership, role, competition, and guild-transition claims.
- `promotion-candidates.json`: evidence-weighted candidates; message volume is not scored.
- `conflict-report.json`: fuzzy-name conflicts, missing source identifiers, and no-merge policy.
- `research-backlog.json`: unresolved identities and evidence acquisition needs.
- `validation-report.json`: claim resolution, alias, ID, dating, deduplication, parse, determinism, test, and whitespace checks.

Regeneration is intentionally review-gated. The campaign does not modify canonical knowledge or graph files.
