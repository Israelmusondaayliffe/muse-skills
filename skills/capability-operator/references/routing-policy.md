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

## Handoffs

Add a handoff only when the primary route cannot complete a later stage and the receiving capability is actually present. A companion is optional until its handoff condition becomes true. Absence of a related skill must not stop the primary route from completing its owned work.

## Connector order

For data work, select the connector that owns the data first, then the workflow capability that operates on the retrieved material. Connector choice does not decide workflow ownership.

## Fallbacks

Prefer a workspace skill over a bundled copy of the same name, and name the choice explicitly when the user selected it. If no skill matches a request cleanly, say so and ask the user which route to take rather than inventing ownership.
