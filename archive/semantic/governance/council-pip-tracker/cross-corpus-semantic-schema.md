# Cross-Corpus Semantic Schema

## Source classes

- `TIER_1_OFFICIAL_DISCORD_ANNOUNCEMENT`
- `TIER_1_COUNCIL_OPERATIONAL_TRACKER`
- `TIER_1_COUNCIL_REVIEW_GUIDANCE`

## Required epistemic distinctions

- announcement ≠ release;
- proposal ≠ vote;
- passed ≠ implemented;
- milestone reported complete ≠ independently verified completion;
- Council ROI assessment ≠ independently verified outcome;
- operational tracker status ≠ immutable historical record;
- withdrawn after passage ≠ failed vote;
- terminated or canceled implementation preserves the original passed result.

## Cross-corpus reconciliation keys

- PIP number and UUID;
- event date;
- title and canonical entity;
- product or program name;
- announcement source ID;
- Council tracker row source ID;
- implementation evidence URI or transaction ID.

## Promotion policy

Both the Discord announcement enrichment and Council tracker enrichment are review layers.
Canonical promotion requires:

1. exact supporting source;
2. explicit attribution;
3. lifecycle reconciliation;
4. contradiction and supersession review;
5. independent implementation evidence where an execution claim is made.
