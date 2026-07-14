# Public written corpus ingestion

This review-gated pipeline normalizes a preserved creator-grouped inventory into one deterministic record per canonical URL. Normalization performs no network requests, never modifies its input, and never promotes records into canonical knowledge.

## Install and run

From the repository root:

```powershell
python -m pip install -e operations/pipeline
python -m star_atlas_ingest.cli normalize `
  archive/raw/manifests/star_atlas_content_url_inventory_2026-07-12.json `
  archive/normalized/manifests/normalized-urls.jsonl `
  --provenance archive/provenance/manifests/star_atlas_content_url_inventory_2026-07-12.provenance.json
```

Output is sorted by stable `url_id`, so rerunning the same inventory is reproducible. Written public platforms are marked `PENDING`; audiovisual, private, and unsupported platforms are retained as metadata with `DEFERRED`.

## Repository flow

```text
source
-> archive/raw
-> archive/normalized
-> archive/source-records and archive/ingestion-packages
-> proposed knowledge updates and proposed graph updates
-> human review
-> knowledge/ and graph/
```

Campaign code must write archival artifacts beneath `archive/` and must not automatically update `knowledge/` or `graph/`. Promotion is a separate, reviewed operation.

## Safety boundaries

- Preserve source manifests byte-for-byte and record their SHA-256 digest.
- Do not fetch, bypass robots rules, or evade access controls during normalization.
- Keep raw retrievals and generated state out of canonical knowledge files.
- Promote generated records only after human review.

## Tests

```bash
python -m pytest -c operations/pipeline/pyproject.toml operations/tests/pipeline
```
