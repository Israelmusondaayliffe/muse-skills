---
name: ask-matt
description: "Use when the user asks which skill or flow fits their situation, with trigger phrases like ask Matt, what should I use, or which skill should I use. It routes over the skills in this repo: the main idea-to-ship flow, the on-ramps for bugs and big efforts, the phase-boundary protocol, and the standalone skills."
---

Invocation: user-invoked only

Router over the flows. Map the user's situation to one of the sections below and invoke that skill. A **flow** is a path through the skills. Most paths run along one **main flow**, and two **on-ramps** merge onto it.

## Main flow: idea → ship

The route most work travels, from an idea to something built.

1. **`/grill-with-docs`** sharpens the idea by interview. Start here whenever you are **working in a working directory**: it is stateful, retaining what it learns in `CONTEXT.md` and ADRs. (No working directory? Use `/grill-me` instead. Both run the same `/grilling` primitive; `grill-with-docs` leaves a paper trail, which makes it the better of the two whenever a repo is there to leave it in.)
2. **Branch: can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`/handoff`** in both directions:
   - **`/handoff`** out, then open a fresh session against that file,
   - **`/prototype`** to answer the question with throwaway code,
   - **`/handoff`** back what you learned, and reference it from the original idea thread.
3. **Branch: is this a multi-session build?**
   - **Yes** → **`/to-spec`** (thread into a spec), then **`/to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. Local tracker: one file per ticket under `.scratch/<feature>/issues/`, worked blockers-first by hand. Real tracker: edges become native blocking links, so any ticket whose blockers are done can be grabbed. Kick off **`/implement`** per ticket, **`/clear`ing context between each one**. Each ticket is self-contained, so the last one's context is disposable.
   - **No** → **`/implement`** right here, in the same context window.
   - Either way, **`/implement`** builds each issue by driving **`/tdd`** internally (one red-green slice at a time), then closes out by running **`/code-review`**, a two-axis review (Standards + Spec) of the diff, before committing. Reach for **`/tdd`** alone to build a concrete behaviour test-first without a full spec, and **`/code-review`** alone to review a branch or PR against a fixed point.

### Context hygiene

Keep steps 1-3 in **one unbroken context window** (don't compact or clear until after `/to-tickets`) so the grilling, spec, and tickets all build on the same thinking. Each `/implement` then starts fresh, working from the ticket.

The limit is the **smart zone**: the window (~150k tokens on state-of-the-art models) within which the model still reasons sharply. If a session approaches it before `/to-tickets`, don't push on degraded; `/compact` at the nearest phase boundary and carry on.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **`/triage`**. Moves issues through triage roles and produces agent-ready issues, which **`/implement`** later picks up. Triage is only for issues **you didn't create**: bug reports, incoming feature requests, anything that arrives raw. Tickets `/to-tickets` produced are already agent-ready, so **don't triage them**.
- **Something's broken** → **`/diagnosing-bugs`**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** (one command that already goes red on *this* bug), then fixes with a regression test. Its post-mortem hands off to **`/improve-codebase-architecture`** when the real finding is that there's no good seam to lock the bug down.
- **A huge, foggy effort** (greenfield project or huge feature build, too big for one session) → **`/wayfinder`**. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** and resolves them one at a time, producing **decisions, not deliverables**, until the fog is pushed back. It is slower and denser than `/grill-with-docs`, so save it for the idea you can't hold in one session, never a well-scoped feature. When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`/to-spec`**, which collapses the map's linked decisions into a buildable plan, then `/to-tickets` and `/implement` as usual. Going straight from the map to `/implement` skips that collapse and throws the linked detail away, so do it only when the effort turned out genuinely small.

## Codebase health

Not feature work, just upkeep.

- **`/improve-codebase-architecture`** runs whenever you have a spare moment to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one *generates an idea* you can take into the main flow at `/grill-with-docs`. It's the survey that finds the candidates; **`/codebase-design`** is the bench you design the chosen one on.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills, each the single source of truth for its vocabulary. Reach for `/domain-modeling` or `/codebase-design` directly when the **words**, not the process, are the problem; otherwise let the other briefs pull them in.

- **`/domain-modeling`**: sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline `/grill-with-docs` drives to keep `CONTEXT.md` a clean glossary.
- **`/codebase-design`**: the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. `/tdd` and `/improve-codebase-architecture` both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. A phase ends when you think "ok, we're done with that". At the **boundary** between two phases you have five options:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what's next.
- **`/handoff`**: writes a portable markdown file. Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent**: send a tightly-scoped task to its own window and get a report back.
- **`/compact`**: compresses this context and seeds a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Work the tree top to bottom at the boundary. The first **yes** wins.

1. **Can you continue in this session?** Yes when the next phase needs this phase as a **primary source**, or you have enough smart zone left (~150k tokens) for the next phase to fit. Grilling → implementation is the standard yes: the implementation wants the reasoning verbatim, not a summary of it. Continue costs nothing and loses nothing, so rule it out before anything else.
2. **Is the context irrelevant to what comes next?** Is everything here (the exploration, the decisions, the dead ends) disposable? If so, **`/clear`**. The cheapest move on the board. Clearing a *relevant* context loses the **why** behind what you built, and no amount of reading the diff back returns it. Not terminal: the old session stays resumable.
3. **Do you need to hand off?** `/handoff` is narrow: a **new harness** (Claude → Codex), a **new directory** or repo, a **colleague**, or a side task forked **mid-phase**. What it buys is **portability**: a file that travels. If nothing is travelling, you don't need it.
4. **Can the task be done AFK?** Scoped tightly enough to run with you away from the keyboard, no steering? Then send it to a **subagent** and leave this session untouched. Automated review is the standard case.
5. **Otherwise, `/compact`.** Relevant context, same harness, same directory, and you need to stay in the loop: this is where the tree lands, and it lands here often. Pass an instruction (`/compact we're going to QA this area`) so the summary keeps what the next phase needs. It is the **default, not the first reach**: the four questions above it are all cheaper or more precise, and a fresh session is confidently wrong about a decision the summary flattened.

Every move except **Continue** turns a **primary source** into a **secondary source**: the session as it happened, replaced by a summary of it. Primary sources carry full information and lots of noise with little room to move; secondary sources are lossy, quieter, and give room to move. This is why question 1 comes first: you only pay the lossiness when staying costs more than it saves.

Make the decision **at** a boundary. Mid-phase there is no decision: continue, or split the work left into subagents.

## Standalone

Off the main flow entirely.

- **`/grill-me`**: the same relentless interview as `/grill-with-docs`, but **stateless**: it saves nothing locally and builds no `CONTEXT.md`. Reach for it when you are **not working in a working directory** (a plan, a design, a piece of writing, anything with no repo under it). In a working directory, use `/grill-with-docs` instead: strictly the better one.
- **`/grilling`**: the interview primitive itself: rounds, the frontier, facts are the agent's job and decisions are yours. `/grill-me` and `/grill-with-docs` are the two named ways in, and `/triage`, `/wayfinder`, and `/improve-codebase-architecture` all run grilling internally. Reach for it directly only when you want the interview with no wrapper around it.
- **`/resolving-merge-conflicts`**: works an in-progress merge or rebase conflict hunk by hunk, resolving by **intent** traced to each side's primary source rather than by picking lines, then finishes the operation. It never runs `--abort`. Standalone and off every flow: reach for it when you are already mid-conflict.
- **`/prototype`**: a small, throwaway program that answers one design question. Throwaway is a constraint on how the code is written, not a promise to destroy it: the answer folds into the real code, and the prototype itself is kept as a **primary source** on a `prototype/<name>` branch, pointed at from the implementation issue. It's the detour in step 2 of the main flow, but reach for it any time a design question is hard to settle on paper.
- **`/research`**: delegate reading legwork to a **background agent**: it investigates a question against **primary sources**, then leaves a cited Markdown file in the repo. Keep working while it reads. Its file feeds `/grill-with-docs`, since research feeds the thinking rather than replacing it.
- **`/to-questionnaire`**: when the blocker isn't in your head or the codebase but in **someone else's**, it interviews you about the **send** (who it's going to, what you need back) and writes them a questionnaire. The inverse of `/grill-me`. What comes back is material for `/grill-with-docs` or `/to-spec`.
- **`/wizard`**: for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets. Model-invoked: the agent reaches for it the moment it hits a wall only you can pass. If the agent could just do it itself, it should; this is for where a human is genuinely in the loop.
- **`/wait-what`**: the corrective for a message that didn't land. Use it mid-conversation, inside any other skill: the agent re-pitches what it just said with the context you were missing, in plain English, using the `CONTEXT.md` vocabulary. It works after the fact; `/grill-with-docs` is the upfront cure, because a shared language agreed early is what stops the jargon arriving at all.
- **`/teach`**: learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`/writing-for-agents`**: the reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Precondition

**`/setup-matt-pocock-skills`**: run before your first engineering flow to configure the issue tracker, triage labels, and doc layout the other skills assume. Custom issue trackers also work.
