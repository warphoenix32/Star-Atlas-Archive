---
source_id: SRC-LORE-REPO-9A2489C393EE
preferred_name: "Faction Power Classification"
lore_type: REGISTRY_AUDIT
repository_entity_type: DOCUMENT
upstream_commit: 22555f277eb1496e34c0839c8f1f382842bd1d2b
upstream_path: canon/meta/faction_power_classification.md
authority_scope: ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_AND_NOMENCLATURE
---

# Faction Power Classification

## Normalization Note

The text below is a line-ending-normalized derivative of the preserved upstream page. No source wording was rewritten. Taxonomy and link metadata are stored in the paired JSON record.

## Preserved Source Text
# Faction Power Classification

**Purpose**: Standardized scale for categorizing faction power and territorial scope across Galia

---

## Overview

Not all factions are created equal. The **Faction Power Classification** is a 5-tier system that categorizes factions by their **territorial scope** and **operational scale** — from galaxy-spanning superpowers to single-station enterprises. This classification is independent of the Galactic Indices (GFI, GWI, GPI), which measure specific capabilities; the Power Tier measures **reach**.

---

## The Five Tiers

| Tier | Name | Scope | Description |
|------|------|-------|-------------|
| **T1** | **Galactic Power** | Multi-sector + Safe Zone | Controls a Safe Zone, governs multiple sectors, maintains standing fleets, and holds a seat at the Council of Peace. The three major factions |
| **T2** | **Sector Power** | Dominates or governs one sector | Controls governance, economy, or security across an entire sector (MRZ or Safe Zone sub-region). May project influence into neighboring sectors |
| **T3** | **Regional Influence** | Multiple systems within a sector | Operates across several systems but does not control the sector as a whole. May dominate trade routes, specific resources, or cultural spheres |
| **T4** | **Local Power** | Single system or station | Controls a single system, planet, station, or installation. Significant within its domain but invisible at the sector level |
| **T5** | **Cell / Network** | No fixed territory | Operates through decentralized networks, cells, cultural influence, or covert operations. May span the galaxy in reach without controlling any territory |

---

## Classification Guide

### T1 — Galactic Power

- **Characteristics**: Standing military fleets, Safe Zone territory, COP representation, galactic economic infrastructure
- **Examples**: **MUD**, **ONI Consortium**, **ECOS**
- **Note**: Only three T1 factions exist. Creation of a fourth would require galaxy-altering events

### T2 — Sector Power

- **Characteristics**: Sector-wide governance or dominant economic/military presence. May have formal government or operate as de facto rulers
- **Examples**: **Merchant Princes of Denebula** (MRZ-13), **Jorvik** (MRZ-18), **Pergamos Shadow Banks** (MRZ-8), **Slavers of Frenir** (historical, MRZ-19), **Mycenas Government** (MRZ-2), **Anfoil State** (MRZ-15)

### T3 — Regional Influence

- **Characteristics**: Multi-system presence, specialized capability, significant reputation. May be feared, respected, or sought after — but cannot dictate sector policy
- **Examples**: **Balifa Grove**, **Ka-Dara**, **Garadar DAC**, **Scriptorium of the Lumikir**, **Iris Academy**, **Dark Photoli**, **Ophek**, **House Akalma** (HRZ)

### T4 — Local Power

- **Characteristics**: Controls one system, station, or installation. Significant within its domain; invisible beyond it. May generate outsized cultural influence relative to its territorial reach
- **Examples**: **Barrot Entertainment Company** (wormhole system, MRZ-14), **Bluevael Mining Colonies**, **Coral Sector Settlers**, **Gate Garrison**

### T5 — Cell / Network

- **Characteristics**: No permanent territory. Operates via cells, agents, cultural transmission, or ideological networks. May be galaxy-spanning in reach but holds no ground
- **Examples**: **Order of Seasons** (assassin cult), **The Real Truth Network** (media/propaganda), **Church of the Dreamer Below** (religious cult), **Nimrod Trackers** (bounty hunter network)

---

## Usage

Every faction canon document should include a `**Scale**` field in its header:

```
**Scale**: T4 — Local Power (operates within a single system in MRZ-14)
```

The classification is supplementary to the existing **Galactic Indices** (GFI, GWI, GPI), which measure Force, Wealth, and Political influence respectively. A T5 Cell can have a GPI of 5 (massive political influence through fear) while controlling zero territory.

---

## Cross-References

- Galactic Indices — defined per-faction in individual canon documents
- Council of Peace — `canon/institutions/council_of_peace.md` (T1 factions hold COP seats)
- Sector geography — `canon/geography/sectors/` (T2 factions typically map to one sector)
