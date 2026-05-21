"""Validate that workflows with critical tools declare approval.required = true."""
import sys
from pathlib import Path
import yaml

CRITICAL_TOOL_PREFIXES = [
    "kubernetes.apply",
    "kubernetes.rollback",
    "docker.run",
    "github.delete",
    "simulation.apply_setup",
    "race_command.apply_setup",
]


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_approval_gates(workflow):
    steps = workflow.get("steps", [])
    approval = workflow.get("approval", {})
    critical_steps = [
        step for step in steps
        if any(step.get("tool", "").startswith(p) for p in CRITICAL_TOOL_PREFIXES)
    ]
    if critical_steps and not approval.get("required"):
        return {
            "passed": False,
            "message": "Workflow contains critical tools but approval.required is false.",
            "critical_steps": [s.get("id") for s in critical_steps],
        }
    return {"passed": True, "message": "Approval gates valid."}


def main():
    repo_root = Path(__file__).parent.parent
    workflow_files = list((repo_root / "workflows").rglob("*.workflow.yaml"))
    errors = []
    for wf_path in sorted(workflow_files):
        workflow = load_yaml(wf_path)
        result = validate_approval_gates(workflow)
        if not result["passed"]:
            errors.append(f"{wf_path.name}: {result['message']} Steps: {result.get('critical_steps')}")
    if errors:
        print(f"Approval gate validation FAILED ({len(errors)} error(s)):")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"Approval gate validation PASSED ({len(workflow_files)} workflow(s) checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
