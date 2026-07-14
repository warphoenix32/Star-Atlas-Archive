# HNN Transcript Archive Promotion Validation

## Package

- Campaign ID: `hnn-combined-transcript`
- Input archive: `HNN_transcript_archive_campaign.zip`
- Input archive SHA-256: `22dfad8dfbbb44de7e81b12b1acf47252491b6ea8fc39e4923de0906b188801b`
- Packaged files: 180
- Manifest-listed artifacts: 179; the manifest intentionally does not checksum itself
- Repository schema: 2.1

## Validation

- ZIP CRC and safe-path validation: PASS
- Packaged artifacts copied byte-for-byte: PASS (180 of 180)
- Manifest size and SHA-256 verification: PASS (179 of 179)
- JSON parsing: PASS (92 of 92)
- Markdown structural and relative-link validation: PASS (87 of 87)
- UTF-8 decoding: PASS
- Source IDs: PASS (85 unique; no repository collisions)
- Entity IDs: PASS (none emitted by this campaign)
- Campaign ID: PASS (unique in the repository)
- Raw-to-normalized internal references: PASS
- Campaign counts: PASS (85 Source Records; 53,935 transcript segments)
- Duplicate titles and sources: PASS (none reported)

## Promotion Scope

The campaign was promoted only into `archive/` and `operations/campaigns/`. No files under `knowledge/`, `graph/`, or `publication/` were modified. The proposed knowledge and graph deltas supplied by the campaign remain staged and empty.

## Review Warnings

The supplied campaign reports four manual-review blockers: original URLs are absent, publication dates are absent, many speaker identities are absent, and semantic extraction/external verification has not yet been performed. Reconciliation remains `NOT_STARTED`. These limitations are preserved without reinterpretation.

The legacy Wave 1.5 migration validator is snapshot-specific: it hard-codes exactly 960 reconciliation JSON files and reports the campaign's valid reconciliation index as an unexpected 961st file. Its JSON parsing and local Markdown-link checks pass, and the campaign-specific manifest validation passes. The migration validator was not changed because it is outside this promotion's authorized paths.
