# Prompt Migration Audit and Rewrite

Audit mode is read-only unless the user separately authorizes a rewrite. An
audit never silently rewrites the prompt: it produces a finding ledger and a
verification list, then hands the authorized rewrite to the target model's
builder procedure.

## 1. Record the migration

Source model, target model, prompt surface, the full source prompt, and the
evidence set (owner docs checked, dates). Migration preserves the user job but
never preserves unsupported parameters.

## 2. Verify the target surface

Check current owning documentation when settings, parameters, or tool behavior
affect the result. Never assume names stayed stable across ChatGPT, the API, or
third-party surfaces. If docs are unreachable, mark every dependent fact as
unverified.

## 3. Audit checklist

Check the prompt job, input contract, output contract, tool policy, effort or
reasoning controls, formatting, refusal behavior, and evaluation criteria.

- **Stale model assumptions:** instructions that only compensated for the source
  model's weaknesses. Target-model candidates: enumerated behavior lists,
  anti-laziness language, forced interim summaries, aggressive subagent
  authorization, code-review recall workarounds, vision compensation rituals,
  tool-triggering pressure, emphasis tricks ("CRITICAL: You MUST").
- **Unsupported parameters:** model slugs, effort enums, caching options,
  thinking budgets, prefilled turns, reasoning-extraction instructions. Remove
  or flag; never copy across.
- **Copied over-instruction:** repetition of the same instruction, "be concise"
  stacks, approval language repeated more than once.
- **Tool-policy drift:** tools exposed the new task does not need, stale return
  shapes, missing error behavior.
- **Output-contract loss:** any required section, schema field, length, or tone
  constraint the rewrite would drop.
- **Unverified current claims:** model behavior stated as current without a
  live source check.

## 4. Ledger

Write findings as a table: finding, category (stale assumption / unsupported
parameter / over-instruction / tool drift / contract loss / unverified claim),
outcome risk (high/medium/low), and disposition (remove / rewrite / verify /
keep). Prioritize by outcome risk.

## 5. Verification list

The facts that must be checked on the target surface before the rewrite ships:
model string, effort or verbosity settings, caching, tool availability, refusal
behavior. Leave unchecked items as open; do not fill them from expectation.

## 6. Authorized rewrite (only if the user approved it)

Follow `references/build-prompt.md` with the target model's profile, and add a
migration appendix:

```
### Migration Path
- Source model → target model; model strings
- Effort: [baseline kept / changed after comparison, with result]

### Lean Log (one entry per removal group)
- Removed: [group, the weakness it compensated for]
- Consolidated: [duplicated instructions merged, prior locations]
- Converted: [ALWAYS/NEVER on judgment calls → decision rules]
- Kept: [invariants retained, stated once]

### Additions
- [Target-model patterns added, with rationale]

### Rollback
- [How to revert: model string, effort, restored groups]
```
