---
title: "Resources, Mining, Crafting, and Trade"
seo_title: "Star Atlas Resources: Mining, Crafting, R4, and Trade History"
seo_description: "A product-qualified guide to Star Atlas resource systems across SCORE, Escape Velocity, SAGE Labs, Starbased, Holosim, and C4 testing."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: MEDIUM
page_risk_score: 7
page_risk_class: R3
evidence_basis:
  - "knowledge/gameplay/SCORE-and-Faction-Fleet.md"
  - "knowledge/gameplay/Escape-Velocity.md"
  - "knowledge/gameplay/SAGE.md"
  - "knowledge/gameplay/Holosim.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-D023F6DAFA12F9AA.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-E061D3A6454697AB.md"
known_limitations:
  - "Recipes, rates, resource names, and costs vary by product and build and are not comprehensively versioned in the current repository."
  - "PTR, simulation, and mainnet mechanics are documented separately and cannot be assumed equivalent."
research_gaps:
  - "Capture versioned recipes, resource tables, parameter changes, program/game IDs, production totals, market volumes, and deprecation notices for each product surface."
review_after: 2026-10-23
---

# Resources, Mining, Crafting, and Trade

Resources are the connective tissue of the Star Atlas economy. They keep fleets operating, give mining and transport a purpose, supply crafting systems, and create goods that can move through markets. Yet the meaning of "resource gameplay" has changed substantially across products. R4 in SCORE is not a complete model of SAGE Labs mining; Escape Velocity loot is not a Starbased recipe; Holosim balances are not mainnet balances; and C4 PTR documentation describes a test environment.

## R4 and the SCORE era

SCORE/Faction Fleet required four consumable resources commonly grouped as R4: fuel, food, ammunition, and toolkits. The resources functioned as operating inputs for enlisted ships. Their economic role was tied to a passive emissions loop in which ship operation and resource replenishment supported ATLAS rewards.

This system made resources economically important before players had a broad production chain. It also created dependence on the supply channels available at the time, including DAO sales. Later announcements sought to reduce that administrative supply role.

## Escape Velocity and active discovery

Escape Velocity introduced resource discovery through active on-chain movement. In June 2023 ATMTA announced that Escape Velocity resource generation would rise to nearly eight times its baseline and that unlimited DAO R4 sales would end after a finite 30-day supply. The change was presented as a transition toward player-generated resources through Escape Velocity and Claim Stakes. [SRC-OFF-D023F6DAFA12F9AA](../../archive/source-records/campaign-delta-official/SRC-OFF-D023F6DAFA12F9AA.md)

The publication supports the announced direction and stated parameter change. It does not independently establish the exact quantity produced, the final DAO sale transaction, or the resulting prices.

## SAGE Labs: mining, transport, and crafting

SAGE Labs connected resources to fleet movement, mining locations, cargo capacity, crafting, and market exchange. Resources became inputs and outputs inside a strategy loop rather than only upkeep items. The historical record should attach every mechanic to the relevant build because SAGE Labs, Starbased, SAGE 3D, and C4 have different states and interfaces.

Crafting adds another layer of version sensitivity. A recipe is a relationship among a named output, required inputs, quantities, duration, location, program/game configuration, and effective date. Repeating a current support recipe as a timeless rule would erase economic updates.

## Starbased and shared infrastructure

Starbased added shared starbases and related progression systems. Resource use therefore expanded beyond individual fleet operations toward collective infrastructure, upgrading, upkeep, and faction-scale activity. The release and first epoch had documented limitations, so later operational states must not be backdated to launch.

## Holosim and C4

Holosim can model mining, fleets, progression, or market-like systems using simulation-specific values. Its resource balances and `zATLAS` do not establish mainnet supply or player holdings.

C4 PTR support records document mining and other mechanics in a Public Test Realm. They support that the named features were available for testing at the evidence date. They do not prove production deployment or final balance parameters. [SRC-OFF-E061D3A6454697AB](../../archive/source-records/campaign-delta-official/SRC-OFF-E061D3A6454697AB.md)

## Trade and the marketplace boundary

Resources may be traded through product-specific or broader marketplace surfaces, but "the marketplace" should not be assumed to mean one contract, interface, or order book across all periods. A SAGE in-game market reference can identify a trading mechanic without proving equivalence to every workflow in the Galactic Marketplace.

## Evidence model for a resource rule

A defensible resource record should identify:

- product and named build;
- environment, such as mainnet, PTR, or simulation;
- program and game ID when documented;
- resource and unit;
- source and destination;
- production or consumption rule;
- effective and supersession dates;
- announcement, deployment, observation, and verification states;
- original parameter text and any later correction.

## Review status

`QUALIFIED`. The major transitions from upkeep supply to discovery, production, crafting, shared infrastructure, simulation, and PTR testing are supported. Complete versioned mechanics and independently reconciled economic outcomes remain missing.
