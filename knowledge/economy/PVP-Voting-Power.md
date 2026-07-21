---
title: "POLIS Voting Power (PVP)"
seo_title: "POLIS Voting Power (PVP): How Star Atlas DAO Voting Works"
seo_description: "A clear, evidence-linked explanation of POLIS Voting Power, lock duration, proposal tallies, election mechanisms, and repository vote adjudication rules."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: SYSTEM-POLIS-VOTING-POWER
aliases:
  - "PVP"
  - "POLIS Voting Power"
first_seen: 2022-07-31
last_reviewed: 2026-07-20
source_priority:
  - A1
  - A2
related_entities:
  - POLIS
  - Star Atlas DAO
  - POLIS Locker
depends_on:
  - knowledge/governance/Star-Atlas-DAO.md
  - knowledge/governance/PIP-Lifecycle-and-Legislative-Process.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/campaign-delta-official/SRC-OFF-45B0F6196BC7966E.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-0D4A8B8F235B43B8.json"
  - "archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.json"
editorial_adjudications:
  - "COMPLETED_BINARY_VOTE_RULE — owner-approved repository interpretation; not asserted as text contained in PIP-1"
adjudication_basis:
  - "operations/campaigns/knowledge-context-refresh-2026-07-17/review-adjudications.json"
known_limitations:
  - "The reviewed sources describe the inputs and decay behavior but do not provide a complete independently verified implementation formula."
  - "Current interface instructions and reward parameters may change."
research_gaps:
  - "Reconcile the exact deployed calculation with program code and version history."
  - "Document historical changes to lock multipliers, rewards, and proposal-activation requirements."
review_after: 2027-01-17
---

# POLIS Voting Power (PVP)

POLIS Voting Power, abbreviated PVP, is the voting-weight measure used by the Star Atlas DAO. It is obtained by locking POLIS, and its weight depends on both the amount locked and the lock duration.

PVP is a governance measurement, not a separate transferable token. A person's wallet balance, locked POLIS amount, PVP at a snapshot, ballot selection, and a proposal's final result are distinct records.

## Governance role

PIP-1 defines the DAO as a system in which people lock and vote with POLIS and states that voting weight is based on the amount controlled and the duration of the lock. This establishes PVP as the formal weight used in PIP voting; it does not establish that every interface or reward parameter has remained unchanged since ratification. [PIP-1; SRC-PIP-01-BC8475E4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

Official support documentation updated in December 2025 states that longer locks receive more PVP per POLIS and that locked POLIS cannot be withdrawn before the selected period ends. [SRC-OFF-45B0F6196BC7966E](../../archive/source-records/campaign-delta-official/SRC-OFF-45B0F6196BC7966E.md)

An official Discord announcement dated 2022-07-31 said PVP locking rewards would go live on 2022-08-02 and described ATMTA's intention to target approximately 65% of total PVP in the near term, initially using a five-year team lock. This is evidence of announced intent and timing, not proof that the target was continuously maintained or that the described locks remain current. [SA-DISCORD-ANN-0D4A8B8F235B43B8](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-0D4A8B8F235B43B8.json)

## Technical behavior

The official DAO-program overview describes the Tribeca locked-voter component as calculating PVP from locked amount and duration, with voting power decaying linearly over time. It separately describes a snapshot component that records historical voting-power states. These descriptions are A2 technical documentation, not a substitute for code-level verification of the deployed version. [SRC-OFF-4312E3B0005E60A3](../../archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md)

The reviewed evidence supports the following model without supporting a complete formula:

- **principal:** more locked POLIS contributes more voting weight;
- **duration:** a longer selected lock receives more PVP per POLIS;
- **time:** official documentation says voting power decays linearly as the remaining lock period shortens;
- **snapshot:** voting records can use a historical voting-power state rather than an unqualified present balance;
- **custody constraint:** locked POLIS is unavailable for withdrawal until its selected lock period ends.

The archive does not yet establish the live multiplier curve, rounding behavior, maximum duration, program version, or whether historical user-interface displays always matched the deployed program. Those details must come from versioned code and on-chain state, not extrapolation from explanatory prose.

## Decision boundaries

PVP measures voting weight. It does not by itself establish proposal passage, implementation, or execution. PIP-1 contains historical quorum language but does not specify a numeric quorum threshold in the captured text.

The **completed-binary vote rule is an owner-approved repository editorial adjudication**, not source-native governance text and not a rule asserted to appear in PIP-1. For completed captured binary votes, the repository compares YES and NO PVP and preserves abstentions as non-decisive; elections use their separate ranked-choice mechanism. This curatorial rule is recorded as `COMPLETED_BINARY_VOTE_RULE` in the campaign's [review adjudications](../../operations/campaigns/knowledge-context-refresh-2026-07-17/review-adjudications.json) so later editors and graph work can distinguish source-derived mechanics from repository interpretation. See the [PIP Registry](../governance/PIP-Registry.md) and [PIP lifecycle](../governance/PIP-Lifecycle-and-Legislative-Process.md).

For binary proposals, raw ballot count and PVP weight can tell different stories. The official captures retain both `count` and `pvp`; the governing result is weight-based. Abstaining PVP contributes to participation reporting but is not silently added to either YES or NO. For elections, advancing candidates, final winners, and ranked-choice mechanics must be interpreted from the specific PIP rather than forced into the binary rule.

### Worked example: PIP-33

The preserved PIP-33 export illustrates why ballot count and voting weight must remain separate. It contains 141 YES ballots, 59 NO ballots, and 20 abstentions across 220 effective wallets. Their normalized weights are 170,240,400.01174 YES PVP, 24,857,540.34942 NO PVP, and 83,860,459.54910 abstain PVP. YES therefore represents 87.25894% of the decisive YES-plus-NO weight under the repository's completed-binary adjudication.

Those numbers establish a captured ballot result; they do not identify every voter, prove the present distribution of POLIS, or establish that the approved reimbursement was paid. The ingestion package did not replay transaction signatures, and only one wallet identity received human validation. [PIP-33 vote source record](../../archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.md)

## Historical development

| Date | Evidence | What it establishes | What it does not establish |
|---|---|---|---|
| 2022-07-31 | Official Discord announcement `SA-DISCORD-ANN-0D4A8B8F235B43B8` | ATMTA announced PVP locking rewards for 2022-08-02 and described an intended near-term team-position target. | Continuous attainment of the target, present team voting weight, or unchanged reward terms. |
| 2024-07-08 | PIP-1 publication `SRC-PIP-01-BC8475E4` | Formal proposal language defining amount-and-duration-weighted PVP in the PIP process. | A numeric quorum threshold or full deployed formula. |
| 2025-12 update | Official support records `SRC-OFF-45B0F6196BC7966E` and `SRC-OFF-4312E3B0005E60A3` | Official user-facing and technical descriptions of locks, duration weighting, decay, and snapshots. | Independent code audit or proof that every historical deployment used identical parameters. |

The 2022 announcement's approximate 65% near-term target is an attributed ATMTA intention. It should not be used as evidence of governance capture at a later date without snapshot or on-chain data.

## Current state

As of 2026-07-20, the repository supports amount-and-duration weighting, lock-period restrictions, linear decay in official technical documentation, and use of PVP in governance. PIP-33 adds a mechanism-aware completed-vote case, while the exact live formula, deployed program version, historical parameter changes, and complete voter-identity history remain open for code and on-chain reconciliation.

## Review status

This R2 page is ready for publication with its current qualifications. The repository's completed-binary YES-versus-NO rule remains explicitly identified as an owner-approved curator interpretation—not text asserted to appear in PIP-1—and election mechanisms remain separate.
