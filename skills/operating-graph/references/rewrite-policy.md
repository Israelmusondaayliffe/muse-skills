# Rewrite Policy

Every rewrite starts as a proposal with an ID, run ID, base graph version, trigger, evidence event IDs, risk, reason, predicted effect, primitive operations, approval requirement, and rollback version.

## Primitive operations

Use only `add_node`, `update_node`, `disable_node`, `add_edge`, `disable_edge`, and `set_priority`. Compile split, merge, replace, reviewer, reroute, fan-out collapse, serialization, arbitration, and pattern promotion into these primitives.

## Triggers

- Two failures by one node: propose replacement or a reviewer.
- Material contradiction: propose arbitration.
- Budget use outpaces progress: propose fan-out collapse or serialization.
- An isolated task is over-decomposed: collapse optional fan-out and execute inline.
- Competing state writers: serialize branches.
- An unsatisfiably blocked required node: reroute or escalate.
- Terminal evaluator rejection: add new corrective work.

Evaluate after failure, blockage, evaluator rejection, artifact invalidation, budget thresholds of 50, 75, and 90 percent, contradiction signals, epoch completion, requirement changes, or incomplete deadlock.

## Risk

Low-risk changes may apply automatically only inside existing budgets and permissions. Examples include priority changes, optional serialization, independent evaluator or diagnostic additions, disabling unstarted optional nodes, bounded next-epoch feedback, and redundant optional fan-out collapse.

Medium risk requires human approval for worker replacement, execution or skill changes, required rerouting, merges, critical splits, increased concurrency or budget, distribution destination changes, and accepted-artifact invalidation.

High risk requires explicit approval for disabling critical work, removing required evaluation, changing terminal distribution, adding external side effects, or resuming after event-chain corruption.

Never change the goal, weaken criteria, change authority, expand permissions, remove approvals, erase audit or evidence history, rewrite old versions, increase hard limits without approval, permit self-evaluation, or permit worker state writes.

Every applied rewrite revalidates the full graph, writes the next immutable version, emits `rewrite.applied`, preserves prior versions, atomically updates state, and records rollback.

On Hatch, approval means the user explicitly saying yes (the `human-authority` node). Present the proposal — evidence, predicted effect, risks, rollback — and wait. Do not infer approval from silence.
