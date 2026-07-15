# Knowledge Promotion Campaign 003 — Validation Report

**Validation date:** 2026-07-14

## Passed

- Promotion ledger JSON parses successfully.
- All 24 individually reviewed candidate IDs reconcile to the semantic input.
- All candidate segment IDs, source IDs, and timestamps reconcile to `segment-index.json`.
- Ledger accounting reconciles all 3,306 input candidates: 10 accepted, 3,289 deferred, 4 duplicate, and 3 rejected.
- All 43 local Markdown links in changed and newly added Markdown resolve.
- Schema compatibility suite passed: 3 tests.
- Pipeline assertion suite passed: 5 tests. The environment did not provide `pytest`, so the repository's five plain assertion functions were imported and executed directly.
- `git diff --check` passed.
- No changed path exists under `archive/`, `graph/`, or `publication/`.
- Changed paths are confined to `knowledge/` and `operations/campaigns/knowledge-campaign-003-institutional-expansion/`.

## Repository baseline warning

`operations/migrations/validate_wave_1_5.py` completed its parse and link checks but returned failure because the repository contains 962 reconciliation records while the validator's fixed expectation is 960. Campaign 003 does not modify reconciliation or any archive evidence, so this count drift is outside the authorized scope and remains unchanged for repository-owner review.

Validator output before the count assertion:

- Source records: 800
- Extractions: 800
- Reconciliation records: 962
- Campaign summary files: 8
- Schema packages: 2
- JSON documents parsed: 1,880
- JSONL records parsed: 3,232
- Local Markdown links checked: 334
