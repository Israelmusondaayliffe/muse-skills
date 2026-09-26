# Routing policy

Use this when ownership is unclear, several workspace skills could fit, or a request spans capability domains. A focused request should use the matching skill directly — no routing needed.

Explicit user selection chooses the operating method. Preserve the user's outcome and definition of done across every route and handoff.

## Collision decisions

When two or more skills collide on the same request, record one primary route:

- The minimum phrases that distinguish the collision.
- The one primary skill that owns it.
- `companions`: later routes allowed only at a documented handoff; empty when no handoff is required.
- `excluded_routes`: plausible routes deliberately not selected.
- `reason`: short evidence-based reason why the primary owns this stage.

Keep no standing collision list unless real collisions have been reviewed. Do not infer collisions from names alone.

## Reviewed collisions in this collection

These were reviewed against the skills' own descriptions. Each has one owner, and no route hands the request back to a skill that already declined it.

| Request | Primary | Not selected, and when they do own it |
|---|---|---|
| "grill me", "interview me", "pressure-test this decision" with no other named workflow | `strategy-room` | `matt-partok-bundled-plugin-for-knowledge-work` only when the user names Matt, Matt Pocock, or the bundle; `outcome-engine` only inside an Outcome Engine run; `gauntlet-loop` grilling only inside a gauntlet-loop project |
| "run the gauntlet" with a bar to beat or a blind comparison, or existing `.gauntlet/runs/` | `gauntlet` | `gauntlet-loop` |
| "gauntlet loop", governed workstreams, or existing `.gauntlet/state.json` | `gauntlet-loop` | `gauntlet` |
| bare "run the gauntlet" with no state and no edition signal | neither yet: ask one choice question | both, until the user picks |

A route that reaches an owner is final. If the owner's own skill says the request is not its job, report that and name the reviewed owner once; do not route back to the router or to the previous skill.

## Handoffs

Add a handoff only when the primary route cannot complete a later stage and the receiving capability is actually present. A companion is optional until its handoff condition becomes true. Absence of a related skill must not stop the primary route from completing its owned work.

## Connector order

For data work, select the connector that owns the data first, then the workflow capability that operates on the retrieved material. Connector choice does not decide workflow ownership.

## Fallbacks

Prefer a workspace skill over a bundled copy of the same name, and name the choice explicitly when the user selected it. If no skill matches a request cleanly, say so and ask the user which route to take rather than inventing ownership.
