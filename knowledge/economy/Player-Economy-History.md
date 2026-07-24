---
title: "History of the Star Atlas Player Economy"
seo_title: "Star Atlas Economy History: Ships, Tokens, Resources, and Trade"
seo_description: "A source-qualified history of the Star Atlas player economy from early asset markets and SCORE emissions through SAGE resources, crafting, trade, and economic reporting."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: MEDIUM
page_risk_score: 8
page_risk_class: R3
evidence_basis:
  - "knowledge/economy/ATLAS-Token-History.md"
  - "knowledge/economy/POLIS-Token-History.md"
  - "knowledge/economy/Economic-Report-Catalog.md"
  - "knowledge/gameplay/SCORE-and-Faction-Fleet.md"
  - "knowledge/gameplay/SAGE.md"
  - "knowledge/gameplay/Galactic-Marketplace.md"
known_limitations:
  - "Official economic reports are first-party measurements whose methodologies, coverage, and revisions vary by period."
  - "The repository does not yet contain a reconciled transaction-level history of emissions, trading, resource production, sinks, burns, or treasury activity."
research_gaps:
  - "Build time-series ledgers for token supply, emissions, sinks, resource production, crafting, marketplace activity, and participant concentration."
  - "Reconcile official reported metrics to program versions, game IDs, transactions, and independent methodology."
review_after: 2026-10-23
---

# History of the Star Atlas Player Economy

The Star Atlas player economy began before most of its planned game systems existed. Assets and tokens reached markets first; ships then gained utility through SCORE; locking connected tokens to rewards and fees; Escape Velocity tested resource discovery; SAGE Labs introduced mining, crafting, transport, and trade; and Starbased reorganized parts of the economy around shared infrastructure and new progression systems.

There has never been one timeless "Star Atlas economy." It is a sequence of related economic systems, each with its own products, rules, assets, and evidence.

## 2021: markets, tokens, and the first ship loop

The Galactic Marketplace was officially described as operational in August 2021. The Galactic Asset Offering followed in September, alongside public ATLAS and POLIS sale activity. These events created a market in Star Atlas assets and tokens, but ownership did not imply that every future gameplay use already existed.

SCORE/Faction Fleet changed that relationship in December. Ships could be enlisted in faction service and receive ATLAS emissions while consuming resources. It was a narrow loop, yet historically significant: ships moved from principally collectible and tradable assets toward recurring game-economic utility. [SCORE and Faction Fleet](../gameplay/SCORE-and-Faction-Fleet.md)

## 2022: locking and a changing marketplace

The POLIS Locker connected locked POLIS positions to governance and rewards. The separate ATLAS Locker connected ATLAS locking to marketplace-fee discounts and POLIS rewards. These programs must not be collapsed: ATLAS locking did not itself create PVP governance power, while POLIS locking involved position duration and voting mechanics.

ATMTA also introduced a replacement Galactic Marketplace in July 2022. The earlier and replacement surfaces have different lifecycle records; later support documentation establishes workflows for the newer marketplace without proving historical continuity or unchanged fee rules. [Galactic Marketplace](../gameplay/Galactic-Marketplace.md)

## 2023: resources move toward player production

Escape Velocity introduced active on-chain movement and resource discovery. In June, ATMTA announced that its resource output would rise sharply and that unlimited DAO R4 sales would end after a finite period, shifting greater responsibility toward Claim Stakes and player production. [SRC-OFF-D023F6DAFA12F9AA](../../archive/source-records/campaign-delta-official/SRC-OFF-D023F6DAFA12F9AA.md)

SAGE Labs then created a more sustained resource economy in September. Fleets could mine, craft, move cargo, and participate in markets. This was not simply "SCORE with more features": it introduced distinct game accounts, programs, resource chains, and operational risks.

## 2024: Starbased and the emissions transition

Starbased reorganized the SAGE Labs economy around shared starbases, Loyalty Points, Council Rank XP, epochs, and revised incentives. The SCORE emissions program was announced for deprecation during the same transition. The evidence supports an intended shift away from passive fleet emissions and toward a broader strategy economy, but the exact final SCORE reward transaction and residual interface state remain unresolved.

Starbased itself launched with constraints. The first epoch began with zero ATLAS and no Loyalty Point deposits. A system can therefore be accurately described as live while still lacking portions of its intended economic state at launch.

## 2025-2026: simulation, reports, and test environments

Holosim uses `zATLAS`, a simulated currency that should not be merged with on-chain ATLAS. C4 PTR documentation describes test-environment mechanics whose balances and outcomes cannot automatically be treated as mainnet economic activity.

Official economic reports provide the most systematic first-party measurements preserved in the Archive. They can establish what ATMTA reported about transactions, assets, resources, markets, or participation in a stated period. They remain publisher-generated analyses rather than independent audits. Comparisons across quarters require attention to methodology, coverage, and product changes. [Economic Report Catalog](Economic-Report-Catalog.md)

## The economy's major layers

The historical economy can be separated into:

1. **Asset issuance and ownership** - ships, land-related assets, claims, and other tokens.
2. **Market exchange** - buy and sell orders, fees, price discovery, and liquidity.
3. **Token utility** - ATLAS payments and costs, POLIS governance, and locking programs.
4. **Emissions** - SCORE rewards and other scheduled or product-specific distributions.
5. **Production** - resource discovery, mining, crafting, and player-generated supply.
6. **Consumption and sinks** - fuel, food, ammunition, crafting inputs, fees, upkeep, and other costs.
7. **Infrastructure and progression** - starbases, Loyalty Points, Council Rank XP, and epochs.
8. **Governance and treasury** - authorizations, accounts, grants, and payments, which remain distinct from the player economy even when denominated in the same tokens.

## What remains unmeasured

The repository cannot yet answer, with transaction-level confidence, how wealth and activity were distributed; how much ATLAS entered circulation through each program; when every emission or sale parameter changed; how many unique players remained active; or which systems created durable sinks rather than temporary incentives.

Those are not reasons to avoid history. They are reasons to distinguish the documented design and official measurements from independently reconciled outcomes.

## Review status

`QUALIFIED`. The major product and policy transitions are well documented. Quantitative outcomes, participant behavior, transaction reconciliation, and cross-period comparability remain research priorities.
