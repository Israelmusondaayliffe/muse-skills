# Transcript export: Muse sessions → scanner JSONL

The scanner reads JSONL event streams; Muse's work traces live in the app
database, so this skill exports a bounded window into normalized JSONL before
scanning. Exports live under `~/workspace/practice-compiler/session-exports/<YYYY-MM-DD>_<YYYY-MM-DD>/`,
outside the replaceable skill folder (older exports may still sit in the package's `hidden_files/session-exports/`),
and are never attached to handoffs or shown beyond redacted snippets.

## Steps

1. **Confirm scope with the user.** Ask which chats to include (by thread
   title) and agree on an exact inclusive `--since`/`--until` window and
   timezone. Export only the selected sessions.
2. **List candidate sessions** (bounded, read-only queries via the `muse.db` tool):

```sql
SELECT s.session_id, m.thread_title, s.created_at
FROM agent.sessions s
LEFT JOIN agent.session_metadata m ON m.session_id = s.session_id
WHERE s.created_at >= '2026-09-16T00:00:00Z'
  AND s.created_at <  '2026-09-24T00:00:00Z'
ORDER BY s.created_at DESC
LIMIT 30;
```

3. **Pull the three event kinds** for each selected session. Keep every
   projection bounded (`left(...)`); session ids come from step 2:

```sql
-- User-authored messages (verify the 'user' role label against the enum if this returns nothing)
SELECT mg.message_id, mg.created_at, left(mg.body, 4000) AS body
FROM runtime.messages mg
JOIN agent.context_items ci ON ci.message_id = mg.message_id
JOIN agent.agents a ON a.agent_id = ci.agent_id
WHERE (a.session_id = '<SESSION_ID>' OR a.root_session_id = '<SESSION_ID>')
  AND mg.role = 'user'
ORDER BY mg.created_at
LIMIT 500;
```

```sql
-- Tool calls (arguments kept small; commands are extracted client-side)
SELECT tc.tool_name, tc.status, tc.created_at, left(tc.arguments_json, 2000) AS args
FROM runtime.tool_calls tc
JOIN agent.context_items ci ON ci.tool_call_id = tc.tool_call_id
JOIN agent.agents a ON a.agent_id = ci.agent_id
WHERE (a.session_id = '<SESSION_ID>' OR a.root_session_id = '<SESSION_ID>')
ORDER BY tc.created_at
LIMIT 1000;
```

```sql
-- Tool outputs; failures are the signal that matters
SELECT too.call_id, too.status, too.created_at,
       left(too.output_text, 2000) AS out_text,
       left(too.error_text, 1000) AS err_text
FROM runtime.tool_outputs too
JOIN agent.context_items ci ON ci.tool_output_id = too.tool_output_id
JOIN agent.agents a ON a.agent_id = ci.agent_id
WHERE (a.session_id = '<SESSION_ID>' OR a.root_session_id = '<SESSION_ID>')
ORDER BY too.created_at
LIMIT 1000;
```

4. **Write one JSONL file per session** in the normalized event schema below.
   Assistant prose is not a signal class — skip it.

## Normalized event schema

First line, every file:

```json
{"type": "session_meta", "payload": {"id": "<session_id>", "thread_source": "user", "timestamp": "<iso>"}}
```

- `thread_source`: `user` for direct chats; `subagent` for spawned child
  sessions; `automation` for cron/hook-driven runs; `synthetic` for
  eval or test runs. When unsure, ask the user.

User turn:

```json
{"type": "user_message", "payload": {"content": "<message body>"}, "timestamp": "<iso>"}
```

Shell command executed (e.g. `muse.exec`); the scanner detects repeated
workflows from the `command` argument:

```json
{"type": "response_item", "payload": {"type": "function_call", "name": "muse.exec", "arguments": "{\"command\": \"<cmd>\"}"}, "timestamp": "<iso>"}
```

Other tool calls (omit arguments or keep a small JSON summary — never dump
large payloads):

```json
{"type": "response_item", "payload": {"type": "function_call", "name": "<tool_name>"}, "timestamp": "<iso>"}
```

Failure, for outputs with an error status or nonzero exit:

```json
{"type": "response_item", "payload": {"type": "function_call_output", "output": "exit_code: <n> <error text>"}, "timestamp": "<iso>"}
```

## Notes

- Private model reasoning is not readable through these tables; do not try to
  export it, and do not quote it from elsewhere into the export.
- The scanner redacts emails, API-key shapes, and secrets when writing
  signals; exports themselves stay under `~/workspace/practice-compiler/` on this machine.
- Source classes (`user`, `automation`, `subagent`, `synthetic`) are labeled
  at export time via `thread_source`; the scan's `--source-class` flag filters
  them. Include non-user classes only when the user selects them.
