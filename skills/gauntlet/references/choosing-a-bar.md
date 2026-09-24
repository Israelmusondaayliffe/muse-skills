# Choosing a bar

The bar is the single most consequential decision in the brief. Every critic verdict, every verifier pass, and the final evidence report are measured against it. A soft bar makes the whole run theater.

## What makes a bar valid (INV-1)

The bar is external and inspectable. It is a real artifact, source set, test suite, benchmark, or measurement that exists before the run starts and does not move during it.

- **External.** The run did not produce it and will not produce it. A bar that references the run's own output is circular: the work would be graded against itself.
- **Inspectable.** A fresh-context critic can compare the work against it using a method from the closed set (`run`, `test`, `measure`, `screenshot`, `render`, `reader-proxy`, `claim-audit`, `source-reach`, `red-team`, `read`). If no method can put the bar and the artifact side by side, it is not a bar.
- **Frozen.** Where the bar includes a rubric (mostly `strategy`), the rubric is fixed at brief time and its hash recorded by `hash_plan.py`. A rubric edited during a run is an integrity failure, not a refinement.
- **Never a self-authored mid-run rubric.** An agent writing its own grading criteria while it works is self-grading with extra steps.
- **Never prose adjectives.** "Excellent", "world-class", and "really polished" are aspirations, not bars. A critic cannot lose to an adjective, so it will always find a way to pass.

## The failure taxonomy `validate_bar.py` enforces

The script fails the bar, and blocks the stage, when any of these holds:

| Failure | What it looks like | Fix |
|---|---|---|
| Nothing backs it | No file, command, source set, or measurement behind the bar text | Name the concrete comparator and put it, or a fetch script, in `bar/refs/` |
| Adjectives only | "Best-in-class quality", "extremely clear" | Replace every adjective with an artifact or a number |
| Self-referential | The bar cites an artifact this run will produce | Find an external comparator, or a frozen rubric plus red-team where none exists |
| No inspection method | The bar names a comparator but not how the work is compared against it | Declare one method from the closed set, with the command where the method requires one |
| Unhashed rubric | `bar/rubric.md` exists but no frozen hash is recorded | Run `hash_plan.py` before proceeding |
| Unresolvable reference | A path in `bar/refs/` or a bar ref in `pieces.json` does not resolve | Fetch and store the real file. A described reference is not a reference |

A failed bar blocks the brief. There is no override.

## Worked examples: soft bar to concrete bar

### code

Soft: "Make the importer fast and reliable."

Concrete:

- Bar: the existing test suite at `tests/importer/` passes, plus a latency target of p95 under 300 ms per 10k-row file, measured by `scripts/bench_importer.sh` against the three fixture files stored in `bar/refs/fixtures/`. Baseline numbers from the current implementation recorded in `bar/refs/baseline.json` at brief time.
- Inspection: `test` (`inspection_command: pytest tests/importer/`) and `measure` (`inspection_command: scripts/bench_importer.sh`).
- Blind: partial, on behavior. Critics compare outputs and measurements from both implementations, never the source text.
- `done_means`: measured threshold.

### prose

Soft: "The editorial should be really compelling."

Concrete:

- Bar: three reference openings and three reference argument sections, copied verbatim into `bar/refs/reference-openings.md` and `bar/refs/reference-arguments.md`, drawn from named published pieces at the target clarity and compression. The reference is a floor for clarity and information density, not a voice to copy.
- Inspection: `reader-proxy` with frozen questions ("What is this arguing?", "Why does a reader continue past line three?") plus blind prose pairing against the reference via `blind_pair.py`, plus `claim-audit` for any factual claims.
- Blind: strong.
- `done_means`: blind win, defined as the critic picking ours in 2 consecutive rounds.

### visual

Soft: "A landing page that looks premium."

Concrete:

- Bar: real screenshots of three named best-in-class pages in the same category, fetched and stored as image files in `bar/refs/` (or a `fetch_refs.sh` that retrieves them). Descriptions of screenshots are not screenshots; a missing reference file fails bar validation.
- Inspection: `screenshot` at each target viewport (`inspection_command` renders and captures 390px, 768px, 1440px), blind-paired against the reference captures.
- Blind: strong.
- `done_means`: blind win, plus the integrity check that the page builds and renders at every target viewport with no placeholder assets.

## Fair comparators

`bar_rationale` must say why the comparator is fair, and the brief should be able to defend it in one paragraph. A fair comparator:

- Matches the artifact's genre, audience, and scale. Comparing a two-page memo against a book chapter measures length tolerance, not quality.
- Is beatable in principle but not trivially. A comparator so far above reach that every round loses identically produces no gradient (the no-gain rule will fire and stall the piece). A comparator below the current draft converges in one round and proves nothing.
- Is stable for the whole run. Swapping comparators mid-run because the work keeps losing is moving the bar, and the plan hash exists to catch it.
- Is honest about domain limits. Where no fair comparator exists (most `strategy` work), do not fake one: use a rubric frozen at brief time with its hash recorded, plus an adversarial red-team pass.

## Choosing done_means

Closed set: `blind win` | `measured threshold` | `user judgment`.

- **blind win.** Use when blind comparison is strong (`prose`, `visual`, `deck`, `prompt-system`, `brand`). Define the win condition numerically: the default is 2 consecutive blind wins. Never fabricate a blind comparison where blinding is infeasible.
- **measured threshold.** Use when a number or test result decides it (`code` latency and coverage, `research` coverage requirement, citation ratio floor, and disconfirming-evidence quota). The threshold and its measuring command are fixed at brief time.
- **user judgment.** Use when the user insists on holding the final call, or when the domain resists both blinding and measurement. It still requires the run to reach verification first: user judgment decides done, it never replaces the quality and integrity verifiers, and caps still pause rather than certify.

Pick exactly one primary `done_means` for the run. Pieces may carry stricter acceptance criteria, never looser ones.
