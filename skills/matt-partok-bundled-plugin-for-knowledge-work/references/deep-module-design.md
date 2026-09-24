# Deep-Module Design Vocabulary

Use these terms exactly — don't substitute "component," "service," "API," or
"boundary." Consistent language is the whole point.

- **Module**: anything with an interface and an implementation. Deliberately
  scale-agnostic: a function, class, package, or tier-spanning slice. _Avoid_:
  unit, component, service.
- **Interface**: everything a caller must know to use the module correctly:
  the type signature, plus invariants, ordering constraints, error modes,
  required configuration, and performance characteristics. _Avoid_: API,
  signature (too narrow — type-level surface only).
- **Implementation**: what's inside a module. Distinct from **Adapter**: a
  thing can be a small adapter with a large implementation (a Postgres repo)
  or a large adapter with a small implementation (an in-memory fake). Reach
  for "adapter" when the seam is the topic; "implementation" otherwise.
- **Depth**: payoff at the interface — the amount of behavior a caller (or
  test) can exercise per unit of interface they have to learn. A module is
  **deep** when a lot of behavior sits behind a small interface, **shallow**
  when the interface is nearly as complex as the implementation.
- **Seam** (Feathers): a place where you can alter behavior without editing in
  that place; the *location* at which a module's interface lives. Where to
  put the seam is its own design decision, distinct from what goes behind it.
  _Avoid_: boundary (overloaded with DDD's bounded context).
- **Adapter**: a concrete thing that satisfies an interface at a seam.
  Describes *role* (what slot it fills), not substance (what's inside).
- **Payoff**: what callers get from depth — more capability per unit of
  interface learned. One implementation pays back across N call sites and M tests.
- **Locality**: what maintainers get from depth — change, bugs, knowledge, and
  verification concentrate in one place. Fix once, fixed everywhere.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep
  module can be internally composed of small, mockable, swappable parts —
  they just aren't part of the interface. A module can have **internal seams**
  (private to its implementation, used by its own tests) as well as the
  **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes,
  it was a pass-through. If complexity reappears across N callers, it was
  earning its keep.
- **The interface is the test surface.** Callers and tests cross the same
  seam. If you want to test *past* the interface, the module is probably the
  wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.**
  Don't introduce a seam unless something actually varies across it.

## Designing for testability

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params =
   simpler test setup.

## Deepening: dependency categories

When deepening a cluster of shallow modules, classify its dependencies — the
category determines how the deepened module is tested across its seam:

1. **In-process** (pure computation, no I/O): always deepenable; merge and
   test through the new interface directly. No adapter needed.
2. **Local-substitutable** (a local test stand-in exists, e.g. PGLite for
   Postgres, in-memory filesystem): deepenable if the stand-in exists; test
   with the stand-in. The seam stays internal — no port at the external
   interface.
3. **Remote but owned** (your own services across a network boundary): define
   a **port** (interface) at the seam; the deep module owns the logic; the
   transport is injected as an adapter. Tests use an in-memory adapter;
   production uses the HTTP/gRPC/queue adapter.
4. **True external** (third-party services you don't control): the deepened
   module takes the dependency as an injected port; tests provide a mock
   adapter.

**Seam discipline:** don't introduce a port unless at least two adapters are
justified (typically production + test) — a single-adapter seam is just
indirection. Don't expose internal seams through the interface just because
tests use them.

## Design it twice

When exploring alternative interfaces for a deepening candidate (Ousterhout:
your first idea is unlikely to be the best):

1. **Frame the problem space** in a user-facing explanation first: constraints
   any interface must satisfy, dependency categories, a rough illustrative
   code sketch to ground the constraints (not a proposal — a way to make the
   constraints concrete).
2. **Produce at least three meaningfully different interfaces** — via parallel
   subagents when delegation is permitted, otherwise sequentially while
   isolating the design constraints. Brief each with a different constraint:
   - Minimize the interface: 1–3 entry points max; maximize payoff per entry point.
   - Maximize flexibility: support many use cases and extension.
   - Optimize for the most common caller: make the default case trivial.
   - (Optional) Design around ports & adapters for cross-seam dependencies.
3. Compare on depth, payoff, locality, and seam placement; include both this
   vocabulary and the `CONTEXT.md` domain vocabulary in each brief so names
   stay consistent.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout):
  rewards padding the implementation. Use depth-as-payoff instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public
  methods**: too narrow — interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or
  **interface**.
