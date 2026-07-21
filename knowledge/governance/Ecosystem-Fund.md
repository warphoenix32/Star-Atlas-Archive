---
title: "Star Atlas Ecosystem Fund"
seo_title: "Star Atlas Ecosystem Fund: PIP-4, PIP-23, and Funding Rules"
seo_description: "The history and operating rules of the Star Atlas Ecosystem Fund, including PIP-23 supersession, reserve limits, Council duties, and payment evidence boundaries."
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"
  - "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"
known_limitations:
  - "Current-state statements are date-bound."
  - "Absence of evidence is not evidence of non-occurrence."
research_gaps:
  - "Independent execution evidence remains incomplete where explicitly noted."
review_after: 2027-01-15
---

# Star Atlas Ecosystem Fund

The Ecosystem Fund is a bounded DAO treasury allocation and proposal process for financing ecosystem work. Its controlling captured framework is PIP-23, which replaces PIP-4 in full. It is neither the whole DAO Treasury nor a separate legislature, and a PIP's passage does not prove payment or completion.

Its historical role is to translate DAO authority into a repeatable route for community projects. That route constrains who may request funds, how much may be committed, what reserves must remain, which institution administers the program, and what later evidence is needed before an award can be described as paid or complete.

## Policy history

PIP-4 proposed the original fund, including a budget linked to 20% of the DAO treasury and a stated USD limitation. Its official vote capture records 421 YES ballots carrying 81,843,902.51 PVP, 33 NO ballots carrying 14,242,581.32 PVP, and six abstentions carrying 203,935.94 PVP. The proposal text says an approved fund would remain until modified, revoked, or exhausted; it does not prove the initial allocation occurred. [PIP-4; SRC-PIP-04-AD1945D8](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-04-AD1945D8.json)

PIP-23, published on 2025-11-03 by the second Star Atlas Council, continued the fund and expressly replaced PIP-4 in its entirety. Its capture records 77 YES ballots carrying 86,030,422.03 PVP, 34 NO ballots carrying 24,262,645.41 PVP, and six abstentions carrying 792,710.92 PVP. Historical references to PIP-4 remain useful for the fund's origin, but policy interpretation as of 2026-07-17 begins with PIP-23. [PIP-23; SRC-PIP-23-0ECF2928](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

## Wallets and allocation formula

PIP-23 identifies:

- DAO Treasury: `CuwnarNh7FEqZMmffFjRyWj54RecyS7zwFg1CxfzNudi`;
- Ecosystem Fund: `BxKehkp298nQunu8BWxh5U6VvfphFyjEB3t7USst7Uag`.

The initial and continuous allocation model targets 20% of combined eligible assets in the fund, subject to separate asset rules. For ATLAS, PIP-23 states no corresponding reserve limitation. For USDC, only 20% of the amount above a USD 500,000 DAO-treasury threshold is allocated; if the DAO Treasury holds USD 500,000 or less in USDC, no USDC is allocated. The proposal calls for quarterly review on or about March 31, June 20, September 30, and December 31.

Funding applications must state their request in USDC, while the fund pays only in ATLAS; the text also calls for received USDC to be converted to ATLAS in a timely manner while USDC remains an insignificant treasury component. No single Ecosystem Fund PIP may exceed 5% of the `Balance After` value from the last refill transaction or run longer than 12 months. The 5% ceiling therefore changes with the last refill balance; it is not 5% of the proposal's requested amount or of an unqualified current treasury balance. [PIP-23; SRC-PIP-23-0ECF2928](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

## Application and institutional roles

Applicants remain subject to PIP-1's drafting process and the additional DAO knowledge-base requirements cited by PIP-23. A proposal must identify the people or entities involved, describe outputs and audience, explain ecosystem benefit, disclose conflicts, specify milestones and deliverables, provide a timeline, and itemize a USDC-denominated budget. Scope examples include player tools, events, education, community information, and creative work; examples are not proof that any specific project qualifies.

The Council's specified duties are to review and steward eligible proposals, coordinate special approval where needed, implement passed PIPs, and track payments. The same text says the Council does not authorize legally binding contracts, execute fund-refill transactions, conduct KYC/KYB, or approve a PIP before voting. These are policy assignments, not proof that a particular transfer occurred.

The Foundation and DAO therefore retain distinct roles. POLIS holders approve or reject a PIP through the applicable voting process; the Council administers the program within delegated bounds; the Foundation provides legal and administrative implementation and wallet controls where supported. None of those roles permits this archive to infer payment from approval.

## Reported refill history

PIP-23 reports two fund-refill transactions in its own proposal text:

| Reported date | Reported transfer | Additional claim in PIP-23 | Evidence status |
|---|---:|---|---|
| 2024-10-04 | 159,713,142 ATLAS | Initial allocation; stated day-of-transfer value USD 517,609.53; no initial USDC because the treasury reportedly held less than USD 500,000 USDC. | Transaction link supplied in PIP-23; not independently reconciled in this campaign. |
| 2025-07-03 | 87,551,239 ATLAS | Refill from a reported balance before of 136,543,091 ATLAS to a balance after of 224,094,330 ATLAS; proposal example derives an 11,204,716.50 ATLAS 5% ceiling. | Transaction link and calculation supplied in PIP-23; not independently reconciled in this campaign. |

These are attributed refill reports with primary transaction references embedded in an official proposal. They are stronger than an unsupported summary but do not, without transaction inspection, establish signer authority, transfer interpretation, recipient payments, or completed work.

[PIP-33](PIP-33-ATMTA-Historic-Expense-Reimbursement.md) is outside this mechanism. Its proposal expressly requests a direct DAO Treasury measure exceeding the ordinary Ecosystem Fund limit, and the Council tracker semantic record marks `ecosystem_fund: NO`. It must not be used when calculating or describing Ecosystem Fund recipient activity. [Council tracker semantic records](../../operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl)

## Decision and payment boundaries

An approved grant proposal authorizes an action under the applicable policy. It does not by itself establish that funds were transferred, milestones were accepted, or deliverables were completed. Council tracker fields are retained as attributed operational assessments:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

## Current state

As of 2026-07-17, PIP-23 is the supported superseding policy. Its two reported refill references do not independently verify the refills, recipient payments, or deliverables, which remain incomplete for many funded PIPs.

## Research priorities

- verify both refill transactions, token mint, source and destination wallets, block times, and exact quantities;
- reconstruct each refill's `Balance Before`, `Balance After`, and resulting 5% ceiling;
- reconcile every Council-reported Ecosystem Fund payment to primary transactions;
- distinguish ATLAS paid, USDC requested, USD-equivalent proposal values, and contemporaneous conversion prices;
- verify milestones and deliverables separately from payment;
- document any later PIP that modifies or revokes PIP-23.

## Evidence references

- [PIP registry](PIP-Registry.md)
- [PIP-23 source record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

## Review status

This R2 page is ready for publication as a qualified policy history. PIP-23's approval and supersession of PIP-4 are preserved separately from awards, reported payments, transaction verification, milestone acceptance, and independent outcome evidence.
