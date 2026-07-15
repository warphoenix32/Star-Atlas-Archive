# Validation report

Overall status: **PASS**

## Checks

- **PASS — Raw and normalized counts**: 799 raw rows; 796 normalized posts
- **PASS — Unique post IDs reconcile**: 796 unique evidence IDs and 796 semantic IDs
- **PASS — Duplicate rows remain documented**: Three duplicate export rows remain in the preserved raw CSV
- **PASS — Original/retweet counts**: 528 originals and 268 explicit retweets
- **PASS — PIP sequence and UUIDs**: PIP-1 through PIP-33; 33 unique UUIDs
- **PASS — Source ID uniqueness**: 829 campaign source IDs are unique
- **PASS — URL validity**: All social and governance URLs are absolute HTTPS URLs
- **PASS — Controlled social taxonomies**: All assigned social tags are controlled values
- **PASS — Retweet evidence boundary**: No retweet is promoted as an original first-party claim
- **PASS — Governance lifecycle separation**: Proposal, vote, approval, and execution use distinct fields
- **PASS — Execution evidence rule**: No execution inferred from a passed vote
- **PASS — No orphan semantic records**: Every semantic record has a source record

## Scope

Only `archive/` and `operations/campaigns/social-governance-semantic-enrichment/` are changed by this campaign. Canonical knowledge, graph facts, and publication outputs remain untouched.

## Repository validation context

- The three standalone schema compatibility tests pass.
- The five pipeline test functions pass when invoked directly; `pytest` is not installed in the available runtimes.
- The legacy `validate_wave_1_5.py` validator reports a baseline mismatch: it expects 960 reconciliation files while current `main` contains 962. This campaign does not add or modify reconciliation files.
- Campaign-specific dependency-free validation parses all campaign JSON/JSONL, verifies manifest hashes, checks source-ID collisions, and reconciles every social and governance record.
