---
title: "Star Atlas DAO"
seo_title: "Star Atlas DAO: POLIS Voting, Authority, and Governance History"
seo_description: "How the Star Atlas DAO uses POLIS voting power, how proposals become decisions, and why passage remains separate from implementation."
knowledge_status: CANONICAL
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 3
page_risk_class: R1
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
known_limitations:
  - "The captured PIP corpus establishes the designed governance system but does not independently verify every later operation."
  - "Current participation, membership, and interface behavior may change after the as-of date."
research_gaps:
  - "Recover versioned governance-framework publications and independent execution evidence for unresolved passed proposals."
review_after: 2027-07-20
---

# Star Atlas DAO

The Star Atlas DAO is the governance system through which people who hold and commit POLIS voting power can make collective decisions about the Star Atlas ecosystem. It is best understood as an electorate and a decision process—not as a synonym for ATMTA, the Star Atlas Foundation, the Star Atlas Council, or every wallet associated with governance.

The captured text of PIP-1 describes a decentralized, program-based system deployed on Solana. Its historical importance lies in establishing both an authority and a procedure: POLIS holders may decide eligible proposals through PVP-weighted voting, but proposals must still pass through defined administrative and voting stages. [PIP-1 Source Record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

## What the DAO can establish

Within the preserved framework, the DAO can approve or reject policy proposals, elect Council members under the mechanism defined for the election, and authorize treasury or program actions. That is formal decision authority. The authority is collective and vote-based; it should not be attributed to whichever organization authored a proposal or operates the surrounding software.

Voting weight is measured through POLIS Voting Power, or PVP. PVP reflects the governance mechanism defined in the captured record and is not interchangeable with a simple wallet count. A ballot table can therefore show more individual wallets on one side while the PVP-weighted result is determined by the voting power attached to those ballots. See [PVP Voting Power](../economy/PVP-Voting-Power.md).

## How a DAO decision is made

A proposal begins as an authored request. Administrative review determines whether it can advance under the procedural framework. Publication opens the text to the community, and a voting window allows eligible voting power to participate. Only the completed result establishes passage or failure under the applicable mechanism.

That sequence matters for historical language:

1. **Published** means a proposal existed.
2. **Voting** means a decision process opened.
3. **Passed** means the vote supplied authorization.
4. **Implementation announced** means an actor reported intended action.
5. **Executed or paid** requires evidence of the actual operation.
6. **Independently verified** requires separate primary evidence beyond the actor's own report.

Election proposals require mechanism-aware interpretation. A qualifying round may select advancing candidates without filling any Council seat. A portal status of “passed” does not identify winners when the underlying election record is absent. The [Council Election History](Council-Election-History.md) preserves those distinctions.

## Relationship to the Foundation and Council

The [Star Atlas Foundation](Star-Atlas-Foundation.md) supplies legal and administrative capacity described in the governance framework. It can review procedural compliance and mediate implementation within legal, safety, and operational constraints. The [Star Atlas Council](Star-Atlas-Council.md) is an elected process steward with delegated duties that can include author support, governance operations, program administration, and milestone or payment review.

Neither institution replaces the electorate. Conversely, a DAO vote does not eliminate the need for lawful administration, custody, technical execution, or supporting records. This distribution of responsibility is why the archive tracks institutional action after a vote instead of reporting passage as a completed outcome.

## Treasury authority

Some PIPs authorize economic action. The [Ecosystem Fund](Ecosystem-Fund.md) is one governed funding pathway; direct treasury proposals are another. The wider [treasury architecture](../economy/DAO-Treasury-Architecture.md) includes distinct accounts and programs, while the named DAO Treasury account is a particular address defined in the relevant PIPs. These concepts must remain separate for later entity and graph work.

[PIP-33](PIP-33-ATMTA-Historic-Expense-Reimbursement.md) demonstrates the boundary clearly. The completed vote supports authorization of the proposal's terms. It does not, by itself, prove that either scheduled tranche was paid.

## Historical and current limits

As of 2026-07-20, the archive supports the DAO's institutional identity, its PVP-weighted voting model, and a captured PIP-1 through PIP-33 corpus. It does not establish that the corpus represents every informal governance discussion, that every portal state remained current, or that every approved action was executed.

For proposal-level history, results, and open conflicts, continue to the [PIP Registry](PIP-Registry.md), [PIP Lifecycle](PIP-Lifecycle-and-Legislative-Process.md), and [Governance Evidence States](Governance-Implementation-and-Evidence-States.md).

## Review status

This R1 institutional page is ready for canonical publication within its as-of boundary. It establishes the DAO's reviewed voting and authorization role without assigning Foundation, Council, treasury-account, or execution functions to the electorate.
