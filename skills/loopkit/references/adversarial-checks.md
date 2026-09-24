# Adversarial completion checks

Check for these shortcuts before approving completion:

1. Required checks were removed, renamed, skipped, or narrowed.
2. Errors were caught and converted to passing output.
3. A stub, constant, or empty result replaced real behavior.
4. A comment deletion or wording change was presented as a functional fix.
5. Evidence was produced before the latest artifact change.
6. The verifier inspected the builder's explanation but not the artifact.
7. Only the optimized signal was tested, with no separate acceptance gate.
8. A missing external dependency was reported as a clean no-op.
9. A blocked approval was bypassed.
10. The run changed files outside the contract boundary.
11. The completed state lacks a valid receipt.
