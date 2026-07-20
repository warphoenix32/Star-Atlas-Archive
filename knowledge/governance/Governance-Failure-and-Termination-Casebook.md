---
title: "Governance Failure and Termination Casebook"
seo_title: "Star Atlas Governance Failures, Cancellations, and Withdrawals"
seo_description: "Case studies of failed, terminated, canceled, withdrawn, superseded, and unverified Star Atlas PIPs without erasing their distinct vote histories."
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
  - "archive/source-records/social-governance-semantic-enrichment/governance/"
known_limitations:
  - "Post-vote reasons, milestone states, and payments are Council-authored operational assessments unless independently sourced."
  - "The Council tracker does not consistently preserve terminal-state dates."
research_gaps:
  - "Recover author withdrawal notices, Foundation implementation decisions, transactions, and deliverable records for every terminal case."
review_after: 2027-01-17
---

# Governance Failure and Termination Casebook

Governance initiatives can end at different stages. This casebook separates proposals rejected by voters from proposals that passed and were later terminated, canceled, withdrawn, superseded, or left without verified execution. The distinctions matter because a failed vote supplies no authority, while a terminated passed proposal remains part of constitutional and treasury history.

These cases are not grouped to assign blame. They are grouped because unsuccessful and incomplete initiatives reveal the system's operational boundaries: voter rejection, author withdrawal, administrator termination, policy replacement, and missing evidence are different events with different institutional meanings.

## Case taxonomy

| State | Meaning in this archive |
|---|---|
| `FAILED_VOTE` | The completed vote did not authorize the proposal. |
| `PASSED_THEN_TERMINATED` | The proposal passed, but the Council later reported a terminal implementation state. |
| `PASSED_THEN_WITHDRAWN` | The proposal passed, then the author withdrew it before implementation. |
| `SUPERSEDED` | A later instrument replaced the governing policy; the older vote remains historical. |
| `EXECUTION_UNVERIFIED` | Passage exists, but payment or implementation evidence is missing. This alone is not failure. |

## Failed votes: no PIP authorization

| PIP | Proposed action | Supported finding |
|---|---|---|
| [PIP-13](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-13-B721D8E7.json) | Council term limits | `FAILED_VOTE`; no term-limit rule entered force through this PIP. |
| [PIP-15](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-15-BD065AD2.json) | In-person community meetups platform | `FAILED_VOTE`; no funding authorization. |
| [PIP-19](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-19-1EB3D15E.json) | Independent economic research and data resources | `FAILED_VOTE`; no Ecosystem Fund award. |
| [PIP-26](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-26-B70AC545.json) | Crew Adventure Series | `FAILED_VOTE`; no production funding authorization. |

Derived tracker records sometimes normalize milestone cells such as `1/1` or `N/A` into completion-like states for these failed PIPs. Knowledge rejects that inference: implementation lifecycle is `NOT_APPLICABLE` because the vote supplied no authority. The raw tracker value remains preserved as a source conflict.

## Passed, then terminal

### PIP-14 — Deepening THEO Integration

[PIP-14](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-14-FED98016.json) passed. The Council tracker later reports `TERMINATED`, attributes the reason to non-performance, reports one of two milestones, 4,462,301 ATLAS paid, and 25,125,628.14 ATLAS remaining. These are Council-authored operational assessments, not independently verified transfers or deliverables. [Council row](../../archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-5AA7278EA3F455A3.json)

### PIP-17 — Star Atlas Ecosystem Media Expansion

[PIP-17](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-17-4DF4C199.json) passed. The Council tracker reports cancellation/termination for non-performance, zero of one milestones, and zero paid. The terminal date and independent evidence of notice are absent. [Council row](../../archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-BA1C2F2A01C7D040.json)

### PIP-31 — Star Seekers 2

[PIP-31](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-31-E71FB1A7.json) passed. The Council tracker says the author later withdrew the proposal and that it would not be implemented. This is `PASSED_THEN_WITHDRAWN`, not a failed vote. [Council row](../../archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-84B04A340610C0C9.json)

## Supersession case

PIP-4 passed and created the original Ecosystem Fund framework. PIP-23 later replaced it in full. Supersession changes which policy controls after the later proposal; it does not retroactively make PIP-4 a failed proposal or erase actions reported under it.

## Analytical lessons

1. Vote result and implementation lifecycle occupy different axes.
2. Payment can occur before termination and does not prove completed value.
3. Zero reported payment is not proof that no transaction occurred without an independent ledger.
4. Withdrawal after passage preserves the authorization event but ends the supported implementation path.
5. Failed proposals may remain historically important without becoming policy.
6. Council assessments must retain attribution:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

## Missing artifacts

For PIPs 14, 17, and 31, recover dated termination/withdrawal notices, author and Foundation correspondence, Council decisions, transaction IDs, recipient addresses, milestone submissions, acceptance/rejection records, refund records, and any surviving deliverables. For failed PIPs, recover final result announcements and later resubmissions without treating them as implementation.

## Review status

`QUALIFIED`. Vote states are supported by the captured portal. Post-vote terminal states remain attributed to the Council tracker.
