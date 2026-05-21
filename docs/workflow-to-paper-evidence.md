# Workflow to Paper Evidence

## Methodological contribution

> The Agentic Workflows repository formalizes multi-agent execution as declarative, versioned and
> auditable workflows, enabling reproducible coordination between agents, tools, skills, data
> pipelines, documentation, simulation and human approval.

## Measurable claims

| Metric | What it shows |
|---|---|
| `workflow_completion_rate` | Fraction of executions that complete without failure |
| `workflow_approval_compliance` | Fraction of critical actions with recorded approval |
| `workflow_evidence_generation_rate` | Fraction of executions producing all required evidence |
| `workflow_reuse_rate` | Distinct workflows used across experiments |
| `workflow_kdd_stage_coverage` | Fraction of KDD stages covered by at least one workflow |

## Evidence workflows

| Workflow | Paper artefact |
|---|---|
| `generate-paper-section` | Paper section with evidence packet |
| `export-paper-evidence` | Evidence packet from KDD data |
| `export-evidence-packet` | Evidence packet from knowledge base |
| `generate-reproducibility-report` | Reproducibility report |
| `build-paper-artifact` | Final assembled paper |

## KDD coverage table

| KDD Stage | Workflows | Status |
|---|---|---|
| selection | ingest-telemetry-session, ingest-document, index-repository | proposed |
| preprocessing | clean-telemetry | proposed |
| transformation | extract-features, build-cag-cache | proposed |
| data_mining | mine-patterns, tire-collapse-prediction | proposed |
| interpretation | pre-grand-prix, run-setup-what-if, fp1-analysis, race-strategy | proposed |
| documentation | generate-paper-section, create-new-feature, validate-autoskill | validated |
| deployment | deploy-to-kubernetes, rollback-kubernetes | proposed |
