---
name: writing-quality
description: Write in the user's voice, or review and tighten prose. Use when the user asks to write something that sounds like them, calibrate their writing style, clean up AI-sounding text, tighten a draft, audit a document for generic AI patterns, or rewrite something without changing its meaning. Calibrates from user-supplied writing samples before any voice work.
metadata: { "includeInPrompt": true }
---

# Writing Quality

## Purpose

Make Muse write like the user, and keep everything Muse writes free of generic AI patterns. Two operations:

- **Voice writing / rewriting** — draft or rewrite prose in the user's established voice.
- **Detect-only review** — audit prose for AI patterns and report findings without changing the text.

Never invent or fake the user's voice. Voice work starts with calibration.

## Workflow

### 1. Calibrate the voice (first use, or when the user asks)

1. Check `references/voice-profile.md`. If a calibrated profile exists, load it and go.
2. If none exists, ask the user for 2–3 samples of their own writing (pasted text, or paths to files they point you at). You may also offer to look through their workspace files for existing writing — only with their go-ahead.
3. Run `python3 bin/voice_profile.py <sample-file>` on the samples for measured signals (sentence length, tone, contractions, structure).
4. Write the profile into `references/voice-profile.md` using the template in `references/voice-calibration.md`. Record the source and confidence. If the sample is too thin, say so and use the generic clarity profile instead.
5. Do not infer personality, opinions, humor, bluntness, or first-person claims from memory, identity history, or unrelated work. If the sample doesn't show it, it doesn't go in the profile.

### 2. Identify the operation

- **Draft or rewrite**: only when the user asked for prose to be written or changed. For anything they didn't write (emails, posts, docs), stay inside the profile: sentence rhythm, vocabulary, formality, structure.
- **Detect / audit**: when the user says detect, audit, scan, flag only, or asks "what AI patterns are in this." Report findings only. Do not rewrite.
- If the request is ambiguous, choose detect-only or ask before changing prose.

### 3. Draft or revise

1. Draft against the voice profile: keep their characteristic phrases, rhythm, and level of polish. Preserve opinions, uncertainty, and first person when the source supplied them; don't smooth those away.
2. Apply the quick pattern pass (`references/unslop-quickref.md`). Voice wins over pattern removal — if a phrase in the profile trips a pattern detector, keep the phrase.
3. Run `python3 bin/check_draft.py <draft-file>` for objective pattern evidence. Treat its score as advisory evidence, not a verdict.
4. Keep claim boundaries (`references/claim-boundaries.md`): don't add facts, numbers, examples, certainty, or results the user didn't supply. Mark or cut unsupported claims.
5. Leave protected material byte-for-byte unchanged: code, commands, logs, quotations, citations, links, paths, identifiers, tables, structured data, frontmatter.
6. Remove em dashes from your own editable prose (use `bin/emdash_replacer.py` on a scratch copy only, review the diff, apply manually). Em dashes inside quoted or protected material stay.

### 4. Validate

Self-check before delivery:

- [ ] Reads like the user's profile (rhythm, vocabulary, structure match)
- [ ] Simple words throughout — plain beats clever
- [ ] No Tier 1 word violations; no P0 credibility patterns
- [ ] Nothing fabricated: no invented facts, opinions, experiences, or first-person claims
- [ ] Protected material unchanged; no unauthorized rewrites
- [ ] Em dashes gone from editable prose

## Output Contract

- **Rewrite**: the revised text, then a short "What changed" section. Keep scores and checklists internal unless asked.
- **Detect**: findings grouped as P0 (fix immediately), P1 (fix before publishing), P2 (polish), each with a quoted example and the pattern name. End with an assessment: which are real problems vs. judgment calls, and whether a patch or full rewrite is warranted.
- If the task is long-form, you may delegate drafting sections to a subagent — it gets the same voice profile and rules. You own the final validation pass.

## Operating Rules

1. Calibration is mandatory for voice work. No sample, no synthetic voice — use the generic clarity profile and say so.
2. Detect-only requests never authorize rewriting. Rewriting never authorizes new facts.
3. Voice preservation wins over pattern removal. Neutral source text stays neutral.
4. The raw scanner score does not decide quality. If the draft reads right in the user's voice, ship it.
5. Context adjusts strictness: investor emails and LinkedIn posts get full rigor; Slack/DMs/casual notes get P0-only treatment.
6. When the user approves a style preference ("no em dashes," "short sentences"), update `references/voice-profile.md` so it persists.
