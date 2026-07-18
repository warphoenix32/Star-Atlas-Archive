---
title: "Star Atlas PIP Registry"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/"
known_limitations:
  - "Current-state statements are date-bound."
  - "Absence of evidence is not evidence of non-occurrence."
research_gaps:
  - "Independent execution evidence remains incomplete where explicitly noted."
review_after: 2027-01-15
---

# Star Atlas PIP Registry

The PIP Registry is the evidence-qualified index of the 33 proposals captured on `main` as of 2026-07-17. It preserves proposal, vote, result, supersession, election meaning, Council-reported lifecycle, execution evidence, and research gaps as separate fields.

The registry is a finding aid, not a substitute for the proposal text or a transaction ledger. Its coverage begins with numbered PIP-1 and ends with PIP-33 because those are the numbered official portal captures available to this campaign. Draft, withdrawn, or unnumbered tracker rows are not silently promoted into the numbered registry.

## Interpretation

`Result` is the reviewed vote or election result. `Council-reported lifecycle` is an attributed operational assessment, not independent verification:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

Results are derived from the official portal capture's completed voting data and the applicable mechanism. Binary PIPs compare YES and NO PVP while preserving abstentions and ballot counts; elections require proposal-specific interpretation. The portal's generic status string is not treated as an implementation state. Council tracker fields supply useful operational context, but their milestone, payment, and ROI fields retain Council attribution.

## Coverage summary

- 33 numbered proposals are captured.
- PIP-13, PIP-15, PIP-19, and PIP-26 failed and therefore supplied no PIP authorization.
- PIP-14 later has a Council-reported terminated state; PIP-17 a canceled/terminated state; PIP-31 was withdrawn after passage and reported not implemented.
- PIP-4 is historically preserved but superseded in full by PIP-23.
- PIP-6 records first-round advancing candidates, while PIP-7 records the final first-Council election.
- Winner identity remains unresolved in this archive for PIP-11, PIP-25, and PIP-27.
- PIP-33 passed as a direct DAO Treasury measure; payment remains unverified.

## Captured proposals

| PIP | Title | Result | Mechanism/category | Council-reported lifecycle | Qualification |
|---|---|---|---|---|---|
| [PIP-1](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json) | Star Atlas DAO | PASSED | Process | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-2](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json) | Star Atlas Foundation | PASSED | Process | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-3](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json) | Star Atlas Council | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-04-AD1945D8.json) | Star Atlas Ecosystem Fund | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Superseded by PIP-23. |
| [PIP-5](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-05-C248D280.json) | Co-Sponsor the Naabathon | PASSED | FUNDING | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-6](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-06-1B792551.json) | Council Election #1 — First Round | PASSED | COUNCIL | MILESTONES_REPORTED_COMPLETE | First-round advancing candidates; not final winners. |
| [PIP-7](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-07-91652743.json) | Council Election #1 — Second Round | PASSED | COUNCIL | MILESTONES_REPORTED_COMPLETE | Final first-Council election; winners identified. |
| [PIP-8](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-08-62506041.json) | Star Atlas Comet at Gamescom 2025 | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-9](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-09-1CC4BB6F.json) | Adjust STV Backup Vote Handling | PASSED | DAO | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-10](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-10-ED887A4E.json) | Council: Second Term & Beyond | PASSED | Council | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-11](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-11-7B48A62D.json) | Council Election #2 | PASSED | COUNCIL | MILESTONES_REPORTED_COMPLETE | Council-reported passage; winners unresolved. |
| [PIP-12](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-12-F15380C9.json) | Iris's Bounty: The Feast | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-13](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-13-B721D8E7.json) | Council Term Limits | FAILED | DAO, COUNCIL | MILESTONES_REPORTED_COMPLETE | Failed; no PIP authorization exists. The tracker value is preserved as attributed source data but rejected as an implementation state. |
| [PIP-14](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-14-FED98016.json) | Deepening THEO Integration | PASSED | Funding | TERMINATED | Passed; Council tracker later reports termination. |
| [PIP-15](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-15-BD065AD2.json) | In-Person Community Meetups Platform | FAILED | Funding | MILESTONES_REPORTED_COMPLETE | Failed; no PIP authorization exists. The tracker value is preserved as attributed source data but rejected as an implementation state. |
| [PIP-16](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-16-B11CED4B.json) | Ryden Systems | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-17](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-17-4DF4C199.json) | Star Atlas Ecosystem Media Expansion | PASSED | Funding | TERMINATED | Passed; Council tracker later reports cancellation/termination. |
| [PIP-18](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-18-18750A6A.json) | Gamescom Marketing & Merch Expansion | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-19](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-19-1EB3D15E.json) | Independent Economic Research and Data Resources | FAILED | Funding | MILESTONES_REPORTED_COMPLETE | Failed; no PIP authorization exists. The tracker value is preserved as attributed source data but rejected as an implementation state. |
| [PIP-20](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-20-159CB743.json) | DAO Casters Program | PASSED | Funding | PARTIAL_OR_IN_PROGRESS | Council lifecycle remains attributed; verify execution independently. |
| [PIP-21](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-21-49CAD7E4.json) | Rogue Data Hub | PASSED | Funding | PARTIAL_OR_IN_PROGRESS | Council lifecycle remains attributed; verify execution independently. |
| [PIP-22](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-22-D5D61E64.json) | Iris's Bounty: The Arena | PASSED | Funding | PARTIAL_OR_IN_PROGRESS | Council lifecycle remains attributed; verify execution independently. |
| [PIP-23](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json) | Refresh of PIP-4 | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Supersedes PIP-4. |
| [PIP-24](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-24-8CC6B298.json) | DAO-Supported Hosting for SLY Assistant | PASSED | Funding | MILESTONES_REPORTED_COMPLETE | Council lifecycle remains attributed; verify execution independently. |
| [PIP-25](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-25-91CC73FA.json) | Council Election #3 | PASSED | COUNCIL | MILESTONES_REPORTED_COMPLETE | Council-reported passage; winners unresolved. |
| [PIP-26](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-26-B70AC545.json) | Crew Adventure Series | FAILED | Funding | MILESTONES_REPORTED_COMPLETE | Failed; no PIP authorization exists. The tracker value is preserved as attributed source data but rejected as an implementation state. |
| [PIP-27](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-27-064D252C.json) | DAO Casters Election: Term 1 | PASSED | GOVERNANCE | MILESTONES_REPORTED_COMPLETE | Council-reported passage; winners unresolved. |
| [PIP-28](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-28-D0A5DC75.json) | Temporary Funding for Lore, Design, and Community Functions | PASSED | Funding | PARTIAL_OR_IN_PROGRESS | Council lifecycle remains attributed; verify execution independently. |
| [PIP-29](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-29-8E761702.json) | Star Atlas Relay Program | PASSED | Funding | UNKNOWN | Council lifecycle remains attributed; verify execution independently. |
| [PIP-30](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-30-3BA029F2.json) | ATOM Cloud Infrastructure Sustainability | PASSED | Funding | UNKNOWN | Council lifecycle remains attributed; verify execution independently. |
| [PIP-31](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-31-E71FB1A7.json) | Star Seekers 2 Mobile Game | PASSED | Funding | NOT_IMPLEMENTED | Passed, later withdrawn after passage; Council tracker reports not implemented. |
| [PIP-32](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-32-0B04FF9B.json) | Star Atlas Triad Tournament | PASSED | Funding | UNKNOWN | Council lifecycle remains attributed; verify execution independently. |
| [PIP-33](PIP-33-ATMTA-Historic-Expense-Reimbursement.md) | ATMTA Historic Expense Reimbursement | PASSED | Direct DAO Treasury | UNKNOWN | Passed direct-treasury measure; not an Ecosystem Fund PIP. Knowledge qualification: implementation pending and payment unverified as of 2026-07-17. |

## Registry rules

- Publication establishes a proposal, not approval.
- Passage establishes a DAO result, not payment or implementation.
- PIP-6 advancing candidates are not PIP-7's final winners.
- PIP-11, PIP-25, and PIP-27 retain unresolved winner identity.
- PIP-14, PIP-17, and PIP-31 preserve their passing vote and later Council-reported terminal state.
- PIP-23 supersedes PIP-4 without erasing PIP-4's historical record.
- Failed proposals do not acquire implementation milestones. For PIP-13, PIP-15, PIP-19, and PIP-26, the raw tracker value remains visible in its attributed column; implementation lifecycle does not apply because the vote supplied no authorization.
- [PIP-33](PIP-33-ATMTA-Historic-Expense-Reimbursement.md) is a direct DAO Treasury authorization; passage and scheduled tranches do not prove payment.

## Reconciliation exceptions

| Issue | Evidence conflict | Knowledge treatment |
|---|---|---|
| Failed-PIP milestones | Tracker-derived semantic records display `MILESTONES_REPORTED_COMPLETE` for PIP-13, PIP-15, PIP-19, and PIP-26 even though their official vote result is failed. | Preserve the attributed raw value in the table, but state in prose that implementation lifecycle does not apply because the failed vote supplied no authorization. Do not infer funded work. |
| PIP-33 funding source | A derived semantic label associates PIP-33 with the Ecosystem Fund; the proposal states `DAO Treasury`, says it exceeds the fund cap, and the Council tracker says `ecosystem_fund: NO`. | Classify PIP-33 as a direct extraordinary DAO Treasury measure and retain the derived label as a rejected conflict. |
| PIP-33 tracker result | Council tracker `vote_result` is null although portal totals satisfy the reviewed binary rule and an official Discord post calls it passed. | Use the completed portal record for `PASSED`; retain the tracker null as an operational-data gap. |
| Generic portal status | Captured proposal objects use a status value that does not cleanly express completed vote and implementation lifecycle. | Separate publication/status metadata, vote arithmetic, Council lifecycle, and implementation evidence rather than treating one field as authoritative for all states. |
| Council completion claims | Numerous passed PIPs have Council-reported `1/1` milestones or ROI text without linked primary transaction/deliverable evidence in this campaign. | Attribute the assessment and keep independent verification `UNKNOWN` until proposal-specific reconciliation. |

## Research workflow

For each proposal selected for deeper promotion, researchers should inspect the source record, raw portal capture, Council tracker row, official announcements, and any primary transaction or deliverable evidence. The minimum record should preserve publication and vote dates, author, mechanism, PVP and ballot totals, result, funding denomination, supersession, implementation state, payment state, conflicts, and unresolved evidence. Later correction must append or revise the knowledge interpretation without rewriting preserved evidence.

## Evidence references

- [Structured PIP registry](../../archive/semantic/governance/pip-registry-semantic.json)
- [PIP source reconciliation](../../archive/semantic/governance/pip-source-reconciliation.json)
- [PIP lifecycle](PIP-Lifecycle-and-Legislative-Process.md)
