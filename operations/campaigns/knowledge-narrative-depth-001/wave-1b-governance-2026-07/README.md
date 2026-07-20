# Knowledge Revision Wave 1B — Governance

This campaign revises every human-readable page in `knowledge/governance/` and reconciles the machine-readable PIP ledger with the preserved PIP-33 ballot source.

## Editorial objective

The domain now reads as an institutional history rather than a collection of governance fields. It introduces the DAO, Foundation, Council, proposal lifecycle, constitutional development, elections, funding, and terminal cases through connected narratives. Taxonomy and review controls remain in front matter and campaign artifacts instead of interrupting the public text.

## Evidence boundary

- proposal, vote, passage, authorization, implementation, payment, and independent verification remain separate;
- election advancement is not final election, and an intended term is not proof of service;
- Council tracker statements remain attributed operational assessments;
- the completed-binary rule remains an owner-approved editorial adjudication, not PIP-1 text;
- PIP-33 ballot evidence does not establish payment or implementation;
- no treasury transaction or deliverable is independently verified without its primary artifact.

## Commands

```text
python operations/campaigns/knowledge-narrative-depth-001/wave-1b-governance-2026-07/build_wave.py
python operations/campaigns/knowledge-narrative-depth-001/wave-1b-governance-2026-07/validate_wave.py
```

The generator produces deterministic evidence packets, inventory, revision ledger, and summary. The validator checks metadata, narrative depth, references, internal links, PIP-33 vote/payment boundaries, generated-artifact reconciliation, and repository scope.
