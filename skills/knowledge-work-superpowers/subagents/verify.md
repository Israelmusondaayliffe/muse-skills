---
name: verify
description: "Use when work is about to be called complete and needs fresh, evidence-backed verification. Triggers include the final pass before delivery, a draft that looks finished and polished, a stakeholder asking whether the output is accurate or ready, and any claim of completeness that has not yet been backed by a check run just now. A previous review, a polished artifact, or a passed earlier check is not sufficient proof. Runs the verification gate: identify what would prove the claim, run the complete fresh check, read the result, compare with the brief, fix failures or report actual status, and state completion only when the evidence supports it."
---

# verify

Fresh, evidence-backed verification before delivery.

## Purpose

Require evidence for completion claims. A polished artifact and a previous review are not fresh verification.

## Core rule

Do not say the work is complete, accurate, ready, or verified until the relevant checks have just been run and their results inspected.

## The gate

1. Identify what would prove the claim.
2. Run the complete fresh check.
3. Read the result.
4. Compare with the brief.
5. Fix failures or report actual status.
6. State completion only when the evidence supports it.

## Checklist

- **Brief:** every required question answered; scope and exclusions respected; audience and decision served; required format, length, template followed.
- **Evidence:** every key factual claim has support; citations open and support the nearby claim; quotations and numbers match sources; primary sources used where required and available; counterevidence and conflicts represented.
- **Analysis:** fact, inference, dispute, and recommendation distinguished; assumptions visible; recommendations follow from evidence and decision; unresolved claims narrowed, labeled, or removed.
- **Freshness:** time-sensitive facts checked live; publication and update dates inspected; memory or prior notes not treated as confirmed current state.
- **Calculations and data:** rerun with a deterministic tool; units, denominators, date ranges, populations match; tables and charts agree with underlying data.
- **Safety and permissions:** confidential or personal information handled within scope; no external message, publication, or destructive action without authority; domain-specific review used when required.
- **Artifact:** file exists in the correct output location; filename and version follow the rules; file opens, renders, or parses correctly; no placeholders remain; evidence package present when required.

## File-based check

Run from the research bundle root:

```bash
python3 ../bin/verify_research_bundle.py /path/to/bundle --profile deliverable
```

This structural check does not replace opening sources and inspecting claim support.

## Failed verification

- Do not claim completion.
- State the failing check and the evidence.
- Fix it when within scope; re-run the complete affected check.
- Record any unresolved limitation.

State what was verified and name the evidence briefly. Avoid claims broader than the checks that ran.
