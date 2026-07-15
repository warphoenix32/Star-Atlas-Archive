# Star Atlas Transcript Semantic Enrichment — Revised

PR #12 now separates lexical tag detection from promotion, timeline, and quote eligibility while preserving all 1,910 semantic segments and all 78,752 caption assignments.

- Promotion candidates: **1,909 → 76** (1834 excluded with recorded reasons)
- Timeline candidates: **1,590 → 83** (1827 excluded with recorded reasons)
- Quote candidates: **526 → 41**
- Near-duplicate promotion clusters: **3**
- Promotion confidence: {'HIGH': 3, 'LOW': 26, 'MEDIUM': 47}
- Timeline confidence: {'HIGH': 1, 'MEDIUM': 82}
- Quote confidence: {'MEDIUM': 41}

Every retained candidate includes exact caption references, deterministic reasons, confidence, and manual-review status. Excluded promotion and timeline decisions remain auditable. PR #11 is merged; this branch is based on current `main`. No archive evidence or canonical layers were modified.
