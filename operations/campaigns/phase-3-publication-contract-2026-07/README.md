# Phase 3 Publication Contract

Campaign ID: `phase-3-publication-contract-2026-07`

This campaign closes Phase 3 of the Star Atlas Library roadmap by defining the
reviewed handoff from canonical `knowledge/` into the public Library. It does
not create public articles, rewrite evidence, or change the current GitHub
Pages site.

## Scope

- Establish one human-first publication contract.
- Establish a deterministic, machine-readable publication manifest.
- Keep only `PUBLISHED` entries eligible for the public build.
- Hide internal workflow metadata from ordinary readers.
- Preserve the ten official-source freshness candidates unchanged.
- Reconcile the Atlas Brew URL/date gap closed by the completed playlist
  campaign.
- Condense the four placeholder publication READMEs into pointers without
  deleting their paths.

## Protected paths

The campaign must not modify:

- `archive/`
- `knowledge/`
- `graph/`
- `publication/site/`

## Validation

Run:

```text
python operations/campaigns/phase-3-publication-contract-2026-07/validate_campaign.py
python -m unittest discover operations/tests/publication_contract
```

The validator writes deterministic JSON and Markdown reports. Phase 4 may
start only after the contract, roadmap, coverage reconciliation, and path
boundaries pass.
