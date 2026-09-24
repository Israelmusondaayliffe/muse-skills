# Run Protocol Reference

States: draft contract → validate → execute (≤3 drafts) → verify → aggregate → store-or-discard → report.

Caps per run: 3 inner drafts, 2 execution attempts, 2 verifier executions, 20 tool calls, 30 wall-clock minutes, 2 local record writes, at most one `candidate_lesson`, zero promotions. A capped draft executes only with explicit best-effort contract authorization plus a passing deterministic pre-execution gate (no known failure, no safety issue).

Retrieval: off by default. Display the record's exact content and SHA-256 digest, then bind an affirmative current-turn user decision to (task ID, record ID, digest, `retrieve`).

Terminal outcomes: `completed_verified`, `completed_unverified`, `blocked`, `budget_exhausted`, `ineligible_learning_disabled`, `policy_denied`, `capability_missing`, `security_quarantine`.

Storage profiles: `none` (write nothing — forced for learning-ineligible topics), `ephemeral` (in-turn evidence only, the default), `workspace_ledger` (JSON records under `~/workspace/proofloop/ledger/` — only when atomic-store guarantees are actually proven; otherwise downgrade to `ephemeral`), `durable_adapter` (reserved for a real atomic backend — treat as `ephemeral` on this host until one exists).
