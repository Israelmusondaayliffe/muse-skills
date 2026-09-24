# Routing workflow

## Decision sequence

1. Confirm the analysis is checked, partial, or disputed.
2. Identify the decision and the smallest audience that must act.
3. Select one primary delivery format.
4. Declare the evidence limits and production companions.
5. Hand the route to visual audit or readout production.

## Format table

| Need | Primary format | Production path on this host |
| --- | --- | --- |
| Inspect calculations or reproduce methods | notebook | Markdown walkthrough + referenced source files |
| Explain one relationship | chart | Media pipeline image or Markdown data table |
| Monitor changing measures | dashboard | Local brief: state that a live dashboard needs a publishing surface |
| Preserve full analysis and methods | report | Markdown/HTML report in `~/workspace/` |
| Lead a live decision discussion | deck | HTML/Markdown deck file, or browser task if live slides needed |
| Enable a fast decision | executive-readout | Readout mode of this skill |
| Publish an interactive external artifact | site | Static HTML in workspace + expiring share link; state the limit |

Select one primary delivery format. Add a secondary export only when another audience or access need requires it.

## Readiness rules

- `checked`: production may continue with stated caveats.
- `partial`: continue only if the decision can tolerate the named gaps.
- `disputed`: stop production and return the disagreement to the analysis owner.

## Zero-companion fallback

All production companions are optional. The `required_companions` field records the capabilities a later production step needs. It does not report availability and does not block creation of the route artifact.

When no selected companion is available, create a self-contained local Markdown or JSON story brief. Include the decision question, audience, source artifact paths, analysis state, chosen format, evidence limits, production needs, risks, and next skill. Mark unsupported production or publication incomplete. Do not claim that the requested deck, dashboard, site, or other unsupported deliverable was produced or published.
