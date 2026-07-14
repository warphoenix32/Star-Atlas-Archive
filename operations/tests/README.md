# Tests

Run from the repository root:

```bash
python -m pytest -c operations/pipeline/pyproject.toml operations/tests/pipeline
python operations/tests/schema/test_schema_compatibility.py
python operations/migrations/validate_wave_1_5.py
```
