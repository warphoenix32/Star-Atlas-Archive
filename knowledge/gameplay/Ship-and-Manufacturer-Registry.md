---
title: "Star Atlas Ship and Manufacturer Registry"
seo_title: "Star Atlas Ships: Base-Ship Registry and Manufacturer Evidence"
seo_description: "A qualified registry of 63 Starbased base-ship templates, shorthand codes, roles, lineage limits, and lore manufacturer evidence."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: MEDIUM
page_risk_score: 8
page_risk_class: R3
evidence_basis:
  - "archive/normalized/starbased-ship-states/metadata.json"
  - "archive/normalized/starbased-ship-states/base-ships.jsonl"
  - "archive/provenance/starbased-ship-states/rydn_starbased_ships_20260718.json"
  - "archive/normalized/lore/entities.jsonl"
known_limitations:
  - "The 63-row export was distributed by Ryden Systems and asserted to duplicate an authoritative Star Atlas sheet, but the upstream URL and version were not independently recovered."
  - "The dataset does not establish collection completeness, present marketplace availability, or manufacturer identity as a separate field."
  - "Values are base templates intended for SAGE and C4; Holosim uses a different value system, future rebasing is possible, and components may modify individual ships."
research_gaps:
  - "Recover the upstream Star Atlas ship-stat document, version history, marketplace IDs and URLs, explicit manufacturer fields, and change notices."
  - "Create separate versioned registries for Holosim and component-modified ship instances."
review_after: 2026-10-23
---

# Star Atlas Ship and Manufacturer Registry

Ships are among the most recognizable objects in Star Atlas, but "a ship" can refer to several different things: a named design in lore, a marketplace asset, a base game template, a player-owned token, or an individually modified in-game instance. This registry begins with the narrowest normalized dataset presently available: 63 **base-ship templates** captured from a Ryden Systems export dated 2026-07-18.

The repository operator identified Ryden as the distributor and stated that the sheet duplicated an authoritative Star Atlas document. Because the upstream document URL and version were not recovered, the Archive records that lineage as highly plausible operator context rather than independently verified first-party provenance.

## How to read the registry

Each row preserves the observed ship name, shorthand code, and specialization. The codes often align with marketplace identifiers, but that alignment is not verified row by row. A code is therefore a stable identifier inside this captured dataset, not a guaranteed marketplace address.

The normalized metrics describe base templates intended to apply across SAGE and C4. They should not be used as timeless universal stats:

- future ship-stat rebasing is likely;
- Holosim uses a different set of values;
- components may later modify ships at the individual level;
- most units and scales remain as captured unless explicitly documented;
- warp speed is the literal fixed rate of 100,000 astronomical units per second for all 63 rows, while cooldowns and fuel requirements differ.

## Captured base-ship templates

| Record ID | Observed ship name | Code | Observed specialization |
|---|---|---|---|
| SHIP-PULSE | Busan Pulse | PULSE | Racer |
| SHIP-FBLAIR | Fimbul Airbike | FBLAIR | Racer |
| SHIP-FBLEUN | Fimbul ECOS Unibomba | FBLEUN | Bomber |
| SHIP-OGKARU | Ogrika Ruch | OGKARU | Racer |
| SHIP-OPALJ | Opal Jet | OPALJ | Racer |
| SHIP-PX4 | Pearce X4 | PX4 | Fighter |
| SHIP-VZUSSO | VZUS solos | VZUSSO | Racer |
| SHIP-CALMAX | Calico Maxhog | CALMAX | Transport |
| SHIP-CALSCD | Calico Scud | CALSCD | Racer |
| SHIP-FBLLOW | Fimbul Lowbie | FBLLOW | Transport |
| SHIP-OGKANR | Ogrika Niruch | OGKANR | Transport |
| SHIP-OPALJJ | Opal Jetjet | OPALJJ | Racer |
| SHIP-PX5 | Pearce X5 | PX5 | Fighter |
| SHIP-IMP1 | Armstrong IMP Tip | IMP1 | Miner |
| SHIP-THRILL | Busan Thrill of Life | THRILL | Fighter |
| SHIP-CALMED | Calico Medtech | CALMED | Rescue |
| SHIP-CALSHIP | Calico Shipit | CALSHIP | Freighter |
| SHIP-FBLBEA | Fimbul BYOS Earp | FBLBEA | Fighter |
| SHIP-OGKAMK | Ogrika Mik | OGKAMK | Fighter |
| SHIP-OPALRF | Opal Rayfam | OPALRF | Data runner |
| SHIP-PR6 | Pearce R6 | PR6 | Repair |
| SHIP-PX6 | Pearce X6 | PX6 | Fighter |
| SHIP-CHI | Rainbow Chi | CHI | Fighter |
| SHIP-TUFAFE | Tufa Feist | TUFAFE | Fighter |
| SHIP-VZUSAM | VZUS ambwe | VZUSAM | Bounty hunter |
| SHIP-VZUSAR | VZUS arma | VZUSAR | Fighter |
| SHIP-IMP2 | Armstrong IMP Tap | IMP2 | Miner |
| SHIP-CALATS | Calico ATS Enforcer | CALATS | Fighter |
| SHIP-CALCH | Calico Compakt Hero | CALCH | Multi-role |
| SHIP-CALEV | Calico Evac | CALEV | Rescue |
| SHIP-FBLBPL | Fimbul BYOS Packlite | FBLBPL | Freighter |
| SHIP-FBLBRA | Fimbul BYOS Ranger | FBLBRA | Data runner |
| SHIP-FBLMAM | Fimbul Mamba | FBLMAM | Bounty hunter |
| SHIP-FBLMEX | Fimbul Mamba EX | FBLMEX | Bounty hunter |
| SHIP-OGKATU | Ogrika Tursic | OGKATU | Fighter |
| SHIP-PF4 | Pearce F4 | PF4 | Fighter |
| SHIP-OM | Rainbow Om | OM | Freighter |
| SHIP-VZUSOP | VZUS opod | VZUSOP | Data runner |
| SHIP-FBLBBU | Fimbul BYOS Butch | FBLBBU | Fighter |
| SHIP-FBLEGR | Fimbul ECOS Greenader | FBLEGR | Bomber |
| SHIP-OGKASP | Ogrika Sunpaa | OGKASP | Freighter |
| SHIP-OGKATP | Ogrika Thripid | OGKATP | Fighter |
| SHIP-OPALBB | Opal Bitboat | OPALBB | Transport |
| SHIP-PMR8 | Pearce MR8 | PMR8 | Multi-role |
| SHIP-PR8 | Pearce R8 | PR8 | Refuel/repair |
| SHIP-ARC | Rainbow Arc | ARC | Freighter |
| SHIP-IMP3 | Armstrong IMP | IMP3 | Miner |
| SHIP-HEART | Busan Maiden Heart | HEART | Fighter |
| SHIP-CALFLT | Calico Flattop | CALFLT | Freighter |
| SHIP-CALG | Calico Guardian | CALG | Multi-role |
| SHIP-FBLEBO | Fimbul ECOS Bombarella | FBLEBO | Bomber |
| SHIP-FBLSLE | Fimbul Sledbarge | FBLSLE | Freighter |
| SHIP-OGKAJA | Ogrika Jod Asteris | OGKAJA | Transport |
| SHIP-PC9 | Pearce C9 | PC9 | Fighter |
| SHIP-PD9 | Pearce D9 | PD9 | Salvage |
| SHIP-VZUSBA | VZUS ballad | VZUSBA | Fighter |
| SHIP-FBLBTA | Fimbul BYOS Tankship | FBLBTA | Fighter |
| SHIP-FBLETR | Fimbul ECOS Treearrow | FBLETR | Bomber |
| SHIP-PC11 | Pearce C11 | PC11 | Fighter |
| SHIP-STAND | Busan The Last Stand mk. VIII | STAND | Fighter |
| SHIP-SUPER | Fimbul ECOS Superphoenix | SUPER | Bomber |
| SHIP-T1TAN | Pearce T1 | T1TAN | Fighter |
| SHIP-PHI | Rainbow Phi | PHI | Fighter |

The role distribution is 22 fighters, seven racers, seven freighters, five bombers, five transports, three miners, three data runners, three bounty hunters, three multi-role ships, two rescue ships, and one each for repair, refuel/repair, and salvage.

## Manufacturer evidence

Names such as Busan, Fimbul, Ogrika, Opal, Pearce, Rainbow, VZUS, Calico, and Armstrong visibly form ship-name families. This registry does **not** automatically convert the first word of a name into a canonical manufacturer relationship.

The captured lore taxonomy independently identifies Opal Industries, VZUS, and Calico Industries as `MANUFACTURER` entities. It also contains Fimbul-related organizations and houses. Those lore classifications support canonical manufacturer identities within the lore snapshot, but each ship-to-manufacturer edge still requires explicit source evidence or a reviewed deterministic mapping. Apparent naming consistency is a discovery aid, not sufficient proof by itself.

## Metrics and versioning

The normalized record preserves cargo, fuel, crew, passenger, mining, scan, subwarp, warp, respawn, and related fields. Three duplicate or derived-looking USDC/capacity fields were omitted from the concise normalized records because their semantics were unknown; their exact values remain in the immutable raw CSV.

A future authoritative release should not overwrite this snapshot. It should create a new version, record the effective product/build, and identify which rows and fields changed. That approach allows researchers to study rebasing rather than silently replacing the historical balance state.

## Review status

`QUALIFIED`. The 63 names, codes, specializations, and captured values are faithfully normalized. Upstream lineage, completeness, marketplace identity, manufacturer edges, current availability, units, and future balance state require further evidence.
