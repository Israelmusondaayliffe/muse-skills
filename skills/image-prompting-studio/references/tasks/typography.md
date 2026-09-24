# Task: Typography (lettering-critical prompts)

Scope: prompts where lettering, exact text or multilingual typography is the main visual subject or a critical constraint.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. Make an exact text inventory before designing: spelling, capitalization, punctuation, diacritics, script. Distinguish literal copy from instructions — font names, color codes and layout labels must not appear as rendered text unless requested. If translation is needed, treat the translation as content to verify, not something the image model improvises.
2. Describe hierarchy, scale relationships, alignment, spacing, line breaks, reading direction, letterform character and material. A non-Latin script needs its own typographic conventions, not a Latin style mechanically imposed. Specify what must read first and how decorative lettering relates to legible supporting copy. Use fewer text zones when density would defeat the format.
3. NL for expressive lettering; JSON when exact strings, placement and exclusions benefit from separation.
4. Supplied text has authority; proposed copy must be identifiable as proposed. Do not promise error-free lettering or exact reproduction of a named font. A generated layout can serve as a reference for later typesetting when precise production text is needed.

## Recipes

Use `../recipes/typography/gpt-typography.md` for display words, mixed scripts, wordmarks, dense editorial and environmental lettering. Review the written inventory against the prompt; if a rendered image exists, read its actual text rather than assuming the instruction worked.
