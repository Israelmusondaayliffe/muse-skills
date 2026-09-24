# CONTEXT.md Format

`CONTEXT.md` is a glossary — nothing else. Devoid of implementation details.
Never a spec, scratch pad, or implementation-decision repository.

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
A one or two sentence description of the term.
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** Pick the best word; list the rest under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not
  what it does.
- **Only project-context terms.** General concepts (timeouts, error types,
  utility patterns) don't belong, no matter how heavily used. Test before
  adding: is this a concept unique to this context, or a general one?
- **Group terms under subheadings** when natural clusters emerge; a flat list
  is fine when terms cohere.

## Single vs multi-context

- Single context (most repos): one `CONTEXT.md` at the root.
- Multiple contexts: a `CONTEXT-MAP.md` at the root pointing at one
  `CONTEXT.md` per context, plus how they relate:

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) : receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) : generates invoices and processes payments

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

Inference: if `CONTEXT-MAP.md` exists, use it; else root `CONTEXT.md` means
single context; else create a root `CONTEXT.md` lazily when the first term is
resolved. In multi-context repos, infer which context the current topic
relates to — ask if unclear.
