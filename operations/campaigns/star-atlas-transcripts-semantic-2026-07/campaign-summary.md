# Star Atlas Transcript Semantic Enrichment — Revised

This revision preserves the separation between lexical tags and candidate eligibility, and replaces the blanket unknown-speaker penalty with claim-specific speaker dependency while retaining all 1,910 semantic segments and all 78,752 caption assignments.

- Promotion candidates: **1,909 → 81** (1829 excluded with recorded reasons)
- Timeline candidates: **1,590 → 90** (1820 excluded with recorded reasons)
- Quote candidates: **526 → 107**
- Near-duplicate promotion clusters: **3**
- Promotion confidence: {'HIGH': 17, 'LOW': 8, 'MEDIUM': 56}
- Timeline confidence: {'HIGH': 36, 'MEDIUM': 54}
- Quote confidence: {'MEDIUM': 107}

- Speaker dependency: {'NONE': 419, 'PARTIAL': 464, 'REQUIRED': 1027}

Every retained candidate includes exact caption references, deterministic reasons, confidence, and manual-review status. Excluded promotion and timeline decisions remain auditable. PR #11 is merged; this branch is based on current `main`. No archive evidence or canonical layers were modified.
