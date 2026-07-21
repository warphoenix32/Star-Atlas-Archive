# Source Coverage Register

Evidence baseline at `19a447596c6cb3b5e72343a0e6ef9dd87b3e51ed` on 2026-07-20. Package completeness never implies complete external history.

## Medium-by-time matrix

| Source | Medium | Supported interval | Logical records | Status | Priority gaps |
| --- | --- | --- | --- | --- | --- |
| Aephia | written articles | 2021-12-17 to 2026-07-06 | 64 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MANUAL_REVIEW_PENDING | GAP-RAW-WRITTEN, GAP-LEGACY-REVIEW |
| Intergalactic Herald | written articles | 2022-12-11 to 2026-07-03 | 259 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MANUAL_REVIEW_PENDING | GAP-RAW-WRITTEN, GAP-LEGACY-REVIEW |
| Hologram News Network | written articles | 2022-04-08 to 2025-11-11 | 157 | PARTIAL_DATE_COVERAGE, MANUAL_REVIEW_PENDING | GAP-RAW-WRITTEN, GAP-HNN-WRITTEN-FAILURES |
| Official Star Atlas web corpus | web publications and documentation | 2021-03-16 to 2026-07-10 | 320 | PARTIAL_DATE_COVERAGE, CURRENT_TO_CAPTURE_DATE, MANUAL_REVIEW_PENDING | GAP-RAW-WRITTEN, GAP-OFFICIAL-FRESHNESS, GAP-DELETED-OFFICIAL |
| Official Star Atlas Medium | written articles | 2021-01-15 to 2025-10-10 | 520 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, PARTIAL_DATE_COVERAGE, MANUAL_REVIEW_PENDING | GAP-MEDIUM-DISCOVERY, GAP-OFFICIAL-FRESHNESS |
| Star Atlas Discord, repository-designated announcements export | Discord messages | 2021-03-16 to 2026-07-12 | 1071 | CONTINUOUS_REPRESENTED_INTERVAL, CURRENT_TO_CAPTURE_DATE, PARTIAL_DATE_COVERAGE | GAP-DISCORD-CHANNELS, GAP-DISCORD-NATIVE-IDS, GAP-DISCORD-ATTACHMENTS, GAP-OFFICIAL-FRESHNESS |
| Official @staratlas X account | social posts | 2024-11-05 to 2026-07-14 | 796 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, PARTIAL_DATE_COVERAGE, CURRENT_TO_CAPTURE_DATE | GAP-X-HISTORY, GAP-OFFICIAL-FRESHNESS |
| Atlas Brew | video transcripts | unknown to unknown | 4937 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MISSING_REQUIRED_ARTIFACT, MANUAL_REVIEW_PENDING | GAP-ATLAS-BREW-METADATA |
| HNN combined transcript | video transcripts | unknown to unknown | 85 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MISSING_REQUIRED_ARTIFACT | GAP-HNN-TRANSCRIPT-METADATA, GAP-HNN-TRANSCRIPT-SEMANTICS |
| Town Hall, DAO, and Economic Forum transcript package | video transcripts | unknown to unknown | 1910 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, PARTIAL_DATE_COVERAGE, MISSING_REQUIRED_ARTIFACT | GAP-OFFICIAL-TRANSCRIPT-METADATA, GAP-OFFICIAL-BROADCAST-INVENTORY |
| Star Atlas Lore Repository | GitHub documentation and lore pages | unknown to 2026-06-29 | 8430 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, CURRENT_TO_CAPTURE_DATE | GAP-LORE-REFERENCES, GAP-OFFICIAL-FRESHNESS |
| Star Atlas governance and Council PIP tracker | governance records and spreadsheet | unknown to 2026-07-10 | 152 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MANUAL_REVIEW_PENDING, CURRENT_TO_CAPTURE_DATE | GAP-GOVERNANCE-IMPLEMENTATION, GAP-ONCHAIN-EVIDENCE, GAP-OFFICIAL-FRESHNESS |
| PIP-33 vote event reconciliation | Solana vote export | 2026-06-27 to 2026-07-10 | 220 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, PROVENANCE_METADATA_CORRECTION_PENDING | GAP-PIP33-PROVENANCE-CORRECTION, GAP-ONCHAIN-EVIDENCE |
| DAO PIP-1 through PIP-32 vote evidence | Solana vote export | 2024-07-10 to 2026-06-11 | 8404 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MANUAL_REVIEW_PENDING | GAP-ONCHAIN-EVIDENCE, GAP-GOVERNANCE-IMPLEMENTATION |
| Starbased base ship states | spreadsheet/CSV | unknown to 2026-07-18 | 63 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MANUAL_REVIEW_PENDING | GAP-SHIP-UPSTREAM |
| Community wallet attributions | spreadsheet | unknown to 2026-07-19 | 84 | PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE, MANUAL_REVIEW_PENDING | GAP-WALLET-ATTRIBUTION, GAP-ONCHAIN-EVIDENCE |

## Critical interpretation

- The repository contains only one Discord export family, designated as announcements by repository path; no native channel identity was captured.
- The 173 confirmed Medium articles are fully ingested, but publication discovery is incomplete.
- Alpha through Delta preserve extracted text and Source Records but not immutable raw page captures.
- Transcript-package completeness is distinct from complete program or episode coverage.
- Council-reported governance state is not independent implementation or payment evidence.
