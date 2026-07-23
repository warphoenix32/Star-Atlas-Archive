---
title: "Star Atlas Research Backlog"
seo_title: "Star Atlas Historical Research Backlog and Missing Sources"
seo_description: "Prioritized missing evidence for Star Atlas governance, products, economy, lore, Discord, publications, organizations, and technology."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
evidence_basis:
  - "operations/campaigns/canonical-pip-governance-ledger-2026-07/governance-research-backlog.md"
  - "operations/campaigns/discord-community-indexing-001/discord-channel-gap-report.json"
  - "operations/campaigns/lore-repository-ingestion-2026-07/research-backlog.md"
  - "knowledge/index/source-registry/Public-Source-Registry.md"
  - "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json"
  - "operations/campaigns/atlas-brew-url-reconciliation-2026-07/campaign-summary.json"
  - "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07/campaign-summary.json"
known_limitations:
  - "This backlog describes gaps visible in the repository as of the review date; unindexed holdings may exist."
  - "An acquisition target may no longer be publicly recoverable."
research_gaps:
  - "Each open item below is itself a research gap and includes the preferred resolving artifact."
review_after: 2026-10-20
---

# Star Atlas Research Backlog

The Archive now contains substantial governance, publication, transcript, social, product, lore, and community evidence. The remaining problem is no longer simply “collect more.” It is to acquire the specific missing artifacts that would change what the repository can responsibly conclude.

## Highest-value acquisitions

| Priority | Gap | What is already preserved | Artifact that would materially resolve it |
| --- | --- | --- | --- |
| P0 | Governance payments and execution | PIP-1 through PIP-33 ledger, captured text, votes, and Council-reported states | Transaction signatures, source and recipient accounts, mint metadata, contracts, Foundation execution notices, and proposal-to-transfer mappings |
| P0 | Election outcomes | Mechanism-aware records with unresolved PIP-11, PIP-25, and PIP-27 outcomes | Official STV tabulation, candidate totals, transfer rounds, and final winner announcements |
| P0 | Discord channel coverage | 1,071 announcement-export messages, March 2021–July 12, 2026 | Native exports for each material channel with server/channel/message/author IDs and timezone offsets |
| P0 | Product release chronology | Reviewed product histories and selective transcript candidates | Versioned release notes, build manifests, public-test notices, deployment timestamps, and retired interface snapshots |
| P1 | Medium publication discovery | 181 confirmed articles fully ingested; all 216 known review candidates terminally resolved | A new publication-native discovery snapshot or owner export capable of finding deleted, moved, or previously unindexed articles |
| P1 | Town Hall history | Partial preserved transcript and source-record coverage | Complete episode inventory, original URLs, publication dates, transcripts, and timestamp metadata |
| P1 | Atlas Brew event context | 124 public recordings reconciled to URLs and upload dates; 123-source selective semantic layer plus qualified #7 ASR | Complete event ledger, live-event dates, hosts/guests, original-platform lineage, and speaker review only for authority-dependent claims |
| P1 | Lore continuity | Commit-pinned canonical taxonomy and 4,632 extracted entities | Newer official lore, complete CORE catalog, primary chronology sources, and maintainer reconciliation of canon/docs differences |
| P1 | Corporate and institutional history | Reviewed ATMTA, DAO, Foundation, Council, and role pages | Formation records, dated leadership announcements, charters, delegated-authority records, and current role confirmations |
| P2 | Technical provenance | Technology and program registry | Program IDs, upgrade authorities, audit reports, SDK/API release histories, repository archival notices, and architecture publications |

## Source coverage by medium

### Discord

Only one repository-designated **announcements** export has been ingested. It contains no native channel identity and must not be described as the entire Star Atlas Discord. High-value future exports include governance, DAO chat, economics, foundation rooms, product support, guild coordination, events, and general community channels. Each should arrive as a native export where possible, preserving channel metadata and stable message identifiers.

Unrelated politics, culture-war discussion, unrelated games, and off-topic personal attacks may remain in immutable raw exports but are excluded from Star Atlas knowledge evaluation. Star Atlas-related disputes, alliances, animosities, corrections, and sustained relationship patterns remain eligible when contextualized and reviewed.

### Video and audio

Atlas Brew and other recordings should be evaluated by discussion significance, not just keyword density. Unknown speakers do not invalidate timestamped product, event, or historical evidence. Speaker review should be concentrated on claims of institutional authority, named-person positions, direct quotations, and adverse interpretations.

### Publications and social platforms

Official Medium is complete for the frozen 181-article included manifest, not
for total publication discovery. All 216 known review candidates are resolved;
future work is new discovery, not closure of an inherited manual-review queue.
Official X, newsroom, GitHub, support, governance, and other living sources
require dated refresh jobs that distinguish newly discovered material from
checksum-identical records. HNN, Intergalactic Herald, and Aephia still contain
targeted authorship and lineage questions tracked in the [Community Source
Attribution Backlog](Community-Source-Attribution-Backlog.md).

## Domain research program

### Governance and treasury

- Recover final candidate-level results for PIP-11, PIP-25, and PIP-27.
- Obtain primary termination, cancellation, or withdrawal records for PIP-14, PIP-17, and PIP-31.
- Reconcile PIP-33's two approximately equal, conditional 75% USDC / 25% ATLAS tranches without correcting the preserved one-cent discrepancies by inference.
- Acquire transaction-level evidence before changing any payment state beyond `REQUESTED`, `AUTHORIZED`, `COUNCIL_REPORTED`, `UNVERIFIED`, or `MISSING_ONCHAIN_EVIDENCE`.
- Recover timestamped portal state transitions without using portal status as implementation proof.

### Economy and assets

- Reconstruct ATLAS and POLIS issuance, emissions, sinks, locking, and supply changes from dated primary records.
- Acquire asset-sale, ship, land, Claim Stake, crew, and resource-sale histories.
- Reconcile marketplace metrics and quarterly economic-report methodology changes.
- Separate authorized treasury amounts, reported payments, verified transfers, and independently verified outcomes.

### Products and events

- Establish build-level histories for SCORE emissions and residual surfaces, SAGE Labs, Starbased, SAGE 3D, C4, Fleet Command, Escape Velocity, Holosim, and UE5 Showroom.
- Preserve `PLANNED`, `IN_DEVELOPMENT`, `TESTING`, `LIVE`, `UPDATED`, `DEGRADED`, `RESOLVED`, `SUPERSEDED`, `DEPRECATED`, and `CANCELED` at the narrowest named object.
- Acquire occurrence evidence for announced events before describing them as held.
- Reconcile product incidents, corrections, service degradation, and restoration with dated operational records.

### Lore

- Complete the CORE and graphic-novel publication catalog and real-world chronology.
- Recover ARC Cypher history and outcome evidence.
- Reconcile source-tree canon with generated docs where narrative text diverges.
- Resolve legacy mappings for CORE and The Voice of Iris without collapsing their ambiguity.
- Track newer official lore that postdates the pinned canonical taxonomy snapshot.

### Organizations, people, and guilds

- Acquire dated evidence for leadership, moderation, guild membership, mergers, splits, dissolutions, and role changes.
- Preserve true aliases separately from roles, stages, guild tags, and successor organizations.
- Document guild relationships and rivalries only from Star Atlas-relevant evidence; avoid importing unrelated personal or political conflict.

## Refresh and closure rules

A living source should record its last discovery attempt, last successful item, collection method, manifest boundary, and unresolved candidates. Automated refreshes may discover and stage evidence, but they must not silently promote new knowledge.

A backlog item closes only when the resolving artifact is preserved, normalized, source-identified, and reconciled to the affected knowledge claim. If the artifact disproves an earlier assumption, the repository records the correction and historical state rather than deleting the old evidence.

## Review status

This backlog was reconciled after the PIP ledger, Discord channel assessment, Medium ingestion review, Atlas Brew semantic precision work, lore taxonomy ingestion, and Knowledge Narrative Depth Waves 1–4. It is ready to guide future acquisitions; it does not itself authorize factual promotion.
