# Foundation Room and Council Evidence Ingestion

This preservation campaign imports:

- the operator-supplied `2026-07-23` Star Atlas Council PIP tracker CSV snapshot;
- the native-ID `😎┃foundation-room` Discord export;
- the native-ID `💥┃fr-chat` Discord export.

The Discord captures are losslessly stored as deterministic gzip files because the
uncompressed `fr-chat` export exceeds GitHub's per-file limit. Provenance records
retain the original filenames, byte counts, SHA-256 values, export identifiers,
collector versions, server and channel IDs, requested ranges, actual ranges, and
collector warnings. Validation reconstructs the original bytes before accepting
the preserved inputs.

The normalized Discord layer is partitioned by channel and month. Each message
retains its native Discord message, channel, server, author, reply, timestamp,
jump-link, attachment metadata, and exact captured text. Display names and aliases
remain exporter observations; they do not independently establish real-world
identity. Media binaries excluded by the collector are not claimed as preserved.

The Council snapshot is preserved separately from the earlier workbook snapshot.
Its payment, implementation, and outcome fields remain attributed as
`COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT`. Reported payment values use
`COUNCIL_REPORTED`; unknown or absent verification remains `UNVERIFIED` or
`MISSING_ONCHAIN_EVIDENCE`. The campaign performs no on-chain verification and
does not collapse proposal, vote, authorization, payment, implementation, or
completion.

Run from the repository root:

```powershell
python operations/campaigns/foundation-room-council-evidence-ingestion-2026-07/build_campaign.py
python operations/campaigns/foundation-room-council-evidence-ingestion-2026-07/validate_campaign.py
```

No files under `knowledge/`, `graph/`, or `publication/` are generated or changed.
