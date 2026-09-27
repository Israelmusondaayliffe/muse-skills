---
name: teach
description: "Teach the user a new skill or concept, within this workspace. Use when the user asks to learn something, be taught a topic, or study a new concept over multiple sessions."
---

Invocation: user-invoked only

# Teach

The user has asked you to teach them something. This is a stateful request: they intend to learn the topic over multiple sessions.

## Teaching Workspace

Treat the current directory as a teaching workspace. The state of their learning is captured in this directory in several files:

- `MISSION.md`: the _reason_ the user is interested in the topic. Use this to ground all teaching.
- `./reference/*.html`: reference materials: the compressed learnings from lessons (cheat sheets, reference algorithms, syntax, glossaries). They are raw units of learning: beautiful documents that print out well, designed for quick reference.
- `RESOURCES.md`: resources used to ground your teaching in contextual knowledge, or to acquire knowledge and wisdom.
- `learning-records/*.md`: records of what the user has learned. These are like ADRs in software development: they capture non-obvious lessons and key insights that may need revising later, or drive future sessions. They are titled `0001-<dash-case-name>.md`, where the number increments each time. They are used to calculate the zone of proximal development.
- `lessons/*.html`: lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching in this workspace.
- `./assets/*`: reusable **components** shared across lessons (stylesheets, quiz widgets, simulators, diagram helpers). See [Assets](#assets).
- `NOTES.md`: a scratchpad for you to jot down user preferences, or working notes.

## Philosophy

Deep learning needs three things:

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Before `RESOURCES.md` is well-populated, your focus should be to find high-quality resources which will help the user acquire knowledge. Never trust your parametric knowledge.

Some topics need more skills than knowledge (yoga), others more knowledge than skills (theoretical physics).

### Fluency vs Storage Strength

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give an illusory sense of mastery; storage strength is the real goal. Design lessons that build long-term retention through desirable difficulty: retrieval practice (recall from memory), spacing (distributing practice over time), and interleaving (mixing up different but related topics, for skills practice only).

## Lessons

A lesson is the main thing you produce. Each lesson is one self-contained HTML file, saved to `lessons/` and titled `0001-<dash-case-name>.html`, incrementing each time.

A lesson should be **beautiful**, with clean, readable typography and layout, since the user will return to these later to review. Think Tufte. It should be short and completable very quickly: working memory is very small. But each lesson should give the user a single tangible win they can build on. It must be directly tied to the mission, and must sit in the user's zone of proximal development.

If possible, open the lesson file for the user by running a CLI command. Each lesson should link via HTML anchors to other lessons and reference documents.

Each lesson should recommend a primary source for the user to read or watch: the most high-quality, high-trust resource you found on the topic.

Each lesson should contain a reminder to ask followup questions to the agent: the agent is their teacher, and can assist with anything that's unclear.

Lesson design: lessons are built around a skill the user is going to learn. Teach the knowledge first (only what's required to acquire that skill), then get the user to practice via an interactive feedback loop. Keep lessons littered with citations, links to external resources backing up any claim made. For knowledge acquisition, difficulty is the enemy: it eats working memory needed for understanding.

## Assets

Reuse is the default, not the exception. Before authoring a lesson, read `./assets/` and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it; never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns: every lesson links it, so the lessons look like one consistent course rather than a pile of one-offs. As the workspace grows, so should the component library.

## The Mission

Every lesson should be tied into the mission: the reason the user is interested in learning about the topic.

If the user is unclear about the mission, or `MISSION.md` is not populated, your first job is to question the user on why they want to learn this. Failing to understand the mission means lessons feel too abstract and you have no way of judging what to teach next. Missions may change as the user develops: when they do, update `MISSION.md` and add a learning record to capture the change, confirming with the user before changing the mission.

`MISSION.md` captures:

- **Why**: 1-3 sentences. The concrete real-world goal. Push for the underlying outcome, not "to understand X".
- **Success looks like**: specific, observable things the user will be able to do.
- **Constraints**: time, budget, prior commitments, learning preferences, anything bounding the approach.
- **Out of scope**: adjacent topics the user doesn't want to chase right now, protecting the zone of proximal development.

Rules: one mission per workspace. Concrete over abstract ("run a half marathon by October" beats "get fitter"). Push back on vagueness: interview the user before writing anything. Revise when reality shifts. Keep it short: past a screen, it's a plan, not a compass.

## Zone Of Proximal Development

Each lesson, the user should feel challenged "just enough".

If the user doesn't specify what to learn, calculate their zone of proximal development by: reading their `learning-records`, figuring out the right thing to teach based on their mission, and teaching the most relevant thing that fits in their zone of proximal development.

## Knowledge

Knowledge should first be gathered from trusted resources. Use `RESOURCES.md` to keep track of them, curated high-trust only: primary sources, recognised experts, peer-reviewed work, and strongly-moderated communities. Annotate every entry with one line on what it covers and when to reach for it. Group by **Knowledge** / **Wisdom**, surface gaps explicitly with a `## Gaps` section, and prune ruthlessly: better five sharp sources than thirty mediocre ones. Record community preferences (e.g. if the user has opted out of joining communities) so future sessions don't keep proposing them.

For skill acquisition, difficulty is the tool. Effortful retrieval is what builds storage strength. Teach skills through interactive lessons: quizzes and light in-browser tasks, or lessons guiding the user through real-world steps (e.g. yoga poses). Each should run on a **feedback loop** where the user gets feedback on performance, as tight as possible: immediate, and ideally automatic. Quiz rule: each answer should be exactly the same number of words (and characters, if possible). Don't give the user clues about the answer through formatting.

## Acquiring Wisdom

Wisdom comes from true real-world interaction: testing skills outside the learning environment.

When the user asks a question that appears to require wisdom, default to attempting an answer, but ultimately delegate to a **community**: a place (online or offline) where the user can test skills in the real world (a forum, a subreddit, a real-world class if budget permits, a local interest group). Find high-reputation communities the user can join. If the user says they don't want to join a community, respect it.

## Reference Documents

While creating lessons, also create reference documents: the compressed essence of lessons, in a format designed for quick reference. Lessons will rarely be revisited later; reference documents will be.

Some learning topics lend themselves to reference: syntax and code snippets (programming), algorithms and flowcharts (processes), poses and sequences (yoga), exercises and routines (fitness), and glossaries for any topic with its own nomenclature.

Glossaries are essential: once created, adhere to the glossary in every lesson. Build the glossary as part of learning: compressing a concept into a tight definition is evidence the user understands it. Glossary rules: add a term only when the user understands it (it's a record of compressed knowledge, not a dictionary to learn from). Be opinionated, listing rejected aliases under `_Avoid_`. Keep definitions tight (one or two sentences, what the term IS). Use the glossary's own terms inside definitions. Group under subheadings when natural. Flag ambiguities explicitly. Revise as understanding deepens.

## Learning Records

Write a learning record (a single-paragraph record in `learning-records/`, numbered `0001-slug.md`, `0002-slug.md`, ...) when: the user demonstrated genuine understanding of something non-trivial (evidence, not mere coverage); the user disclosed prior knowledge (record the depth claimed); a misconception was corrected; or the mission shifted in response to learning (cross-link and update `MISSION.md`). Optional sections when they add value: **Status** frontmatter (`active | superseded by LR-NNNN`), **Evidence**, **Implications**. When a later record contradicts an earlier one, mark the old one `Status: superseded by LR-NNNN` rather than deleting it.

## `NOTES.md`

The user will sometimes express preferences for how they want to be taught, or things you should keep in mind. Record these here, and refer back when designing lessons or working with the user.

See `references/teach-formats.md` for the lesson formats.