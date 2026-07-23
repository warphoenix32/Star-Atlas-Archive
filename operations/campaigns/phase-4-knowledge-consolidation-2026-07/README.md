# Phase 4 Knowledge Consolidation

Campaign ID: `phase-4-knowledge-consolidation-2026-07`

This campaign consolidates existing, reviewed repository evidence into current
human-readable knowledge. It does not ingest new sources and does not create
public Library articles.

## Gate 1

The first gate:

- inventories the 81-file knowledge corpus;
- selects ten historically valuable dossier candidates;
- creates three evidence packets for newly merged evidence;
- updates stale Medium, Atlas Brew, and economic-report knowledge;
- keeps archive evidence, graph facts, and publication outputs unchanged.

The dossier portfolio is a Phase 4 planning and evidence artifact. It does not
add entries to the publication manifest or authorize Phase 5 drafting.

## Gate 2

The second gate completes reviewed evidence packets for all ten selected
dossiers. Each packet states:

- which evidence authority supports the dossier;
- which material claims are safe to carry forward;
- which tempting inferences are prohibited;
- which unresolved artifacts still limit the history.

Gate 2 does not rewrite source evidence or knowledge prose. Its purpose is to
freeze the evidence boundary before the ten dossiers are deliberately
consolidated. Reader-oriented lore entity pages remain part of that next
consolidation gate.

## Validation

```text
python operations/campaigns/phase-4-knowledge-consolidation-2026-07/validate_campaign.py origin/main
python -m unittest discover operations/tests/phase4_knowledge_consolidation
```
