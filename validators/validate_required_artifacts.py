"""Validate that evidence.outputs reference names declared in outputs."""
import sys
from pathlib import Path
import yaml


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_required_artifacts(workflow):
    evidence = workflow.get("evidence", {})
    outputs = workflow.get("outputs", [])
    output_names = {item["name"] for item in outputs if "name" in item}
    evidence_outputs = set(evidence.get("outputs", []))
    missing = evidence_outputs - output_names
    return {"passed": len(missing) == 0, "missing": sorted(missing)}


def main():
    repo_root = Path(__file__).parent.parent
    workflow_files = list((repo_root / "workflows").rglob("*.workflow.yaml"))
    errors = []
    for wf_path in sorted(workflow_files):
        workflow = load_yaml(wf_path)
        result = validate_required_artifacts(workflow)
        if not result["passed"]:
            errors.append(f"{wf_path.name}: evidence.outputs references undeclared outputs: {result['missing']}")
    if errors:
        print(f"Artifact validation FAILED ({len(errors)} error(s)):")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"Artifact validation PASSED ({len(workflow_files)} workflow(s) checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
