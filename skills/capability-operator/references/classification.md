# Overlap states

- **identical-mirror**: the name and SKILL.md fingerprint match. Safe to keep both only if the duplication is intentional; otherwise pick one home.
- **drifted-copy**: the name matches but the fingerprint differs. Review both sources, decide which is canonical, and retire or repoint the other.
- **cross-layer**: the same skill name exists in the workspace layer and the bundled layer. The bundled copy is upstream and read-only; if they differ, decide whether the workspace copy is a deliberate override and name that decision explicitly.
- **trigger-collision**: different names claim substantially the same user intent. Found only by reading descriptions side by side. Cite the colliding trigger text in the audit report.
- **superseded**: an explicit owner and migration decision identifies the replacement.
- **unresolved**: evidence does not establish the relationship. Keep both, record the open question.

Never infer supersession from recency alone.

## Disposition rules

1. Match a group to one state above before recommending any action.
2. Semantic (trigger) overlap and retirement decisions always require judgment and source review — never automate deletion.
3. Require explicit user authorization and a current inventory backup before any consolidation.
4. Record each decision (keep / merge / retire) with its reason so later audits don't relitigate it.
