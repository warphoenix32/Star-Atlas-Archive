---
title: "Governance Implementation and Evidence States"
seo_title: "Star Atlas Governance Evidence: Passage, Payment, and Execution"
seo_description: "The evidence model used to distinguish Star Atlas proposal publication, voting, authorization, payment, implementation, and independent verification."
knowledge_status: CANONICAL
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 3
page_risk_class: R1
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
known_limitations:
  - "Evidence-state labels describe what the repository can establish, not whether an undocumented event occurred."
research_gaps:
  - "Independent execution and payment evidence remains incomplete for several passed proposals."
review_after: 2027-07-20
---

# Governance Implementation and Evidence States

Governance history is vulnerable to a simple but consequential error: treating a successful vote as proof that the promised work happened. The Star Atlas Archive avoids that collapse by recording legislative, administrative, financial, and verification states separately.

The model is not a judgment about whether a project was good or bad. It is a statement about what the preserved evidence can establish.

## The evidence ladder

| State | What the evidence establishes | What remains unproven |
| --- | --- | --- |
| `PROPOSED` | An authored request was published. | Voting, approval, factual accuracy, or execution. |
| `VOTING` | A decision process opened under a stated mechanism. | The completed result. |
| `PASSED` / `FAILED` | The applicable vote produced a result. | Payment, deployment, completion, or outcome. |
| `AUTHORIZED` | A passing result permits the proposal's stated action, subject to applicable institutional boundaries. | That any responsible actor performed the action. |
| `IMPLEMENTATION_ANNOUNCED` | An identified institution stated that implementation would begin or had begun. | Completion or independent confirmation. |
| `PARTIAL_OR_IN_PROGRESS` | Attributed operational evidence describes incomplete work. | Full delivery. |
| `PAID` | A specific payment record has been identified and reconciled to the proposal. | Successful work, correct accounting, or intended outcome. |
| `EXECUTED` | A concrete action, deployment, transfer, or accepted milestone is evidenced. | Every promise or downstream effect. |
| `TERMINATED` / `CANCELED` / `WITHDRAWN` | Later evidence ended or withdrew the implementation path. | Reversal of the historical vote. |
| `SUPERSEDED` | A later instrument replaced the governing policy. | Erasure of the older policy's historical period. |
| `INDEPENDENTLY_VERIFIED` | A separate primary artifact corroborates the claimed operation within its scope. | Universal correctness beyond that evidence. |

## Authority, implementation, and outcome are different questions

A vote answers whether the electorate approved the proposal under its mechanism. An implementation notice answers what an institution said it would do. A transaction answers whether assets moved between identified accounts. A deliverable or deployment record answers whether a particular operation occurred. Outcome evidence asks whether the operation achieved its stated purpose.

One artifact rarely answers every question. A treasury transaction can prove payment without proving a milestone's quality. A working product can prove availability without proving that it contains every roadmap feature. A Council tracker can preserve the Council's assessment without functioning as independent verification.

## Council tracker treatment

Council tracker statements are preserved with a durable qualification:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

The tracker may be the most specific surviving account of milestones, payments, termination, cancellation, or non-implementation. Its institutional authorship makes it valuable evidence, but a self-reported operational state is not transformed into an independent finding by inclusion in the archive.

For example, the tracker reports that PIP-14 was terminated after passage, that PIP-17 was canceled, and that PIP-31 was withdrawn and not implemented. Those are supported Council-attributed lifecycle findings. Independent confirmation would require the relevant notices, correspondence, transactions, deliverables, or other primary records.

## Payment vocabulary

Treasury pages use a deliberately narrow vocabulary:

- `REQUESTED` — the proposal asks for assets.
- `AUTHORIZED` — a passing result permits the payment under the proposal's terms.
- `COUNCIL_REPORTED` — the Council tracker reports an amount or payment state.
- `UNVERIFIED` — no primary transfer evidence has been reconciled.
- `MISSING_ONCHAIN_EVIDENCE` — the question specifically requires a transaction dataset or signature that is not present.

These states prevent requested and approved values from appearing as paid amounts. They also prevent a Council-reported payment from being presented as on-chain verified when no transaction has been reconciled.

## Absence, conflict, and stale records

“No independent evidence identified” is a finding about the repository's current holdings, not proof that an event never occurred. Portal status can also become stale: a page may retain “passed” even after a later cancellation or supersession. The archive preserves both records, dates them, and explains their relationship.

When sources conflict, the preferred response is not silent correction. The ledger records the source-native values, identifies the conflict, applies the narrowest supported interpretation, and adds the missing artifact to the research backlog.

## Applying the model

Use the [PIP Lifecycle](PIP-Lifecycle-and-Legislative-Process.md) to understand the decision process, the [PIP Registry](PIP-Registry.md) for proposal-level states, the [Treasury Authorization and Payment Ledger](../economy/Treasury-Authorization-and-Payment-Ledger.md) for funding claims, and the [Failure and Termination Casebook](Governance-Failure-and-Termination-Casebook.md) for proposals whose later lifecycle diverged from their vote result.
