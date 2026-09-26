# Lead-agent prompt skeleton

Fill the placeholders, keep the result under 400 words, and run `python3 {{skill_dir}}/scripts/lint_prompt.py {{run_dir}}/prompt.md --domain {{domain}}` before surfacing it. Do not add architecture, file layouts, module lists, tech stacks, or round counts.

---

{{goal}}

The bar: {{bar_description}}. The reference artifacts and measurements are at {{bar_paths}}. Beat that bar. You may not argue with it, soften it, or replace it.

Split the goal into the smallest independently judgeable pieces. You own the decomposition and may re-split as you learn.

For each piece, loop in rounds: a builder improves the real artifact, then a separate critic with fresh context judges it against the bar. The critic never sees the builder's reasoning, history, or summaries.

Compare blind wherever possible: neutral labels, no provenance, judgment on the inspected output rather than on descriptions of it.

{{knowledge_work_clause}} <!-- include for prose, research, strategy, deck, and prompt-system domains: "Inspect every knowledge-work piece with a fresh reader-proxy agent against its frozen question set, and maintain a claim ledger validated by claim_audit.py." -->

Loop each piece until it beats the bar or the user stops the run. Caps pause work; they never certify it.

Write all state to {{run_dir}} after every round.

Keep the live progress page at {{run_dir}}/workbench.html regenerated from state after every round.

Use subagents within the approved launch cap and work at the highest effort setting the user selected. Before each dispatch, run check_stops.py with the proposed launches and cost; a fired stop pauses the run. Any scheduled job needs its own explicit user approval; the round loop always owns the gauntlet, never the scheduler.
