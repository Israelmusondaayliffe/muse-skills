# Signal policy

Persist evidence, not transcript dumps.

Primary practice signal classes:

- `repeated-task`: a task request or workflow that recurs across sessions.
- `recurring-feedback`: a repeated correction, preference, or constraint the user gives the assistant.
- `follow-up-instruction`: an instruction the user adds after the initial request, such as verification, publication, or scope constraints.

Operational signal classes:

- `command-failure`: an actual tool call or output with a failed command.
- `executed-command`: an actual normalized tool command used only to detect repeated workflow evidence.
- `cost-decision`: remarks about cost, waste, tokens, or budgets.
- `missed-tool`: remarks that a better tool should have been used.
- `repeated-repair`: remarks that something needs fixing again.
- `user-method`: a reusable method the user describes in their own words.

Content and config clues are metadata on the primary signal classes. Do not treat a mention of a command as execution.

Do not scan these sources recursively as user-authored feedback:

- injected system instructions;
- AGENTS.md text;
- skill blocks;
- goal context;
- quoted transcripts;
- tool output.

Do not stage a proposal from a one-off unless the user explicitly requests it.

Group semantically equivalent wording with a deterministic token similarity rule. Persistent scans keep a redacted cumulative signal index so repetition and semantic similarity remain visible across cursor-separated runs. Keep the stable proposal fingerprint in `proposal-registry.json` so later scans merge evidence instead of creating duplicate staged proposals.

Redact credentials, Bearer tokens, private keys, common API-key forms, and email addresses before writing a signal. Each proposal records the signal class, destination, distinct-session count, confidence, stable fingerprint, and evidence objects containing `session_id`, source path, line, citation, source class, and redacted snippet. Approval creates a handoff record only. It does not apply the destination change.
