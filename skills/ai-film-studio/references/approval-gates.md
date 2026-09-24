# Approval Gates

The skill may plan, draft, validate, and classify inside the project scope. It
must stop before any externally consequential action unless an approval names
that exact action and target.

| Action type | Minimum approval evidence |
| --- | --- |
| `paid_generation` | target surface, cost exposure, approval ID |
| `account_signin` | named account or surface, approval ID |
| `upload` | destination, files, approval ID |
| `purchase` | vendor, amount or pricing exposure, approval ID |
| `destructive_replacement` | exact target, recovery plan, approval ID |
| `publication` | destination, public/private scope, approval ID |
| `material_scope_expansion` | exact scope delta, cost preview, approval ID |

## Rules

- An approval is scoped to one action and one target. A previous approval does
  not authorize a new cost, upload, replacement, or publication.
- The user can deliver approval through: the live browser (I watch them act),
  a browser task they confirm, their own connected accounts/skills, or plain
  explicit text naming the action, target, cost, and approval ID.
- When approval is absent, return a **stopped** result that names the blocked
  action, the evidence required, and the exact next step — then wait.
- Never claim a live generation, upload, purchase, sign-in, or publication
  occurred without matching evidence (a receipt, the produced artifact, or the
  user's confirmation).
