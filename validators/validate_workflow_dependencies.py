"""Validate that workflow dependency references resolve to known workflow IDs."""
import sys
from pathlib import Path
import yaml


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    repo_root = Path(__file__).parent.parent
    catalog = load_yaml(repo_root / "catalog" / "workflows.yaml")
    deps = load_yaml(repo_root / "catalog" / "workflow-dependencies.yaml")
    known_ids = {entry["id"] for entry in catalog.get("workflows", [])}
    errors = []
    for dep in deps.get("dependencies", []):
        wf_id = dep.get("workflow_id")
        if wf_id not in known_ids:
            errors.append(f"Unknown workflow_id in dependencies: '{wf_id}'")
        for dep_wf in dep.get("depends_on_workflows", []):
            if dep_wf not in known_ids:
                errors.append(f"Workflow '{wf_id}' depends on unknown workflow: '{dep_wf}'")
    if errors:
        print(f"Dependency validation FAILED ({len(errors)} error(s)):")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"Dependency validation PASSED ({len(deps.get('dependencies', []))} entries checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
