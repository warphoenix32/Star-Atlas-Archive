# Repository Operations

Engineering and archival operations live here, separate from historical evidence and canonical knowledge.

- [`schema/`](schema/README.md): repository and ingestion schemas
- [`templates/`](templates/README.md): source and knowledge record templates
- [`pipeline/`](pipeline/README.md): ingestion package and CLI
- [`campaigns/`](campaigns/README.md): campaign and promotion reports
- [`migrations/`](migrations/README.md): architecture and schema migrations
- [`tests/`](tests/README.md): compatibility and preservation validation
- [`docs/`](docs/README.md): doctrine and implementation documentation
- [`agents/`](agents/README.md): repository role contracts, handoff boundaries, and specialist activation rules

New campaigns should use the [Simplified Promotion Pipeline](docs/SIMPLIFIED-PROMOTION-PIPELINE.md): `PRESERVE -> DRAFT -> REVIEW -> PUBLISH`. The visible workflow is compact while risk-based checks retain stricter handling for consequential claims. Staging remains distinct from promotion, and automated approval never authorizes a merge to `main`.
