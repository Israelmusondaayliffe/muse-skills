---
name: writing-quality
description: Write in the user's voice, or edit, tighten, and review prose. Use when the user asks for a draft or rewrite that sounds like them, a neutral edit or cleanup of supplied text, removal of AI-sounding patterns, an audit of a document for generic AI patterns, or a rewrite that keeps the meaning. Neutral edits start at once; only new writing in the user's own voice uses a stored or freshly calibrated voice profile.
metadata: { "includeInPrompt": true }
---

# Writing Quality

Deliver the finished piece of writing the user asked for: the full draft, the full revision, or the full audit. Keep the prose plain, keep claims supported, keep protected material exact, and keep the user's voice where the task calls for it.

## Start here

1. Name the deliverable in one line: what text comes back, how long, for whom. A request for an article gets an article, not an outline.
2. Pick the route from what the user actually asked:

| The request | Route | Voice source | Calibration |
|---|---|---|---|
| "detect", "audit", "flag", "scan", "what AI patterns are in this" | **Detect** | none | never |
| Tighten, proofread, clean up, shorten, restructure, de-slop, or fix supplied text | **Neutral edit** | the supplied text | never |
| Write or rewrite something "in my voice" / "so it sounds like me" | **Voice write** | stored profile, else samples | only if no stored profile and no samples in the request |
| Write new prose with no voice request (a summary, a doc, a reply) | **Clear write** | generic clarity profile | never |
| "Calibrate my voice", or the user supplies samples to learn from | **Calibrate** | the samples | this is the task |

If "clean this up" could mean detect or edit, and the user supplied the text with no other signal, edit it. They handed you the text to improve. Choose detect only when they say report, flag, or audit.

3. Read the inputs before acting: the full supplied text, any files they named, and any stated audience, length, or channel.
4. For **Voice write** only, run `python3 bin/voice_state.py status` and load the active profile it reports. If it says to migrate, run `python3 bin/voice_state.py migrate` first.

## Routes

### Detect
Run `python3 bin/check_draft.py --verbose <file>` on the text. Read the text yourself as well; the scanner misses context and flags voice markers. Report findings grouped P0 (fix now), P1 (fix before publishing), P2 (polish), each with a quoted example and pattern name. End with an assessment: real problems versus judgment calls, and whether a patch or a rewrite is warranted. Do not change the text.

### Neutral edit
1. Keep the author's register, point of view, and level of formality. Neutral text stays neutral.
2. Make the smallest edit that achieves the request. Cut filler, replace inflated words with plain ones (`references/unslop-quickref.md`), fix structure only where it blocks the reader.
3. Protect exact material (see Protected material). Keep every claim within its original scope (`references/claim-boundaries.md`).
4. Run `python3 bin/check_draft.py <file>` on the result as advisory evidence.
5. Return the full revised text, then a short "What changed" list.

### Voice write
1. Load the active profile. If none exists and the request includes samples, calibrate from those samples first (see Calibrate) and continue in the same turn. If none exists and there are no samples, ask once for 2 or 3 samples. If the user declines or wants the draft now, write with the generic clarity profile and say so in one line.
2. Draft against the profile: rhythm, vocabulary, formality, characteristic phrases. Keep opinions, uncertainty, and first person only where the source or profile supplies them.
3. Apply the pattern pass. Voice wins: if a profile phrase trips a detector, keep it.
4. Check claims, protected material, and em dashes, then deliver the whole piece.

### Clear write
Write with the generic clarity profile in `references/voice-calibration.md`. No calibration and no voice questions. Deliver the whole piece.

### Calibrate
1. Save the samples to scratch files and run `python3 bin/voice_profile.py <sample-file>` on each for measured signals.
2. Read the samples yourself. Fill the template in `references/voice-calibration.md` with what the samples show and nothing more. Never infer personality, opinions, humor, or bluntness from memory or unrelated work.
3. Store it with `python3 bin/voice_state.py save <profile-file>`. The profile lives at `~/workspace/writing-quality/voice-profile.md`, outside this package, so skill updates never erase it. Never write a profile into this skill folder.
4. Tell the user where it is stored and what confidence the samples support.

## Protected material

Leave these byte-for-byte unchanged: code, commands, logs, quotations, citations, links, URLs, paths, identifiers, tables, structured data, frontmatter, and prompts. Before delivering an edit of Markdown or structured text, compare each protected span in the original with the output and restore any that changed. Removing bold markers is allowed only when the emphasized words survive exactly. For a saved revision, run `python3 bin/protected_scope_validator.py <original> <revision>` from this skill folder. A nonzero exit means inspect the changed categories and restore unauthorized edits. This checks recognizable spans, not factual accuracy; separately compare claims with the source.

Remove em dashes from your own editable prose. `bin/emdash_replacer.py` works only on a scratch copy; review its diff and apply the edit by hand. Em dashes inside quoted or protected material stay.

## Worked example (illustrative)

Request: "Tighten this paragraph for our team update. Keep it short."

> Our team has been working diligently to leverage cutting-edge tooling in order to streamline the onboarding process, and we're excited to share that the new checklist has reduced setup time significantly. Run `make setup` to try it.

Route: Neutral edit. No calibration: the supplied text is the voice source. First action: read it, mark `make setup` as protected, note that "significantly" has no number behind it.

Output:

> We built a new onboarding checklist that shortens setup. Run `make setup` to try it.

What changed: cut filler ("worked diligently", "excited to share"), replaced inflated words ("leverage cutting-edge tooling", "streamline"), and kept "shortens" without a size because the source gave none. The command is unchanged.

A wrong version would ask for voice samples first, return "reduced setup time by 40%" (an invented number), or hand back suggestions instead of the edited paragraph.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop and ask when |
|---|---|---|---|
| About to ask for samples on a tighten or cleanup request | Wrong route | Switch to Neutral edit and proceed | never; this is not a question for the user |
| `voice_state.py status` reports a conflict | Old and new profiles both exist and differ | Use the state-path profile; mention the conflict in one line | the user wants the profiles merged |
| `check_draft.py` flags a phrase that appears in the profile or source | Voice marker, not slop | Keep it; note it | never |
| A claim needs a number, date, or source you do not have | Missing evidence | Narrow the claim or mark it; do not invent | the claim is the point of the piece |
| A protected span changed in your output | Over-editing | Restore the original span exactly | never |
| A helper script fails to run | Missing Python or bad path | Do the check by reading the text; say which script failed | never; finish the piece |

## Completion

The task is done when the user has the complete requested text (or the complete audit), protected spans match the source, no claim goes beyond its evidence, and the output follows the chosen route. Keep scores and checklists internal unless asked.

## Operating rules

1. Detect-only requests never authorize rewriting. Rewriting never authorizes new facts.
2. Calibration applies only to voice writing. Neutral edits and clear writing never wait on samples.
3. No sample, no synthetic voice. Without a profile or samples, use the generic clarity profile and say so.
4. The scanner score is evidence, not a verdict. If the text reads right for its route, ship it.
5. Context sets strictness: investor emails and public posts get full rigor; chat messages and casual notes get P0-only treatment.
6. When the user approves a lasting style preference, update the stored profile with `voice_state.py save`.
7. For long pieces you may delegate sections to a subagent with the same profile and rules. You own the final pass and deliver the whole piece.
