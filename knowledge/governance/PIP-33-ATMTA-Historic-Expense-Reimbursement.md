---
title: "PIP-33 — ATMTA Historic Expense Reimbursement"
knowledge_status: PROVISIONAL
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 7
page_risk_class: R3
canonical_entity: GOVERNANCE-PIP-33
aliases:
  - "PIP-33"
  - "ATMTA Historic Expense Reimbursement"
first_seen: 2026-06-24
last_reviewed: 2026-07-17
source_priority:
  - A1
  - A2
  - A3
related_entities:
  - ATMTA
  - Michael Wagner
  - Star Atlas DAO
  - DAO Treasury
depends_on:
  - knowledge/governance/PIP-Registry.md
  - knowledge/economy/DAO-Treasury-Architecture.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"
  - "archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-D1DADF7EB8437119.json"
  - "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-AA9B47413B9C587D.json"
known_limitations:
  - "The expense, tax, invoice, runway, and supporting-document statements originate in the proposal and its author-provided appendices and are not independently audited by this repository."
  - "The Council tracker contains no populated payment fields for this proposal."
  - "Passage authorizes the proposal but does not prove either scheduled tranche was paid."
research_gaps:
  - "Reconcile both scheduled tranches to primary transactions and Foundation execution records."
  - "Independently review the cited tax calculation, Walkers services, Leeward invoice, reserve condition, and conflict-management process."
review_after: 2026-10-17
---

# PIP-33 — ATMTA Historic Expense Reimbursement

PIP-33 is a passed proposal authorizing a historic-expense reimbursement to ATMTA. It is an extraordinary direct DAO Treasury measure, not an Ecosystem Fund disbursement. Its passage, scheduled payment terms, and actual payment state remain separate.

The primary record is the official portal capture published on 2026-06-24 and updated later that day. The repository treats its expense descriptions, tax calculations, invoice schedules, and claimed business effect as statements submitted by the conflicted beneficiary, not independently audited facts.

## Proposal and disclosed conflict

The official proposal was authored by Michael Wagner on behalf of ATMTA and requested $469,513.53. It identified ATMTA as the sole beneficiary and disclosed the author's conflict of interest. The request comprised $318,092.47 for a tax obligation the proposal attributed to 2021 DAO R4-sale income of $1,533,271.51, $142,779.80 for Walkers services, and $8,641.26 for a Leeward invoice. Those descriptions and appendices are author-provided evidence; this repository does not independently validate the expenses. [SRC-PIP-33-397FEE39](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json)

The proposal attributes the tax component to applying ATMTA's stated 20.75% effective 2021 federal rate to $1,533,271.51 of December 2021 R4 ATLAS-sale income. Its Walkers appendix lists $226,999.80 in total invoices but identifies $142,779.80 as unreimbursed through this proposal; several later invoices are marked previously reimbursed. Its Leeward appendix lists one $8,641.26 invoice dated 2022-09-26. These are useful itemized claims, but the underlying tax return, complete transaction identifiers, invoices, and accounting workbooks are not independently reconciled in this knowledge campaign.

## Funding channel and schedule

The proposal describes itself as a `DAO Treasury` measure that exceeds the ordinary Ecosystem Fund limit. It specifies a 75% USDC and 25% ATLAS mix and two scheduled tranches of $234,756.76, with the second due 180 days later subject to the proposal's reserve protection. These are approved terms, not evidence that either transfer occurred.

| Scheduled component | Tranche 1 | Tranche 2 | Total approved basis |
|---|---:|---:|---:|
| USDC | $176,067.57 | $176,067.57 | $352,135.15 in the proposal's rounded total |
| ATLAS equivalent | $58,689.19 | $58,689.19 | $117,378.38 |
| Total USD-equivalent basis | $234,756.76 | $234,756.76 | $469,513.53 |

For each tranche, the proposal calls for the ATLAS amount to be calculated using a seven-day ATLAS/USDC VWAP on the preceding business day. The proposal names Birdeye or Jupiter TWAP as examples rather than preserving a final oracle record. Consequently, the authorized USD-equivalent basis does not establish an ATLAS token quantity. Tranche 2 is further limited to an amount that would retain enough DAO/Foundation capital for an additional year of operating costs, as assessed when due.

The displayed schedule contains one-cent rounding inconsistencies: two tranches of $234,756.76 sum to $469,513.52, while the proposal total is $469,513.53; two displayed USDC portions of $176,067.57 sum to $352,135.14, while the proposal's total table gives $352,135.15. The archive preserves the proposal's stated total and component values rather than silently correcting the approved instrument. Transaction reconciliation must determine the executed amounts.

## Vote result

The captured portal record contains 170,240,400.0117 YES PVP, 24,857,540.3494 NO PVP, and 83,860,459.5491 abstaining PVP. Under the reviewed binary rule, the result is `PASSED`. An official Discord acknowledgment on 2026-07-12 also described the proposal as passed and characterized participation as the highest PVP participation since DAO inception. The vote totals support the comparison within the captured PIP-1–33 corpus; the broader historical characterization remains an attributed statement. [SA-DISCORD-ANN-AA9B47413B9C587D](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-AA9B47413B9C587D.json)

The portal records 220 ballots: 141 YES, 59 NO, and 20 abstentions, totaling approximately 278,958,399.91 PVP. Ballot count is not the decision weight. The Council tracker reports approximately 279 million PVP and 37.63% participation but leaves its `vote_result` field null. That null means the tracker alone is insufficient for the result. The page therefore derives `PASSED` from the completed official vote record and uses the tracker only as attributed operational evidence.

## Approved implementation schedule

The proposal's relative schedule is conditional on passage and is not converted here into inferred calendar dates:

| Relative point | Proposed action | Archival state as of 2026-07-17 |
|---|---|---|
| T+7 | ATMTA confirms and publishes recipient treasury address. | Not independently identified. |
| T+14 | Foundation calculates VWAP, transfers tranche 1, and publishes confirmation. | Payment unverified. |
| T+194 | Foundation repeats the process for tranche 2, subject to the reserve condition, and publishes final confirmation. | Future/conditional and unverified. |

The proposal calls the documentation publication complete during its draft period. That is the author's milestone assertion, not this repository's confirmation that every supporting document was captured or audited.

## Implementation state

As of 2026-07-17, the Council tracker semantic record has no populated payment fields and retains `independent_verification_status: UNKNOWN`. The supported state is therefore `IMPLEMENTATION_PENDING` / `PAYMENT_UNVERIFIED`, not paid or completed. [Council tracker semantic records](../../operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl)

The tracker also records `ecosystem_fund: NO`, category `DAO Treasury`, an amount of 469,513.53 USDC, and no completed or total milestones. A separate semantic funding-source label elsewhere in the campaign identifies the Ecosystem Fund; because it contradicts both the primary proposal and tracker, that label is rejected for knowledge promotion and preserved as a research/audit defect.

## Evidence interpretation

- Proposal publication establishes the request and disclosed terms.
- Vote totals establish the reviewed passing result.
- The scheduled tranches establish intended timing, not transfer.
- Proposed Council or Foundation verification controls do not prove that verification occurred.
- No statement here independently validates the underlying expense claims.
- The proposal's estimate that reimbursement would extend ATMTA runway by 6–12 months is a beneficiary-authored forecast, not a verified outcome.
- Passage does not resolve whether the disclosed conflict mitigations were performed, whether the Foundation accepted the documentation, or whether any recipient address or transaction was published.

## Research checklist

- locate the published recipient address and Foundation execution notice;
- reconcile each USDC and ATLAS transfer to the DAO Treasury address and recipient;
- preserve the exact VWAP source, observation window, price, and resulting ATLAS quantity for each tranche;
- verify the second-tranche reserve calculation and whether the condition reduced or deferred payment;
- audit the cited tax return, Walkers invoices, Leeward invoice, and prior reimbursement markings;
- document Council verification and conflict-management steps separately from the beneficiary's assertions.
