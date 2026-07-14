# Repository Operations

Engineering and archival operations live here, separate from historical evidence and canonical knowledge.

- [`schema/`](schema/README.md): repository and ingestion schemas
- [`templates/`](templates/README.md): source and knowledge record templates
- [`pipeline/`](pipeline/README.md): ingestion package and CLI
- [`campaigns/`](campaigns/README.md): campaign and promotion reports
- [`migrations/`](migrations/README.md): architecture and schema migrations
- [`tests/`](tests/README.md): compatibility and preservation validation
- [`docs/`](docs/README.md): doctrine and implementation documentation

Future ingestion follows `source -> archive/raw -> archive/normalized -> archive/source-records and archive/ingestion-packages -> proposed knowledge/graph updates -> human review`. Staging remains distinct from promotion.
