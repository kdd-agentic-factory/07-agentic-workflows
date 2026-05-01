from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_WORKFLOWS = {
    "create-new-repository.workflow.yaml",
    "create-new-feature.workflow.yaml",
    "create-new-skill.workflow.yaml",
    "validate-autoskill.workflow.yaml",
    "generate-paper-section.workflow.yaml",
    "run-kdd-experiment.workflow.yaml",
    "deploy-to-docker.workflow.yaml",
    "deploy-to-kubernetes.workflow.yaml",
}

EXPECTED_EXAMPLES = {
    "feature-document-analysis",
    "feature-telemetry-anomaly",
    "paper-section-generation",
}

REQUIRED_WORKFLOW_KEYS = (
    "id:",
    "version:",
    "description:",
    "inputs:",
    "outputs:",
    "guards:",
    "steps:",
)


def test_expected_top_level_files_exist():
    assert (ROOT / "README.md").is_file()
    assert (ROOT / "AGENTS.md").is_file()
    assert (ROOT / "workflows").is_dir()
    assert (ROOT / "examples").is_dir()
    assert (ROOT / "tests").is_dir()


def test_expected_workflows_exist():
    workflow_names = {path.name for path in (ROOT / "workflows").glob("*.workflow.yaml")}
    assert workflow_names == EXPECTED_WORKFLOWS


def test_workflows_expose_required_contract_keys():
    for workflow_path in (ROOT / "workflows").glob("*.workflow.yaml"):
        content = workflow_path.read_text(encoding="utf-8")
        missing_keys = [key for key in REQUIRED_WORKFLOW_KEYS if key not in content]
        assert not missing_keys, f"{workflow_path.name} misses {missing_keys}"


def test_examples_are_documented():
    example_names = {path.name for path in (ROOT / "examples").iterdir() if path.is_dir()}
    assert example_names == EXPECTED_EXAMPLES

    for example_name in EXPECTED_EXAMPLES:
        readme = ROOT / "examples" / example_name / "README.md"
        assert readme.is_file()
        assert "Separacion de responsabilidades" in readme.read_text(encoding="utf-8")
