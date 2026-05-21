# Architecture

## Repository role

`07-agentic-workflows` is the workflow definition layer of the KDD-governed agentic platform.

```
00-kdd-governance          defines rules and policies
01-agent-orchestrator      executes workflows
07-agentic-workflows       defines workflows  <- this repository
02-mcp-gateway             executes tools
04-skills-autoskills-registry   executes skills
05-documentation-agent     generates documentation
06-kdd-data-pipelines      processes data
15-race-command-center / 16-race-ai-copilot / 17-digital-twin-simulation-lab
                           consume and produce operational actions
```

## What this repository contains

- Workflow definitions (YAML)
- Schemas (JSON Schema)
- Catalog (index of all workflows with metadata)
- Validators (Python scripts)
- Tests (pytest suites)
- Documentation
- Examples (sample workflow run inputs)

## What this repository does NOT contain

- APIs or microservices
- Business logic or algorithms
- ML models or training code
- Kubernetes or Docker manifests
- Dashboard UI code
- Telemetry processing code

## Orchestrator integration

```
orchestrator.run(workflow_id, inputs)
    -> load catalog/workflows.yaml
    -> find workflow by id
    -> validate inputs against workflow.inputs
    -> execute steps sequentially
    -> for each step: invoke agent | skill | tool | pause for approval
    -> collect evidence
    -> report metrics
    -> return outputs
```

## Metrics emitted

```
workflow_execution_total
workflow_execution_duration_seconds
workflow_approval_required_total
workflow_approval_rejected_total
workflow_evidence_generated_total
workflow_failure_total
workflow_kdd_stage_total
workflow_skill_usage_total
workflow_tool_usage_total
```
