# Applied Review Corrections

The Chief of Staff review identified three overstatements in the first generated reconciliation layer. The branch now applies conservative corrections:

1. The 24 broad event sequences are withdrawn. Category-plus-entity grouping is insufficient to establish shared event identity across months or years.
2. The 148 Discord promotion candidates remain available in the single-source Discord queue, but are removed from the cross-source queue until each has an explicit second-source relationship.
3. The contradiction artifact now reports only that deterministic rules found zero explicit conflicts in the relationships evaluated. It does not claim the corpora contain no contradictions.

Run order for deterministic regeneration:

```text
python operations/campaigns/discord-announcements-semantic-enrichment/build_campaign.py
python operations/campaigns/discord-announcements-semantic-enrichment/apply_review_corrections.py
python operations/campaigns/discord-announcements-semantic-enrichment/validate_campaign.py
```

Future event-sequence generation must require a shared event or incident identifier plus bounded temporal adjacency. Future cross-source promotion records must identify the additional source and claim-level relationship.
