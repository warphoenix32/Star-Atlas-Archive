# Atlas Brew URL Reconciliation

This additive campaign reconciles the public YouTube playlist
`PL4_auqu2sZgDlW6cG3-vfpvLEsQtyaKpB` with the 123 preserved Atlas Brew
transcript Source Records.

It does not rewrite the supplied combined transcript or infer speakers. Stable
YouTube video IDs are the primary external identifiers; canonical watch URLs are
derived from those IDs.

The playlist contains one recording absent from the supplied combined
transcript: Atlas Brew #7 (`Yb8lZZ_zbhE`). YouTube exposes no manual or automatic
caption track for this video. The campaign therefore preserves a separate,
qualified machine transcript derived from the public audio. It does not add the
episode to the immutable combined transcript or reuse one of its 123 Source IDs.

## Commands

```text
python operations/campaigns/atlas-brew-url-reconciliation-2026-07/reconcile_playlist.py generate
python operations/campaigns/atlas-brew-url-reconciliation-2026-07/reconcile_playlist.py validate
python operations/campaigns/atlas-brew-url-reconciliation-2026-07/build_episode_7_artifacts.py generate
python operations/campaigns/atlas-brew-url-reconciliation-2026-07/build_episode_7_artifacts.py validate
```

`transcribe_episode_7.py` is the documented recovery utility. It requires a
locally supplied audio capture and `faster-whisper 1.2.1`; it is not part of
ordinary deterministic CI because the checked-in raw ASR artifact is the fixed
recovery baseline.

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
- Atlas Brew #7 raw, provenance, normalized, Source Record, and ingestion-package
  artifacts under the `atlas-brew-youtube-recovery` archive family
- `archive/manifests/atlas-brew-youtube-recovery-2026-07.json`
- campaign summary, manual-review queue, and validation reports in this folder

The metadata patch is additive and applies only to high-confidence matches.
Existing Source Records remain unchanged until a separately reviewed metadata
application step.

## Atlas Brew #7 recovery boundary

- The recording identity and YouTube publication metadata are high confidence.
- Transcript wording is medium-confidence machine recognition and is not
  presented as a source-supplied transcript.
- Santi and ZeSKK are preserved as hosts attributed by the video description;
  individual transcript segments remain speaker-unattributed.
- The public recording is the verification surface for important claims.
- Semantic extraction and knowledge promotion remain out of scope.
