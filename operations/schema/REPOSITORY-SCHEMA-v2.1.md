# Repository Schema v2.1

## Purpose

Repository Schema v2.1 is an additive evolution of v2.0 for preserving Star Atlas historical information with stronger provenance, entity typing, evidence, lifecycle tracking, and transcript normalization. Existing Wave 1 artifacts remain valid and must not be rewritten solely to conform to v2.1.

## Compatibility contract

- v2.0 packages remain accepted.
- v2.1 fields are additive unless explicitly marked required for newly generated v2.1 packages.
- Existing IDs remain valid aliases during migration.
- Historical source text and raw transcripts are immutable.
- Missing v2.1 fields in v2.0 artifacts mean `unknown` or `not captured`, not false.

## Package metadata

New v2.1 packages declare:

```json
{
  "metadata": {
    "repository_schema": "2.1",
    "artifact_type": "INGESTION_PACKAGE",
    "ingestion_id": "INGEST-..."
  }
}
```

## Provenance

Claims, events, quotes, relationships, and timeline updates support:

```json
"provenance": {
  "source_id": "SRC-...",
  "speaker": "PERSON-...",
  "timestamp_start": "00:00:00",
  "timestamp_end": "00:00:30",
  "confidence": 1.0
}
```

Rules:

- `source_id` identifies the registered source.
- `speaker` may contain a canonical entity ID or an unresolved speaker label.
- timestamps use `HH:MM:SS` when available; empty values preserve uncertainty.
- provenance confidence measures confidence in the complete provenance link.

## Entity model

```json
{
  "entity_id": "PERSON-000001",
  "canonical_name": "Michael Wagner",
  "entity_type": "PERSON",
  "aliases": [],
  "role": "CEO",
  "confidence": 1.0
}
```

Supported entity types:

- `PERSON`
- `ORGANIZATION`
- `DAO`
- `CORPORATION`
- `TOKEN`
- `FEATURE`
- `TECHNOLOGY`
- `GAME_SYSTEM`
- `GAME_MODE`
- `SHIP`
- `LOCATION`
- `RESOURCE`
- `EVENT`
- `DOCUMENT`
- `PRODUCT`
- `COMMUNITY`
- `GUILD`

For backward compatibility, readers should map v2.0 `name` to v2.1 `canonical_name` when the latter is absent.

## Stable canonical IDs

New canonical IDs use type-prefixed, zero-padded identifiers:

```text
PERSON-000001
FEATURE-000024
EVENT-000117
ORG-000008
```

ID allocation is registry-controlled. Ingestion agents must not invent permanent IDs when a registry service is unavailable. Existing semantic IDs such as `ACTOR-MICHAEL-WAGNER` remain valid and may be recorded in `legacy_ids` during migration.

## Claim lifecycle

Supported statuses:

- `ANNOUNCED`
- `PLANNED`
- `IN_DEVELOPMENT`
- `IN_TESTING`
- `RELEASED`
- `LIVE`
- `DEPRECATED`
- `CANCELLED`
- `SUPERSEDED`

Lifecycle behavior:

- status changes append new dated evidence; they do not erase prior states;
- `RELEASED` indicates an initial public release;
- `LIVE` indicates currently operating or available;
- `SUPERSEDED` requires a reference to the replacing record when known;
- uncertainty remains explicit when implementation cannot be verified.

## Evidence

Evidence supplements summaries and does not replace them.

```json
"evidence": [
  {
    "type": "quote",
    "text": "..."
  },
  {
    "type": "transcript_reference",
    "timestamp": "00:14:32"
  }
]
```

Recommended evidence types include `quote`, `transcript_reference`, `document_reference`, `message_reference`, `commit_reference`, and `on_chain_reference`.

## Related entities

Claims, events, timeline updates, and research tasks support:

```json
"related_entities": [
  "ORG-000008",
  "TOKEN-000004",
  "PERSON-000001"
]
```

References must use canonical IDs when resolved. Unresolved references remain visible and should generate research tasks when materially important.

## Confidence semantics

Confidence values range from `0.0` to `1.0` and are independent by concern:

```json
"confidence": {
  "entity_resolution": 0.98,
  "speaker_identification": 1.0,
  "relationship_extraction": 0.92,
  "claim_extraction": 0.97,
  "timestamps": 0.75
}
```

- `1.0`: directly and unambiguously supported.
- `0.8–0.99`: strong evidence with minor uncertainty.
- `0.5–0.79`: plausible but incomplete or indirect.
- below `0.5`: weak or unresolved; review is normally required.

A scalar confidence field remains accepted for v2.0 compatibility.

## Three-artifact transcript standard

```text
Raw Transcript
↓
Normalized Transcript
↓
Repository Extraction Package
```

### Raw transcript

- immutable source capture;
- preserves original ordering, errors, timestamps, and speaker labels;
- never silently corrected.

### Normalized transcript

- fixes formatting and obvious transcription artifacts without changing meaning;
- standardizes speaker labels and timestamps;
- records uncertain words and normalization notes;
- retains links back to raw source locations.

### Repository extraction package

- contains entities, claims, events, quotes, relationships, timeline updates, research tasks, tags, and evidence;
- references the normalized transcript and raw source;
- never substitutes summaries for original evidence.

## Minimum v2.1 validation

A v2.1 package must include `metadata.repository_schema = "2.1"`, `sources`, and the standard top-level extraction arrays. Extracted objects may omit optional fields when the information is genuinely unavailable, but provenance gaps should be surfaced in repository health or research tasks.
