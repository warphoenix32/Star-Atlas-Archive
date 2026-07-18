---
title: "Official Star Atlas X Account Profile"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: SOURCE-STAR-ATLAS-X
aliases:
  - "@staratlas"
  - "Official Star Atlas Twitter account"
first_seen: 2024-11-05
last_reviewed: 2026-07-17
source_priority:
  - A2
related_entities:
  - Star Atlas
  - ATMTA
depends_on:
  - archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv
  - archive/semantic/social-media/staratlas-posts-semantic.jsonl
supersedes: []
superseded_by: []
evidence_basis:
  - "operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json"
  - "operations/campaigns/social-governance-semantic-enrichment/validation-report.json"
known_limitations:
  - "The supplied collection begins in November 2024 and is not presented as the account's complete lifetime history."
  - "Linked media binaries were not included in the source package."
  - "Retweets prove official resharing, not first-party authorship of the underlying claim."
research_gaps:
  - "Recover earlier account history and linked media."
  - "Reconcile high-value posts with newsroom, Discord, release, and governance records."
review_after: 2027-01-17
---

# Official Star Atlas X Account Profile

The preserved `@staratlas` collection is a dated record of activity from an official Star Atlas social account. It is useful for announcement discovery, terminology, corrections, and public positioning during the captured period. Original account posts and retweets have materially different provenance and evidentiary meaning, so the archive preserves and evaluates them separately.

## Scope and provenance

The raw input is a CSV export containing post IDs, account and handle labels, text, engagement fields, dates, URLs, and a retweet flag. The campaign reports 799 raw rows reconciled to 796 unique posts. Stable `SRC-X-STARATLAS-*` source records preserve the platform post ID, publication date, canonical post URL, original-versus-retweet status, evidence tier, and raw/normalized collection paths.

Engagement counts are point-in-time observations from the export, not permanent attributes of a post. Linked images and other media were not downloaded. The source package therefore preserves post text and metadata but may not preserve claims communicated only through an image, video, quote-post rendering, or other linked object.

## Preserved corpus

The validated collection contains 796 unique posts dated 2024-11-05 through 2026-07-14: 528 original account posts and 268 retweets. The precision review retained 28 promotion candidates and 26 timeline candidates, while recording 25 duplicate clusters. It excluded 768 posts from promotion and 770 from timeline candidacy. Candidate reduction preserves the full post corpus while preventing generic marketing, questions, weak lexical matches, retweets, and weaker duplicates from entering higher-trust research queues. [Campaign summary](../../operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json) [Validation report](../../operations/campaigns/social-governance-semantic-enrichment/validation-report.json)

Of the 28 retained promotion candidates, seven are high-confidence and 21 medium-confidence extraction records. The timeline set contains four high-confidence and 22 medium-confidence extraction records. Those labels measure the quality and specificity of the extracted candidate, not the independent truth of its claim.

This date range describes the supplied archive, not the full lifetime of the account. Absence of an earlier post from the collection is not evidence that it was never published.

The campaign summary still carries a stale overall `FAIL` field from an earlier packaging state, while the final validation report records `PASS`. This profile relies on the reconciled counts and final validator result and preserves the discrepancy for operational follow-up rather than silently rewriting campaign artifacts.

## Authority boundary

- An original `@staratlas` post is A2 evidence of what the official account stated on its publication date.
- A retweet is evidence that the official account reshared another source. It does not convert the underlying author's statement into a first-party Star Atlas claim.
- A post announcing a product, partnership, test, vote, or event does not establish delivery, outcome, result, or occurrence.
- A repeated marketing post is not independent corroboration of an earlier claim.
- Candidate confidence describes extraction quality rather than truth.

An original post is first-party publication evidence, but its subject determines what else is required. It can establish the wording and timing of an announcement. It cannot, without further evidence, establish that a roadmap item was delivered, a partnership achieved an outcome, a vote passed, funds moved, an event occurred, or a production system became available. A post that links to a longer publication should be cited alongside the preserved destination record when the knowledge claim depends on details contained only there.

## Completeness and identity boundaries

The collection begins in November 2024 and is not represented as the account's complete lifetime history. Deleted posts, edits, replies outside the export, quote-post context, and earlier account activity may be absent. The account and handle labels recorded by the export identify the publishing account; they do not establish which employee drafted a post. No personal authorship should be inferred.

The 268 retweets remain valuable for studying what the official account chose to amplify. For claim provenance, however, the original creator remains the primary author and must be retained. Official resharing is contextual evidence, not transfer of authorship or automatic endorsement of every proposition in the reshared material.

## Research use

The corpus is appropriate for locating first public mentions **within the captured period**, official terminology, announcement timing, corrections, and links to longer-form material. A rigorous citation should preserve the `SRC-X-STARATLAS-*` identifier, exact publication date, post URL, original/retweet status, and any relevant duplicate-cluster context. Researchers should inspect adjacent or later posts for corrections, delays, changed dates, or superseding announcements.

Where a claim concerns release, deployment, payment, execution, vote outcome, or event occurrence, cite a separate release, deployment, transaction, governance, or operational source. A matching Discord or newsroom announcement demonstrates repeated official publication; it should not be described as independent corroboration unless the second record carries distinct evidence of the claimed state.

## Evidence references

- [Raw social export](../../archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv)
- [Semantic post records](../../archive/semantic/social-media/staratlas-posts-semantic.jsonl)
- [Promotion decisions](../../archive/semantic/social-media/promotion-candidate-decisions.jsonl)
- [Timeline decisions](../../archive/semantic/social-media/timeline-candidate-decisions.jsonl)
