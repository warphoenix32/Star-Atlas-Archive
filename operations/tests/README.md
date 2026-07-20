# Tests

Repository tests cover ingestion compatibility, schema contracts, campaign-specific validation, the Library front end, the simplified promotion pipeline, and repository-local agent contracts. The promotion tests verify that only fully qualified R1 candidates can be automatically approved onto draft branches and that elevated-risk candidates retain human-review and authorization requirements. Agent-contract tests preserve the four-stage ownership model, human-controlled merge authority, human-first narrative standard, and public taxonomy boundary.

Run from the repository root:

```bash
python -m pytest -c operations/pipeline/pyproject.toml operations/tests/pipeline
python operations/tests/schema/test_schema_compatibility.py
python operations/migrations/validate_wave_1_5.py
```
