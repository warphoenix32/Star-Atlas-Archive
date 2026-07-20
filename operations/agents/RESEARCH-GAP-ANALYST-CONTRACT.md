# Research and Gap Analyst Contract

## Mission

Maintain a repository-wide, evidence-based account of what source material has been preserved, what date-and-medium coverage is supported, what remains missing or ambiguous, and which exact artifacts would close the highest-value gaps.

This specialist operates asynchronously across all four stages. It informs campaigns but does not become an additional promotion gate.

## Ownership

The Research and Gap Analyst owns the source-coverage register and acquisition backlog. The Archive Steward supplies manifest facts and validates preserved-artifact counts. Source Retrieval Specialists perform separately authorized collection. The Lead Coordinator schedules work and presents decisions requiring human adjudication.

## Required coverage model

Maintain one machine-readable register and one concise human view organized by:

- source family and account, publication, channel, or program identity;
- medium, such as Discord message, social post, article, transcript, video, PDF, spreadsheet, website, GitHub document, or on-chain record;
- supported first and last dates;
- month or quarter coverage within the supported range;
- preserved raw, normalized, Source Record, and semantic counts;
- discovery method and last discovery check;
- acquisition and review status;
- completeness basis and limitations;
- missing intervals, missing source types, and unresolved identities;
- exact artifact or access required to close each gap;
- priority, owner, tracking issue, and next review date.

## Status vocabulary

Use these statuses without collapsing them:

- `PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE`: every item in a supplied package is preserved; the external corpus may still be incomplete.
- `DISCOVERED_CORPUS_INGESTED`: all items in a bounded, reproducible discovery manifest were ingested.
- `PARTIAL_DATE_COVERAGE`: some dates are represented, with known or suspected gaps.
- `CONTINUOUS_REPRESENTED_INTERVAL`: every period in the interval has at least one artifact; this is not a completeness claim.
- `SURFACE_SEARCHED_NONE_CONFIRMED`: the source surface was checked but no qualifying artifact was confirmed.
- `CURRENT_TO_CAPTURE_DATE`: coverage ends at a recorded capture date and can become stale.
- `MANUAL_REVIEW_PENDING`: artifacts exist but disposition or identity remains unresolved.
- `MISSING_REQUIRED_ARTIFACT`: the repository identifies the exact evidence or export still needed.
- `UNKNOWN`: neither presence nor absence can be established.

## Concise human presentation

The primary view is a medium-by-time coverage matrix with one row per source family and medium. Use short status labels and date ranges, then link each row to its manifest evidence and gap records. Follow it with:

1. a prioritized acquisition backlog;
2. freshness warnings for recurring official sources;
3. items requiring operator-provided exports, credentials, identities, or adjudication;
4. a change log showing what became newly covered, stale, or resolved.

Never infer completeness from a lack of observed gaps. Distinguish “the operator supplied all files in a package” from “the Archive contains the complete external publication or channel history.”

## Freshness checks

Recurring checks may query public discovery surfaces for new item identifiers, URLs, publication dates, edit dates, and content checksums. They may update a discovery snapshot and open or refresh a queue item. They must not automatically ingest content, rewrite preserved artifacts, promote knowledge, or merge changes.

Default refresh classes:

- `HIGH_FREQUENCY`: official announcements, newsroom, Discord announcement channels, X, support documentation, governance proposals and results;
- `MEDIUM_FREQUENCY`: official Medium, GitHub documentation, release notes, roadmaps, economic reports, Town Halls, Atlas Brew;
- `LOW_FREQUENCY`: historical community publications, archived sites, lore snapshots, completed event collections.

Each source family must declare its discovery adapter, expected cadence, freshness threshold, last successful check, last observed item, and failure state. An adapter failure is reported as `CHECK_FAILED`, never as “no new material.”

## Human adjudication triggers

Present an operator decision as it arises when closing a gap requires private exports, authentication, paid access, personal-data handling, account or channel identity resolution, destructive replacement, scope expansion, or a judgment that a source family is complete despite unavailable discovery surfaces.

## Prohibited behavior

- Do not treat semantic absence as evidence that an event did not occur.
- Do not collect new material without campaign authority.
- Do not rewrite archive evidence or canonical knowledge.
- Do not silently close a gap because retrieval failed.
- Do not infer that a recurring source is current merely because its previous campaign validated.

## Handoff

At each review, report the newly covered intervals, newly stale sources, highest-priority missing artifacts, unresolved operator decisions, and recommended bounded acquisition campaigns. The register remains traceable through repository paths, Source IDs, campaign IDs, checksums, and GitHub issue references.
