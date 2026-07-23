# Atlas Brew URL Reconciliation

This additive campaign reconciles the public YouTube playlist
`PL4_auqu2sZgDlW6cG3-vfpvLEsQtyaKpB` with the 123 preserved Atlas Brew
transcript Source Records.

It does not rewrite transcript text, infer speakers, or ingest playlist-only
videos. Stable YouTube video IDs are the primary external identifiers; canonical
watch URLs are derived from those IDs.

## Commands

```text
python operations/campaigns/atlas-brew-url-reconciliation-2026-07/reconcile_playlist.py generate
python operations/campaigns/atlas-brew-url-reconciliation-2026-07/reconcile_playlist.py validate
```

## Matching policy

Candidate scoring uses:

- exact episode number: 70%;
- normalized title similarity: 20%;
- transcript-to-video duration agreement: 10%.

A match is high confidence only when it has an exact episode number, a score of
at least 0.82, and a margin of at least 0.08 over the next candidate.
Medium-confidence matches and unmatched records remain in the manual-review
queue. Duplicate episode numbers are never resolved by episode number alone.

## Outputs

- `archive/provenance/atlas-brew-combined/youtube-playlist-manifest.json`
- `archive/reconciliation/atlas-brew-combined/youtube-url-reconciliation.json`
- `archive/reconciliation/atlas-brew-combined/youtube-source-metadata-patch.json`
- campaign summary, manual-review queue, and validation reports in this folder

The metadata patch is additive and applies only to high-confidence matches.
Existing Source Records remain unchanged until a separately reviewed metadata
application step.
