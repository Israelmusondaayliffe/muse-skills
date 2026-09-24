# GPT-5.4 — Legacy Route

GPT-5.4 is the legacy GPT route. Build new work on GPT-5.6; use 5.4 when the user
targets it or as the migration source. Most 5.5/5.6 philosophy (outcome-first,
subtractive) descends from 5.4 practice, with leaner execution and intent
inference added later.

## Key 5.4 facts

- 1M token context with native compaction; the `phase` parameter for multi-step
  workflows; `tool_search` tool; computer use; `xhigh` top reasoning tier (no
  `max`); personality controls; research mode with citation gating;
  dependency-aware tool persistence; verification loops and completeness
  contracts; frontend design patterns.
- 5.4-era prompts tend to be heavier: explicit completeness contracts, tool
  routing enforcement, and verbosity management written around the 5.4 default.
  When migrating to 5.6, those are the first subtraction candidates — but
  re-test, since completeness contracts still matter for batch work.

## Migration from 5.4 to 5.6 (or to Fable 5)

1. Record the 5.4 effort setting as the baseline; never silently change tiers.
2. Run the lean pass from `references/gpt-5-6.md`: remove one group at a time,
   rerun the same evals, keep or restore.
3. Retest every "be concise" / verbosity instruction — 5.6's default is more
   concise still, and stacked brevity nudges overshoot.
4. Consolidate ask-first language into one compact autonomy policy (repetition
   causes approval noise on 5.6).
5. Review API surface: model strings, caching config, persisted reasoning, and
   any Chat Completions → Responses migration.
6. See `references/migrate.md` for the audit procedure and `references/diagnose.md`
   for failure categories.
