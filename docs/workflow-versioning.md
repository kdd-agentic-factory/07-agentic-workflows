# Workflow Versioning

## Format

```yaml
version: 0.1.0
```

## When to bump versions

| Change type | Version bump |
|---|---|
| Adding an optional input or output | PATCH |
| Adding a new non-breaking step | MINOR |
| Renaming an input, output or step | MINOR |
| Removing an input, output or step | MAJOR |
| Changing approval requirements | MAJOR |
| Changing the KDD stage | MAJOR |

## Initial versioning

All new workflows start at `0.1.0` with `status: proposed`.
They advance to `1.0.0` when they reach `status: validated` and have been executed successfully.
