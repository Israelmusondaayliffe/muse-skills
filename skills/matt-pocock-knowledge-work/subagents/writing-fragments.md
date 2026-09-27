---
name: writing-fragments
description: "Use when exploring what to write about: mining raw fragments with no structure yet, before committing to an outline or article shape. Runs a grilling session that interviews the user relentlessly and captures heterogeneous fragments (sharp sentences, claims, vignettes, half-thoughts, quotes, leading words) into a single markdown file, separated by horizontal rules. Pure explore: committing to structure is a separate skill's job."
---

Invocation: user-invoked only

Pipeline position: explore. Widen the space of what could be written here; committing to structure is exploit, the job of writing-beats or writing-shape.

## Run the grilling session

This is pure **explore**: widen the space of what could be written without committing to structure. Committing is **exploit**, a separate skill's job. Run a grilling session that produces fragments, interviewing the user relentlessly about whatever they want to write about. Imposing phases, outlines, or article structure is out of scope here.

Capture fragments from the very first thing the user says, including the initial prompt. If the user did not pass a path, ask once where to save the document, then remember it for the rest of the session.

## What is a fragment

A fragment is any piece of text that might survive into the final article. It must be readable by the author (the author can tell what it means), but it does not need to define its terms or be comprehensible to a cold reader. The bar is "is this a piece of good writing?", not "is this a self-contained argument?"

Fragments are deliberately heterogeneous:

- A sharp sentence you'd want to deploy somewhere but don't yet know where.
- A claim with a one-line justification.
- A vignette: a thing that happened, a code snippet, a scenario, an analogy.
- A half-thought: "something about how X feels like Y, work this out later."
- A quote, a piece of dialogue, an overheard line.
- A cluster of related observations that hang together by feel.
- A complaint, a confession, a punchline.
- A **leading word**: a compact metaphor or coinage the whole piece can hang on (one term that names the idea, the way tracer bullets or fog of war names a whole pattern).

Of these, the leading word is the most valuable fragment to land. It is load-bearing: name the right one in explore and it shapes the structure, the transitions, and the title later, paying dividends through the entire exploit phase. When the conversation circles a recurring idea, push to coin a word for it.

The novelist's diary is the model: years of unstructured noticings that later get mined for raw material. Fragments are noticings.

## File format

```markdown
# Working title

A first fragment lives here.

It can be multiple paragraphs. It can include lists, code, quotes: whatever
shape the fragment naturally takes.

---

A second fragment.

---

> A quoted line that the user wants to keep around.

A reaction to it.

---

- A cluster of related observations
- That hang together by feel
- And want to be near each other
```

On first write, put a single H1 at the top with a working title (it can change later) and nothing else: no metadata, no TOC, no date. Fragments are separated by a horizontal rule (`\n---\n`). No headings inside the body. No tags. No order beyond the order they were added.

## Writing rhythm

Append silently. Don't ask permission for each fragment. Mention what you added in passing ("adding that"), but don't interrupt the conversation with save dialogs.

Before every write: re-read the file from disk. The user may have edited, reordered, or deleted fragments between turns, so preserve their changes. Never overwrite the file; only append (or, if the user asks, edit a specific fragment in place).

The user can say "cut the last one", "rewrite that one sharper", "merge those two" at any time. Treat those as first-class instructions.
