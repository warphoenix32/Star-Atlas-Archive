---
title: "Governance Constitutional History"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json"
  - "archive/semantic/governance/pip-registry-semantic.json"
known_limitations:
  - "This is an archival periodization of captured instruments, not a legal opinion or complete constitutional record."
  - "The relationship between the 2023 PIP-1 rollout and the 2024 captured proposal requires article-level reconciliation."
research_gaps:
  - "Recover and compare the full 2023 PIP-1 Medium publication with the 2024 portal text."
  - "Verify implementation of each passed process amendment independently from Council assessments."
review_after: 2027-01-17
---

# Governance Constitutional History

Star Atlas governance developed in layers rather than through one founding event. The surviving record distinguishes an operational DAO and locking release in 2022, a public PIP-1 design rollout in 2023, formal ratification proposals and voting in 2024, and later amendments to elections, Council terms, and treasury policy. This history treats publication, deployment, ratification, passage, implementation, and supersession as separate states.

## Interpretive scope

“Constitutional” describes instruments that establish or materially modify the governance system: the DAO charter, Foundation mandate, Council mandate, PIP procedure, voting mechanics, and treasury/fund rules. It does not imply that every instrument has the same legal status or that the repository has independently verified implementation.

The principal evidence is the captured official PIP text and vote data. Discord and newsroom records establish public rollout chronology, but an announcement cannot substitute for the governing instrument it describes.

## Constitutional periods

### 1. Operational pre-ratification, 2022

ATMTA stated on 2022-07-21 that the initial DAO governance and POLIS-locking module had launched. On 2022-09-29 it published the Sustainable Governance Framework and separately announced the ATLAS Locker. These records establish official release and design statements, not the later PIP-1 vote or the complete execution history of each named program. [DAO release](../../archive/source-records/campaign-delta-official/SRC-OFF-E5AEFD6B36E3CE06.md) [Governance framework](../../archive/source-records/campaign-delta-official/SRC-OFF-68D126528852339E.md)

### 2. Public PIP design rollout, 2023

Official Discord records show a delayed PIP-1 rollout on 2023-06-28, a next-day release notice on July 5, and a July 6 announcement that PIP-1 and three explanatory articles were live. These are publication-history anchors. They do not prove that the 2023 text was identical to the proposal captured in 2024. [Delay](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-24BD0BFCDB6F73B4.json) [Release notice](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-F9EDF3D624192133.json)

### 3. Founding ratifications, 2024

Four founding proposals were published on the governance portal in July 2024. The captured vote records establish their proposal-specific results; later implementation remains a separate question.

| Instrument | Institutional function | Archival state |
|---|---|---|
| [PIP-1 — Star Atlas DAO](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json) | Ratified the PIP process, PVP-weighted voting, DAO scope, implementation referral, and named governance programs/accounts. | `PASSED`; deployment history predates the vote; later execution is not inferred from passage. |
| [PIP-2 — Star Atlas Foundation](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json) | Ratified the legal and administrative implementation body and a bounded operating budget. | `PASSED`; authorized budget is not payment evidence. |
| [PIP-3 — Star Atlas Council](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json) | Established the elected process-steward and program-administration model. | `PASSED`; officeholder history requires election evidence. |
| [PIP-4 — Ecosystem Fund](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-04-AD1945D8.json) | Created the original bounded community-funding framework. | `PASSED`, then fully superseded by PIP-23. |

PIP-1 assigns formal voting authority to holders controlling locked POLIS through PVP. Successful proposals are referred to the Foundation for implementation, while the Foundation may decline unsafe or unlawful implementation under the stated conditions and explanation duties. That safeguard does not erase the vote result or create a separate legislative sovereign.

### 4. Procedural amendment and institutional continuity, 2024–2025

PIP-6 and PIP-7 conducted the two-stage first Council election. PIP-9 later changed STV backup-vote handling, while PIP-10 modified the Council framework for later terms. These instruments show constitutional maintenance through proposal-specific amendments rather than replacement of the entire charter. [PIP-9](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-09-1CC4BB6F.json) [PIP-10](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-10-ED887A4E.json)

PIP-13 proposed Council term limits and failed. Its policy therefore did not enter the supported constitutional framework. A failed amendment is historical evidence of a debated alternative, not authority for the rule it proposed. [PIP-13](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-13-B721D8E7.json)

### 5. Treasury-policy consolidation, 2025–2026

PIP-23 replaced PIP-4 in full and restated the Ecosystem Fund’s wallet, allocation formula, reserve rule, request denomination, payment medium, project cap, term limit, and Council duties. Supersession changes the controlling policy without deleting PIP-4’s historical role. [PIP-23](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

PIP-33 demonstrates that the DAO could consider an extraordinary direct DAO Treasury authorization outside the ordinary Ecosystem Fund cap. Its passage does not establish payment. [PIP-33 case study](PIP-33-ATMTA-Historic-Expense-Reimbursement.md)

## Authority chain and evidence states

| Stage | What the evidence establishes | What it does not establish |
|---|---|---|
| Draft or announcement | Proposed design and publication timing | Portal publication, vote, or adoption |
| Portal publication | A numbered proposal existed in captured form | Approval |
| Voting | Ballots/PVP were recorded under a mechanism | Passage until the completed result is adjudicated |
| Passage | The electorate authorized the proposal | Payment, implementation, or successful outcome |
| Foundation implementation | An administrative action was taken | Independent correctness or completeness |
| Transaction | Asset movement occurred | Milestone acceptance or project success |
| Council assessment | The Council reported an operational state | Independent verification |

## Constitutional conflicts and qualifications

- PIP-1 contains quorum language but no numeric quorum threshold in the captured text. The repository’s completed-binary YES-versus-NO rule is an owner-approved editorial adjudication, not text asserted to appear in PIP-1.
- Generic portal status fields remained stale for several completed votes. Vote windows, vote totals, election mechanics, and reviewed results are evaluated separately.
- Council tracker milestone values cannot create implementation authority for a failed proposal.
- A pre-ratification deployment statement may establish operational chronology while the later PIP establishes formal ratification; neither should be silently backdated into the other.

## Missing artifacts

Priority recovery targets are the full 2023 PIP-1 Medium article and explanatory series; versioned governance-framework texts; program deployment and upgrade transactions; Foundation implementation notices; current delegation instruments; complete later-election result records; and proposal-specific transaction and deliverable evidence.

## Review status

`QUALIFIED` as of 2026-07-17. The constitutional sequence is well supported at the instrument level, while implementation and version-to-version reconciliation remain incomplete.

## Related pages

- [PIP lifecycle and legislative process](PIP-Lifecycle-and-Legislative-Process.md)
- [Council Election History](Council-Election-History.md)
- [Governance Failure and Termination Casebook](Governance-Failure-and-Termination-Casebook.md)
- [Governance implementation evidence states](Governance-Implementation-and-Evidence-States.md)
