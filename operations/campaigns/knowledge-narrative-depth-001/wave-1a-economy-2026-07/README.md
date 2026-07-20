# Knowledge Revision Wave 1A — Economy

This campaign revises the seven pages in `knowledge/economy/` as the first implementation slice of the complete 80-page baseline.

## Editorial objective

The pages are written for human readers while retaining source-linked limitations. Machine taxonomy remains in front matter; the public narrative explains identity, chronology, evidence state, conflicts, and missing artifacts without exposing pipeline mechanics as the main reading experience.

## Evidence boundary

- historical token quantities remain dated publisher claims;
- proposal passage remains separate from payment and implementation;
- Council tracker fields remain attributed operational assessments;
- PIP-33's captured vote confirms its ballot result only;
- no on-chain payment verification is claimed;
- report publication is separate from metric verification.

## Commands

```text
python operations/campaigns/knowledge-narrative-depth-001/wave-1a-economy-2026-07/build_wave.py
python operations/campaigns/knowledge-narrative-depth-001/wave-1a-economy-2026-07/validate_wave.py
```

The generator is deterministic. The validator checks page metadata, narrative depth, evidence paths, internal links, generated-artifact reconciliation, repository scope, and the PIP-33 vote/payment boundary.
