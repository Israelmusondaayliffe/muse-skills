# Fable 5.1 — Overlay

Read `references/fable-5.md` first. This file adds the Fable 5.1-specific rules.
Fable 5.1 (`claude-fable-5-1` — verify the exact string against current Anthropic
docs before shipping) is a sibling in the Claude 5 family; all Fable 5 behavior
and prompting guidance applies unless stated otherwise here.

1. Confirm the target host exposes the Fable 5.1 model string before executing.
2. Check Anthropic's Fable 5.1 prompting guide and model overview for current API
   controls and availability. Treat 5.1 availability, slugs, parameters, and
   pricing as unverified until the owning docs confirm them.
3. Preserve the user's job, output contract, sources, and authority. Start from
   an existing prompt when one is supplied.
4. Diagnose the observed failure before adding instructions. For long tool runs:
   keep useful progress updates visible, batch independent calls, keep API
   history append-only.
5. Test effort against the task; do not impose any publisher's preferred model
   settings on other users.
6. Keep Fable 5 guidance as explicit compatibility, not as the current-model
   default, when 5.1 is the selected model.
