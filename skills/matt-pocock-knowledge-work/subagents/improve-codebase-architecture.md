---
name: improve-codebase-architecture
description: "Use when the user wants to scan a codebase for deepening opportunities, see them as a visual HTML report, and then grill through whichever candidate they pick."
---

Invocation: user-invoked only

## Procedure

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

Use the codebase-design vocabulary exactly (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**). Never drift into "component," "service," "API," or "boundary." Use the domain language in `CONTEXT.md` for names, and respect ADRs in `docs/adr/`.

### 1. Explore

**Scope before you scan: YAGNI.** Deepening pays off where future changes happen, so weight recently changed parts.

- If the user named a direction (a module, a subsystem, a pain point), take it and skip inference.
- Otherwise, walk back `git log --oneline` to find hot spots: files and areas that keep coming up. If changes are scattered with no clear hot spot, widen the net.

Read `CONTEXT.md` and relevant ADRs first. Then spawn a sub-agent to walk the codebase organically, noting friction:

- Where does understanding one concept require bouncing between many small modules?
- Which modules are **shallow**, with an interface nearly as complex as the implementation?
- Where were pure functions extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts are untested, or hard to test through the current interface?

Apply the **deletion test** to suspected shallow modules: would deleting it concentrate complexity, or just move it? "Concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory (from `$TMPDIR`, fallback `/tmp`, or `%TEMP%` on Windows) at `<tmpdir>/architecture-review-<timestamp>.html`. Open it for the user (`xdg-open` on Linux, `open` on macOS, `start` on Windows) and tell them the absolute path.

Build the report with **Tailwind via CDN** for layout and **Mermaid via CDN** for graph-shaped diagrams (call graphs, dependencies, sequences). Use hand-crafted CSS/SVG for editorial visuals (mass diagrams, cross-sections, collapse animations). Every candidate gets a **before/after visualisation**.

Each candidate gets a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture causes friction
- **Solution**: plain English description of what changes
- **Benefits**: explained in terms of locality and leverage, and how tests improve
- **Before / After diagram**: side-by-side, showing the shallowness and the deepening
- **Recommendation strength**: `Strong`, `Worth exploring`, or `Speculative`, as a badge

End with a **Top recommendation** section: which candidate to tackle first and why.

**ADR conflicts**: surface a candidate that contradicts an ADR only when the friction is real enough to warrant revisiting it. Mark it clearly (a warning callout like "contradicts ADR-0007, but worth reopening because..."). Do not list every theoretical refactor an ADR forbids.

Do NOT propose interfaces yet. After the file is written, ask: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, use the grilling skill to walk the decision tree: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Keep side effects inline as decisions crystallize, using domain-modeling:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md`. Create it lazily if missing.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR: "Want me to record this as an ADR so future architecture reviews don't re-suggest it?" Only for reasons a future explorer needs; skip ephemeral ones ("not worth it right now").
- **Want alternative interfaces?** Use codebase-design's design-it-twice pattern: parallel sub-agents design radically different interfaces, then compare on depth, locality, and seam placement.

## Knowledge-work port

- Step 1 becomes: survey recent edits to find the hot documents, then note friction: shallow sections, duplicated claims, fuzzy terms.
- Step 2 becomes: a visual report of restructuring candidates with before/after shape, ranked Strong / Worth exploring / Speculative.
- Step 3 becomes: grill one candidate, update the glossary as terms sharpen, record load-bearing rejections as decisions.
- Never propose the final structure before the reader picks a direction.
- The grilling loop ports directly: constraints, shape, what survives.

See `references/html-report-format.md` for the HTML report format.