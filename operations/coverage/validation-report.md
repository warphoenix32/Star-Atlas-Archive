# Phase 1 Validation Report

**Result:** `PASS`

## Checks

- **PASS — deterministic_generation:** {'expected': 17, 'generated': 17}
- **PASS — json_parses:** {'files': 10, 'errors': []}
- **PASS — coverage_records:** 15
- **PASS — coverage_evidence_paths_resolve:** []
- **PASS — coverage_gaps_reconcile:** []
- **PASS — campaign_registry:** 19
- **PASS — campaign_status_evidence_resolves:** []
- **PASS — archive_holdings_reconcile:** {'path': 'archive', 'files': 8291, 'bytes': 267075970}
- **PASS — normalized_inventory_boundary:** {'records': 3232, 'pending': 902, 'deferred': 2330, 'status': 'STALE_REQUIRES_RECONCILIATION', 'path': 'archive/normalized/manifests/normalized-urls.jsonl'}
- **PASS — no_unconditional_repository_deletions:** []
- **PASS — seven_phase_roadmap:** [1, 2, 3, 4, 5, 6, 7]
- **PASS — phase_one_active:** {'phase': 1, 'name': 'Repository and evidence baseline', 'status': 'READY_FOR_REVIEW', 'percent_complete': 85, 'remaining_gate_items': ['Reconcile stale normalized URL dispositions', 'Classify the unique economic-report branch', 'Schedule recovery campaigns for missing raw captures']}
- **PASS — library_index_fixed_point:** PASS search index fixed point: 80 records
- **PASS — social_campaign_status_reconciled:** {'summary': 'PASS', 'validation': 'PASS'}

## Limitations

- The register is a repository snapshot, not proof of external corpus completeness.
- Freshness adapters are policy-defined but not implemented.
- Windows lore fixed-point comparison remains sensitive to Git CRLF conversion; Linux repository CI is authoritative until line-ending policy is added.
