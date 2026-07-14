---
title: Star Atlas Public Source Registry
entry_type: source-registry
status: active
updated: 2026-07-12
publication_status: public
---

# Star Atlas Public Source Registry

This registry records public source families and individual high-value sources discovered during open-source sweeps. Each major source should eventually receive an individual record with capture date, author, completeness, archival status and the claims it supports.

## Official project sources

| Source ID | Source | Function | Reliability notes |
|---|---|---|---|
| SRC-OFF-WEBSITE | https://staratlas.com/ | Current public positioning, products, economy counters and community links | Strong for current official claims; not a historical archive |
| SRC-OFF-NEWSROOM | https://experience.staratlas.com/newsroom | Official announcement and newsletter archive | Strong for what was publicly announced at a given time; page contains test or duplicate entries requiring review |
| SRC-OFF-ROADMAP | https://staratlas.notion.site/ | Official roadmap linked from the newsroom | Roadmaps describe intentions and priorities, not proof of delivery |
| SRC-OFF-GALIA | https://staratlas.com/game/galia/ | Current setting and gameplay description | Official current lore and product positioning |
| SRC-OFF-LIFE-GALIA | https://staratlas.com/game/life-in-galia/ | Factions, Council of Peace, Tufa and current lore summary | Official current canon; check against earlier publications |
| SRC-OFF-PRESS-KIT | https://experience.staratlas.com/newsroom/press-kit | Founding date, white papers, economics paper, visual assets | Strong official index; linked documents require separate ingestion |
| SRC-OFF-SUPPORT-TOKENS | https://support.staratlas.com/hc/en-us/articles/47061439814547-What-are-the-Star-Atlas-tokens | Current ATLAS and POLIS descriptions | Official support language; updated Dec. 8, 2025 |
| SRC-OFF-EPIC-FAQ | https://store.epicgames.com/p/star-atlas-faq-fb116c | UE5 product description, iterative release strategy and historical feature snapshot | Official storefront content but may contain stale roadmap language |

## Governance and economy

| Source ID | Source | Function | Reliability notes |
|---|---|---|---|
| SRC-DAO-PROPOSALS | https://govern.staratlas.com/proposals | Proposal discovery and voting interface | Proposal text proves what was proposed, not execution |
| SRC-DAO-ECON-REPORTS | https://govern.staratlas.com/economy/economic-reports | Quarterly economic-report archive | Primary official economic series; methodology may evolve |
| SRC-OFF-ECON-LEGACY | https://experience.staratlas.com/newsroom/economic-reports | Legacy economic-report publication index and disclaimer | Useful for publication dates, duplicate entries and historical presentation |
| SRC-DAO-TREASURY | https://govern.staratlas.com/treasury | Treasury interface | Time-sensitive; values require timestamp and asset-level review |

## Builder and technical sources

| Source ID | Source | Function | Reliability notes |
|---|---|---|---|
| SRC-BUILD-HOME | https://build.staratlas.com/ | Official builder, IP and technical documentation hub | Strong for supported integration surfaces |
| SRC-BUILD-WHAT-IS-SA | https://build.staratlas.com/introduction/what-is-star-atlas | Current product architecture | Official current product summary |
| SRC-BUILD-ONCHAIN | https://build.staratlas.com/dev-resources/on-chain-game-systems | On-chain systems index | Documentation presence is not proof of full production readiness |
| SRC-BUILD-SECURITY | https://build.staratlas.com/dev-resources/program-security | Official program-security claim | Attribute the general audit claim; verify individual reports and scope separately |
| SRC-BUILD-RPC | https://build.staratlas.com/developer-rpc-initiative | Developer RPC support program | Official eligibility and program description; operational availability may change |
| SRC-GITHUB-ORG | https://github.com/staratlasmeta | Verified official open-source organization | Strong for code and repository history; deployment claims require verification |

## Community and independent sources

| Source ID | Source | Function | Reliability notes |
|---|---|---|---|
| SRC-COMM-AEPHIA-HOME | https://aephia.com/ | Aephia DAC, publishing and resource hub | Guild-affiliated source; useful for discovery and institutional self-description |
| SRC-COMM-AEPHIA-NEWS | https://aephia.com/star-atlas-news/ | Numbered Weekly Star Atlas Newsletter series and other news | Strong contemporaneous aggregator; older forecasts and guides may be superseded |
| SRC-COMM-AEPHIA-GUIDES | https://aephia.com/star-atlas-guides/ | Gameplay, product, tooling and ecosystem guides | Time-sensitive operational documentation; verify against current products |
| SRC-COMM-AEPHIA-ABOUT | https://aephia.com/star-atlas/about-aephia-industries/ | Aephia self-description, projects and publication model | Authoritative for stated identity and goals, not independent proof of size or awards |

Additional approved source families requiring individual assessment:

- Hologram News Network / The Hologram
- VBTV, formerly Star Atlas TV
- Intergalactic Herald
- Galia Crafters
- MetaVerse Explorer and other long-running video archives
- Atlas Brew recordings
- Guild websites, Discord announcements and public governance statements
- Podcast directories and preserved RSS feeds
- Reddit, X, Medium, YouTube, Facebook and Instagram archives
- Solana explorers and independent analytics dashboards

Community sources are especially valuable for chronology, reaction and institutional memory, but claims should be attributed and cross-checked where practical.

## Completed index artifacts

- `Official-Newsroom-Index.md`
- `../05-economy-and-assets/Economic-Report-Catalog.md`
- `../11-technology-and-infrastructure/Official-Technical-Surface-Inventory.md`
- `../04-game-and-product-history/Official-Current-State-Snapshot-2026-07-12.md`
- `../12-media-and-creators/Aephia-Source-Profile.md`
- `../12-media-and-creators/Aephia-Weekly-Newsletter-Index.md`

## Archival priorities

- Download and hash official white papers and economics papers.
- Preserve all quarterly economic reports locally.
- Archive proposal pages and final vote results.
- Export official GitHub repository metadata and release histories.
- Preserve official newsroom and roadmap snapshots.
- Ingest each high-value newsroom article into chronology and product records.
- Enumerate the complete Aephia weekly newsletter archive and preserve issue metadata.
- Reconcile Aephia forecasts against later releases and official records.
- Recover HNN article URLs, podcast feeds and video metadata.
- Create source records for major Discord exports without publishing sensitive raw content.
