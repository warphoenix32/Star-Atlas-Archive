# Semantic Validation Report — Revised

Status: **PASS**

## Checks

- `json_documents_parsed`: 14
- `source_ids_reconciled`: 36
- `source_ids_unique`: True
- `segment_ids_reconciled`: 1910
- `segment_ids_unique`: True
- `caption_lines_covered`: 78752
- `segment_line_ranges_valid`: True
- `segment_timestamps_valid`: True
- `segment_ranges_non_overlapping`: True
- `controlled_taxonomies_only`: True
- `no_speaker_identity_inferred`: True
- `entity_link_records_reconciled`: 1910
- `canonical_entity_ids_registered`: True
- `quotes_verbatim`: 41
- `promotion_candidates_reconciled`: 76
- `timeline_candidates_reconciled`: 83
- `every_promotion_candidate_has_support`: True
- `every_timeline_candidate_has_support_and_date_basis`: True
- `promotion_decisions_reconciled`: 1910
- `timeline_decisions_reconciled`: 1910
- `every_exclusion_has_reason`: True
- `all_candidate_ids_reconcile`: True
- `duplicate_clusters_reconciled`: 3
- `clustered_candidates`: 6
- `research_gap_sources_reconciled`: 36
- `candidate_research_gaps_typed`: 357
- `quality_manifest_checksums_match`: True
- `generator_deterministic`: True
- `python_sources_compile`: True
- `schema_tests_pass`: True
- `pipeline_tests_pass`: True
- `allowed_paths_only`: True
- `canonical_layers_modified`: False
- `git_diff_check_pass`: True

## Warnings

- All speaker attribution remains UNKNOWN.
- Original URLs are absent and publication dates are incomplete for 33 sources.
- Candidate confidence measures extraction quality, not factual truth.
- Automated transcript text may contain recognition errors.
- Repository Wave 1.5 validation has inherited fixed-count drift: 962 reconciliation records versus an expected 960.
