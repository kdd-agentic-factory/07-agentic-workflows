"""Validate all workflow YAML files against workflow.schema.yaml."""
import sys
from pathlib import Path
import yaml
from jsonschema import validate, ValidationError


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_workflow(workflow_path, schema):
    try:
        workflow = load_yaml(workflow_path)
        validate(instance=workflow, schema=schema)
        return []
    except ValidationError as exc:
        return [f"{workflow_path}: {exc.message}"]
    except Exception as exc:
        return [f"{workflow_path}: {exc}"]


def main():
    repo_root = Path(__file__).parent.parent
    schema = load_yaml(repo_root / "workflow.schema.yaml")
    workflow_files = list((repo_root / "workflows").rglob("*.workflow.yaml"))
    if not workflow_files:
        print("No workflow files found.")
        return 1
    errors = []
    for wf_path in sorted(workflow_files):
        errors.extend(validate_workflow(wf_path, schema))
    if errors:
        print(f"Schema validation FAILED ({len(errors)} error(s)):")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"Schema validation PASSED ({len(workflow_files)} workflow(s) validated).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
