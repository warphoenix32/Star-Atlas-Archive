# Validation Report

Overall status: **PASS**

- **PASS — deterministic_regeneration**: generator must reproduce every output byte-for-byte
- **PASS — record_and_decision_coverage**: exactly 1,071 unique messages and two complete decision layers
- **PASS — date_coverage**: earliest 2021-03-16 and latest 2026-07-12
- **PASS — promotion_decisions_supported**: every inclusion/exclusion has exact source text and reasons
- **PASS — timeline_decisions_supported**: every timeline decision has exact text plus event/date basis or exclusion
- **PASS — candidate_reconciliation**: candidate indexes equal eligible decisions
- **PASS — provenance_warnings**: collection and authorship warnings preserved on every record
- **PASS — no_orphan_messages**: every semantic message has a source record
- **PASS — duplicate_clusters**: clusters reference preserved evidence and a strongest member
- **PASS — raw_export_checksum**: original Discord export byte-for-byte checksum
- **PASS — json_utf8_parse**: parsed 1094 JSON/JSONL artifacts
- **PASS — manifest_reconciliation**: all recorded bytes and SHA-256 values match
- **PASS — canonical_layers_unchanged**: knowledge, graph, and publication are untouched
- **PASS — discord_not_duplicated**: nested Discord ZIP is not ingested
- **PASS — git_diff_check**: no whitespace errors
