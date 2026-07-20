---
title: "Star Atlas Council Election History"
seo_title: "Star Atlas Council Elections: Results, Candidates, and Open Gaps"
seo_description: "A mechanism-aware history of Star Atlas Council elections that separates nominations, advancing candidates, final winners, intended terms, and verified service."
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-06-1B792551.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-07-91652743.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-11-7B48A62D.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-25-91CC73FA.json"
known_limitations:
  - "The archive identifies final winners only for the first Council election."
  - "Intended term dates do not independently prove service or current officeholding."
research_gaps:
  - "Recover official final-result records and service rosters for Council elections 2 and 3."
  - "Verify deployment of the PIP-9 STV amendment in the voting program used by later elections."
review_after: 2026-10-17
---

# Star Atlas Council Election History

The captured record documents one fully resolvable two-stage Council election and two later Council elections whose winning rosters remain absent. This page preserves candidate advancement, final election, intended term, service, and current membership as distinct claims.

Council elections are a useful test of archival discipline. A proposal page can prove that an election was scheduled, an aggregate result can prove that voting occurred, and a winner record can identify elected members—but none of those artifacts alone proves that each winner accepted, served an entire term, or remains in office. The history below stops at the strongest state supported for each election.

## Election framework

[PIP-3](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json) established the Council framework. It did not elect a Council. Election results arise from the applicable election PIP and completed vote record. [PIP-9](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-09-1CC4BB6F.json) later amended STV backup-vote handling; its passage does not by itself prove that a particular deployed voting program used the amended logic.

## Election registry

| Election stage | Vote window | Captured participation | Result supported by archive | Qualification |
|---|---|---:|---|---|
| [PIP-6 — Election #1, first round](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-06-1B792551.json) | 2024-09-14 through 2024-09-21 | 587 ballots; 161,327,889.08397183 PVP | Twelve candidates advanced | Advancers are not elected Council members. |
| [PIP-7 — Election #1, second round](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-07-91652743.json) | 2024-09-27 through 2024-10-11 | 575 ballots; 174,532,321.58451426 PVP | Five final winners identified | Establishes the first elected roster, not indefinite current service. |
| [PIP-11 — Council Election #2](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-11-7B48A62D.json) | 2025-03-23 through 2025-04-06 | 348 ballots | Election completed/passed; winners unresolved | Proposal intended a 2025-04-11 to 2026-01-11 term; service requires separate evidence. |
| [PIP-25 — Council Election #3](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-25-91CC73FA.json) | 2025-11-26 through 2025-12-10 | 176 ballots | Election completed/passed; winners unresolved | Proposal intended a 2026-01-11 to 2026-10-11 term; current membership is not inferred. |

PIP-27 is a DAO Casters election and is not a Council election. Similar voting mechanics do not merge the offices or their histories.

## First election: advancement and final selection

PIP-6’s captured result identifies the following **advancing candidates**: `king_bryan`, `funcracker`, `krigs`, `bodhi_tree`, `rome_i_emperor`, `ajota_lrnr`, `notcatz`, `jp`, `jith_blade`, `drumcarl05`, `dmark`, and `xalexus`.

PIP-7 identifies the final first Council roster as `jp`, `funcracker`, `king_bryan`, `bodhi_tree`, and `drumcarl05`. This is the only roster the present archive can promote as a completed Council-election result. It should be described as the first elected roster, not the current Council.

## Later elections

The PIP-11 and PIP-25 portal captures preserve election text, vote windows, participation, and reviewed completion, but their normalized winner fields are empty. Official Discord announced PIP-11 voting as live; that notice cannot supply the missing final roster. [PIP-11 voting notice](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-4857334329D3BC55.json)

Until a final result artifact is preserved, individual claims of election, appointment, or present service after the first term remain research leads.

The gap is historically meaningful. It prevents the archive from turning familiar community identities, later public appearances, or a Council-authored tracker into an unofficial roster. A future recovery should preserve the final tally and winner announcement first, then connect acceptance, seating, vacancy, replacement, and term-end records as separate events.

## Evidence rules

- Nomination is not advancement.
- First-round advancement is not election.
- A completed election is not evidence of service throughout the intended term.
- An intended term is not proof of current membership.
- A Council-authored tracker row is not an election result.
- A person mentioned in a Town Hall, Atlas Brew, article, or role profile is not thereby a Council member.

## Missing artifacts

Required evidence includes official final tallies and winner announcements for PIP-11 and PIP-25; acceptance or seating records; resignations, vacancies, replacements, and removal records; term-start and term-end confirmations; and the deployed STV program/version used in each election.

## Review status

`QUALIFIED`. First-election results are high confidence. Later winner identity and current Council composition remain unresolved.
