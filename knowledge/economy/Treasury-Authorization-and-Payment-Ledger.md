---
title: "Treasury Authorization and Reported Payment Ledger"
seo_title: "Star Atlas Treasury Authorization and Payment Evidence Ledger"
seo_description: "A source-linked ledger separating Star Atlas DAO spending proposals, authorization, Council-reported payments, implementation, and independent verification."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: MEDIUM
page_risk_score: 8
page_risk_class: R3
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
  - "archive/raw/governance/council-pip-tracker/Star_Atlas_DAO_Council_PIP_Tracker_and_Grading_Rubric.xlsx"
  - "archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.json"
known_limitations:
  - "The ledger preserves Council-reported payments but has not independently reconciled most values to transactions."
  - "Mixed ATLAS, USDC, USD, and EUR values cannot be added without dated conversion and transaction evidence."
research_gaps:
  - "Recover transaction signatures, recipient wallets, payment dates, token mints and decimals, and conversion records for every reported disbursement."
  - "Verify current DAO Treasury and Ecosystem Fund balances and signer authority on-chain."
review_after: 2026-10-17
---

# Treasury Authorization and Reported Payment Ledger

This ledger separates what the DAO authorized from what the Star Atlas Council later reported as paid. It is not a verified general ledger. Proposal text and completed vote records are primary evidence for authorization; the Council tracker is an attributed operational assessment whose payment, milestone, and remaining-balance fields require transaction-level reconciliation.

## Ledger vocabulary

| Field | Meaning |
|---|---|
| `REQUESTED` | Amount or authority requested in proposal text. |
| `AUTHORIZED` | Proposal passed under the reviewed vote mechanism. |
| `FOUNDATION_ACTION` | Separate implementation action, when preserved. |
| `COUNCIL_REPORTED_PAID` | Amount entered in the Council tracker; not independently verified. |
| `TRANSACTION_VERIFIED` | Asset movement independently reconciled to a primary transaction. |
| `DELIVERABLE_VERIFIED` | Deliverable existence and acceptance independently reviewed. |

No entry in this page currently reaches both `TRANSACTION_VERIFIED` and `DELIVERABLE_VERIFIED`.

## How to read an entry

Each row answers a deliberately narrow question. The instrument and purpose describe what voters were asked to authorize. The vote state records the decision produced by the applicable mechanism. Payment fields reproduce an attributed operational report when one exists. Verification fields state whether the Archive has connected that report to a primary transaction or independently reviewed the deliverable.

This structure allows a proposal to be historically significant even when later evidence is incomplete. It also prevents a blank payment field from becoming an assertion that no payment occurred, or a `complete` tracker label from becoming an unqualified claim that a project achieved its intended outcome.

## Treasury architecture boundary

The [treasury architecture](DAO-Treasury-Architecture.md) contains multiple named components. The **DAO Treasury account** is `CuwnarNh7FEqZMmffFjRyWj54RecyS7zwFg1CxfzNudi`; the **Ecosystem Fund wallet** is `BxKehkp298nQunu8BWxh5U6VvfphFyjEB3t7USst7Uag`. Lockers, emissions, sales, and fund wallets are not aliases of the DAO Treasury account.

## Direct DAO Treasury and constitutional authorizations

| Instrument | Authorized purpose | Vote state | Payment evidence |
|---|---|---|---|
| [PIP-2](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json) | Annual Foundation basic-operations budget capped at USD 100,000; excess requires separate approval | `PASSED` | Tracker USDC-paid value is `?`; no amount promoted. |
| [PIP-5](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-05-C248D280.json) | Naabathon co-sponsorship | `PASSED` | Council reports 6,000,000 ATLAS; transaction unverified. |
| [PIP-28](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-28-D0A5DC75.json) | Temporary lore, design, and community-function funding | `PASSED` | Tracker does not provide a reconciled payment amount in this campaign. |
| [PIP-33](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json) | USD 469,513.53 historic ATMTA expense reimbursement in two displayed tranches of USD 234,756.76; each tranche is 75% USDC and 25% ATLAS; tranche 2 is scheduled 180 days later and reserve-conditional | `PASSED` | All tracker payment fields null; `PAYMENT_UNVERIFIED`. |

PIP-33 must not be relabeled as an Ecosystem Fund award. Its primary text identifies a direct, extraordinary DAO Treasury measure exceeding the ordinary fund cap, and the Council tracker marks `ecosystem_fund: NO`. [PIP-33 case study](../governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md)

The preserved vote export now establishes the completed ballot result independently of the proposal portal's display: 220 effective wallets cast 141 YES, 59 NO, and 20 abstain ballots. The normalized totals are 170,240,400.01174 YES PVP, 24,857,540.34942 NO PVP, and 83,860,459.54910 abstain PVP. Under the repository's owner-approved completed-binary adjudication—YES PVP greater than NO PVP, with abstentions reported but non-decisive—the result is `PASSED`, with YES representing 87.25894% of decisive PVP. This evidence confirms the vote outcome only. The capture did not replay Solana transaction signatures and contains no payment or implementation evidence. [PIP-33 vote source record](../../archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.md)

Each displayed tranche decomposes into USD 176,067.57 USDC and USD 58,689.19 in ATLAS-equivalent value. The schedule contains two preserved one-cent discrepancies: the two tranche totals add to USD 469,513.52 rather than the stated USD 469,513.53 total, and the two displayed USDC portions add to USD 352,135.14 rather than the stated USD 352,135.15 USDC total. The ATLAS-equivalent portions reconcile at USD 117,378.38. These differences are not silently normalized. Neither the approved schedule nor the asset composition proves that either tranche was transferred.

## Ecosystem Fund authorization and reported-payment ledger

| PIP | Authorized initiative | Council-reported paid | Council-reported remaining/lifecycle | Verification status |
|---|---|---:|---|---|
| [8](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-08-62506041.json) | Gamescom 2025 community meetup | 7,723,034 ATLAS | Complete | `UNKNOWN` |
| [12](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-12-F15380C9.json) | Iris’s Bounty: The Feast | 7,429,420 ATLAS | Complete | `UNKNOWN` |
| [14](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-14-FED98016.json) | THEO integration | 4,462,301 ATLAS | 25,125,628.14 ATLAS remaining; terminated; 1/2 milestones | `UNKNOWN` |
| [16](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-16-B11CED4B.json) | Ryden Systems | 8,464.79 USDC **and** 7,985,657 ATLAS | Complete | `UNKNOWN`; denomination relationship unresolved |
| [17](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-17-4DF4C199.json) | Ecosystem Media Expansion | 0 | Terminated/canceled; 0/1 milestones | `UNKNOWN` |
| [18](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-18-18750A6A.json) | Gamescom marketing and merch | 5,781,393 ATLAS | Complete | `UNKNOWN` |
| [20](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-20-159CB743.json) | DAO Casters program | 4,320,000 ATLAS | 5,400,000 ATLAS remaining; partial/in progress | `UNKNOWN` |
| [21](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-21-49CAD7E4.json) | Rogue Data Hub | 2,083 USDC **and** 7,317,073 ATLAS | 35,225,130.9 ATLAS remaining; partial/in progress | `UNKNOWN`; denomination relationship unresolved |
| [22](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-22-D5D61E64.json) | Iris’s Bounty: The Arena | 2,000,000 ATLAS | 9,000,000 ATLAS remaining; partial/in progress | `UNKNOWN` |
| [24](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-24-8CC6B298.json) | SLY Assistant hosting | `?` | Complete | `UNKNOWN`; amount missing |
| [29](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-29-8E761702.json) | Relay Program pilot | 13,143,639 ATLAS | Lifecycle unknown | `UNKNOWN` |
| [30](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-30-3BA029F2.json) | ATOM cloud infrastructure | 1,650 USDC **and** 6,433,164 ATLAS | 6,710,475 ATLAS remaining; lifecycle unknown | `UNKNOWN`; denomination relationship unresolved |
| [31](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-31-E71FB1A7.json) | Star Seekers 2 | None established | Withdrawn after passage; not implemented | `UNKNOWN` |
| [32](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-32-0B04FF9B.json) | Triad Tournament | None established | Lifecycle unknown | `UNKNOWN` |

Values are transcribed from Council tracker semantics and are not summed. The workbook is preserved at SHA-256 `6a477ee0ce428df4f04cd32b4a24bfb21b80bfa23341be38b192d2e4b0dadc24`; preservation of the workbook proves the captured assessment, not the underlying payments.

## Fund-refill reports

PIP-23 reports two prior Ecosystem Fund refills:

| Reported date | Reported transfer | Evidence state |
|---|---:|---|
| 2024-10-04 | 159,713,142 ATLAS | Transaction reference embedded in PIP-23; not independently reconciled here. |
| 2025-07-03 | 87,551,239 ATLAS | Transaction reference and balance calculation embedded in PIP-23; not independently reconciled here. |

Refills fund the bounded wallet; they are not recipient payments and do not prove any project outcome.

## Reconciliation protocol

Each reported payment requires the transaction signature, block time, source and destination accounts, token mint and decimals, exact amount, signer/authority context, proposal mapping, recipient identity, and any currency-conversion basis. Deliverable verification then requires milestone text, submission, acceptance authority, acceptance date, surviving artifact, and outcome evidence.

## Known conflicts

- Mixed USDC and ATLAS tracker fields may represent separate payments, conversions, or duplicated valuations; the archive does not choose without transaction evidence.
- A Council `complete` label does not prove every milestone or outcome.
- A passed proposal with no reported payment is not proof of non-payment.
- PIP-33’s derived semantic funding-source label conflicts with primary text and is rejected.

## Missing artifacts

The ledger still requires proposal-linked transaction signatures, block times, source and destination accounts, token mints and decimals, payment dates, signer authority, recipient identity, conversion bases, milestone submissions, acceptance records, and surviving deliverables. Current DAO Treasury and Ecosystem Fund balances also require dated on-chain reconciliation rather than extrapolation from older proposal text.

## Review status

`QUALIFIED`, risk class `R3`. Authorization is generally source-grounded; reported payment and completion states remain provisional operational evidence.
