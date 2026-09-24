# Suite schema

`suite.json` fields:

- `schema_version`: integer `1`.
- `target`: absolute path of the evaluated skill directory.
- `limits`: positive integers `max_iterations` and `max_minutes`; optional positive integer `max_tokens` (null means no token budget).
- `trigger_cases`: at least ten entries with `should_trigger: true` and ten with `should_trigger: false`. Each entry: non-empty string `id`, `prompt` (realistic phrasing a user might send), `expected` (what the skill should do), and boolean `should_trigger`.
- `functional_cases`: at least one entry with the same `id`/`prompt`/`expected` shape; `expected` must describe an objectively observable outcome (file content, command result, generated artifact).
- `rubric`: at least one criterion with non-empty string `id`, `criterion` (what good looks like), and `ground_truth` (external source, original brief, or fixed checklist the criterion is judged against).

IDs must be unique across all three groups and stable across suite versions.

Result files (`cases.json`, `rubric.json`): `{"results": [{id, passed, evidence}]}` — `passed` boolean, `evidence` a non-empty string describing what was actually observed. IDs must cover every suite ID exactly once; unknown or duplicate IDs invalidate the file.

Validation rules enforced by the script: rejects missing cases, duplicate IDs, non-positive limits, and rubric criteria without ground truth. Never invents results for tests that were not run. Receipts compare case and rubric pass rates against the pinned baseline; a baseline with no pinned run yields no deltas.
