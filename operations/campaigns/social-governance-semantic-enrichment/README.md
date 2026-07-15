# Social Media and PIP Semantic Enrichment

This campaign preserves full semantic recall for 796 `@staratlas` posts and 33 official PIPs while maintaining separate, precision-oriented candidate layers. It never modifies canonical `knowledge/`, `graph/`, or `publication/` content.

## Deterministic decision model

Social promotion requires an identifiable institutional object plus a concrete action, relationship, or date/amount/metric. Retweets, questions without answers, weak marketing, engagement prompts, and weaker duplicate variants are excluded. Scores reward identifiable objects, concrete event language, specific details, explicit relationships, and canonical entity links. Eligible scores map to `HIGH_PRIORITY` (7+), `MEDIUM_PRIORITY` (5-6), or carefully justified `LOW_PRIORITY` (4); confidence describes extraction quality, not factual truth.

Timeline candidates independently require a material event type, identifiable entity/system, exact supporting post text, and the official post publication date as the date basis. All included and excluded decisions remain auditable in JSONL.

Near-duplicate clustering uses normalized exact text or deterministic token overlap of at least 0.72 with six shared meaningful tokens. Evidence is never deleted; each cluster identifies its strongest record and ordered members.

## Governance rules

Completed binary PIPs use `YES > NO => PASSED` and `NO >= YES => FAILED`; abstentions are recorded but non-decisive and no quorum is required. Ranked-choice PIPs use only the portal `electionResults` field. Raw portal status, reviewed vote result, approval, and implementation are separate. A passed vote is never implementation evidence.

The governing human review is `pip-corpus-review.md` with structured conclusions in `pip-corpus-review-summary.json`. Every semantic PIP record is reconciled to it and marked `REVIEWED`.

## Reproduction

```text
python operations/campaigns/social-governance-semantic-enrichment/build_campaign.py
python operations/campaigns/social-governance-semantic-enrichment/validate_campaign.py
```
