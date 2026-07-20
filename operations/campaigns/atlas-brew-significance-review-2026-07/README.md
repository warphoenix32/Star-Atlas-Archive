# Atlas Brew Significance Review — 2026-07

This campaign revises the semantic decision layer created by Atlas Brew Semantic Retagging Campaign 001. It does not re-segment transcripts, infer speakers, or modify normalized evidence.

## Purpose

The original layer preserved all 4,937 discussion segments but promoted 3,306 and treated 1,423 as timeline events. This review separates recall from selection:

- the segment index remains complete;
- statement and lifecycle tags use stricter contextual rules, with legacy tags retained for audit;
- every promotion and timeline decision records eligibility, confidence, reasons, exact captions, and an exclusion reason;
- unknown speaker attribution affects confidence only when the claim depends on personal or institutional authority;
- every retained item remains traceable to an Atlas Brew recording, Source ID, and timestamp.

## Commands

```text
python operations/campaigns/atlas-brew-significance-review-2026-07/review_semantic_layer.py
python operations/campaigns/atlas-brew-significance-review-2026-07/validate_review.py
```

## Evidence boundary

The campaign assesses whether a discussion contains useful evidence. It does not declare transcript claims true, identify an unknown speaker, convert roadmap language into delivery, or promote canonical knowledge.
