---
title: "Governance and Economy Overview"
seo_title: "Star Atlas Governance and Economy: POLIS, Treasury, and Funding"
seo_description: "How POLIS voting, the Star Atlas DAO, Foundation, Council, treasury architecture, and Ecosystem Fund connect without collapsing authority into execution."
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 5
page_risk_class: R2
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
known_limitations:
  - "Current-state statements are date-bound."
  - "Absence of evidence is not evidence of non-occurrence."
research_gaps:
  - "Independent execution evidence remains incomplete where explicitly noted."
review_after: 2027-01-15
---

# Governance and Economy Overview

Star Atlas governance connects POLIS-based decision making to treasury policy and ecosystem funding. The connection is institutional, not evidentiary shorthand: a vote can authorize an economic action without proving a payment or outcome.

This overview maps the captured governance model as of 2026-07-17. It does not claim that every constitutional power, wallet control, budget, payment, or funded deliverable has been independently verified in current operation.

The central relationship is simple but easy to misstate: governance can authorize economic action, while financial evidence establishes whether that action occurred. The historical record becomes more reliable when these are told as connected chapters rather than compressed into a single “approved and paid” label.

## Institutions and instruments

POLIS holders exercise formal PVP-weighted voting authority through the [Star Atlas DAO](Star-Atlas-DAO.md). The [Star Atlas Foundation](Star-Atlas-Foundation.md) performs legal and administrative functions described in the captured PIPs, while the [Star Atlas Council](Star-Atlas-Council.md) stewards process and delegated programs. The [Ecosystem Fund](Ecosystem-Fund.md) is a policy instrument rather than a separate sovereign body.

[PVP voting power](../economy/PVP-Voting-Power.md) is the vote-weight mechanism; it is not a second token or a treasury asset. The [DAO Treasury](../economy/DAO-Treasury-Architecture.md) is the broader governed asset pool. The Ecosystem Fund is a bounded funding mechanism drawn from that treasury under PIP-23. A direct treasury proposal can therefore sit outside the Ecosystem Fund, as [PIP-33](PIP-33-ATMTA-Historic-Expense-Reimbursement.md) does.

## Institutional decision chain

| Stage | Principal evidence | Supported conclusion | Conclusion that requires later evidence |
|---|---|---|---|
| Draft/publication | Official PIP text | A proposal and its author's requested terms existed. | Community approval, implementation, or factual accuracy of supporting claims. |
| Voting | Official portal ballot and PVP totals | The captured electorate produced a result under the applicable mechanism. | Foundation execution, payment, or project success. |
| Passage | Completed result plus governing rule | The DAO authorized the proposal as written, subject to institutional and legal implementation boundaries. | That every authorized action occurred. |
| Administrative implementation | Foundation or delegated operational record | An institution reported or instructed an implementation step. | Asset movement or successful delivery unless separately evidenced. |
| Payment | Primary transaction reconciled to proposal and recipient | A specified asset moved between identified accounts. | Milestone acceptance, value delivered, or independent economic benefit. |
| Completion/outcome | Deliverable, acceptance, and outcome evidence | The evidenced milestone or result occurred within the stated scope. | Broader or continuing success beyond the evidence window. |

PIP-1 establishes the proposal process and allows the Foundation to refuse unsafe or improper implementation with an explanation. PIP-2 establishes the Foundation's legal and administrative role and a recurring basic-operations budget ceiling. PIP-3 establishes the Council's governance-process role. These institutions are related but not interchangeable: POLIS holders supply formal PVP-weighted approval; the Foundation implements within legal and safety constraints; the Council assists and administers delegated programs.

## Economic evidence boundaries

For each funding PIP, the archive distinguishes requested amount, denomination, vote result, authorized maximum, payment report, and deliverable state. A requested dollar value is not a verified transaction. An ATLAS-denominated payment is not silently converted into a historical USD value. Repeated announcements are not independent corroboration.

Economic records should preserve at least six separate values when available: requested denomination, approved cap, token quantity paid, transaction date, conversion basis, and unpaid balance. A Council tracker value is an attributed A3 operational assessment. It becomes independently verified only after reconciliation to the relevant transaction and proposal terms.

PIP-23 supersedes PIP-4 and is the supported current fund framework as of 2026-07-17. The captured registry also contains passed, failed, in-progress, terminated, canceled, and non-implemented proposals; those states remain distinct. [Governance semantic registry](../../archive/semantic/governance/pip-registry-semantic.json)

## Two treasury pathways in the captured record

**Ecosystem Fund.** PIP-23 governs a bounded allocation with a formula, a USDC reserve threshold, a rolling 5% per-PIP ceiling, a 12-month duration ceiling, USDC-denominated applications, and ATLAS payments. Its Council stewardship provisions do not make the Council the contracting or refill-execution authority.

**Direct DAO Treasury.** PIP-33 is an extraordinary reimbursement measure submitted directly against the DAO Treasury because it exceeds the Ecosystem Fund limit. Its two approved tranches are payment terms, not proof of payment. Treating it as an Ecosystem Fund grant would distort both the policy cap and recipient history.

## Source conflicts and interpretive controls

- Where primary PIP text conflicts with a derived semantic label, the primary text controls the knowledge statement and the conflict remains documented.
- A failed proposal cannot have authorized implementation milestones even when the Council tracker contains a generic `1/1` milestone value.
- Council-reported `MILESTONES_REPORTED_COMPLETE`, payment amounts, and ROI narratives remain attributed assessments until independently reconciled.
- Roadmap or proposed timing is not converted into execution dates.
- Present-tense claims about balances, signer authority, program deployment, or institutional officeholders require a dated current source.

## Current limitations

The repository does not yet independently reconcile every Council-reported payment to a transaction or every milestone to an accepted deliverable. Economic measurements and institutional statements remain source-attributed.

Priority gaps are a transaction-level treasury ledger, versioned program and signer verification, an Ecosystem Fund refill/payment ledger, and proposal-specific implementation files that connect authorization to execution without collapsing intermediate states.

## Related pages

- [PIP Registry](PIP-Registry.md)
- [PIP-33 reimbursement measure](PIP-33-ATMTA-Historic-Expense-Reimbursement.md)
- [Governance evidence states](Governance-Implementation-and-Evidence-States.md)
- [DAO Treasury Architecture](../economy/DAO-Treasury-Architecture.md)
- [PVP Voting Power](../economy/PVP-Voting-Power.md)
- [Economy index](../economy/README.md)
