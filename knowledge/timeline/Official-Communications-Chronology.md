---
title: "Official Communications Chronology"
seo_title: "Star Atlas Official Communications History"
seo_description: "A history of Star Atlas official communication channels, their preserved coverage, authority boundaries, and major archival gaps."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
evidence_basis:
  - "archive/campaign-summaries/campaign-delta-official/campaign-summary.json"
  - "operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json"
  - "operations/campaigns/social-governance-semantic-enrichment/validation-report.json"
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/source-records/campaign-delta-official/SRC-OFF-2A930EF6763F8490.md"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D27B5214B5BAC6AA.json"
known_limitations:
  - "No preserved source family is demonstrably complete across the lifetime of Star Atlas."
  - "Repeated official publication across surfaces is not independent corroboration of execution or outcome."
research_gaps:
  - "Complete article-level Medium review after its separate ingestion campaign is merged and approved."
  - "Recover deleted/edited posts, attachments, correction chains, and pre-2024 X history."
review_after: 2027-01-17
---

# Official Communications Chronology

Star Atlas has communicated through a newsroom, recurring newsletters, Discord, X, Medium, governance portals, support documentation, builder documentation, and live community formats. This chronology tracks the surviving publication surfaces and their evidentiary boundaries. It is not a product-release timeline and does not treat repeated announcements as independent proof of delivery.

## Preserved source-family coverage

| Surface | Preserved coverage | Strongest use | Principal limitation |
|---|---|---|---|
| Official written corpus | 320 successful retrievals from 321 attempts; 2021-03-16 through 2026-07-10 | First-party announcements, support, technical docs, lore, partnerships, roadmap, economic report | Multi-surface corpus, not a complete newsroom history; 1 failure and 1,172 manual-review items in reconciliation. [Summary](../../archive/campaign-summaries/campaign-delta-official/campaign-summary.json) |
| Official Discord announcements | 1,071 messages; 2021-03-16 through 2026-07-12 | Exact captured announcement text and timing | Export explicitly says collection incomplete; author grouping inferred; attachments absent. [Profile](../media/Official-Discord-Announcements-Profile.md) |
| Official X account | 796 unique posts; 2024-11-05 through 2026-07-14 | Captured official-account publication and resharing | Partial-period export; 268 retweets are not first-party authorship; linked media absent. [Profile](../media/Official-X-Account-Profile.md) |
| Governance portal | 33 numbered PIP captures | Proposal text, vote windows, mechanics, results | Portal status can be stale; passage does not establish implementation. [PIP Registry](../governance/PIP-Registry.md) |
| Official Medium | Discovery references on current `main` | Identifying publication leads | Article-complete ingestion is not merged into this campaign; no article-level claims are promoted here. [Profile](../media/Star-Atlas-Medium-Publication-Profile.md) |
| Town Hall | 14 preserved transcript sources | Source-level event content and research leads | Dates, URLs, and speakers largely unresolved. [History](../media/Star-Atlas-Town-Hall-History.md) |
| Atlas Brew | 123 transcript sources | Long-form institutional discussion and timestamped research leads | Dates/URLs absent; numbering gaps and duplicates; speakers unknown. [History](../media/Atlas-Brew-History.md) |

## Chronological development

### 2021 — Newsletter, newsroom, Discord, and recurring live formats

The earliest dated official record in Campaign Delta is *Atlas Star Issue #1* on 2021-03-16. The earliest preserved Discord announcement on the same date links that issue, showing a cross-surface publication pattern from the start of the archive. [SRC-OFF-2A930EF6763F8490](../../archive/source-records/campaign-delta-official/SRC-OFF-2A930EF6763F8490.md) [SA-DISCORD-ANN-D27B5214B5BAC6AA](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D27B5214B5BAC6AA.json)

By May 2021, *Atlas Star Issue #3* described Friday Town Halls as an established tradition. Token-sale, marketplace, and SCORE publications later supplied the principal official economic and product announcements of the year. [Town Hall source](../../archive/source-records/campaign-delta-official/SRC-OFF-DD9175EF794C1F8D.md)

### 2022 — Product releases, governance framework, and programmatic community media

Official communications documented the DAO/POLIS-locking release, ATLAS Locker, Sustainable Governance Framework, Showroom, and SAGE naming roadmap. Atlas Star issues described Town Hall cadence and Atlas Brew as a weekly live Discord audio discussion. These sources support publication and release chronology but do not prove continuous operation or every roadmap outcome. [DAO release](../../archive/source-records/campaign-delta-official/SRC-OFF-E5AEFD6B36E3CE06.md) [Atlas Brew description](../../archive/source-records/campaign-delta-official/SRC-OFF-2E4DE78B3C355FA9.md)

### 2023 — Formal PIP design and on-chain product operations

Discord announced a delayed then live PIP-1 information rollout in June–July 2023. The official PIP design announcement is dated 2023-07-07, while the formal captured PIP-1 proposal was published in July 2024. Design publication, proposal publication, voting, passage, and implementation are therefore separate chronology entries. [PIP-1 design](../../archive/source-records/campaign-delta-official/SRC-OFF-50186C400EF7CC79.md)

The same year’s official and community records document SAGE Labs release and a community-reported SAGE 3D/SAGE Labs V2 transition. The latter remains community-attributed and month-level.

### 2024 — Governance portal becomes a formal public record

The four founding PIPs and first Council election created a structured official record of proposal text, vote windows, PVP, results, and institutional roles. Discord notices are useful for public timing, but the portal captures are the stronger evidence for proposal-specific governance facts.

### 2025 — Support documentation and official-account social corpus expand

The preserved X corpus begins in November 2024 and becomes dense in 2025. Official support pages published in December 2025 provide a broad dated functional snapshot across products and governance. Documentation establishes what the official publisher described on its update date; it cannot prove when each function first shipped.

### 2026 — Current technical, PTR, and treasury communications

Campaign Delta includes technical and support updates through 2026-07-10. Discord preserves C4 PTR, Chapter 2, and PIP-33 communications; the latest captured announcement is a PIP-33 follow-up on 2026-07-12. The X export extends to 2026-07-14. These boundaries describe preserved collections, not the actual end of official publication.

## Cross-surface evidence rules

- A Discord or X post linking an article establishes that the account circulated the link; it does not preserve the article text.
- An article and a social post repeating the same announcement show cross-surface publication, not independent confirmation of delivery.
- A support page establishes a dated documented state, not historical first availability.
- A PIP announcement is not a proposal result; a passed PIP is not a payment.
- A retweet preserves official amplification while retaining the original creator’s authorship.
- A live discussion transcript supports exact timestamped content only when source, date, speaker, and context are reconciled.

## Known conflicts and missing artifacts

The older Official Newsroom Index lists 93 entries ending in 2023 and is narrower than Campaign Delta’s multi-surface corpus. Discord is explicitly incomplete; X starts late; Medium is not article-complete on `main`; Town Hall and Atlas Brew lack original URLs and speaker attribution. Deleted posts, edits, attachment binaries, revision histories, and systematic corrections remain incomplete.

PR #19 contains a separate Medium ingestion campaign but is unmerged and therefore excluded from this knowledge campaign. After that evidence passes review and merges, the Medium profile and this chronology should be re-evaluated rather than manually copying draft evidence.

## Review status

`QUALIFIED`. Surface-level coverage and major publication transitions are well supported; completeness and cross-surface correction history remain unresolved.
