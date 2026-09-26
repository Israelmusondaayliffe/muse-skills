# Voice Calibration

Extract voice markers from user-supplied samples BEFORE any voice writing. Techniques never override voice.

## Gathering samples

- Ask the user for 2–3 samples of their own writing. Accept pasted text or file paths they point you to.
- With their go-ahead, you may search their workspace files for existing writing they authored.
- Never fabricate samples. Never infer personality, opinions, humor, bluntness, or first-person style from memory, identity history, or unrelated work. No sample, no voice — use the generic clarity profile below.

## Measurement

Run `python3 bin/voice_profile.py <sample-file>` for objective signals: average sentence length, tone indicators, contraction and question frequency, first-person frequency, structure preference, emphasis method. Treat the output as evidence, not gospel — read the sample yourself too.

## Voice marker categories

### Sentence patterns

- **Short-punchy:** avg under 10 words, deliberate fragments, one idea per sentence.
- **Flowing:** avg over 20 words, compound sentences, transitional phrases.
- **Varied:** mix of short and long; pacing through structure.

### Tone markers

- **Formal:** complete sentences, few contractions, third person or passive.
- **Conversational:** contractions common, first/second person, questions to reader.
- **Direct:** imperative verbs, clear stance, minimal hedging ("Do X," not "you might consider X").
- **Curious:** embedded questions, "I wonder / I noticed," uncertainty acknowledged.

### Characteristic phrases

**Preserve these exactly** even when they trip pattern detectors. Types: signature transitions ("Here's the thing,"), personal markers ("In my experience,"), preferred domain vocabulary, emotional markers (how they express enthusiasm, doubt, conviction). Look for phrases repeated across samples.

### Structure preferences

- **Prose-dominant:** paragraphs flow, headers rare.
- **List-dominant:** bullets for key points, numbered steps for processes, headers for navigation.
- **Hybrid:** prose for explanation, lists for actions, headers for major sections.

### Emphasis patterns

Bold for key terms, ALL CAPS for strong points, or structural emphasis (short paragraphs, line breaks, repetition). Note which one they actually use.

## Voice profile template

Write the profile to a scratch file, then store it with `python3 bin/voice_state.py save <scratch-file>`. It lands at `~/workspace/writing-quality/voice-profile.md`, outside the skill package, and any earlier profile is kept as a dated backup. Never write the profile into this skill folder.

```
VOICE PROFILE
=============
Source: [what the user supplied — filename/description + date]
Confidence: [high / medium / low]

Tone: [formal / conversational / direct / curious]
Sentence style: [short-punchy / flowing / varied / medium]
Structure: [prose / lists / hybrid]
Emphasis method: [bold / caps / structural / none]

PRESERVE (characteristic phrases, exact):
- [phrase 1]
- [phrase 2]

Domain vocabulary: [terms they prefer]
Structure notes: [e.g., headers for navigation, prose for content]

BANNED (from user preferences):
- [patterns they dislike]

Voice notes: [anything distinctive that doesn't fit above]
```

Keep it readable and user-editable. When the user states a lasting style preference in conversation, update the stored profile the same way (edit a scratch copy, then `save`).

## When calibration is not needed

Calibration is for writing new prose in the user's own voice. Skip it for neutral work: tightening, proofreading, clarity edits, restructuring, or de-slopping text the user supplied. The supplied text is the voice source for those tasks. Keep its register, and do not add personality it lacks.

## Generic clarity profile (fallback)

Use when no sample exists. This is a clarity profile, not a claim about the user's voice. Say so when using it.

- Tone: clear, competent, appropriately formal
- Sentence style: medium length, complete thoughts
- Structure: headers for navigation, prose for content
- Banned: em dashes, AI clichés, excessive hedging
- Emphasis: bold for key terms

## Edge cases

- **Thin sample:** too short or generic to extract patterns. Ask for a representative sample or explicit style instruction. If none comes, use the generic profile, keep edits light, and flag: "I couldn't detect a strong voice pattern, so I applied minimal changes."
- **Conflicting signals:** formal tone but casual phrases. Note the conflict, ask which to preserve. If unreachable, preserve both and minimize changes.
- **Voice vs. quality conflict:** a user's characteristic phrase triggers a pattern detector. Voice wins. Keep the phrase and note: "Preserved '[phrase]' as it matches your voice."
- **After edits:** compare output to the profile. Characteristic phrases intact? Tone and rhythm matched? No banned patterns introduced? Roll back anything that broke consistency.

## Remember

Voice extraction comes first because the techniques should serve voice, not override it. The goal is not generic quality — it's the user's quality. Their voice, at their best. And never manufacture what's not there: no invented opinions, anecdotes, emotions, profanity, first-person claims, identity claims, examples, numbers, or certainty.
