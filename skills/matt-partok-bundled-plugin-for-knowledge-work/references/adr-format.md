# ADR Format

ADRs live in `docs/adr/`, numbered `0001-slug.md`, `0002-slug.md`, … Create the
directory lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: context, what was decided, and why.}
```

That is the whole format for most ADRs. The value is recording *that* a
decision was made and *why* — not filling out sections.

## Optional sections

Only when they add genuine value:

- **Status** (`proposed | accepted | deprecated | superseded by ADR-NNNN`) —
  useful when decisions are revisited.
- **Considered Options** — only when the rejected alternatives are worth
  remembering.
- **Consequences** — only when non-obvious downstream effects need calling out.

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When to offer an ADR

All three must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful.
2. **Surprising without context** — a future reader will wonder "why on earth
   did they do it this way?"
3. **The result of a real trade-off** — genuine alternatives existed and were
   picked for specific reasons.

If a decision is easy to reverse, skip it — you'll just reverse it. If it's
not surprising, nobody will wonder why. If there was no real alternative,
there's nothing to record beyond "we did the obvious thing."

## What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is
  event-sourced; the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate
  via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth
  provider, deployment target — the ones that would take a quarter to swap,
  not every library.
- **Boundary and scope decisions.** "Customer data is owned by the Customer
  context; others reference it by ID only." Explicit no-s are as valuable as
  yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL
  instead of an ORM because X." These stop the next engineer from "fixing"
  something deliberate.
- **Constraints not visible in the code.** "We can't use AWS for compliance
  reasons." "Responses must be under 200ms per the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** Recorded so
  nobody suggests GraphQL again in six months.
