# Ingestion Schema v2.1

## Purpose

Schema v2.1 strengthens traceability, entity semantics, lifecycle tracking, and evidence preservation while remaining backward compatible with v2.0 ingestion packages.

## Three-artifact ingestion model

Every transcript-based source should produce three distinct artifacts:

1. **Raw transcript** — immutable source evidence. Preserve wording, uncertainty, speaker boundaries, timestamps, and transcription defects.
2. **Normalized transcript** — corrected terminology, resolved speakers, and standardized names without summarization or semantic deletion.
3. **Repository extraction package** — structured claims, events, entities, relationships, evidence, knowledge deltas, and research tasks.

The raw transcript is never overwritten by normalization or extraction.

## Provenance

Claims, events, quotes, relationships, and timeline updates may include:

```json
{
  "provenance": {
    "source_id": "SRC-...",
    "speaker": "PERSON-...",
    "timestamp_start": null,
    "timestamp_end": null,
    "speaker_confidence": "HIGH",
    "timestamp_confidence": "UNKNOWN",
    "extraction_confidence": "HIGH"
  }
}
```

Use `null` and `UNKNOWN` when timestamps or speaker attribution cannot be reliably resolved. Never invent provenance.

## Typed entities

Entities support:

```json
{
  "entity_id": "ENT-...",
  "canonical_name": "...",
  "entity_type": "PERSON",
  "aliases": [],
  "role": null,
  "resolution_confidence": "HIGH"
}
```

Supported entity types include:

- PERSON
- ORGANIZATION
- DAO
- CORPORATION
- TOKEN
- FEATURE
- TECHNOLOGY
- GAME_SYSTEM
- GAME_MODE
- SHIP
- LOCATION
- RESOURCE
- EVENT
- DOCUMENT
- PRODUCT
- COMMUNITY
- GUILD

## Stable identifiers

Existing identifiers remain valid. New records should use deterministic, globally stable identifiers. A future migration may map legacy IDs to typed IDs such as `PERSON-000041` or `ORG-000008`, but existing IDs must not be rewritten without an explicit migration table.

## Lifecycle status

Claims and events may use:

- ANNOUNCED
- PLANNED
- IN_DEVELOPMENT
- IN_TESTING
- RELEASED
- LIVE
- DEPRECATED
- CANCELLED
- SUPERSEDED

Status changes create new evidence-backed records; they do not erase prior states.

## Evidence

Claims, events, and relationships may include an evidence array:

```json
{
  "evidence": [
    {
      "type": "TRANSCRIPT_REFERENCE",
      "source_id": "SRC-...",
      "timestamp_start": null,
      "timestamp_end": null,
      "excerpt": null
    }
  ]
}
```

Evidence supplements summaries. Excerpts must remain short and exact.

## Entity cross-references

Claims, events, timeline updates, and research tasks may include `related_entities` containing canonical entity IDs.

## Confidence

Confidence is independently recorded for:

- extraction
- entity resolution
- speaker identification
- timestamp resolution
- relationship classification

Allowed values: `HIGH`, `MEDIUM`, `LOW`, `UNKNOWN`.

## Backward compatibility

A valid v2.0 package remains valid repository evidence. v2.1 fields are additive. Readers must tolerate absent v2.1 fields and treat them as unknown rather than false.

## Promotion rule

Ingestion packages are evidence artifacts. They must not directly rewrite canonical timeline, actor, guild, lore, product, or governance records without an audited promotion step.