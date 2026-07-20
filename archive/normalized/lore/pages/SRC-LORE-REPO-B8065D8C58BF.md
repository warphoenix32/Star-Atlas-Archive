---
source_id: SRC-LORE-REPO-B8065D8C58BF
preferred_name: "Star Atlas Species Master Guide: Identification & Pipeline"
lore_type: TAXONOMY
repository_entity_type: DOCUMENT
upstream_commit: 22555f277eb1496e34c0839c8f1f382842bd1d2b
upstream_path: canon/species/species_master_guide.md
authority_scope: ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_AND_NOMENCLATURE
---

# Star Atlas Species Master Guide: Identification & Pipeline

## Normalization Note

The text below is a line-ending-normalized derivative of the preserved upstream page. No source wording was rewritten. Taxonomy and link metadata are stored in the paired JSON record.

## Preserved Source Text
# Star Atlas Species Master Guide: Identification & Pipeline

This guide centralizes all identifiers and procedural logic for classifying the various species within the Star Atlas Galia Expanse.

---

## 1. Visual Identification Heuristics

### MUD (Manus Ultima Divina) - Humans

- **Visuals**: Standard biological humans.
- **Clothing**: Tactical "PEARCE" gear, corporate uniforms, headsets.
- **Traits**: High hair color variety (Red, Blue, Cyan, Multicolor).
- **Reference IDs**: 001-002, 006-007, 013-026, 029, 031 (F, Red hair), 032 (F, Blue hair), 034 (F, Cyan hair, Monocle), 038 (F, Multicolor), 039 (M, Blonde), 040-051, 055, 060, 065, 070, 080, 090, 100, 110, 120, 130, 140, 150, 166, 169, 185, 195, 210, 235, 300.

### Ustur (Sentient Androids)

- **Visuals**: Robotic/mechanical humanoid constructs.
- **Key Features**: Geometric plates, cyan/orange/blue core illumination. High armor variety with distinctive helmet types: Sleek, Bird-like/Avian (orange/yellow), Beetle-like, Insect-like, and Horned.
- **Reference IDs**: 003, 004, 005, 008-011, 033, 035, 036, 167, 170-178, 180, 200, 225, 250, 290.

### Sogmian (Warrior Philosophers)

- **Visuals**: Noble alienoids, purple/pale blue skin.
- **Dimorfismo**:
  - **Sogmian Male**: Smoother head, distinctive cranial structure.
  - **Sogmian Female**: Glowing red visors; head-tails/tentacles.
- **Reference IDs**: 012 (F), 028 (F), 165 (M), 205. (Note: Initial scan of 160-200 range showed high density of Mierese, High Punaab and Ustur).

### Mierese (Ethereal Oral storytellers)

- **Visuals**: Lavender/lilac skin, slender frames, pointed ears.
- **Dimorfismo**:
  - **Mierese Male**: Extremely long dreadlock-like head tentacles.
  - **Mierese Female**: Shorter braid-like tentacles, elaborate cranial crest.
- **Reference IDs**: 160 (M), 163 (F), 164 (F), 168 (M), 190 (F), 215 (F), 220 (F), 240 (F), 260 (F), 270 (F).

### Punaab (Sentient Mammals) ⚠️ SCALE SENSITIVE

- **High Punaab**: White/light tiger-patterned fur. Ornate gold mantles. **NO tails**. **Scale**: 60cm (Knee height).
- **Profound Punaab**: Grey/dark fur. Small furry constructs. **NO tails**. Tactical/industrial gear with monocles. **Scale**: 40cm (Calf height).
- **Reference IDs**:
  - **High**: 161, 162, 198, 280.
  - **Profound**: 027, 030, 037.

### Tufa (Metagenic Swarm)

- **Visuals**: Biomechanical and mineral hybrids; crystalline shell structures.
- **Key Features**: Strange geometric forms, pulsing energy cores.

### Photoli (Beings of Light)

- **Visuals**: Extra-galactic lifeforms made of pure essence/energy.
- **Schism**: 7 Dark Photoli (arrogant predatory exiles who consume essence). Mainstream Photoli = benevolent teachers with hidden agenda to access Iris.

---

To manage the acervo of 350+ unique crew members, assets are organized through a dedicated script-driven pipeline.

### Current Inventory Status (Feb 2026)

- **Total identified assets**: 350
- **Total classified assets**: 101 (28.8% progress)
- **Classification Pace**: Lotes de 10-20 imagens via inspeção visual.
- **Range Observations**: Lower ranges (000-100) are predominantly MUD (humans). Range 160-200 shows high density of Ustur, Mierese, and Punaab.
- Mierese: 10
- Ustur: 25
- Sogmian: 4
- Punaab (High + Profound): 7
- MUD: 55

⚠️ **Goal**: Complete classification for the remaining 249 assets to reach 100% coverage.

### Detailed ID Lookup (Species by ID Range/List)

- **Ustur**: [3, 4, 5, 8-11, 33, 35, 36, 167, 170-178, 180, 200, 225, 250, 290]
- **Sogmian**: [12, 28, 165, 205]
- **Mierese**: [160, 163, 164, 168, 190, 215, 220, 240, 260, 270]
- **High Punaab**: [161, 162, 198, 280]
- **Profound Punaab**: [27, 30, 37]
- **MUD**: [1, 2, 6, 7, 13-26, 29, 31, 32, 34, 38-51, 55, 60, 65, 70, 80, 90, 100, 110, 120, 130, 140, 150, 166, 169, 185, 195, 210, 235, 300]

### Directory Structure

```text
star_atlas_crew/
├── all_crews/             # Raw harvested JPEG assets
│   ├── crew_000XXX.jpeg   # Padded naming convention (001-300)
│   └── crew_X.jpeg        # Non-padded naming convention (1-50)
├── species/               # Classified assets
│   ├── mud/ | ustur/ | sogmian/ | mierese/ | high_punaab/ | profound_punaab/
├── species_classifier.py  # Primary sorting script
├── classifications.json   # Unified metadata mapping (Species/Gender)
└── scene_generator.py     # Production pipeline for character scenes
```

### Classification Workflow

1. **Audit**: Visual identification using the heuristics in Section 1.
2. **Hardcoded Mapping**: Update `KNOWN_CLASSIFICATIONS` dictionary in `species_classifier.py`.
3. **Execution**: Run `species_classifier.py` to physically move files and generate `classifications.json`.
4. **Scene Generation**: `scene_generator.py` queries the JSON to select characters and inject specific "Grimdark" descriptors.
