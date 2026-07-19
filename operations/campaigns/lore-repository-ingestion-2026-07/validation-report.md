# Lore Repository Ingestion Validation

- Result: `PASS`
- Checks passed: 44 / 44
- Source pages: 192
- Entities: 4632
- Relationships: 3798
- Documented upstream warning groups: 0

## Checks

- [x] `raw_commit_archive_sha256`
- [x] `raw_commit_archive_byte_length`
- [x] `source_snapshot_file_count`
- [x] `source_text_utf8`
- [x] `raw_workstation_paths_preserved`
- [x] `generated_artifacts_fixed_point`
- [x] `deterministic_build`
- [x] `all_generated_json_parses`
- [x] `all_generated_jsonl_parses`
- [x] `campaign_counts_reconcile`
- [x] `upstream_commit_pinned`
- [x] `source_ids_unique`
- [x] `normalized_page_pairs_complete`
- [x] `source_record_pairs_complete`
- [x] `every_page_has_complete_artifact_chain`
- [x] `entity_ids_unique`
- [x] `entity_sources_reconcile`
- [x] `repository_entity_types_schema_compatible`
- [x] `controlled_lore_taxonomy_only`
- [x] `authority_boundary_explicit`
- [x] `relationship_ids_unique`
- [x] `relationship_sources_reconcile`
- [x] `relationships_are_evidence_bound_references`
- [x] `unresolved_references_documented`
- [x] `repository_file_inventory_complete`
- [x] `every_markdown_page_inventoried`
- [x] `working_material_excluded_not_lost`
- [x] `media_inventory_and_extraction_reconcile`
- [x] `existing_lore_ids_all_mapped_or_deferred`
- [x] `curator_adjudicated_mappings_resolved`
- [x] `historical_rewrites_prohibited`
- [x] `provenance_branch_and_deployment_distinct`
- [x] `atmta_affiliation_operator_confirmed_not_inferred_from_capture`
- [x] `human_review_register_curator_adjudicated`
- [x] `oni_css_historical_snapshot_not_current_taxonomy`
- [x] `workstation_paths_redacted_from_normalized_and_public_derivatives`
- [x] `licensing_requirements_removed`
- [x] `schema_v21_package_minimum`
- [x] `ingestion_did_not_promote_knowledge_or_graph`
- [x] `campaign_and_archive_manifests_match`
- [x] `manifest_checksums_reconcile`
- [x] `prohibited_repository_domains_untouched`
- [x] `changed_paths_within_campaign_scope`
- [x] `git_diff_check`

## Interpretation

A passing result means the preserved snapshot, generated artifact chains, controlled taxonomy, identifiers, manifests, and repository boundaries reconcile. It does not resolve the documented upstream identity, mirror, chronology, link, or legacy-mapping warnings.
