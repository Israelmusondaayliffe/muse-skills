# Domain Evidence Mapping

What counts as evidence depends on the task family. Map each success criterion to a verifier on this host; self-review is E1, never E3.

- **code** (`task_family: code`): run the real checks on the VM terminal — test suites, build, lint, type checks, runtime postconditions, and a careful diff review. A passing test suite you did not author or modify is E3.
- **research**: use browser.search/browser.open — primary-source coverage, citation entailment (does the cited passage actually support the claim?), contradictions across sources, freshness, and stated uncertainty. A claim entailed by a fetched primary source is E2.
- **structured_artifact**: schema validation (`bin/validate-contract` / `bin/validate-record` or a JSON-schema check), required sections present, formulas evaluated, links reachable, file opens cleanly.
- **creative_preference**: the user's own direct selection or pairwise preference, brief compliance, and project scope. No verified-evidence level above E2 without human judgment.

A verification subagent is an already-authorized host capability: give it the contract, the candidate, and the verifier instructions, and require it to return evidence, not an opinion. Its output is E1 unless the evidence itself is deterministic (E3) or user-judged (E2).
