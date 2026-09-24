# Voiceover and audio

## Narration — use the podcast skill

Narration is produced with the `generate_podcast` skill (multi-voice audio
composition). Feed it the `SCRIPT.md` lines; get back `narration.wav` plus
word-level timings when the skill provides them. Keep those timings —
captioning (references/captioning.md) consumes them directly.

Before generating, ask the user (or accept their standing preference):

- Voice: which voice/persona (the podcast skill lists options).
- Music: BGM yes/no, and mood if yes.
- Language and pace.

Never invent a voice preference — if the user doesn't care, say "default
voice" explicitly and move on.

## Script prep

- One line per beat; write for the ear (short sentences, no jargon stacks).
- Mark emphasis and pauses with punctuation and line breaks, not stage
  directions the TTS will read aloud.
- Estimate duration: ~800–900 characters/minute for English narration.
  Size beats to the script, not the other way round.

## Music and SFX

- BGM: user-supplied track first. Otherwise ask — do not pull music from
  the open web. For SFX (whooshes, pops, risers, UI clicks), use the bundled
  `assets/sfx/` library (Pixabay Content License, commercial use allowed;
  credits in `assets/sfx/CREDITS.md`).
- Mix: narration on top, BGM ducked under it. Recipe in
  references/rendering-recipes.md. Peak levels: narration −3 dB, BGM bed
  −18 to −24 dB under narration.

## Word timings → captions

If the podcast skill returns word timings, save them as `audio/words.json`
(`[{"start": 0.0, "end": 1.2, "text": "..."}]`) and build the SRT with:

```bash
python3 <SKILL_DIR>/bin/burn_captions.py narration-cut.mp4 --words audio/words.json -o renders/captioned.mp4
```

The script groups words into readable cues (≤ ~84 chars, splits on pauses).
