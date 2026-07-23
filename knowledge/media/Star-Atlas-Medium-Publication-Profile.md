---
title: "Star Atlas Medium Publication Profile"
seo_title: "Official Star Atlas Medium Archive and Publication History"
seo_description: "A source-critical profile of the official Star Atlas Medium corpus: 181 confirmed articles, 2021–2025 coverage, retrieval provenance, resolved review candidates, and completeness limits."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
canonical_entity: SOURCE-STAR-ATLAS-MEDIUM
aliases:
  - "Star Atlas Medium"
  - "Official Star Atlas Medium publication"
first_seen: 2021-01-15
last_reviewed: 2026-07-23
source_priority:
  - A2
related_entities:
  - Star Atlas
  - ATMTA
depends_on:
  - archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json
  - archive/source-records/medium/star-atlas/
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json"
  - "operations/campaigns/star-atlas-medium-ingestion-2026-07/campaign-manifest.json"
  - "operations/campaigns/star-atlas-medium-ingestion-2026-07/manual-review-adjudication.json"
known_limitations:
  - "Ingestion is complete for 181 confirmed included articles, but publication-level discovery remains incomplete."
  - "All 216 campaign review candidates have terminal dispositions; deleted or unindexed stories may still be undiscovered."
  - "Current live text may contain edits made after an article's original publication."
  - "Article media is URL-referenced rather than downloaded."
research_gaps:
  - "Repeat publication-native discovery and recover deleted or unindexed stories that were not represented in the frozen campaign inventory."
  - "Reconcile article-level revisions and recover historical snapshots where current text may have changed."
review_after: 2027-01-20
---

# Star Atlas Medium Publication Profile

The official Star Atlas Medium publication is one of the archive's most substantial first-party written corpora. The repository now preserves **181 confirmed articles** published from January 2021 through October 2025. All 181 included records were retrieved and extracted successfully. That achievement is complete ingestion of the confirmed set—not proof that every article ever published by Star Atlas on Medium has been discovered.

## What the campaign preserved

The publication-native campaign separated URL discovery from retrieval. Its final frozen manifest contains 588 discovered URLs: 181 included and 407 excluded. All **216** review candidates received terminal dispositions, leaving no campaign item deferred or awaiting manual review. Every included article has a stable Source ID, raw capture, normalized record, Source Record, ingestion package, checksums, dates, author and publisher fields, links, and retrieval provenance.

| Retrieval path | Articles | Meaning |
|---|---:|---|
| Live direct HTML | 142 | Article body recovered from current public HTML |
| Live browser DOM | 1 | Browser rendering was required to recover the article |
| RSS content | 1 | Feed content was accepted only after completeness checks |
| Web-archive snapshot | 37 | An archived snapshot preserved an unavailable or historical page |

Extraction confidence is `HIGH` for 180 articles and `MEDIUM` for one. Media binaries were intentionally not downloaded; 247 article-body media references remain URL-preserved with placement metadata.

## Coverage by year

| Year | Confirmed articles ingested |
|---:|---:|
| 2020 | 0 |
| 2021 | 52 |
| 2022 | 72 |
| 2023 | 33 |
| 2024 | 12 |
| 2025 | 12 |
| 2026 | 0 |

The 2020 publication and profile surfaces were searched, but no 2020 article belonging to the official Star Atlas publication was confirmed or included. This is a coverage finding, not proof that no such article ever existed.

## Why discovery remains incomplete

Medium's year archives can expose hydration shells or incomplete rendered results. RSS covers only a recent subset, and available sitemaps are not exhaustive. Deleted or unindexed stories may remain undiscoverable when no repository link or web-archive record survives. Shortlinks and truncated historical URLs can also lose the post ID needed for deterministic identity.

The review queue now has zero unresolved items. That resolves the campaign's known candidates, but it does not transform the manifest into a complete history of the publication. A future discovery pass can still find a deleted, moved, or previously unindexed article and should append it through a new campaign rather than silently changing the frozen 2026-07 inventory.

## Publisher and author identity

An article belongs to the official Star Atlas publication only when captured page evidence establishes that membership. The individual author remains a separate field. A Star Atlas profile URL and publication URL can point to the same Medium post ID; that is one article with multiple observed URLs, not two sources.

Official sharing alone does not transform a partner or community article into Star Atlas-authored content. Reposts, responses, account activity, author profiles, and landing pages were excluded and ledgered rather than treated as publications.

## Authority and citation boundary

An official article is strong evidence of what Star Atlas published, the terminology it used, and the timing of that publication. It does not automatically prove delivery, execution, economic accuracy, partnership outcomes, or event occurrence.

- An announcement is not a release.
- A roadmap date is not a delivery date.
- A governance proposal is not passage or implementation.
- A current article is not proof that identical wording appeared on the original date.
- Repetition across Medium, Discord, and X may show dissemination without independent corroboration.

When an article quotes, summarizes, or republishes another source, its source lineage should preserve that original creator and relationship.

## Research use

Researchers should cite the article-level Source Record rather than this profile. A durable citation includes the `SRC-MEDIUM-STARATLAS-*` identifier, canonical and observed URLs, author, publisher, original and normalized dates, retrieval tier, capture timestamp, and checksum. Historical-text comparisons should prefer archived snapshots or explicit revision evidence.

## Evidence references

- [Campaign summary](../../archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.md)
- [Article Source Records](../../archive/source-records/medium/star-atlas/)
- [Campaign manifest](../../operations/campaigns/star-atlas-medium-ingestion-2026-07/campaign-manifest.json)
- [Deferred review queue](../../operations/campaigns/star-atlas-medium-ingestion-2026-07/manual-review-queue.json)

## Review status

`QUALIFIED`. The 181 confirmed included articles are completely ingested and validated, and all 216 known review candidates have terminal dispositions. The historical publication inventory remains incomplete because undiscovered or unrecoverable material may still exist.
