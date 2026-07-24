# Phase 5 Knowledge Readiness Wave

This wave closes the thirteen targeted Knowledge gaps identified by the approved
Phase 5 publication portfolio. It creates or expands reviewed-style Knowledge
dossiers; it does not publish Library articles.

Run:

```text
python build_campaign.py
python validate_campaign.py
```

The build reads the fixed page portfolio and produces evidence packets and
campaign reports. Validation checks metadata, evidence paths, Markdown links,
front-matter states, portfolio reconciliation, and forbidden repository scope.

Human semantic review was completed on 2026-07-23. The operator adjudicated
manufacturer coverage, independent FTX corroboration, the standard for
high-confidence current-membership inference, and the historical canonical
lore-snapshot treatment. The decisions are retained in
`human-adjudication-ledger.json`; the reviewed pages are approved as future
publication inputs.
