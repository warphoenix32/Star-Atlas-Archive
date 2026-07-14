# Schema v2.1 Migration Notes

## Migration principle

Wave 1 records are historical artifacts. Migration is additive and non-destructive. Do not rewrite raw transcripts, delete legacy fields, or replace legacy IDs without preserving an alias.

## Reader compatibility

Consumers should normalize records at read time:

| v2.0 field | v2.1 interpretation |
|---|---|
| `metadata.repository_schema: "2.0"` | valid legacy package |
| entity `name` | `canonical_name` fallback |
| scalar `confidence` | overall confidence fallback |
| object-level `source_id`, `speaker`, `timestamp` | may be mapped into `provenance` |
| absent `evidence` | evidence was not separately captured |
| absent `related_entities` | relationships were not explicitly resolved |

## Writer behavior

- New extraction packages use schema `2.1`.
- Existing v2.0 packages remain unchanged unless they are otherwise being curated.
- A curated migration may add v2.1 fields while retaining all v2.0 fields.
- Migration tooling must be idempotent.

## Canonical ID migration

1. Inventory existing entity IDs and names.
2. Resolve duplicates through the Entity and Alias registries.
3. Allocate the next registry-controlled canonical ID for each unique entity.
4. Preserve the previous identifier in `legacy_ids`.
5. Update new records to use canonical IDs.
6. Do not bulk-rewrite historical source artifacts solely to change identifiers.

Example:

```json
{
  "entity_id": "PERSON-000001",
  "legacy_ids": ["ACTOR-MICHAEL-WAGNER"],
  "canonical_name": "Michael Wagner",
  "entity_type": "PERSON"
}
```

## Lifecycle migration

Legacy statuses should be preserved. When a clear mapping exists, readers may interpret:

| Legacy | v2.1 |
|---|---|
| `ACTIVE` | `LIVE` |
| `PLANNED` | `PLANNED` |
| `DEPRECATED` | `DEPRECATED` |
| `CANCELLED` | `CANCELLED` |
| `COMPLETE` | `RELEASED` or domain-specific completion, subject to review |
| `UNKNOWN` | no inferred status |

Do not infer `RELEASED` or `LIVE` solely from an announcement.

## Provenance migration

When legacy fields are available, construct provenance without deleting the originals:

```json
{
  "source_id": "SRC-001",
  "speaker": "Michael Wagner",
  "timestamp": "00:12:20",
  "provenance": {
    "source_id": "SRC-001",
    "speaker": "Michael Wagner",
    "timestamp_start": "00:12:20",
    "timestamp_end": "",
    "confidence": 1.0
  }
}
```

## Rollout

- Phase 1: documentation, examples, validators, and dual-version support.
- Phase 2: new ingestions emit v2.1 by default.
- Phase 3: opportunistic enrichment of high-value Wave 1 artifacts.
- Phase 4: canonical ID registry adoption after duplicate review.

No phase requires destructive conversion of Wave 1 artifacts.
