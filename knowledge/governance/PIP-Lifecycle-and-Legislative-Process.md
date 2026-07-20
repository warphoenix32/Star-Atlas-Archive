---
title: "PIP Lifecycle and Legislative Process"
seo_title: "Star Atlas PIP Process: From Proposal to Implementation"
seo_description: "A step-by-step guide to POLIS Improvement Proposals, voting mechanisms, passage, implementation, payment, and historical evidence states."
knowledge_status: CANONICAL
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 3
page_risk_class: R1
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
known_limitations:
  - "The captured framework does not provide complete operational records for every later proposal."
research_gaps:
  - "Recover versioned submission rules, administrative decisions, and proposal-specific execution records."
review_after: 2027-07-20
---

# PIP Lifecycle and Legislative Process

A POLIS Improvement Proposal, or PIP, is a governed request—not an automatic change to the Star Atlas ecosystem. Its history unfolds through documentary, voting, and operational stages, and each stage answers a different question. This page provides the vocabulary used throughout the archive so a reader can tell what was proposed, what voters decided, and what later evidence shows.

## From an idea to a public proposal

An author can begin with a draft or community discussion. At this point, no DAO decision exists. The proposal must then pass the administrative requirements described in the captured PIP-1 framework. The Foundation or its delegate may request revisions, reject a noncompliant submission with reasons, or advance a compliant text. [PIP-1 Source Record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

Publication makes the proposal available for review. It establishes the text, author, requested action, and—where preserved—the intended voting dates and mechanism. Publication is not endorsement and is not proof that the proposal's supporting factual claims are correct.

## Voting and result

During the voting stage, eligible POLIS voting power participates under the proposal's specified mechanism. The archive preserves PVP totals, ballot counts, and candidate totals where available because these fields are not interchangeable.

Binary proposals compare the applicable YES and NO voting power. The repository's completed-binary interpretation excludes abstaining PVP from that comparison, while preserving abstention in participation totals. That rule is an owner-approved curatorial adjudication used to reconcile completed captured votes; it is **not asserted as text contained in PIP-1**. Election proposals use their actual candidate-ranking or advancement mechanism instead of being forced into binary fields.

A completed result produces passage, failure, or an election outcome. Passage supplies authorization under the proposal. Failure supplies no implementation authority. An election advancement round may narrow the field without choosing officeholders.

## What happens after passage

Authorization begins, rather than ends, the operational history. A passed proposal may require legal review, a recipient address, an implementation plan, a software deployment, a payment, a milestone submission, or another institution's action. Each event needs its own evidence.

The archive uses the following sequence:

1. **PROPOSED** — a request exists.
2. **VOTING** — a decision process is open.
3. **PASSED or FAILED** — the mechanism produced a result.
4. **AUTHORIZED** — passage permits the action described by the proposal.
5. **IMPLEMENTATION_ANNOUNCED** — a responsible actor states that work will begin.
6. **PARTIAL_OR_IN_PROGRESS** — attributed evidence shows incomplete operational work.
7. **PAID or EXECUTED** — a specific transaction or action is evidenced.
8. **INDEPENDENTLY_VERIFIED** — separate primary evidence corroborates the claimed operation.

These stages are not automatic. A proposal may pass and later be withdrawn, canceled, terminated, superseded, or remain without verified execution. The historical vote is still preserved even when the later lifecycle changes.

## Mechanism-aware examples

PIP-6 was the first Council election's advancing round. Its top twelve continued to the next stage; they were not final Council members. PIP-7 identifies the five winners of the final round. Later election records can establish that an election proposal passed without preserving enough evidence to identify the winning candidates.

Funding proposals demonstrate a different boundary. PIP-23 authorized a replacement Ecosystem Fund framework, but a later project proposal still needs a passing result before it becomes an award. Even after an award, Council-reported payment or completion remains attributed until the transaction or deliverable is independently reconciled.

PIP-33 passed as a direct treasury authorization. Its two scheduled tranches remain payment terms until primary transfer evidence establishes execution.

## Reading the registry

The [PIP Registry](PIP-Registry.md) preserves proposal number, title, author, category, publication and vote dates, mechanism, result, supersession, authorization, implementation, payment state, reconciliation status, and open research questions. The [Governance Evidence States](Governance-Implementation-and-Evidence-States.md) defines how those fields should be interpreted, while the [Failure and Termination Casebook](Governance-Failure-and-Termination-Casebook.md) follows proposals that ended at different stages.
