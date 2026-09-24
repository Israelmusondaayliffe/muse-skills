# Teaching Workspace Formats

## MISSION.md

Lives at the workspace root. Every teaching decision traces back to it.
One mission per workspace — two unrelated topics are two workspaces.

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal. What changes in the user's
life or work when they have this skill? Push past "to understand X" to the
underlying outcome. "Run a half marathon by October" beats "get fitter."}

## Success looks like
- {A specific, observable thing the user will be able to do}
- {Another specific thing}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything bounding the approach}

## Out of scope
- {Adjacent topics explicitly not chased right now — protects the zone of proximal development}
```

Rules: push back on vagueness — interview before writing. Revise when the
goal moves (confirm with the user). Keep it short: past one screen it has
become a plan, not a compass.

## RESOURCES.md

Curated high-trust sources. Knowledge comes from here, not parametric
guesses; wisdom from the communities listed.

```md
# {Topic} Resources

## Knowledge

- [Book: _The Science and Practice of Strength Training_ : Zatsiorsky & Kraemer](https://example.com)
  Foundational text on programming and adaptation. Use for: periodisation, recovery, intensity zones.

## Wisdom (Communities)

- [r/weightroom](https://reddit.com/r/weightroom)
  High-signal subreddit, moderated against bro-science. Use for: programme critique, plateau troubleshooting.
```

Rules: high-trust only (primary sources, recognised experts, peer-reviewed
work, well-moderated communities; marketing dressed as education is out).
Annotate every entry: one line saying what it covers and when to reach for
it. Surface gaps explicitly in a `## Gaps` section when the mission needs
something no good resource covers. Prune ruthlessly — five sharp sources beat
thirty mediocre ones. Record community preferences, including an opt-out of
joining communities, so future sessions stop proposing them.

## learning-records/NNNN-slug.md

The teaching equivalent of ADRs: non-obvious lessons, key insights, and
stated prior knowledge that steer future sessions. Used to compute the zone
of proximal development. Create the directory lazily.

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established),
and why it matters for future sessions.}
```

Optional sections only when they add genuine value: **Status** (`active |
superseded by LR-NNNN`); **Evidence** (how the user demonstrated it — a
question answered, an exercise completed); **Implications** (what this enables
or rules out for future sessions).

Numbering: scan `learning-records/` for the highest number, increment by one.

Write a record when: (1) the user demonstrated genuine understanding of
something non-trivial — not mere exposure, but evidence of correct use; (2)
the user disclosed prior knowledge (record it and the depth claimed, so it's
never re-taught); (3) a misconception was corrected (high-value — predicts
future stumbling blocks); (4) the mission shifted in response to learning
(cross-link MISSION.md and update it).

Not records: material merely covered (coverage ≠ learning), anything already
captured tersely in the glossary, session-by-session activity logs. On
contradiction, mark the old record superseded — the history of how
understanding evolved is itself signal.

## GLOSSARY.md

The workspace's canonical language. Every explainer, exercise, and record
adheres to it.

```md
# {Topic} Glossary

{One or two sentence description of the topic.}

## Terms

**Hypertrophy**:
Muscle growth driven by mechanical tension and metabolic stress over repeated training sessions.
_Avoid_: Bulking, getting big

**Progressive overload**:
Systematically increasing the demand on a muscle over time — via load, volume, or intensity.
_Avoid_: Pushing harder, levelling up
```

Rules: add a term only when the user understands it (the glossary records
compressed knowledge; compressing a concept into a tight definition is itself
evidence of understanding). Be opinionated; keep definitions to one or two
sentences (define what it IS); use the glossary's own terms inside
definitions; group under subheadings when natural clusters emerge; flag
ambiguities explicitly; revise in place as understanding deepens.

## Lesson discipline (reference)

- Lessons live in `lessons/NNNN-slug.html`: one self-contained file, one
  tightly-scoped topic, tied to the mission, completable quickly, one
  tangible win, in the zone of proximal development. Beautiful typography —
  the user will return to these. Link lessons to each other via HTML anchors.
  Each lesson recommends a primary source and reminds the user to ask
  follow-up questions.
- Reference docs in `reference/*.html` are the compressed essence for quick
  re-use; lessons are rarely revisited, references are.
- Quiz answers: each option exactly the same number of words (and characters
  if possible) — no formatting clues about the right answer.
- Assets in `assets/*` are reusable components (stylesheet first); build from
  them, never inline what a future lesson could duplicate.
