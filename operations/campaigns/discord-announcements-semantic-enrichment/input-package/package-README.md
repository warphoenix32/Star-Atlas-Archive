# Star Atlas Discord Announcements Semantic Enrichment

## Scope

This package preserves and semantically enriches the user-designated complete Star Atlas Discord announcements corpus.

- Messages: **1,071**
- Date range: **2021-03-16 to 2026-07-12**
- Unique source IDs: **1,071**
- Promotion candidates: **454**
- Timeline candidates: **284**
- Entity links: **1,233**
- Security alerts: **31**
- Incident/resolution records: **70**

## Semantic schema

Each message includes:

- stable source ID and sequence;
- author and timestamp;
- preserved message text, links, attachments, and metadata;
- topics and entities;
- statement types;
- lifecycle states;
- evidence classes;
- confidence;
- promotion-candidate decision;
- timeline-candidate decision.

## Controlled topics

`PRODUCT`, `ASSET_RELEASE`, `GOVERNANCE`, `ECONOMY`, `TECHNOLOGY`, `LORE`,
`CORPORATE`, `COMMUNITY`, `EVENT`, `SECURITY`, `OPERATIONS`, `MARKETING`, `GENERAL`.

## Statement distinctions

The enrichment distinguishes:

- announcement from release;
- roadmap or forward-looking language from live availability;
- incident from resolution;
- governance update from implementation;
- correction or clarification from the original claim;
- security advisory from ordinary announcements.

## Canonical-use boundary

The complete semantic index is a research layer. `promotion-candidates.json` and
`timeline-candidates.json` are review queues, not canonical facts. Every included candidate
retains the complete supporting announcement text and source ID.

## Provenance limitations

The original export header states `Collection complete: no` because the exporter reached its
historical runtime limit. The user has confirmed that the earliest message in the export marks
the beginning of the announcement channel and has designated this corpus as the totality of
Star Atlas Discord announcements. This designation is preserved as user-supplied corpus scope,
not independently proven platform completeness.

Attachments were not downloaded. Author-inferred grouping metadata is preserved but not
treated as verified authorship.
