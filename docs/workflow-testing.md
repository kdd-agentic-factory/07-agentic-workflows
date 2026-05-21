# Workflow Testing

## Test categories

- `test_workflow_schema.py` - All workflow YAML files conform to workflow.schema.yaml
- `test_approval_gates.py` - Approval gate validator logic
- `test_required_artifacts.py` - Evidence outputs reference declared outputs
- `test_workflow_catalog.py` - Catalog entries have files, required fields, unique IDs
- `test_workflow_dependencies.py` - Dependency references resolve to known IDs

## Running tests

```bash
python -m pytest tests/ -v
make test
```

## CI enforcement

Tests run automatically on every pull request via `.github/workflows/validate-workflows.yml`.
A PR cannot merge if any workflow fails schema validation, lacks required approval gates,
has missing evidence outputs, missing catalog files, or broken dependencies.
