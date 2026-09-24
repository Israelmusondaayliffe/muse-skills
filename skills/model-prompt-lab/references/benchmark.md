# Prompt Benchmark Design

Turn a prompt-quality question into a testable benchmark. Benchmark design is
deterministic planning: it produces a specification, and it never claims a model
run occurred. Design is separate from execution — expected behavior is fixed
before results are seen.

## Procedure

1. **Frame the decision.** Record: the user task, baseline prompt, candidate
   prompt, model conditions, and the decision the benchmark must support
   (ship / don't ship, effort A vs B, prompt vs prompt).
2. **Build the case set.**
   - **Success cases:** the main user job, normal inputs.
   - **Boundary cases:** near-misses, ambiguous inputs, long context, tool
     limits, partial evidence.
   - **Failure cases:** malformed inputs, unsupported parameters, missing tools,
     safe-refusal or handoff behavior.
3. **Write assertions.** Objective and observable for deterministic behavior
   (presence of a field, citation attached, tool called before answering);
   reserve subjective qualities for a named human rubric. Assertions must be
   discriminating: they should separate the baseline from the candidate.
4. **Set measurement rules.** Metrics (pass rate, token cost, latency), sample
   size, cost or time limits, and stopping rules (stop when X, not when the
   result looks right).
5. **Record conditions.** Model string, prompt version, tool access, temperature
   or effort settings when supported. Track whole-session usage separately from
   marginal prompt cost.
6. **Hand off to an authorized runner.** Do not fill result fields from
   expectation. Results are evidence; they get recorded in their own table, not
   in the design.

## Specification template

```
## Benchmark: [decision it supports]

### Case set
- Success: [input + expected observable behavior]
- Boundary: [input + expected observable behavior]
- Failure: [input + expected observable behavior]

### Assertions
- [Observable, discriminating, per case type]
- Human rubric (named): [rubric name, dimensions]

### Measurement
- Metrics: [pass rate, tokens, latency]
- Sample size, cost/time limits, stopping rules

### Conditions
- Model string, prompt versions, tool access, effort/temperature

### Results
- [EMPTY until run — filled by the authorized runner]
```
