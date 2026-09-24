# Prototype Modes

## Logic prototype

A tiny interactive terminal app that lets the user drive a state model by
hand. Right when the question is about **business logic, state transitions, or
data shape** — the kind of thing that looks reasonable on paper but only
feels wrong once you push real cases through it. (If the question is "what
should this look like" — wrong branch; use UI.)

1. **State the question.** Before writing code, write down the state model and
   the question in the prototype's README or a top-of-file comment. A logic
   prototype answering the wrong question is pure waste.
2. **Pick the language.** Use whatever the host project uses; if there's no
   obvious runtime (e.g. a docs repo), ask. Match existing tooling conventions
   — don't add a new package manager or runtime just for the prototype.
3. **Isolate the logic in a portable pure module** behind a small interface
   that could be lifted into the real codebase later. The TUI around it is
   throwaway; the logic module isn't. Shape depends on the question:
   - A pure reducer `(state, action) => state` — discrete events, single state value.
   - A state machine — explicit states and transitions; good when "which
     actions are even legal right now" is part of the question.
   - A small set of pure functions over a plain data type — no implicit
     current state, just transformations.
   - A class/module with a clear method surface — only when the logic
     genuinely owns ongoing internal state.
   Pick what fits the question, not what's easiest to wire to a TUI. Keep it
   pure: no I/O, no terminal code. The TUI imports it; nothing flows the other
   direction.

## UI prototype

Generate **several radically different UI variations** — default 3, cap 5
(more stops being radically different and starts being noise) — on a single
route, switchable from a floating bottom bar. The user flips between variants,
picks one (or steals bits from each), then throws the rest away.

A UI prototype is much easier to judge when it's **butting up against the
rest of the app**: real header, real sidebar, real data, real density. A
throwaway route in a vacuum makes every variant look fine in isolation.

- **Sub-shape A (preferred): adjustment to an existing page.** The route
  already exists; variants render on the same route gated by a `?variant=`
  URL search param. Data fetching, params, and auth stay; only the rendering
  swaps. A new section that would naturally live inside an existing page is
  still sub-shape A — mount it there.
- **Sub-shape B (last resort): a new page.** Only when the thing genuinely
  has no nearby home — an entirely new top-level surface or an un-embeddable
  flow. Create a throwaway route following the project's existing routing
  convention, named so it's obviously a prototype (include `prototype` in the
  path or filename). Same `?variant=` pattern.

Process: state the question and pick N (one line, top-of-file); build the
variants; put up the identical floating bottom bar for switching; give the
user one simple way to view it (a URL or one command). No polish beyond what's
needed to judge the design question.
