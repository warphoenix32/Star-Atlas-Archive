---
title: "Star Atlas Canon Registry"
seo_title: "Star Atlas Canon Registry — Lore Authority and Continuity"
seo_description: "A source-qualified registry of Star Atlas lore canon, preferred taxonomy, major factions, settings, narratives, continuity conflicts, and research gaps."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: MEDIUM
page_risk_score: 8
page_risk_class: R3
canonical_entity: STAR-ATLAS-LORE-CANON
aliases:
  - "Star Atlas lore registry"
  - "Star Atlas canon index"
evidence_basis:
  - "archive/normalized/lore/taxonomy.json"
  - "archive/normalized/lore/entities.jsonl"
  - "operations/campaigns/lore-repository-ingestion-2026-07/taxonomy-migration-report.md"
  - "operations/campaigns/lore-repository-ingestion-2026-07/human-review-items.md"
known_limitations:
  - "The principal taxonomy is derived from commit 22555f277eb1496e34c0839c8f1f382842bd1d2b and is a historical snapshot, not a guarantee of current upstream completeness."
  - "ATMTA affiliation and Jose's lore role are repository-operator confirmations; captured repository metadata does not independently establish those facts."
  - "Taxonomy authority does not establish page-level authorship or independently verify every narrative claim."
research_gaps:
  - "Direct source mappings remain deferred for Star Atlas: CORE and The Voice of Iris."
  - "Canon/docs divergences, broken upstream references, and self-reported chronology conflicts require source-level reconciliation."
review_after: 2026-10-20
---

# Star Atlas Canon Registry

Star Atlas lore is not a single unchanging document. It has accumulated through worldbuilding repositories, white papers, website copy, item descriptions, narrative releases, interviews, and promotional material. This registry establishes which source controls names and classifications while preserving the historical differences that show how the universe evolved.

## Authority model

For in-universe taxonomy and preferred nomenclature, the Archive treats Jose's `star-atlas-lore` repository as an ATMTA-affiliated canonical source. The repository operator confirms that Jose is a Star Atlas team member responsible for lore. The captured source remains a personal GitHub repository, so the operator confirmation—and its precise scope—is retained as provenance rather than silently converted into page-level ATMTA authorship.

Authority is applied in this order:

1. the captured Star Atlas lore repository for preferred lore names and classifications;
2. official Star Atlas publications for newer lore not represented in that snapshot;
3. historical Archive sources for what was publicly stated at a given time;
4. operator confirmation for archival ambiguity;
5. derived knowledge for discovery only.

This hierarchy applies only to lore. It does not govern DAO procedure, real-world institutional history, product release state, or provenance. It also does not make every narrative assertion independently verified.

## Taxonomy adopted by the Archive

The normalized taxonomy adopts 26 lore-specific types, including `SPECIES`, `FACTION`, `CORPORATION`, `ORGANIZATION`, `INSTITUTION`, `CHARACTER`, `ARTIFACT`, `PLANET`, `WORLD`, `MOON`, `STATION`, `STAR_SYSTEM`, `SECTOR`, `REGION`, `TECHNOLOGY`, `RESOURCE`, `LORE_EVENT`, and `NARRATIVE`.

Where the repository-wide Schema v2.1 has only a broader type, the original canonical Archive type remains intact and the lore-specific refinement carries the preferred classification. For example, a species remains schema-compatible as a community while `lore_type: SPECIES` preserves the authoritative distinction. Planets, worlds, moons, stations, systems, sectors, and regions similarly refine the broader location type.

Historical IDs are never renamed in place. Compatibility mappings connect older IDs to the preferred lore entities; former names and classifications remain aliases. This preserves citations and lets researchers see which vocabulary a historical source actually used.

## Foundational setting and institutions

| Archive lore identity | Preferred classification | Reviewed description | Boundary |
| --- | --- | --- | --- |
| `LORE-GALIA` | Region | The Galia Expanse is the principal setting in which MUD, ONI, and Ustur interests encounter resources, territory, and anomalies. | Maps to the region; the Galia Expanse Atlas remains a separate reference document. |
| `LORE-CATACLYSM` | Lore event | The Cataclysm is associated with Iris, its child planets, and the resource-rich zone central to later narratives. | Specific causal or scientific descriptions remain source-bound. |
| `LORE-COUNCIL-PEACE` | Institution | The Council of Peace is the post-Convergence-War institution associated with the fragile order among major factions. | The identically named faction is a separate related entity. |
| `LORE-FACTION-MUD` | Faction | Manus Ultima Divina represents humanity's major factional presence and is commonly associated with industry, trade, diplomacy, and human heritage. | Leadership and present-tense descriptions require dated sources. |
| `LORE-FACTION-ONI` | Faction | The ONI Consortium is a multi-species coalition associated with scientific inquiry, exploration, and technological development. | ONI species and institutional components must not be collapsed into the faction. |
| `LORE-FACTION-USTUR` | Faction | The Ustur faction is associated with sentient android civilization, logic, efficiency, and technological mastery. | The Ustur species remains a distinct related entity. |
| `LORE-TUFA` | Species | Tufa are mineral-organic beings associated in published lore with the Cataclysm region and its resources. | Detailed motives and chronology remain narrative claims requiring source citations. |

These descriptions are discovery summaries, not substitutes for the normalized entity records or the upstream prose.

## Narrative canon and unresolved continuity

### Star Atlas: CORE

`LORE-NARRATIVE-CORE` identifies the episodic graphic-novel narrative announced as an expansion of Star Atlas worldbuilding beyond early ReBirth poster lore. A November 7, 2022 official release announced its first public chapter and described a story set shortly before the Convergence War.

The Archive preserves conflicting official spellings of the protagonist's name—**Gyun** and **Geyung**—rather than selecting one through inference. Historical plans for 18 chapters, collectible covers, supplemental lore, and an ARC Cypher are recorded as publication plans, not proof that every planned element was delivered.

A direct one-to-one mapping from the legacy CORE identity to the ingested taxonomy remains deferred pending a sufficiently specific upstream page or later official evidence.

### Voice of Iris

`LORE-VOICE-OF-IRIS` identifies the rumored whisper or transmission described in official CORE-related material. The source associates reported guidance with danger and discovery but explicitly leaves the connection to the planet Iris unproven. That uncertainty is part of the published canon and must remain unresolved.

As with CORE, direct mapping to a single ingested taxonomy entity remains deferred.

## Historical canonical-source snapshots

One captured ONI/CSS lore page exists in the canonical source tree and public sitemap but not in the current published docs surface. Under curator adjudication `LRH-010`, it is preserved as a **historical canonical-source snapshot**, not current canonical taxonomy. This distinction prevents an old deployment state from silently overriding the source's current structure.

More generally, a source can be authoritative evidence for what canon said at a particular moment without controlling present-day names or relationships.

## Canon handling rules

- Record in-universe chronology separately from real-world publication chronology.
- Preserve conflicts among source-tree canon, generated docs, white papers, marketplace copy, graphic novels, official web pages, and interviews.
- Do not silently harmonize names, spellings, dates, titles, or entity classes.
- Treat promotional descriptions as promotional canon until stronger narrative or reference evidence corroborates them.
- Attribute interview clarifications to the speaker, source, and date.
- Keep community interpretation, decoding, and roleplay separate unless an authoritative lore source adopts it.
- Redact upstream workstation paths from normalized and public records while retaining exact bytes in immutable raw evidence.

## What remains to be acquired

The highest-value additions are a complete CORE chapter catalog; ARC Cypher chronology and outcome evidence; dated graphic-novel and narrative releases; official faction, species, manufacturer, ship, and item descriptions; lore-staff interviews; and primary sources resolving known chronology and canon/docs differences.

## Evidence references

- [Lore Repository Campaign](../../operations/campaigns/lore-repository-ingestion-2026-07/README.md)
- [Taxonomy Migration Report](../../operations/campaigns/lore-repository-ingestion-2026-07/taxonomy-migration-report.md)
- [Human Review Register](../../operations/campaigns/lore-repository-ingestion-2026-07/human-review-items.md)
- [Lore Research Backlog](../../operations/campaigns/lore-repository-ingestion-2026-07/research-backlog.md)
- [Lore Index](README.md)

## Review status

This registry incorporates the operator's accepted lore adjudications. Its taxonomy boundary is ready for publication; narrative summaries remain `QUALIFIED` and should be revisited when newer official lore or direct CORE evidence is ingested.
