---
title: "Official Discord Announcements Profile"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
canonical_entity: SOURCE-STAR-ATLAS-DISCORD-ANNOUNCEMENTS
aliases:
  - "Star Atlas Discord announcements"
  - "Official Star Atlas announcement channel export"
first_seen: 2021-03-16
last_reviewed: 2026-07-17
source_priority:
  - A2
  - C1
related_entities:
  - Star Atlas
  - ATMTA
depends_on:
  - archive/raw/discord-announcements/star-atlas-discord-announcements.md
  - archive/semantic/discord-announcements/announcement-semantic-records.jsonl
supersedes: []
superseded_by: []
evidence_basis:
  - "operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json"
  - "operations/campaigns/discord-announcements-semantic-enrichment/validation-report.json"
  - "operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json"
known_limitations:
  - "The export header states that collection was incomplete at acquisition, although it is the total available export supplied to the repository."
  - "Author grouping was inferred from the export structure and is not independently verified."
  - "Attachment binaries were not supplied."
research_gaps:
  - "Reconstruct stricter event sequences using shared event identifiers and bounded temporal adjacency."
  - "Corroborate promotion candidates claim by claim against independent source records."
review_after: 2027-01-17
---

# Official Discord Announcements Profile

The preserved Discord announcement export is a high-value chronological record of messages collected from an official Star Atlas announcement surface. Its strongest use is to establish that particular text appeared in the captured channel at a recorded time. It is neither a complete history of Star Atlas communications nor, because of the acquisition warning, a demonstrably complete history of the channel itself. Export-derived author labels identify how messages were grouped in the supplied file; they do not independently prove personal authorship.

## Scope and provenance

The repository preserves the supplied conversation export as a raw Markdown artifact. Its header identifies the platform as Discord, records an export time of July 15, 2026, lists 1,071 messages, and explicitly states `Collection complete: no`. The accompanying warning says the historical acquisition reached its 180-minute runtime limit before the requested start time. The archive therefore describes the artifact as the **complete supplied export**, not as a complete channel capture.

Each normalized message is linked to a stable `SA-DISCORD-ANN-*` source record. The record retains the sequence position, timestamp, export-derived author label, content checksum, raw and normalized collection paths, and the collection/authorship warning. Semantic records and their inclusion or exclusion decisions are derived research aids; the raw export and matching source record remain the evidentiary anchor.

## Preserved corpus

The validated corpus contains 1,071 unique messages covering 2021-03-16 through 2026-07-12. Every message has a stable source record and complete promotion and timeline decision coverage. The enrichment layer retains 148 single-source promotion candidates, 136 timeline candidates, 30 duplicate clusters, 31 security-alert records, and 70 incident-or-resolution records. It excludes 923 messages from promotion and 935 from the timeline candidate layer. These exclusions increase candidate precision without removing the underlying message from the archive. [Campaign summary](../../operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json) [Campaign validation](../../operations/campaigns/discord-announcements-semantic-enrichment/validation-report.json)

The user designates the supplied export as the total available announcements corpus. The export itself says `Collection complete: no`; therefore the archive can be described as the complete supplied or available export, not as proof that no announcement is missing.

## Review corrections

The first deterministic pass grouped 24 broad event sequences and placed 148 Discord candidates in a cross-source promotion queue. Curator review withdrew both overstatements. The corrected record contains zero accepted event sequences pending stricter identity-based clustering and zero cross-source promotion records pending an explicit second source. The 148 Discord-only candidates remain available for review. [Review corrections](../../operations/campaigns/discord-announcements-semantic-enrichment/REVIEW-CORRECTIONS.md) [Correction status](../../operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json)

This correction is methodologically important: temporal proximity and similar vocabulary do not by themselves prove that messages describe the same event, and the existence of a linked URL does not itself constitute corroboration. The correction record also states that contradiction review was not exhaustively performed by a human reviewer.

## Authority and attribution

- Preserved announcement text may be treated as A2 evidence of what the official channel published when channel provenance is clear.
- The export's grouped author name is C1 unless independently reconciled to another record.
- A linked article, video, or attachment is not preserved merely because its URL appears in a message.
- An announcement is not a release; a security alert is not a resolution; a vote notice is not a vote result; and an event notice is not evidence that the event occurred.
- Candidate confidence measures extraction quality, not factual truth.

## Completeness and preservation boundaries

The capture does not establish that deleted messages, earlier channel history, thread replies, reactions, edits, embeds, or attachment binaries were preserved. Participant labels in the export include deleted and role-formatted accounts, and identity should not be normalized to a person without separate evidence. Links remain discovery leads unless their destination content is independently archived. Absence from this corpus must never be used to claim that Star Atlas made no announcement elsewhere or at another time.

The collection is also a publication record, not an execution ledger. For example, a message saying that a launch is planned is evidence of the plan and its publication date. Confirmation that the launch occurred requires a later operational, release, transaction, or independently preserved first-party record.

## Recommended research use

Use the corpus for dated announcement discovery, incident chronology, corrections, release and test leads, governance notices, and links to underlying publications. Before promoting a material claim:

1. resolve the `SA-DISCORD-ANN-*` identifier to its source record and exact message;
2. preserve the timestamp, export-derived attribution, and completeness warning;
3. classify the statement state precisely, such as announcement, planned test, release, delay, correction, vote notice, or vote result;
4. inspect later messages for corrections or supersession; and
5. reconcile delivery, payment, implementation, or event occurrence claims with a source capable of establishing that later state.

Discord may corroborate a newsroom, X, PIP, support, transaction, or product record only when both records independently express the material claim. Repetition within the same official communications system should be documented as cross-surface publication, not automatically counted as independent corroboration.

## Evidence references

- [Raw supplied export](../../archive/raw/discord-announcements/star-atlas-discord-announcements.md)
- [Semantic announcement records](../../archive/semantic/discord-announcements/announcement-semantic-records.jsonl)
- [Promotion decisions](../../archive/semantic/discord-announcements/promotion-candidate-decisions.jsonl)
- [Timeline decisions](../../archive/semantic/discord-announcements/timeline-candidate-decisions.jsonl)
