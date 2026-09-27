---
name: codebase-design
description: "Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary."
---

Invocation: model or user

## Procedure

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Aim for leverage for callers, locality for maintainers, testability for everyone.

### Glossary

Use these terms exactly. Do not substitute "component," "service," "API," or "boundary."

- **Module**: anything with an interface and an implementation. Scale-agnostic: a function, class, package, or tier-spanning slice.
- **Interface**: everything a caller must know to use the module correctly: type signature, invariants, ordering constraints, error modes, required configuration, performance characteristics.
- **Implementation**: what's inside a module, its body of code. Distinct from **Adapter**: a small adapter can have a large implementation (a Postgres repo), or a large adapter a small one (an in-memory fake).
- **Depth**: leverage at the interface. Behaviour a caller can exercise per unit of interface they must learn. Deep: lots of behaviour behind a small interface. Shallow: interface nearly as complex as the implementation.
- **Seam** (Feathers): a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision.
- **Adapter**: a concrete thing that satisfies an interface at a seam. Describes *role*, not substance.
- **Leverage**: what callers get from depth. More capability per unit of interface learned.
- **Locality**: what maintainers get from depth. Change, bugs, knowledge, and verification concentrate in one place.

### Deep vs shallow

```
Deep:   small interface  + lots of implementation (aim here)
Shallow: large interface + thin implementation  (avoid)
```

When designing an interface, ask: can I reduce the number of methods, simplify the parameters, hide more complexity inside?

### Principles

- Depth is a property of the **interface**, not the implementation. A module may have **internal seams** (private, used by its own tests) plus the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. Wanting to test *past* the interface means the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Do not introduce a seam unless something actually varies across it.

### Designing for testability

1. **Accept dependencies, don't create them.** `processOrder(order, paymentGateway)` beats building the gateway inside.
2. **Return results, don't produce side effects.** `calculateDiscount(cart): Discount` beats mutating the cart in place.
3. **Small surface area.** Fewer methods mean fewer tests; fewer params mean simpler setup.

### Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

### Going deeper

- **Deepening a cluster given its dependencies**, see `references/codebase-design-deepening.md`: dependency categories, seam discipline, and replace-don't-layer testing.
- **Exploring alternative interfaces**, see `references/codebase-design-design-it-twice.md`: design the interface several radically different ways, then compare on depth, locality, and seam placement.

### Rejected framings

- Depth as ratio of implementation-lines to interface-lines (rewards padding). Use depth-as-leverage.
- "Interface" as the TypeScript `interface` keyword or public methods: too narrow.
- "Boundary": overloaded with DDD's bounded context. Say seam or interface.

## Knowledge-work port

- A "deep module" in knowledge work is a section with one clear claim and a short surface, backed by a dense evidence base beneath it.
- "Seam" is where your deliverable's promises meet its internals: headers, summaries, definitions.
- "Shallow" is a section with many headings and little substance, like a pass-through paragraph that adds no leverage.
- "Leverage" is what readers get per unit of text: one finding, reused across many decisions.
- Run the deletion test on every section: if removing it vanishes nothing, it was a pass-through.
