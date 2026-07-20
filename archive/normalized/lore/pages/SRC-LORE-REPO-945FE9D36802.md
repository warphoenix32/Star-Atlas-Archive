---
source_id: SRC-LORE-REPO-945FE9D36802
preferred_name: "Star Atlas Canon — Consistency Audit Report"
lore_type: REGISTRY_AUDIT
repository_entity_type: DOCUMENT
upstream_commit: 22555f277eb1496e34c0839c8f1f382842bd1d2b
upstream_path: canon/meta/consistency_audit.md
authority_scope: ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_AND_NOMENCLATURE
---

# Star Atlas Canon — Consistency Audit Report

## Normalization Note

The text below is a line-ending-normalized derivative of the preserved upstream page. No source wording was rewritten. Taxonomy and link metadata are stored in the paired JSON record.

## Preserved Source Text
# Star Atlas Canon — Consistency Audit Report

**Date**: Feb 11, 2026
**Scope**: All 46 canon files in `star-atlas-lore/canon/`
**Auditor**: Archon (AI Lorekeeper)

---

## ⚠️ Inconsistencies Found

### 1. Punaab Dying World — Sector Reference Mismatch

- **File**: `canon/species/punaab.md` line 136
- **Issue**: States the Dying World is in **"MRZ-3"** (unnamed sector between ONI and Ustur space)
- **Correction**: User confirmed it should be **MRZ-31 (Glowhaven)**, not MRZ-3
- **Note**: MRZ-3 is **Abyd-IX** (a MUD civil war sector, completely different)
- **Status**: 🔴 **Needs fix** in `punaab.md`

### 2. Galactic Regions — Outdated Open Question

- **File**: `canon/geography/galactic_regions.md` line 84
- **Issue**: `Q-GEO3: Location of specific ex-colonies (Redam, Mycenas) - MRZ or HRZ?` is still listed as open
- **Correction**: This has been fully resolved — both are MRZ sectors with detailed files
- **Status**: 🟡 **Minor** — close the question

### 3. Galactic Regions — Incomplete Minor Factions List

- **File**: `canon/geography/galactic_regions.md` line 23 and 51
- **Issue**: Only lists "Jorvik, ECOS" as minor factions. Missing: **Anfoil State, Gate Garrison, House Akalma remnant**
- **Status**: 🟡 **Minor** — update when minor factions are fully mapped

### 4. Galactic Regions — Safe Zone Sector Names

- **File**: `canon/geography/galactic_regions.md` lines 33-37
- **Issue**: Lists "Akenat" and "Usturvana" as Safe Zone sector names
  - Akenat is a **planet** (homeworld), not a sector — the sector is **Evernat**
  - "Usturvana" is not confirmed as a sector name anywhere else in canon. The 5 Ustur Safe Zones are: Eternity, Vostalgia, Soletud, Azut, Foy Fields
- **Status**: 🟡 **Needs clarification** — was "Usturvana" an early placeholder?

### 5. COP Starpath Gates — Corrected But Still In Some References

- **File**: Various — corrected in `council_of_peace.md` but some cross-references may still imply COP ownership
- **Correction**: Star Atlas (sentient blockchain) controls the Starpath Gates independently. COP has legal jurisdiction but does not operate them
- **Status**: 🟢 **Already fixed** in main COP file. Spot-check cross-refs

---

## ✅ Previously Flagged KI Errors (Now Corrected in Canon)

These errors existed in the old `master_lore.md` KI artifact and have been corrected in the canon files:

| Error | Old KI Value | Correct Value | Fixed In |
|-------|-------------|---------------|----------|
| Vaor Scarka faction | ECOS leader | **ONI leader** + COP PM | `mierese.md` |
| Sogmian Vows name | "Simian Vows" | **Du Prah** | `sogmian.md` |
| House Lutavira domain | Arts | **Leadership/Success** | `sogmian.md` |
| Akalma status | Listed as active 7th house | **BANISHED** | `sogmian.md` |
| Paizul gender | Male | **Female** | `sogmian.md` |
| Andreza role | ECOS activist | **Removed** (pending clarification) | `mierese.md` |

---

## 📋 Cross-Reference Gaps

These are not errors but areas where cross-references could be strengthened:

1. **Opos.eldr**: Mentioned in COP but has no entry in `ustur.md` character table
2. **Chior.eldr**: Mentioned in `ustur.md` as faction leader but not in COP leadership table
3. **Pearce Corporation**: Referenced in `human.md` and `calico.md` but has no dedicated file
4. **ECOS**: Referenced in many files but has no dedicated faction file (info scattered across `old_grove.md`, `human.md`, `galactic_regions.md`)
5. **Cradle (COP Titan)**: Mentioned in COP, Pergamos, Akalma Exile — power level confirmed (> 3 faction titans combined) but no dedicated file
6. **Ogrika manufacturer**: Detailed in `punaab.md` but has no dedicated file in `manufacturers/`

---

## 🔮 Deferred Topics Queue

Topics confirmed by Creator but tabled for future sessions:

| Topic | Referenced In | Priority |
|-------|--------------|----------|
| Titans (all factions + Cradle power ranking) | `akalma_exile.md`, `council_of_peace.md` | High |
| Termiks (species deep-dive) | Referenced in conversations | Medium |
| House Akalma remnant (HRZ faction) | `akalma_exile.md` | Medium |
| Gate Garrison (Xianyang org) | `xianyang.md` | Medium |
| Frenir (slave/rebellion history) | `council_of_peace.md` | Medium |
| Glowhaven MRZ-31 (Punaab Dying World) | `punaab.md` | Medium |
| Earth Prime (ECOS HRZ base) | `old_grove.md` | Medium |
| MRZ ONI-influenced sectors | Not yet started | High |
| MRZ Ustur-influenced sectors | Not yet started | High |
| HRZ sectors | Not yet started | Medium |
| Dramatis Personae (character files) | `task.md` | Low |
