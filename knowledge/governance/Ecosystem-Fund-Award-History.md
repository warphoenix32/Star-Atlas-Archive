---
title: "Ecosystem Fund Award History"
seo_title: "Star Atlas Ecosystem Fund Awards, Payments, and Milestones"
seo_description: "An evidence-qualified history of Star Atlas Ecosystem Fund proposals, approved awards, Council-reported payments, milestones, terminations, and missing verification."
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 7
page_risk_class: R3
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"
known_limitations:
  - "Award means a passed eligible funding authorization, not payment, accepted milestones, or completed outcomes."
  - "Council payment and lifecycle fields have not been independently reconciled to transactions and deliverables."
research_gaps:
  - "Reconcile every reported award payment to mint, amount, block time, source wallet, recipient, and milestone."
  - "Recover complete outcomes and termination records for each funded initiative."
review_after: 2026-10-17
---

# Ecosystem Fund Award History

This registry records PIPs that the captured proposal and Council data identify as Ecosystem Fund funding authorizations. “Award” is used narrowly: the proposal passed and was eligible for the fund. It does not mean money moved, deliverables were accepted, or the project succeeded.

Read as a whole, the award history is a record of public experimentation. Community events, tools, media, infrastructure, and game projects were proposed under a shared policy, but their later paths ranged from reported completion to partial work, termination, withdrawal, and unresolved execution.

## Policy boundary

[PIP-4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-04-AD1945D8.json) created the original framework. [PIP-23](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json) later replaced it in full, preserving a separate Ecosystem Fund wallet, a 20% allocation formula, a USD 500,000 USDC reserve rule, USDC-denominated requests, ATLAS payments, a 5% proposal ceiling tied to the last refill balance, and a 12-month maximum project term.

PIP-23 is policy and refill authority, not a recipient award. PIP-33 is excluded because its primary text requests a direct DAO Treasury authorization and the Council tracker marks `ecosystem_fund: NO`.

## Passed authorization registry

| PIP | Initiative | Council-reported lifecycle | Reported payment state | Independent verification |
|---|---|---|---|---|
| [5](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-05-C248D280.json) | Naabathon co-sponsorship | Complete | 6,000,000 ATLAS reported | `UNKNOWN` |
| [8](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-08-62506041.json) | Star Atlas Comet at Gamescom 2025 | Complete | 7,723,034 ATLAS reported | `UNKNOWN` |
| [12](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-12-F15380C9.json) | Iris’s Bounty: The Feast | Complete | 7,429,420 ATLAS reported | `UNKNOWN` |
| [14](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-14-FED98016.json) | THEO integration | Terminated | 4,462,301 ATLAS reported | `UNKNOWN` |
| [16](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-16-B11CED4B.json) | Ryden Systems | Complete | 8,464.79 USDC and 7,985,657 ATLAS reported; denomination relationship unresolved | `UNKNOWN` |
| [17](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-17-4DF4C199.json) | Ecosystem Media Expansion | Terminated/canceled | 0 reported | `UNKNOWN` |
| [18](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-18-18750A6A.json) | Gamescom marketing and merch | Complete | 5,781,393 ATLAS reported | `UNKNOWN` |
| [20](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-20-159CB743.json) | DAO Casters program | Partial/in progress | 4,320,000 ATLAS paid; 5,400,000 remaining reported | `UNKNOWN` |
| [21](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-21-49CAD7E4.json) | Rogue Data Hub | Partial/in progress | 2,083 USDC and 7,317,073 ATLAS paid; 35,225,130.9 ATLAS remaining reported | `UNKNOWN` |
| [22](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-22-D5D61E64.json) | Iris’s Bounty: The Arena | Partial/in progress | 2,000,000 ATLAS paid; 9,000,000 remaining reported | `UNKNOWN` |
| [24](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-24-8CC6B298.json) | SLY Assistant hosting | Complete | Amount recorded as `?` | `UNKNOWN` |
| [29](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-29-8E761702.json) | Relay Program pilot | Unknown | 13,143,639 ATLAS reported | `UNKNOWN` |
| [30](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-30-3BA029F2.json) | ATOM cloud infrastructure | Unknown | 1,650 USDC and 6,433,164 ATLAS paid; 6,710,475 ATLAS remaining reported | `UNKNOWN` |
| [31](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-31-E71FB1A7.json) | Star Seekers 2 | Not implemented/withdrawn | No payment established | `UNKNOWN` |
| [32](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-32-0B04FF9B.json) | Triad Tournament | Unknown | No payment established | `UNKNOWN` |

“Complete,” “partial,” and “terminated” above are Council-authored operational labels, not independent findings. Mixed USDC and ATLAS values are not added or converted because the record does not establish whether they represent separate transfers, valuations, or tracker-entry conventions.

## Rejected applications, not awards

PIPs [15](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-15-BD065AD2.json), [19](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-19-1EB3D15E.json), and [26](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-26-B70AC545.json) failed. They belong in proposal and failure history, not the award registry.

## Research protocol

For each authorization, the evidence chain must be reconstructed as proposal amount and denomination → vote result → Foundation/Council implementation instruction → transaction → recipient → milestone submission → acceptance → outcome. A missing link remains explicit; later marketing or tracker summaries do not fill it automatically.

This sequence also protects successful projects from overstatement. A verified payment says assets moved. A verified deliverable says an agreed artifact existed. Neither fact, by itself, demonstrates durable community value or the return-on-investment language sometimes recorded by program administrators.

## Missing artifacts

Each authorization still needs its transaction signature, block time, source and recipient wallets, mint and decimals, exact amount, dated conversion basis where relevant, milestone package, acceptance record, termination or completion instrument, and outcome evidence. PIPs with mixed USDC and ATLAS tracker fields additionally need source-native accounting records that explain whether the values are transfers, valuations, or duplicate representations.

## Review status

`QUALIFIED`, risk class `R3`. Authorization identity is generally well supported; the payment and outcome layer remains largely unreconciled.

## Related pages

- [Ecosystem Fund policy](Ecosystem-Fund.md)
- [Treasury Authorization and Reported Payment Ledger](../economy/Treasury-Authorization-and-Payment-Ledger.md)
- [Governance Failure and Termination Casebook](Governance-Failure-and-Termination-Casebook.md)
