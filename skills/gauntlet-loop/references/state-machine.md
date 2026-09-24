# State Machine

Allowed primary transitions:

```text
not_initialized -> intake
intake -> grilling
grilling -> plan_proposed
plan_proposed -> plan_approved
plan_approved -> gauntlet_compiled
gauntlet_compiled -> executing
executing -> integrating
integrating -> ready_for_verification
ready_for_verification -> verifying
verifying -> verified | verified_with_caveats | failed_verification | unable_to_verify
failed_verification -> executing
```

Execution may also move to `waiting_for_user`, `blocked`, `paused`, or `stopped`. Resume returns to the prior active state recorded in history.

Every transition records previous state, new state, timestamp, actor, reason, related artifacts, and required next action. Scripts reject invalid transitions.
