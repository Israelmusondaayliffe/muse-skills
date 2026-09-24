# Unslop Quick Reference

Condensed digest of the pattern catalog. For the full tier tables see `word-replacements.md`. Voice wins over pattern removal: if a profile marker trips a detector, keep it.

## Rule Zero: plain language wins. Always.

If a simpler word conveys the same meaning, use it. "Start" beats "commence." "Important" beats "pivotal." "Show" beats "showcase." This overrides every other stylistic judgment. Apply it to everything you write.

## P0: credibility killers (fix immediately)

- Chatbot artifacts: "Certainly!", "I hope this helps!", "Great question!", "would you like me to"
- Cutoff disclaimers: "as of my last update," "based on available information"
- Vague attributions: "experts believe," "industry reports suggest" (name the source or cut the claim)
- Significance inflation: "marking a pivotal moment," "a watershed moment," "plays a crucial role"
- Em dashes in editable prose (see rule below)

## P1: obvious AI smell (fix before publishing)

- Tier 1 words (full table in `word-replacements.md`): delve, leverage, tapestry, realm, paradigm, robust, seamless, utilize, embark, pivotal, cutting-edge, nestled, vibrant, showcase, game-changer, watershed, intricate, holistic, actionable, synergy, empower, serves as, boasts, features (as verb)
- Copula avoidance: "serves as" → "is", "boasts" → "has", "features" → "has/includes"
- Trailing -ing clauses that add nothing: delete if redundant; if it matters, make it its own sentence
- Promotional language: "breathtaking," "renowned," "nestled in the heart of"
- Template phrases: "In the rapidly evolving world of...", "Whether you're X or Y", "Let's dive in"
- Throat-clearing / faux-insight openers: "Here's the thing" (unless it's a voice marker), "What nobody tells you", "the part everyone misses"
- Summary-recap endings: "In conclusion," "Ultimately," "The future looks bright"

## P2: polish (fix when time allows)

- Transition filler: "Moreover," "Furthermore," "In today's fast-paced world"
- Tier 2 words in clusters (2+ in one paragraph): harness, navigate, foster, elevate, streamline, bolster, resonate, facilitate, ecosystem, transformative
- Compulsive rule of three; uniform paragraph lengths; colon reveals for fake drama
- Generic conclusions: replace with a specific thought or cut
- Dramatic fragmentation: short. Staccato. Sentences. (unless the user's rhythm genuinely runs that way)

## Rewrite-vs-patch threshold

If a draft has 5+ P1 hits across 3+ categories, advise a rewrite from the core point outward rather than patching sentence by sentence. Pattern matches never prove who wrote something.

## Divergence enforcement

Conclusions and recommendations must be decisive. Nuance belongs in reasoning; conclusions take a stand.

- "Perhaps we should consider X" → "Do X. Here's why."
- Hedge structures ("on one hand / on the other hand," "there are pros and cons") belong in analysis, never as the conclusion.
- Don't manufacture certainty the user didn't supply — decisiveness applies to recommendations, not facts. Unsupported facts still get cut or marked (see `claim-boundaries.md`).

## Context profiles (strictness by audience)

| Profile | Signals | Notes |
|---|---|---|
| LinkedIn / social | <300 words, hashtags | Fragments OK; full pattern pass |
| Blog / essay | default | Full rigor |
| Technical docs | code, APIs, instructions | Clarity over personality; technical terms get a pass |
| Investor email | fundraising language | Extra strict on promotional language and significance inflation |
| Email / casual | Slack, DMs, quick notes | P0 only; don't over-police |

## Em-dash rule

Remove em dashes (—), en dashes (–), and `--` used as dashes from your own editable prose. Rule of thumb: if a full sentence follows, use a period and capitalize. If it's a continuation, use a comma. Never run a replacer across all output, a source document, or a file tree — work on a scratch copy, review the diff, apply manually. Quoted material, code, citations, and other protected exact text keep their dashes.

## Voice recovery check

After pattern removal, watch for the "clean but lifeless" failure: every sentence the same length, no opinions, no uncertainty, no first person when it would fit, reads like a press release. If the edit stripped the user's texture, restore it — supplied opinions, rhythm, rough edges, and useful asides stay. Restrained clarity beats decorated AI-slop: when the source has little personal texture, keep the edit light instead of performing a synthetic human voice.
