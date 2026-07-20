---
title: "POLIS Token History"
seo_title: "POLIS Token History, Governance, Locking, and PVP"
seo_description: "An evidence-qualified history of the Star Atlas POLIS governance token, locking, voting power, rewards, distribution claims, and unresolved on-chain history."
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
canonical_entity: TOKEN-POLIS
aliases:
  - "POLIS"
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-E5AEFD6B36E3CE06.md"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/campaign-delta-official/SRC-OFF-45B0F6196BC7966E.md"
known_limitations:
  - "Historical supply, team-lock, and emissions statements are source-dated and not a current distribution audit."
  - "PVP is a derived voting-power measure and is not interchangeable with transferable POLIS balance."
research_gaps:
  - "Recover token-genesis, vesting, team-lock, reward-emission, and present distribution transactions."
  - "Measure historical PVP concentration from preserved snapshots without inferring identity."
review_after: 2027-01-17
---

# POLIS Token History

POLIS is the Star Atlas token documented for governance participation and related reward programs. The token, locked token positions, the POLIS Locker program, snapshot program, reward emissions, and PVP voting power are separate entities or states.

## Canonical identity

PIP-1 identifies the POLIS mint as `poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk`, the POLIS Locker as `Lock7kBijGCQLEFAmXcengzXKA88iDNQPriQ7TbgeyG`, and the snapshot program as `snapNQkxsiqDWdbNfz8KVB7e3NPzLwtHHA6WV8kKgUc`. It defines PVP as voting weight based on controlled locked POLIS and lock duration. [PIP-1](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

PVP is not a token, transferable balance, or synonym for POLIS. See [PVP Voting Power](PVP-Voting-Power.md) for the repository’s decision and adjudication rules.

## Why POLIS needs several histories

POLIS has at least four overlapping but non-identical histories: the transferable token and its distribution; the locker program and its technical rules; reward schedules attached to locking; and the use of snapshot-derived PVP in governance. A dated claim about one layer does not automatically describe the others.

For example, an announced team lock is evidence of institutional intent at that date, not a permanent ownership record. A support article explaining current lock behavior is evidence of the documented user experience when updated, not proof that every historical program version behaved identically. A proposal tally records voting weight in a particular decision, not the present POLIS holdings of the participating wallets.

## Lifecycle chronology

| Date | Evidence state | Historical finding |
|---|---|---|
| 2021-08-17 | `SALE_DESIGN` | ATMTA announced an August 26 sale design, then stating 360 million POLIS total supply, 21.6 million expected launch circulation, a 2% sale allocation, and USD 0.138 price. These are historical terms, not current supply. [SRC-OFF-927F495C3F49A56F](../../archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md) |
| 2021-09-08 | `PUBLISHER_REPORTED_OUTCOME` | ATMTA reported token-sale and market-opening outcomes. Independent allocation and settlement evidence is absent. [SRC-OFF-0333A5B22A207D88](../../archive/source-records/campaign-delta-official/SRC-OFF-0333A5B22A207D88.md) |
| 2022-07-21 | `LOCKER_AND_GOVERNANCE_RELEASED` | ATMTA stated that the initial DAO governance and POLIS-locking module had launched and described quantity-and-duration-based PVP. [SRC-OFF-E5AEFD6B36E3CE06](../../archive/source-records/campaign-delta-official/SRC-OFF-E5AEFD6B36E3CE06.md) |
| 2022-07-31 | `REWARD_PLAN` | Official Discord announced locking rewards for August 2 and described ATMTA’s intended near-term PVP share and five-year lock. This is historical intent, not present ownership or control. [SA-DISCORD-ANN-0D4A8B8F235B43B8](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-0D4A8B8F235B43B8.json) |
| 2022-09-29 | `FRAMEWORK_PUBLISHED` | ATMTA published the Sustainable Governance Framework. Publication is distinct from the 2024 PIP-1 ratification. [SRC-OFF-68D126528852339E](../../archive/source-records/campaign-delta-official/SRC-OFF-68D126528852339E.md) |
| 2024-07 | `FORMAL_RATIFICATION` | PIP-1 passed and formally captured the POLIS/PVP governance procedure. Ratification does not backdate the program’s 2022 release. |
| 2025-12 | `DOCUMENTED_CURRENT_MECHANICS` | Official support described lock durations, PVP decay, reward calculation, and POLIS/ATLAS-lock reward surfaces as of the update dates. [Locker mechanics](../../archive/source-records/campaign-delta-official/SRC-OFF-45B0F6196BC7966E.md) [Reward calculation](../../archive/source-records/campaign-delta-official/SRC-OFF-2A076CDCA845BB86.md) |

## Governance role

POLIS holders do not vote with simple wallet balance in the captured framework. They lock POLIS and receive time-weighted PVP. Ballot counts and PVP totals are both historically relevant but answer different questions. A proposal can receive more individual YES ballots while the PVP result depends on weighted positions.

The Foundation administers proposal progression and implementation within the captured rules, while the Council may assist authors and administer delegated processes. Neither role replaces POLIS-holder voting authority.

## Reward and concentration boundaries

Official records describe POLIS rewards from POLIS and ATLAS locking and an emissions schedule extending toward 2030. A schedule is not proof that every reward was emitted as planned. The 2022 announcement about ATMTA’s intended near-term PVP share must not be restated as current concentration without snapshot and identity analysis.

## Missing artifacts

The archive requires mint/genesis transactions, vesting and unlock schedules tied to executed transactions, complete reward-emissions history, locker position and snapshot histories, current distribution, governance-program upgrades, and current PVP concentration analysis. Identity should not be inferred from addresses without separate evidence.

## Review status

`QUALIFIED`. The institutional mechanics are well supported; supply, reward execution, and concentration history remain incomplete.

## Related pages

- [ATLAS Token History](ATLAS-Token-History.md)
- [PVP Voting Power](PVP-Voting-Power.md)
- [Star Atlas DAO](../governance/Star-Atlas-DAO.md)
- [Council Election History](../governance/Council-Election-History.md)
