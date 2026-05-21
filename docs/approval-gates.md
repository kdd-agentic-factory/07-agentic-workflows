# Approval Gates

## When is approval required?

| Scenario | Required approver role |
|---|---|
| Creates or deletes a GitHub repository | `architecture_owner` |
| Promotes an AutoSkill | `architecture_owner` |
| Modifies a governance policy | `governance_owner` |
| Deploys to Kubernetes | `platform_owner` |
| Rolls back a Kubernetes deployment | `platform_owner` |
| Deploys to Docker in a shared environment | `platform_owner` |
| Applies a setup change to a race car | `crew_chief` |
| Issues qualifying or race strategy | `crew_chief` |
| Generates pre-GP recommendations | `crew_chief` |

## How to declare an approval gate

```yaml
approval:
  required: true
  approver_role: crew_chief
  reason: Pre-GP setup and part recommendations require crew chief approval.
```

And as a step:

```yaml
steps:
  - id: request_approval
    type: approval
    approver_role: crew_chief
```

## Approval audit trail

Every approval gate generates an evidence record:

```json
{
  "workflow_id": "deploy-to-kubernetes",
  "step_id": "request_platform_approval",
  "approver_role": "platform_owner",
  "decision": "approved",
  "approver": "john.doe",
  "timestamp": "2026-05-21T10:30:00Z"
}
```
