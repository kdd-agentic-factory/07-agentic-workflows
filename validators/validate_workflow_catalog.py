"""Validate that every workflow in the catalog has a corresponding file."""
import sys
from pathlib import Path
import yaml


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    repo_root = Path(__file__).parent.parent
    catalog = load_yaml(repo_root / "catalog" / "workflows.yaml")
    errors = []
    for entry in catalog.get("workflows", []):
        workflow_path = repo_root / entry.get("path", "")
        if not workflow_path.exists():
            errors.append(f"Catalog entry '{entry.get('id')}' references missing file: {workflow_path}")
    if errors:
        print(f"Catalog validation FAILED ({len(errors)} error(s)):")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"Catalog validation PASSED ({len(catalog.get('workflows', []))} entries checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
