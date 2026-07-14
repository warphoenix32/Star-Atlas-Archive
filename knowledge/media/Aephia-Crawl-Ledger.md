---
title: Aephia Site Crawl Ledger
entry_type: crawl-ledger
status: active
updated: 2026-07-12
publication_status: public
source_entity: MEDIA-AEPHIA
---

# Aephia Site Crawl Ledger

## Purpose

This ledger records which parts of Aephia.com have been traversed, what could be extracted, and what remains inaccessible or unprocessed. It exists to prevent repeated work and to distinguish a failed retrieval from an absent publication.

## Retrieval standard

Aephia is treated as a generally reliable community source for contemporaneous Star Atlas reporting. Reliability is topic-dependent and time-dependent:

- recent factual recaps are useful for discovery and chronology;
- direct quotations and linked primary sources should be followed to the original source;
- roadmap statements remain plans until confirmed by delivery;
- old gameplay guides and economic explanations may be historically accurate but operationally obsolete;
- Aephia guild claims, rankings, awards, membership, and influence claims remain attributed unless independently verified.

## Crawl passes

### Pass 1 — Source profile and recent issue discovery

Completed:

- established Aephia as both a DAC and a community publisher;
- identified the Weekly Star Atlas Newsletter as a numbered Monday digest;
- verified issues #233 through #237 and issue #184;
- created a source profile and newsletter index.

### Pass 2 — Direct article traversal

Completed in part:

- traversed article-to-article through related-post links;
- fully extracted issue #234;
- reconfirmed full extraction for issues #235 and #184;
- verified metadata and synopses for issues #233 through #237;
- tested predictable URLs for issues #227 through #232.

Retrieval limitations:

- several valid article URLs resolved but returned no extractable body text in the available browser path;
- search-engine indexing did not expose a complete series catalog;
- no complete public sitemap or feed was retrievable through the current environment;
- a resolved URL must not be treated as proof that metadata or article contents have been captured.

## Current issue coverage

| Range | Status |
|---|---|
| #233–#237 | Verified; mixed full extraction and synopsis-only coverage |
| #227–#232 | URL-level traversal attempted; metadata/body extraction incomplete |
| #185–#226 | Not yet traversed |
| #184 | Fully extracted |
| #1–#183 | Not yet traversed; series starting number and continuity not independently established |

## High-value findings from pass 2

Issue #234 materially expanded the archive's understanding of the June 2026 development state. It contains community reporting on:

- Combat V2 mechanics and program isolation;
- regional governance and local treasury routing;
- Nemesis NPC development;
- crew utility work;
- LLM-assisted player automation;
- C4 PTR bug fixes and exploit remediation;
- the Star Atlas TTRPG handbook;
- PIP-32 results;
- UE5 Epic Games Store and multiplayer-server availability;
- promotional asset-sale status;
- corrected token circulating-supply figures.

These findings should be transferred into canonical product, governance, economy, and actor files only after their implementation status and original sources are checked.

## Next crawl queue

1. Recover metadata for #227–#232 through an alternate rendering, feed, sitemap, or archive path.
2. Traverse #226 downward in batches, recording URL resolution before deep extraction.
3. Prioritize historically consequential periods rather than treating every issue equally:
   - C4 PTR launch and z.ink transition;
   - SAGE Labs and Starbased releases;
   - FTX aftermath and ATMTA restructuring;
   - Showroom and UE5 releases;
   - DAO formation, elections, and major PIPs;
   - major asset sales and token-economic changes.
4. Preserve linked primary sources from each issue.
5. Create an outcome-reconciliation table for dated forecasts and roadmap claims.

## Outcome reconciliation fields

For each forecast or planned feature, record:

| Field | Meaning |
|---|---|
| issue | Newsletter issue number |
| reported_date | Date Aephia published the claim |
| subject | Product, proposal, event, or economic change |
| status_at_publication | announced, planned, in development, PTR, released, disputed |
| expected_date | Any reported estimate |
| later_outcome | delivered, delayed, redesigned, cancelled, unresolved |
| outcome_source | Later official or independently verified evidence |

## Do-not-infer rules

- Issue numbering alone does not prove uninterrupted weekly publication.
- Approximate weekly dates must not be assigned without page metadata or another reliable source.
- A related-post synopsis is not a substitute for full article extraction.
- A technical item described as completed by Aephia may still require deployed-program or official-release verification.
- Old guides must not be presented as current instructions without a freshness check.
