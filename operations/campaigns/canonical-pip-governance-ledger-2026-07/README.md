# Canonical PIP and Governance Ledger Campaign

This campaign builds one evidence-qualified record for each numbered proposal from PIP-1 through PIP-33. It expands the existing PIP Registry instead of creating a competing human governance index.

## Outputs

- `knowledge/governance/PIP-Registry.json` — machine-readable ledger.
- `knowledge/governance/PIP-Registry.md` — human-readable ledger.
- `conflict-report.json` and `.md` — unresolved and adjudicated source conflicts.
- `governance-research-backlog.json` and `.md` — prioritized missing-artifact plan.
- `campaign-summary.json` and `.md` — campaign scope and counts.
- `validation-report.json` and `.md` — deterministic validation evidence.
- `manifest.json` — checksums for campaign and ledger artifacts.

## Evidence policy

The official portal captures establish proposal text, dates, ballot counts, PVP, candidate options, and any preserved election result list. The reviewed semantic registry supplies explicitly labeled result adjudications. Council tracker data remains a Council-authored operational assessment and never becomes independent payment or implementation verification.

The completed-binary YES-versus-NO rule is an owner-approved repository editorial adjudication. It is not asserted as PIP-1 text. Elections use only their captured ranked-choice evidence. Candidate-level PVP is missing from every election capture and remains null. Repeated Solana sentinel values in captured candidate-wallet fields are preserved as placeholders, never normalized as candidate identities.

Treasury state fields use only `REQUESTED`, `AUTHORIZED`, `COUNCIL_REPORTED`, `UNVERIFIED`, `MISSING_ONCHAIN_EVIDENCE`, or null. No on-chain verification is attempted because the required transaction dataset was not supplied.

## Reproduction

```text
python operations/campaigns/canonical-pip-governance-ledger-2026-07/build_ledger.py
python operations/campaigns/canonical-pip-governance-ledger-2026-07/validate_ledger.py
```

The outputs remain `QUALIFIED`, `DRAFT_FOR_REVIEW`, and `HUMAN_REVIEW_REQUIRED` after structural validation. Human approval is a separate step.

The validator executes the checked-in Draft 2020-12 schema through a campaign-local, fail-closed evaluator covering every keyword used by the schema. It also performs evidence, checksum, mechanism, lifecycle, reconciliation, path-scope, and deterministic-regeneration checks.
