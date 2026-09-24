# muse-skills

Muse-native skills adapted from the [community agent plugins](https://github.com/Israelmusondaayliffe/plugins) marketplace.

The plugins repository ships reusable capabilities for Codex, Claude Code, and Claude Cowork. This repository is its Muse equivalent: each plugin ported into a workspace skill for Muse (Meta's personal AI assistant, running on Hatch).

## What changed in adaptation

- Codex/Claude plugin manifests (`.codex-plugin`, `.claude-plugin`), host-specific hooks, and agent YAML formats were **not** copied literally. Their substance was translated into procedures Muse can actually run: terminal shell, live browser, filesystem, cron/scheduled work, and subagent delegation.
- State paths were re-homed from `~/.claude` / `~/.codex` to `~/workspace/`.
- Scheduling surfaces became Hatch cron jobs; checkpoint hooks became explicit checkpoint procedures.
- Scripts were reviewed before porting; only safe, useful, stdlib-based helpers were kept.
- Nothing user-specific was invented: skills that need personal input (e.g. writing samples for `writing-quality`) ask for it at runtime.

## Skills

| Skill | What it does |
|---|---|
| `agent-ops` | Design, build, and audit reusable agent systems on Hatch. Covers pattern selection (single call, workflows, or autonomous agents), subage... |
| `ai-film-studio` | Explicit-only AI film-production planning: concept grill, film brief, production records, shot packets, and iteration supervision. Trigge... |
| `brand-studio` | Develop brand strategy, briefs, identity systems and brand reviews with current brand context and independent creative judgment. Use when... |
| `capability-operator` | Operate Muse's capability inventory on Hatch. Routes ambiguous or multi-domain requests to the right workspace skill, inventories ~/works... |
| `citizen-forge` | Turn a plain-language internal-tool idea into a governed application with deterministic risk classification, 35 named controls, and relea... |
| `continuity-vault` | Keep work usable and trustworthy across sessions: route continuity operations (task handoffs, durable extraction, knowledge promotion, kn... |
| `data-storytelling-studio` | Turns checked analysis into a decision-facing artifact without recalculating or overstating the source evidence. Routes analysis to the r... |
| `founder-revenue-engine` | Founder-led early revenue work: turn recent public signals into an evidence-backed ICP, commercial narrative, bounded outreach drafts, fo... |
| `gauntlet` | Run the gauntlet: a heavyweight builder-vs-blind-critic loop for mega projects that justify real cost. Use only when the user explicitly... |
| `gauntlet-loop` | Run the Gauntlet Loop: explicit-only governed execution for unusually large, consequential projects — plan grilling, compiled workstreams... |
| `guide-production-studio` | Build source-grounded practical guides: manuals, how-to pages, prompt guides, reference libraries. Owns source lineage, reader-first stru... |
| `harness-engineering` | Design, build, verify, or maintain Muse's personalized operating setup — memory and instruction files, workspace layout, skills, automati... |
| `image-prompting-studio` | Write image-generation prompts: create, edit, camera studies, storyboards, typography, infographics, series, grids, brand interpretation,... |
| `knowledge-work-superpowers` | Run substantial non-coding knowledge work end to end: framing, planning, systematic research, evidence-first analysis, sourced drafting,... |
| `last30days` | Research what people have actually said about any topic in the last 30 days: recent social, community, market, and web signals with hones... |
| `loop-observatory` | Read-only cross-loop telemetry: ingest terminal LoopKit runs and registered run roots, normalize outcome evidence, compare loop performan... |
| `loopkit` | Bounded, resumable Plan-Act-Verify loops with durable on-disk state: design a verifiable contract, execute bounded iterations with receip... |
| `matt-partok-bundled-plugin-for-knowledge-work` | Run Matt Pocock's idea-to-ship knowledge-work flow: grill decisions one question at a time, model the domain, research or prototype unkno... |
| `model-evaluation-lab` | Run reproducible model evaluations: freeze an evaluation plan (decision, baseline, candidates, cases, metrics, budget, stopping rules), e... |
| `model-prompt-lab` | Design, build, migrate, and diagnose production LLM system prompts for GPT-5.x, Claude Fable 5 / Mythos 5, and GPT-6 Astra; design reprod... |
| `operating-graph` | Run bounded, auditable multi-step agent workflows as an explicit operating graph — design typed node/edge topologies, execute with subage... |
| `outcome-engine` | Turn a fuzzy idea into a verified result: clarify with a decision grill, write an outcome brief, slice it into verifiable work packages,... |
| `practice-compiler` | Mine a bounded window of my own work sessions (or selected Codex/Claude Code session roots) for repeated tasks, recurring corrections, fo... |
| `proofloop` | Run an explicitly requested task through ProofLoop's bounded execution-and-verification protocol (task contract, fixed budgets, evidence-... |
| `signal-to-system` | Turn knowledge, evidence, and repeated work into useful outcomes across ten workflows: rank messy ideas (curiosity-compass), scan current... |
| `skill-eval-loop` | Run an evidence-backed eval loop on a workspace skill: build trigger suites (ten positive, ten near-miss negatives), functional checks, a... |
| `strategy-room` | Pressure-test a consequential decision before resources are committed. Use when the user says "grill me", "interview me relentlessly", "p... |
| `video-production-studio` | Coordinate brief-to-video production: route the request, plan, build, and QC the delivery. Use when the user wants a video made — explain... |
| `web-product-studio` | Design and build web products end to end: route the request (greenfield build, redesign, image-first implementation, targeted fix, QA), d... |
| `writing-quality` | Write in the user's voice, or review and tighten prose. Use when the user asks to write something that sounds like them, calibrate their... |

## Layout

```
skills/<name>/
  SKILL.md        # the skill: purpose, workflow, operating rules
  bin/            # helper scripts (Python, stdlib-only)
  scripts/        # helper scripts (some skills)
  references/     # supporting docs, loaded on demand
  assets/         # templates
  agents/         # subagent briefs (some skills)
```

## Install

Copy any `skills/<name>/` directory into your Muse workspace at `~/workspace/skills/<name>/`.

## License

MIT — see [LICENSE](LICENSE). Adapted from the MIT-licensed plugins at https://github.com/Israelmusondaayliffe/plugins.
