# Workflow Lifecycle

## States

```
proposed -> validated -> active -> deprecated -> disabled
```

## State definitions

### proposed
Newly written, not validated or used. Can be modified freely.

### validated
Passes all validators and tests. Minimum state for production use.

### active
Used by the orchestrator in at least one successful execution.

### deprecated
Superseded by a newer version. Kept for compatibility and audit trail.

### disabled
Cannot be executed. Kept for historical record only.

## Transition rules

| From | To | Condition |
|---|---|---|
| proposed | validated | Passes all validators and tests |
| validated | active | At least one successful orchestrator execution |
| active | deprecated | Superseded by newer version |
| active | disabled | Security or compliance issue |
| deprecated | disabled | No longer needed for compatibility |
