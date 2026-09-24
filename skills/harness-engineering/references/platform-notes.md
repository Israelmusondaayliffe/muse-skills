# Hatch Platform Notes

The platform file for this skill. Surfaces differ across platforms; never port a path, command, or capability from another platform's notes on similarity alone.

## Instruction chain (persistent context, widest → narrowest)
- `~/SOUL.md` — assistant persona and tone.
- `~/IDENTITY.md` — who the assistant is.
- `~/USER.md` — who the user is, what to call them, timezone.
- `~/MEMORY.md` — curated long-term memory, kept tight.
- `~/memory/*.md` — daily notes; `~/memory/people/`, `~/memory/groups/` — relationship pages.
- `~/AGENTS.md` — workspace conventions and lessons.
- `~/TOOLS.md` — environment-specific tool quirks.
- `~/docs/` — device and product docs.
- `~/workspace/goals/<slug>/` — goal-scoped files; `~/workspace/your_files/` — user-facing deliverables.

## Capabilities
- `muse.exec` — shell on a persistent Linux VM. `~/workspace` survives reboots; `/tmp` is scratch.
- `muse.*` tools — file read/write/edit, memory search, local place search, visual grounding.
- `browser.search` / `browser.open` — public web search and page text. Live-browser work (visits, clicks, forms, sign-in, purchases) runs as a separate browser task with user confirmation; generic subagents cannot operate it.
- `skill-*` catalog — connectors (Gmail, Calendar, Spotify, etc.), shopping, media library.
- `cron` — scheduled jobs (one-shot or recurring). `hooks` — event-driven automations.
- `subagent` — background child agents. `artifact` / `widget` — durable documents and inline UI.
- `feed` — the user's personal newspaper; `idea` — suggestions corpus.
- `tracking` / `user_goal` — durable commitments and goals.
- Secure Vault — credential capture; credentials are never handled as raw text.

## Deterministic checks
The harness's check script, when one exists, lives beside this skill in `scripts/` or under the workspace run directory. Its failures are the first audit and maintenance work items.
