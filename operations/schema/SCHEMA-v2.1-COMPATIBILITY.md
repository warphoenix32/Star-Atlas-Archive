# Repository Schema v2.1 Backward Compatibility Report

## Result

Repository Schema v2.1 is backward compatible with Wave 1 v2.0 ingestion packages.

## Compatibility decisions

- All v2.0 top-level collections remain valid.
- New fields are additive.
- v2.0 entity `name` remains accepted as a fallback for `canonical_name`.
- Scalar confidence values remain accepted.
- Legacy object-level source, speaker, and timestamp fields remain accepted.
- Existing IDs remain valid and are preserved through `legacy_ids` during optional migration.
- Raw transcripts and historical packages are not rewritten automatically.

## Known limitations

v2.0 records may lack separately modeled provenance, evidence arrays, typed entities, explicit related entities, and granular confidence. Absence means the information was not captured, not that it is false.

## Validation matrix

| Capability | v2.0 | v2.1 |
|---|---:|---:|
| Package accepted | Yes | Yes |
| Existing IDs preserved | Yes | Yes |
| Typed entities | Optional/absent | Supported |
| Provenance object | Optional/absent | Supported |
| Evidence arrays | Optional/absent | Supported |
| Claim lifecycle | Limited | Expanded |
| Related entities | Optional/absent | Supported |
| Granular confidence | Optional/absent | Supported |
| Raw/normalized/extraction model | Not required | Documented standard |

## Conclusion

No Wave 1 artifact requires destructive migration. New ingestion should use v2.1; older artifacts may be enriched opportunistically when they are already under review.
