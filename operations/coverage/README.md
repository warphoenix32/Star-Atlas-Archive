# Repository Coverage

This directory is the Research and Gap Analyst's repository-wide account of preserved holdings, supported date and medium coverage, unresolved gaps, campaign status, cleanup candidates, and refresh policy.

The baseline is generated deterministically:

```text
python operations/coverage/build_inventory.py
python operations/coverage/validate_inventory.py
```

`url-disposition-overlay.jsonl` is a generated reconciliation layer over the immutable 3,232-row discovery inventory. It records exact campaign results and deterministic aggregate exclusions while leaving unsupported rows explicitly unresolved. The historical inventory is never rewritten to imply later campaign state.

The economic-report branch assessment and the Phase 2 recovery schedule close planning gates only. They do not authorize collection, merge the stale branch, or change preserved evidence.

Coverage means that evidence is present for the stated interval or supplied package. It does not imply that an external publication, channel, account, or program is complete unless the record states an independently reproducible completeness basis.

The registers must be reviewed at every campaign closeout. Collection and ingestion remain separately authorized work.
