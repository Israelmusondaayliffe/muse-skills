# Prompt Governance

Use this reference when a harness is being shortened or reorganized around progressive disclosure. The target is not the shortest prompt. The target is the smallest default context that preserves measured behavior.

## Governing thesis
Treat a large reported prompt reduction as directional evidence, never as a quota. Newer models may need less universal coaching, but user policy, authority boundaries, source precedence, and completion criteria remain load-bearing until a controlled subtraction test proves otherwise.

Build the harness as five layers:
1. A compact context kernel containing stable cross-task invariants.
2. Workspace and goal delta-only overlays containing only true local rules.
3. The front-door skill in default context, with specialists loaded through it or by explicit selection.
4. Examples, references, scripts, and tests beside the task that needs them.
5. A prompt-subtraction loop that rejects reductions causing behavioral regressions.

## Placement rules
| Requirement | Smallest correct owner |
| --- | --- |
| Stable identity, voice, fabrication boundary, authority, source precedence, ask/proceed behavior, interrupt behavior | Global context kernel |
| Writable zones, workspace layout, output paths | Workspace overlay |
| Goal ownership, inputs, workflow, acceptance, exclusions | Goal overlay |
| Conditional workflow or recovery detail | Task-owned skill or reference |
| Good behavior demonstration | Task-owned example or evaluation fixture |
| Exact path, format, policy, or validation | Script, validator, scheduled job config, or template |
| Model-specific compensation | Model-specific notes, loaded only for a reproduced failure |

State an invariant once. A closer layer refines scope but does not repeat the broader rule. Do not put capability inventories, connector manuals, CLI catalogs, or failure histories in universal context.

## Evidence freeze before subtraction
Create one dated run directory before editing. Freeze: applicable instruction files and their hashes; complete prompt input and word measurements by section; model, run count, tool inventory, and effective task conditions; the evaluation suite, output schema, raw outputs, and normalized baseline.

Do not compare runs whose model, effort, tools, or task conditions differ.

## Behavior evaluation contract
A useful permanent suite samples the decisions universal context is meant to protect: authority, safety, and source-owner routing; implementation outranking audit artifacts; finite task topology with a forced stop when usage is high but target-state delta is low; unresolved required work reported as incomplete; file layers, output paths, and evidence-backed completion.

Accept a subtraction batch only when:
1. every critical run passes;
2. no category falls below the accepted baseline;
3. overall pass rate meets or exceeds the accepted baseline;
4. prompt input is smaller for the intended reason;
5. duplicated guidance declines.

Word ceilings are diagnostics. They never override behavior acceptance.

## Compact workflow
1. Preserve the stable context kernel.
2. Remove repeated workflow inventories and point to the closest owner.
3. Reduce workspace and goal files to deltas.
4. Move detailed examples and conditional instructions to task-owned files.
5. Move exact checks to deterministic mechanisms.
6. Subtract one coherent instruction group at a time.
7. Run the frozen suite once; repeat only high-risk or historically flaky categories.
8. Restore a failed batch, then add only the smallest missing routing or policy cue demonstrated by the failure.

## Rollback and stopping
Use hash preconditions, dry-run receipts, one approval group at a time, backups, and atomic writes. Roll back in reverse apply order.

Stop immediately when: a hash precondition changes; evaluation conditions become incomparable; a critical or category regression appears; an unexpected file enters a generated operation plan; source and installed state diverge.

## Maintenance cadence
Run prompt subtraction monthly and after a major model update. Reproduce a failure before restoring model-specific compensation. Keep the last accepted prompt, evaluation inputs, raw outputs, normalized comparison, and rollback receipts so the next maintenance run starts from evidence instead of accumulated advice.
