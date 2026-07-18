# Official Star Atlas Medium Validation Report

**Result: PASS**

- Included records: 173
- Successfully validated artifact sets: 173
- Errors: 0
- Warnings: 0

## Checks

```json
{
  "artifact_sets": {
    "included": 173,
    "validated_successes": 173
  },
  "campaign_manifest_artifacts": 1567,
  "candidate_dispositions": {
    "invalid": 0,
    "total": 686
  },
  "corpus_status_boundary": {
    "confirmed_2020": 0,
    "confirmed_article_ingestion_status": "COMPLETE",
    "publication_discovery_status": "INCOMPLETE"
  },
  "coverage_2020": {
    "confirmed_articles_included": 0,
    "surface_queried": true
  },
  "deterministic_outputs": {
    "current_sha256": "655eaeb4ecbd57e05f6d6f8fdb97dca2ba49b93fd2077c7a156f7da0b1fd5915",
    "expected_sha256": "655eaeb4ecbd57e05f6d6f8fdb97dca2ba49b93fd2077c7a156f7da0b1fd5915",
    "match": true,
    "verified_rerun_match": true
  },
  "discovery_coverage": {
    "surfaces": [
      "profile_page",
      "publication_archive",
      "publication_page",
      "repository",
      "rss:profile",
      "rss:publication",
      "sitemap",
      "web_archive"
    ],
    "years": [
      2020,
      2021,
      2022,
      2023,
      2024,
      2025,
      2026
    ]
  },
  "git_diff_check": true,
  "included_identity": {
    "included": 173,
    "unique_post_ids": 173,
    "unique_source_ids": 173
  },
  "manual_review_adjudication": {
    "explicitly_deferred": 51,
    "incomplete_deferred": 0,
    "received": 329,
    "resolved_excluded": 278
  },
  "scope": {
    "changed_paths": 1572,
    "prohibited": []
  }
}
```

## Preserved legacy warning

- operations/migrations/validate_wave_1_5.py contains hard-coded legacy artifact counts and is not an additive-campaign gate.
