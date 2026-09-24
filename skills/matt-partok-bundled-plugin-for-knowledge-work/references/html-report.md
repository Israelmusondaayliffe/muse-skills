# Architecture Report Scaffold

For the Architecture improvement procedure: write a **self-contained HTML
file** to the project-approved output location, with a fresh versioned
filename (e.g. `architecture-report-v1.html`). Verify the file directly or
inspect it on the browser surface, then give the user its absolute path.

## Layout

- Use **Tailwind via CDN** for layout and styling; **Mermaid via CDN** for
  diagrams where a graph/flow/sequence reliably communicates structure. Mix
  hand-crafted CSS/SVG with Mermaid: use Mermaid when relationships are
  graph-shaped (call graphs, dependencies, sequences); use hand-built divs/SVG
  for editorial visuals (mass diagrams, cross-sections, collapse animations).
- **Each candidate gets a before/after visualization** — side by side, showing
  the shallowness and the deepening. Be visual.

## Candidate card

Each card renders:

- **Files** — which files/modules are involved.
- **Problem** — why the current architecture causes friction.
- **Solution** — plain-English description of what would change.
- **Benefits** — in terms of locality and payoff, and how tests improve.
- **Before / After diagram** — side-by-side, illustrating the shallowness and
  the deepening.
- **Recommendation strength** — one of `Strong`, `Worth exploring`,
  `Speculative`, rendered as a badge.
- **ADR conflict callout** (if applicable) — only when a candidate contradicts
  an existing ADR *and* the friction is real enough to warrant revisiting it:
  e.g. a warning callout "contradicts ADR-0007 — but worth reopening
  because…". Never list every theoretical refactor an ADR forbids.

## Closing

End with a **Top recommendation** section: which candidate to tackle first
and why.

## Vocabulary

Use `CONTEXT.md` vocabulary for the domain ("the Order intake module", not
"the FooBarHandler" and not "the Order service") and the deep-module
vocabulary (module, interface, depth, seam, adapter, payoff, locality) for
the architecture. See `deep-module-design.md`.

## After the report

Do **not** propose interfaces yet. Ask the user: "Which of these would you
like to explore?" — then run the grilling loop on the chosen candidate.
