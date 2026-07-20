---
title: "Star Atlas Council"
seo_title: "Star Atlas Council: Elections, Governance Role, and Evidence"
seo_description: "A documented history of the Star Atlas Council, its election process, delegated governance duties, and the limits of Council-reported assessments."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: MEDIUM
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json"
  - "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
known_limitations:
  - "Later captured election records do not identify every final winner or seating change."
  - "Council tracker lifecycle and payment statements are Council-authored operational assessments unless independently corroborated."
research_gaps:
  - "Acquire complete later-election tallies, seating and replacement records, term dates, and independent program execution evidence."
review_after: 2027-01-20
---

# Star Atlas Council

The Star Atlas Council is the elected steward of the Star Atlas DAO's governance process. Its documented purpose is practical rather than sovereign: help proposal authors, sustain governance operations, administer delegated programs, and perform milestone or payment review when an approved policy assigns that work.

The Council does not replace POLIS holders as the legislative electorate, and it is distinct from the [Star Atlas Foundation](Star-Atlas-Foundation.md). Its records are valuable evidence of governance operations, but the archive preserves who made each assessment and whether independent corroboration exists.

## Constitutional origin

[PIP-3](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json) established the Council framework in the captured proposal corpus. Read with PIP-1 and PIP-2, it places the Council inside a divided institutional model: the DAO votes, the Foundation supplies legal and administrative implementation capacity, and the Council supports the process and performs delegated work.

This is why descriptions such as “the Council approved the law” can be misleading. Unless a proposal grants a specific Council decision, formal passage belongs to the applicable PVP-weighted DAO vote. Council action after passage must be described as administration, assessment, delegation, or implementation according to the source.

## Election history

The first captured Council election used more than one stage. PIP-6 selected twelve candidates to advance. Those candidates were not yet Council members. PIP-7 conducted the final round and identifies the five elected members. Conflating the two rounds would turn an intermediate result into a final officeholder record.

Later election PIPs 11 and 25 are preserved as passed, but their captured portal records do not establish the final winner identities. PIP-27 presents a similar limitation for the DAO Casters election. The archive therefore records the election event without inventing a roster. The full mechanism-aware account appears in [Council Election History](Council-Election-History.md).

## Governance operations

Council work described across the preserved evidence includes proposal-author support, public process stewardship, election or program administration, and review of funded-project milestones or payments where delegated. The scope is proposal-specific. A duty established for the Ecosystem Fund, for example, should not be generalized into unlimited control over all DAO Treasury activity.

The Council tracker is especially useful because it records later operational states that may not appear on the original proposal page: milestones, reported amounts paid, remaining balances, termination, cancellation, or withdrawal. Those records preserve institutional memory after the vote.

## How Council assessments are cited

The tracker is also a self-authored operational record. Knowledge pages therefore preserve this qualification:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

“The Council tracker reports completion” is a supported attribution. “The project was independently completed” requires separate deliverable, acceptance, transaction, or deployment evidence. The same rule applies to payments and terminal states.

This distinction does not dismiss Council evidence. It tells the reader precisely what that evidence is capable of proving: the Council recorded an institutional assessment at the captured time. The [Governance Implementation and Evidence States](Governance-Implementation-and-Evidence-States.md) explains how later evidence can strengthen or qualify that finding.

## Current state and open questions

As of 2026-07-20, the archive supports the Council's establishment, first-election structure, process-steward role, and existence of delegated program administration. It does not yet support a complete current membership roster or an independently verified operational history for every program in the tracker.

The highest-value missing artifacts are final later-election results, appointment and replacement notices, term dates, Council resolutions, milestone submissions, payment approvals, transaction signatures, and independent outcome evidence. Until those are acquired, unresolved membership and implementation questions remain visible rather than inferred.
