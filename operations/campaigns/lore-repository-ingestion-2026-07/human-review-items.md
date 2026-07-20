# Lore Repository Human Review Items

## LRH-001 — Upstream identity label

- Status: `ACCEPTED`
- Original decision question: Choose how the Archive should describe the upstream repository without inferring ATMTA authorship.
- Recommended disposition: `KEEP_OPERATOR_DESIGNATED_TAXONOMY_AUTHORITY_WITH_OFFICIAL_AFFILIATION_UNVERIFIED`
- Accepted disposition: `RECOGNIZE_PERSONAL_REPOSITORY_AS_ATMTA_AFFILIATED_CANONICAL_LORE_AUTHORITY`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Decision note: Operator confirms Jose is a Star Atlas team member responsible for lore; his personal repository is treated as ATMTA-affiliated and canonical for lore taxonomy and nomenclature.
- Allowed dispositions: `KEEP_OPERATOR_DESIGNATED_TAXONOMY_AUTHORITY_WITH_OFFICIAL_AFFILIATION_UNVERIFIED`, `DESCRIBE_AS_OFFICIAL_STAR_ATLAS_SOURCE`, `DESCRIBE_AS_FAN_CURATED_SOURCE`
- Evidence: `LRC-001-AUTHORITY-LABEL`, `archive/provenance/lore-repository/authority-assessment.json`

## LRH-002 — Galia Expanse legacy mapping

- Status: `ACCEPTED`
- Original decision question: Map LORE-GALIA to the region, the atlas reference document, both, or neither.
- Recommended disposition: `MAP_TO_REGION_AND_RETAIN_ATLAS_DOCUMENT_AS_REFERENCE`
- Accepted disposition: `MAP_TO_REGION_AND_RETAIN_ATLAS_DOCUMENT_AS_REFERENCE`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `MAP_TO_REGION_AND_RETAIN_ATLAS_DOCUMENT_AS_REFERENCE`, `MAP_TO_ATLAS_DOCUMENT`, `MAP_TO_BOTH`, `DEFER`
- Evidence: `canon/geography/galactic_regions.md`, `canon/reference/atlas/galia_expanse_atlas.md`

## LRH-003 — Council of Peace entity split

- Status: `ACCEPTED`
- Original decision question: Decide whether the institution and faction pages represent distinct canonical entities or two views of one entity.
- Recommended disposition: `KEEP_DISTINCT_INSTITUTION_AND_FACTION_ENTITIES_WITH_SHARED_ALIAS`
- Accepted disposition: `KEEP_DISTINCT_INSTITUTION_AND_FACTION_ENTITIES_WITH_SHARED_ALIAS`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `KEEP_DISTINCT_INSTITUTION_AND_FACTION_ENTITIES_WITH_SHARED_ALIAS`, `MERGE_AS_ONE_INSTITUTION`, `MERGE_AS_ONE_FACTION`, `DEFER`
- Evidence: `canon/institutions/council_of_peace.md`, `canon/factions/council_of_peace.md`

## LRH-004 — Ustur entity split

- Status: `ACCEPTED`
- Original decision question: Decide whether Ustur species and Ustur faction remain distinct canonical entities.
- Recommended disposition: `KEEP_DISTINCT_SPECIES_AND_FACTION_ENTITIES_WITH_SHARED_NAME`
- Accepted disposition: `KEEP_DISTINCT_SPECIES_AND_FACTION_ENTITIES_WITH_SHARED_NAME`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `KEEP_DISTINCT_SPECIES_AND_FACTION_ENTITIES_WITH_SHARED_NAME`, `MAP_LEGACY_ID_TO_FACTION_ONLY`, `MAP_LEGACY_ID_TO_SPECIES_ONLY`, `DEFER`
- Evidence: `canon/species/ustur.md`, `canon/factions/ustur.md`

## LRH-005 — Star Atlas: CORE legacy entity

- Status: `ACCEPTED`
- Original decision question: Choose whether to preserve the unmatched legacy entity or defer it until a direct upstream page is acquired.
- Recommended disposition: `PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING`
- Accepted disposition: `PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING`, `DEPRECATE_LEGACY_ENTITY`, `RESEARCH_FOR_DIRECT_PAGE`
- Evidence: `LORE-NARRATIVE-CORE`, `operations/campaigns/lore-repository-ingestion-2026-07/taxonomy-migration-report.json`

## LRH-006 — The Voice of Iris legacy entity

- Status: `ACCEPTED`
- Original decision question: Choose whether to preserve the unmatched legacy entity or defer it until a direct upstream page is acquired.
- Recommended disposition: `PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING`
- Accepted disposition: `PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `PRESERVE_LEGACY_ENTITY_AND_DEFER_NEW_MAPPING`, `DEPRECATE_LEGACY_ENTITY`, `RESEARCH_FOR_DIRECT_PAGE`
- Evidence: `LORE-VOICE-OF-IRIS`, `operations/campaigns/lore-repository-ingestion-2026-07/taxonomy-migration-report.json`

## LRH-007 — Source branch and live deployment

- Status: `ACCEPTED`
- Original decision question: Confirm whether current main remains the ingestion authority even though the live gh-pages deployment is older.
- Recommended disposition: `KEEP_CURRENT_MAIN_AS_SOURCE_AND_PRESERVE_LIVE_SITE_AS_SEPARATE_SNAPSHOT`
- Accepted disposition: `KEEP_CURRENT_MAIN_AS_SOURCE_AND_PRESERVE_LIVE_SITE_AS_SEPARATE_SNAPSHOT`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `KEEP_CURRENT_MAIN_AS_SOURCE_AND_PRESERVE_LIVE_SITE_AS_SEPARATE_SNAPSHOT`, `USE_LIVE_DEPLOYMENT_TEXT`, `WAIT_FOR_REDEPLOYMENT`
- Evidence: `LRC-003-BRANCH-AUTHORITY`, `LRC-004-DEPLOYMENT-STALE`

## LRH-008 — Canon/docs mirror divergence policy

- Status: `ACCEPTED`
- Original decision question: Choose the standing rule for 86 divergent canon/docs page pairs.
- Recommended disposition: `CANON_CONTROLS_TAXONOMY_AND_BOTH_TEXT_VARIANTS_REMAIN_PRESERVED`
- Accepted disposition: `CANON_CONTROLS_TAXONOMY_AND_BOTH_TEXT_VARIANTS_REMAIN_PRESERVED`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `CANON_CONTROLS_TAXONOMY_AND_BOTH_TEXT_VARIANTS_REMAIN_PRESERVED`, `DOCS_CONTROLS_PUBLISHED_TEXT`, `REQUIRE_PAGE_BY_PAGE_ADJUDICATION`
- Evidence: `operations/campaigns/lore-repository-ingestion-2026-07/mirror-divergence-ledger.json`
- Evidence count: 86

## LRH-009 — Unresolved upstream links

- Status: `ACCEPTED`
- Original decision question: Choose whether 252 broken source-local links remain preserved defects or receive a later repair campaign.
- Recommended disposition: `PRESERVE_SOURCE_AND_STAGE_SEPARATE_LINK_REPAIR_CAMPAIGN`
- Accepted disposition: `PRESERVE_SOURCE_AND_STAGE_SEPARATE_LINK_REPAIR_CAMPAIGN`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `PRESERVE_SOURCE_AND_STAGE_SEPARATE_LINK_REPAIR_CAMPAIGN`, `LEAVE_PERMANENTLY_UNRESOLVED`, `REPAIR_NORMALIZED_LINKS_NOW`
- Evidence: `operations/campaigns/lore-repository-ingestion-2026-07/unresolved-reference-ledger.json`
- Evidence count: 252

## LRH-010 — Live sitemap-only ONI/CSS lore page

- Status: `ACCEPTED`
- Original decision question: Classify the live sitemap URL that is absent from current docs but present in the canon source tree.
- Recommended disposition: `KEEP_AS_CANON_SOURCE_WITH_STALE_DEPLOYMENT_PROVENANCE`
- Accepted disposition: `CLASSIFY_AS_HISTORICAL_CANONICAL_SOURCE_SNAPSHOT_NOT_CURRENT_TAXONOMY`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Decision note: The ONI/CSS page is canonical-source evidence for its captured historical state, not current canonical taxonomy.
- Allowed dispositions: `KEEP_AS_CANON_SOURCE_WITH_STALE_DEPLOYMENT_PROVENANCE`, `TREAT_AS_LIVE_SITE_ONLY`, `DEFER`
- Evidence: `canon/geography/oni_css_lore_layer.md`, `https://joseeduardonoot.github.io/star-atlas-lore/geography/oni_css_lore_layer/`

## LRH-011 — Self-reported chronology ordering errors

- Status: `ACCEPTED`
- Original decision question: Adjudicate or defer each of the 12 source-reported chronology ordering errors.
- Recommended disposition: `DEFER_INDIVIDUAL_CORRECTIONS_UNTIL_OFFICIAL_PRIMARY_EVIDENCE_IS_ATTACHED`
- Accepted disposition: `DEFER_INDIVIDUAL_CORRECTIONS_UNTIL_OFFICIAL_PRIMARY_EVIDENCE_IS_ATTACHED`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `DEFER_INDIVIDUAL_CORRECTIONS_UNTIL_OFFICIAL_PRIMARY_EVIDENCE_IS_ATTACHED`, `ACCEPT_UPSTREAM_ORDER`, `CORRECT_SELECTED_ITEMS_WITH_CITATIONS`
- Evidence: embedded structured evidence, embedded structured evidence, embedded structured evidence, embedded structured evidence, embedded structured evidence
- Evidence count: 12

## LRH-012 — Possible contradiction clusters

- Status: `ACCEPTED`
- Original decision question: Adjudicate or dismiss each of the 20 machine-flagged lexical contradiction clusters.
- Recommended disposition: `TREAT_AS_RESEARCH_CANDIDATES_NOT_CONFIRMED_CONTRADICTIONS`
- Accepted disposition: `TREAT_AS_RESEARCH_CANDIDATES_NOT_CONFIRMED_CONTRADICTIONS`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `TREAT_AS_RESEARCH_CANDIDATES_NOT_CONFIRMED_CONTRADICTIONS`, `REVIEW_CLUSTER_BY_CLUSTER`, `ACCEPT_AS_CONTRADICTIONS`
- Evidence: embedded structured evidence, embedded structured evidence, embedded structured evidence, embedded structured evidence, embedded structured evidence
- Evidence count: 20

## LRH-013 — Orphaned timeline years

- Status: `ACCEPTED`
- Original decision question: Decide whether seven unindexed years require timeline additions or should remain source-local references.
- Recommended disposition: `PRESERVE_AS_RESEARCH_GAPS_PENDING_TIMELINE_EVIDENCE_REVIEW`
- Accepted disposition: `PRESERVE_AS_RESEARCH_GAPS_PENDING_TIMELINE_EVIDENCE_REVIEW`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Allowed dispositions: `PRESERVE_AS_RESEARCH_GAPS_PENDING_TIMELINE_EVIDENCE_REVIEW`, `ADD_TO_LORE_TIMELINE_INDEX`, `DISMISS_AS_NON_EVENT_REFERENCES`
- Evidence: embedded structured evidence, embedded structured evidence, embedded structured evidence, embedded structured evidence, embedded structured evidence
- Evidence count: 7

## LRH-014 — Embedded workstation paths

- Status: `ACCEPTED`
- Original decision question: Choose whether normalized display copies should redact two upstream absolute workstation paths while raw evidence remains immutable.
- Recommended disposition: `PRESERVE_RAW_AND_REDACT_ONLY_IN_FUTURE_PUBLICATION_OUTPUTS`
- Accepted disposition: `PRESERVE_RAW_REDACT_NORMALIZED_AND_PUBLIC_OUTPUTS`
- Decided by: `REPOSITORY_OPERATOR`
- Decided at: `2026-07-19`
- Decision note: Absolute workstation paths remain only in immutable raw evidence and are redacted from normalized records and public-facing derivatives.
- Allowed dispositions: `PRESERVE_RAW_AND_REDACT_ONLY_IN_FUTURE_PUBLICATION_OUTPUTS`, `PRESERVE_EVERYWHERE`, `REDACT_NORMALIZED_DISPLAY_COPIES`
- Evidence: embedded structured evidence, embedded structured evidence
- Evidence count: 2
