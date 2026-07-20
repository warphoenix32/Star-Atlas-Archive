---
source_id: SRC-LORE-REPO-4A332C432AA6
preferred_name: "Star Atlas Master Asset Guide: Inventory & Retrieval"
lore_type: REFERENCE
repository_entity_type: DOCUMENT
upstream_commit: 22555f277eb1496e34c0839c8f1f382842bd1d2b
upstream_path: canon/reference/master_asset_guide.md
authority_scope: ATMTA_AFFILIATED_CANONICAL_LORE_TAXONOMY_AND_NOMENCLATURE
---

# Star Atlas Master Asset Guide: Inventory & Retrieval

## Normalization Note

The text below is a line-ending-normalized derivative of the preserved upstream page. No source wording was rewritten. Taxonomy and link metadata are stored in the paired JSON record.

## Preserved Source Text
# Star Atlas Master Asset Guide: Inventory & Retrieval

This document centralizes the methodologies for retrieving high-resolution assets and catalogs validated models for use as environmental and technical anchors.

---

## 1. Manufacturer Asset Registry (Validated Anchors)

Catalogs assets by manufacturer to ensure architectural consistency in AI-generated scenes.

### 🏛️ Ogrika (Akenat / Punaab Primary)

*Organic curves, bronze/gold metallic hulls, tech-hybrid pods.*

| Model | Role | Local Path |
| :--- | :--- | :--- |
| **Sunpaa** | Luxury Cruiser | `marketplace_assets/ship/Ogrika Sunpaa.jpg` |
| **Jod Asteris** | Heavy Transport | `marketplace_assets/ship/Ogrika Jod Asteris.jpg` |
| **Mik** | Light Interceptor | `marketplace_assets/ship/Ogrika Mik.jpg` |
| **Niruch** | Recon Vessel | `marketplace_assets/ship/Ogrika Niruch.jpg` |
| **Ruch** | General Utility | `marketplace_assets/ship/Ogrika Ruch.jpg` |
| **Thripid** | Specialized Craft | `marketplace_assets/ship/Ogrika Thripid.jpg` |
| **Tursic** | Versatile Hull | `marketplace_assets/ship/Ogrika Tursic.jpg` |

### 🛠️ Calico (MUD/ONI Diplomatic)

*Diplomacy-focused, stealth tech, sustainable agriculture (CARY division). Rivals Pearce Corporation.*

| Model | Role | Local Path |
| :--- | :--- | :--- |
| **Shipit** | Cargo / Transport | `marketplace_assets/ship/Calico Shipit.jpg` |
| **ATS Enforcer** | Security / Police | `marketplace_assets/ship_parts/Ship Parts - Calico ATS Enforcer.png` |
| **Evac** | Medical / Rescue | `marketplace_assets/ship_parts/Ship Parts - Calico Evac.png` |
| **Maxhog** | Heavy Utility | `marketplace_assets/ship_parts/Ship Parts - Calico Maxhog.png` |

### ✨ Busan (Sogmian Luxury)

*Elegant, high-tech, sleek silhouettes, glowing accents.*

| Model | Role | Local Path |
| :--- | :--- | :--- |
| **Maiden Heart** | Luxury Show-piece | `marketplace_assets/ship_parts/Ship Parts - Busan Maiden Heart.png` |
| **Last Stand** | Heavy Combat | `marketplace_assets/ship_parts/Ship Parts - Busan The Last Stand mk. VIII.png` |
| **Thrill of Life** | Racing / Speed | `marketplace_assets/ship_parts/Ship Parts - Busan Thrill of Life.png` |

---

## 2. Character Retrieval (Star Atlas Crew)

### CDN Scraper Pattern

- **CDN Base**: `https://cdn.staratlas.com/crew/v1/{CDN_ID}_full.jpeg`
- **Retrieval Logic**: Use asynchronous batches (max 20 concurrent) to avoid rate limits.

```python
async def download_image(session, img_id, output_dir):
    url = f"https://cdn.staratlas.com/crew/v1/{img_id}_full.jpeg"
    async with session.get(url) as response:
        if response.status == 200:
            (output_dir / f"crew_{img_id:06d}.jpeg").write_bytes(await response.read())
```

### Advanced Filtering (Tensor GraphQL)

Query `api.tensor.so/graphql` using the `staratlascrew` slug to filter by species traits (e.g., Ustur, High Punaab).

---

## 3. Marketplace Retrieval (Ships & Structures)

- **Endpoint**: `https://galaxy.staratlas.com/nfts`
- **Methodology**: Extract high-resolution links from the `image` field in NFT metadata. Links typically point to Google Cloud Storage.

---

## 4. Usage Protocol

1. **Identification**: Match scene faction to manufacturer (Punaab/Akenat = Ogrika, Sogmian = Busan, MUD/ONI diplomacy = Calico).
2. **Path Injection**: Pass the `Local Path` to AI generators via `ImagePaths`.
3. **Prompt Anchor**: explicitly name the model in the prompt for geometric consistency.
