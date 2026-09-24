# Iteration receipt schema

```json
{
  "schema_version": 1,
  "run_id": "from contract.json",
  "iteration": 1,
  "status": "running",
  "action": "One bounded action performed",
  "evidence_paths": ["evidence/example.txt"],
  "checks": [
    {
      "id": "contract machine check id",
      "passed": true,
      "evidence": "Fresh command and result summary"
    }
  ],
  "judgments": [
    {
      "criterion": "Exact judgment criterion from contract.json",
      "passed": true,
      "evidence": "Fresh file, line, screenshot, or review evidence"
    }
  ],
  "outcome": "What changed under fresh verification",
  "next_action": "Next bounded action or terminal handoff",
  "progressed": true
}
```

Use an absolute evidence path or a path relative to the run directory. Every path must exist before the receipt is recorded. For completion, include every machine-check id and judgment criterion exactly once, with every `passed` value set to `true`.
