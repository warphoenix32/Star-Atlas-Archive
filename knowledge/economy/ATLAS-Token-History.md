---
title: "ATLAS Token History"
seo_title: "ATLAS Token History, Utility, Emissions, and Treasury Use"
seo_description: "An evidence-qualified history of the Star Atlas ATLAS token, its economic roles, locking program, gameplay emissions, treasury use, and unresolved supply record."
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
canonical_entity: TOKEN-ATLAS
aliases:
  - "ATLAS"
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-0333A5B22A207D88.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-D07F401D77E9CA13.md"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
known_limitations:
  - "Official sale and economic publications establish publisher claims, not an independently audited token ledger."
  - "The repository lacks a complete mint, burn, emissions, holder, and treasury-balance history."
research_gaps:
  - "Acquire the foundational economics paper PDF, token-genesis transaction, sale settlement records, and complete supply history."
  - "Reconcile every major emissions transition and locker reward to on-chain transactions."
review_after: 2027-01-17
---

# ATLAS Token History

ATLAS is the transferable Star Atlas token documented for exchange, gameplay, marketplace, reward, and treasury uses. Its history must be separated from the ATLAS Locker program, the DAO Treasury’s ATLAS holdings, the Atlas Prime fee-payer program, and Holosim’s simulated `zATLAS` currency.

## Canonical identity and adjacent entities

PIP-1 identifies the ATLAS mint as `ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx`. The same instrument names a separate ATLAS Locker program, DAO Treasury account, DAO Emissions account, and DAO Sales Account. Those components may hold, distribute, lock, or use ATLAS but are not aliases of the token. [PIP-1](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

`zATLAS`, documented in Holosim, is a simulation currency and must not be treated as the on-chain token. [Holosim history](../gameplay/Holosim.md)

## Why the history is layered

ATLAS entered the public record first through token-sale design and exchange utility, then acquired additional roles as successive products reached users. SCORE used it as a faction-fleet reward; locking tied it to marketplace discounts and POLIS rewards; SAGE systems used it inside an on-chain game economy; and governance proposals authorized treasury obligations denominated partly or wholly through ATLAS. Each role begins and changes on its own date.

That layered history prevents two common mistakes. A feature documented for one product should not be projected backward to token launch, and the end of one emissions program should not be described as the end of ATLAS utility generally. The chronology below therefore assigns claims to a dated surface rather than treating every historical feature as permanently current.

## Lifecycle chronology

| Date | Evidence state | Historical finding |
|---|---|---|
| 2021-08-17 | `SALE_DESIGN` | ATMTA announced an August 26 sale design, stating a 36 billion ATLAS total supply, 2.16 billion expected launch circulation, 2% sale allocation, and USD 0.00138 price. These are historical plan terms, not current supply facts. [SRC-OFF-927F495C3F49A56F](../../archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md) |
| 2021-08-26 | `SALE_PUBLICATION` | ATMTA published sale-day economic and utility claims. Publication timing does not independently verify allocations or settlement. [SRC-OFF-E9E5AB15C5DECE43](../../archive/source-records/campaign-delta-official/SRC-OFF-E9E5AB15C5DECE43.md) |
| 2021-09-08 | `PUBLISHER_REPORTED_OUTCOME` | ATMTA reported completed IEO/IDO activity and market availability. The archive lacks an independent allocation and settlement ledger. [SRC-OFF-0333A5B22A207D88](../../archive/source-records/campaign-delta-official/SRC-OFF-0333A5B22A207D88.md) |
| 2021-12-17 | `GAMEPLAY_REWARD_LIVE` | The official SCORE release described faction payments in ATLAS. This establishes the published reward design and release claim, not a complete emissions audit. [SRC-OFF-0AED270D51ACD552](../../archive/source-records/campaign-delta-official/SRC-OFF-0AED270D51ACD552.md) |
| 2022-09-29 | `LOCKER_RELEASED` | ATMTA announced the ATLAS Locker, marketplace-fee discounts, and an eight-year POLIS-reward schedule beginning 2022-09-30. Release and schedule are distinct from proof that every future reward executed. [SRC-OFF-D07F401D77E9CA13](../../archive/source-records/campaign-delta-official/SRC-OFF-D07F401D77E9CA13.md) |
| 2023-09-21 | `SAGE_LABS_LIVE` | SAGE Labs was stated live with an ATLAS-based on-chain economy. Product release does not establish every later emissions state. [SAGE history](../gameplay/SAGE.md) |
| 2024-03-26 to 2024-04-04 | `TRANSITION_ANNOUNCED` / `STARBASED_LIVE` | Starbased records announced a reorientation of ATLAS emissions from older passive systems toward active SAGE activity; execution of every scheduled shutdown remains unverified. [SCORE transition](../gameplay/SCORE-and-Faction-Fleet.md) |
| 2025-12-02 | `DOCUMENTED_CURRENT_MECHANIC` | Support documentation describes ATLAS locking, POLIS rewards, marketplace discounts, and a 21-day withdrawal cooldown as of its update. This is a dated support snapshot, not original launch evidence. [SRC-OFF-A5D64DE1191E1208](../../archive/source-records/campaign-delta-official/SRC-OFF-A5D64DE1191E1208.md) |

## Economic roles by surface

- **Marketplace means of exchange:** official publications describe ATLAS for NFT and item transactions. The exact fee schedule changed by surface and date.
- **Gameplay reward and cost token:** SCORE and SAGE records use ATLAS for rewards, fees, crafting, and other economic activity. Each program needs its own emissions and sink chronology.
- **Locking asset:** the ATLAS Locker is an economic utility program that can affect marketplace fees and POLIS rewards; it does not confer PVP voting power merely by locking ATLAS.
- **Treasury asset and payment medium:** governance proposals can request USD/USDC-equivalent value while directing payment in ATLAS. Authorization and payment remain separate.
- **DAO-governed economic parameter:** late-2025 support describes mint/burn policy as governance-related. That description is not a current supply audit.

## Supply and emissions boundary

Historical supply statements must be dated to the source that made them. The repository does not yet contain a complete on-chain reconstruction of genesis minting, vesting, unlocks, sales, burns, gameplay emissions, locker rewards, treasury movements, or circulating supply. Marketing repetition is not independent corroboration.

## Conflicts and missing artifacts

The foundational economics paper is referenced but not preserved as a reviewed primary artifact. The archive also lacks sale settlement records, mint-authority history, current distribution, current treasury balances, a complete emissions schedule with executed transactions, and a program-by-program burn/sink ledger.

## Review status

`QUALIFIED`. Token identity and major official lifecycle statements are high confidence; quantitative supply and execution history remains incomplete.

## Related pages

- [POLIS Token History](POLIS-Token-History.md)
- [Treasury ledger](Treasury-Authorization-and-Payment-Ledger.md)
- [SAGE](../gameplay/SAGE.md)
- [Galactic Marketplace](../gameplay/Galactic-Marketplace.md)
