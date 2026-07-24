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
  - "archive/source-records/campaign-delta-official/SRC-OFF-7FFFCA6E3EFC320C.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-8917A64EB222FB1E.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-A49DE58EC808D004.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-C4DA380B01338D57.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-F9654AA6FF1D8010.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-A2F14F878C41366F.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-81AC1295ED8D5F75.md"
  - "operations/campaigns/knowledge-narrative-depth-001/phase-5-readiness/external-source-review.json"
known_limitations:
  - "The 63-row export was distributed by Ryden Systems and asserted to duplicate an authoritative Star Atlas sheet, but the upstream URL and version were not independently recovered."
  - "The dataset does not establish collection completeness or present marketplace availability, and it does not contain a dedicated manufacturer field."
  - "Values are base templates intended for SAGE and C4; Holosim uses a different value system, future rebasing is possible, and components may modify individual ships."
research_gaps:
  - "Recover the upstream Star Atlas ship-stat document, version history, marketplace IDs and URLs, and change notices."
  - "Reconcile the 63-row dataset with the eleventh official root manufacturer, Floyd Line, and with any ship models omitted from the captured export."
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

The 63 rows represent ten root manufacturer families. This is not a rule that every first word in an arbitrary ship list is a manufacturer. It is a reviewed mapping supported by the exact captured names, official ship records, the official asset library's brand organization, and the manufacturer table in the historical lore snapshot.

| Root manufacturer | Captured templates | Reviewed mapping | Notes |
|---|---:|---|---|
| Armstrong Industries | 3 | `Armstrong …` | The three captured ships form the IMP mining line. |
| Busan | 4 | `Busan …` | Official records also use Busan as a ship brand. |
| Calico Industries | 9 | `Calico …` | The lore snapshot and official records identify Calico as a manufacturer. |
| Fimbul | 15 | `Fimbul …` | Five core Fimbul, five Fimbul BYOS, and five Fimbul ECOS templates are preserved separately. |
| Ogrika | 7 | `Ogrika …` | Official records identify multiple Ogrika ship models. |
| Opal Industries | 4 | `Opal …` | The lore snapshot and official records identify Opal as a manufacturer. |
| Pearce | 11 | `Pearce …` | Official records identify Pearce ship models and Pearce Industries. |
| Rainbow | 4 | `Rainbow …` | The captured family includes Chi, Om, Arc, and Phi. |
| Tufa | 1 | `Tufa …` | The captured family contains the Tufa Feist. |
| VZUS | 5 | `VZUS …` | The lore snapshot and official records identify VZUS as a manufacturer. |

An official 2021 design update said that seven primary and four minor manufacturers had been defined. The later lore component table names eleven root makes—Pearce, Busan, VZUS, Calico, Ogrika, Opal, Armstrong Industries, Fimbul, Tufa, Rainbow, and Floyd Line—and separately records Fimbul BYOS and Fimbul ECOS variants. The 63-row capture contains the first ten root families but no Floyd Line ship. That absence means this dataset is not a complete catalog of every Star Atlas manufacturer or ship.

Fimbul BYOS and Fimbul ECOS are retained as distinct product lines beneath Fimbul because the captured names and official lore both distinguish them. They are not counted as separate root manufacturers in the eleven-manufacturer reconciliation.

## Metrics and versioning

The normalized record preserves cargo, fuel, crew, passenger, mining, scan, subwarp, warp, respawn, and related fields. Three duplicate or derived-looking USDC/capacity fields were omitted from the concise normalized records because their semantics were unknown; their exact values remain in the immutable raw CSV.

A future authoritative release should not overwrite this snapshot. It should create a new version, record the effective product/build, and identify which rows and fields changed. That approach allows researchers to study rebasing rather than silently replacing the historical balance state.

## Review status

`QUALIFIED`. The 63 names, codes, specializations, captured values, and ten manufacturer-family mappings are supported. Upstream sheet lineage, collection completeness, marketplace identity, current availability, most units, and future balance state still require further evidence.
