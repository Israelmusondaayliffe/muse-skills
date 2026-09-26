# muse-skills

Muse-native skills adapted from the [community agent plugins](https://github.com/Israelmusondaayliffe/plugins) marketplace.

The plugins repository ships reusable capabilities for Codex, Claude Code, and Claude Cowork. This repository is its Muse equivalent: each plugin ported into a workspace skill for Muse (Meta's personal AI assistant, running on Hatch).

## How these skills work

Each skill provides a concrete route from a request to a finished result: required inputs, approach choices, useful examples, execution steps, recovery, and evidence of completion. Read the entrypoint first and load its linked references when the task calls for them. A clear request with settled decisions should lead to work, without restarting an interview.

These are skill packages, not Codex or Claude plugins. Host-specific hooks and agent configurations become explicit procedures. Muse must check its available tools before using a browser, scheduler, renderer, connector, or subagent. A host name does not prove a capability or an isolated reviewer. Scripts check mechanical conditions; they cannot certify output quality or user approval.

Personal voice and runtime state belong outside replaceable package folders. Upgrades preserve legacy state and local edits. The collection does not include private host configuration or the user's local skills.

## Skills

| Skill | What it does |
|---|---|
| `agent-ops` | Choose and build an agent workflow with clear roles, tool contracts and bounded tests. |
| `ai-film-studio` | Develop approved film records and shot packets; supervise continuity and iterations. |
| `brand-studio` | Build brand strategy, briefs and identity systems; review artifacts against the brief. |
| `capability-operator` | Inspect available capabilities and route work to the appropriate skill. |
| `citizen-forge` | Turn an internal-tool brief into a governed application with explicit release checks. |
| `continuity-vault` | Create usable handoffs, extract durable knowledge and preserve source authority. |
| `data-storytelling-studio` | Turn checked analysis into accurate charts and decision-facing readouts. |
| `founder-revenue-engine` | Develop evidence-backed customer hypotheses and bounded outreach drafts. |
| `gauntlet` | Run an explicitly requested, capped builder and blind-critic improvement loop. |
| `gauntlet-loop` | Run explicitly selected compiled workstreams with execution and acceptance controls. |
| `guide-production-studio` | Produce complete source-grounded guides with usable, verified examples. |
| `harness-engineering` | Audit, build and verify an approved assistant setup with recoverable changes. |
| `image-prompting-studio` | Deliver copyable image prompts and coherent sets that preserve reference constraints. |
| `knowledge-work-superpowers` | Execute substantial research and writing through to a supported deliverable. |
| `last30days` | Research recent signals and report coverage, dates and meaningful changes. |
| `loop-observatory` | Compare recorded loop outcomes without inventing missing telemetry. |
| `loopkit` | Run bounded, resumable work under a concrete contract and stop conditions. |
| `matt-partok-bundled-plugin-for-knowledge-work` | Use the explicitly selected Matt workflow for idea-to-delivery knowledge work. |
| `model-evaluation-lab` | Freeze evaluation cases and compare actual model results against stated criteria. |
| `model-prompt-lab` | Build or migrate model prompts with verified settings and measured evaluation. |
| `operating-graph` | Execute explicitly requested typed workflow graphs with bounded state transitions. |
| `outcome-engine` | Turn an objective into bounded work packages and a verified result. |
| `practice-compiler` | Inspect an authorized session window and stage redacted improvement proposals. |
| `proofloop` | Execute an explicitly requested bounded task with evidence-based verification. |
| `signal-to-system` | Convert selected ideas, evidence or repeated work into a useful artifact. |
| `skill-eval-loop` | Record real skill evaluations, compare candidates and stage approved repairs. |
| `strategy-room` | Resolve consequential decisions while skipping questions already settled. |
| `video-production-studio` | Build and inspect a requested video, distinguishing plans and partial renders. |
| `web-product-studio` | Build or repair web products and verify the requested rendered flows. |
| `writing-quality` | Write or revise complete prose while preserving supported claims and protected text. |

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

## Install and update

Use Python 3.10 or later for the collection tools. Read the selected skill's requirements as well; video rendering, browser work and other runtime capabilities are checked separately.

For a first installation, copy a selected `skills/<name>/` folder only when the destination does not exist. For an update, never copy over the installed tree or use a blanket delete/sync. Stage an exact reviewed revision outside `~/workspace/skills/`, then use [the scoped installer](tools/muse_install.py) and its [30-skill policy](tools/install-policy.json). It preserves unlisted local files and skills, the private voice profile, and legacy state.

The example commands below run from the staged repository. Substitute absolute paths and the actual installed baseline commit. Keep manifests and backups outside replaceable packages. Generating a manifest is not approval; review that exact manifest and diff before applying.

```sh
python3 tools/muse_install.py manifest --git-ref <installed-baseline-commit> > /absolute/baseline.json
python3 tools/muse_install.py manifest --tree /absolute/staged/skills > /absolute/reviewed-release.json
python3 tools/muse_install.py plan --staged /absolute/staged/skills --installed /absolute/installed/skills --baseline /absolute/baseline.json --staged-manifest /absolute/reviewed-release.json --only-skill writing-quality
```

The dry-run blocks local modifications, missing baseline files, unexpected files at new release paths, symlinks, and staged hash drift. Resolve conflicts explicitly; do not relabel locally modified files as a new baseline just to make the check pass. Retired package files are reported and left in place.

After the user approves the exact release and replacement, apply the same pilot selection:

```sh
python3 tools/muse_install.py apply --staged /absolute/staged/skills --installed /absolute/installed/skills --baseline /absolute/baseline.json --staged-manifest /absolute/reviewed-release.json --only-skill writing-quality --backup-dir /absolute/new-pilot-backup --approval-ref "recorded user approval"
```

Freeze the reviewed manifest once at review time and verify its pinned SHA-256 before each apply. Never regenerate it from an unreviewed tree merely to clear a mismatch.

The approval reference records authority already given; it does not create authority. Apply requires the reviewed manifest and binds every payload to its approved hash. It backs up changed files and journals recovery before writing. Do not modify source or destination concurrently. Replacing several files is not a single atomic transaction; interrupted work may need recovery.

Verify the pilot's installed hashes, actual catalog discovery, loaded source, and a representative task in a fresh Muse context. Catalog refresh behavior must be observed, not assumed. If that succeeds, plan and apply the remaining collection with a separate backup directory (omit `--only-skill` to include all 30; unchanged files are skipped). No update is complete until the required installed behavior passes.

For Writing Quality, `bin/voice_state.py status` locates the active voice profile. After approval, `migrate` copies a calibrated legacy profile outside the package and refuses conflicts. Never publish the profile. Practice Compiler and Skill Eval Loop document their state locations and migration separately. Preserve both old and new state during rollback.

```sh
python3 tools/muse_install.py rollback --manifest /absolute/new-pilot-backup/manifest.json
```

Rollback refuses to overwrite newer user edits. Stop on a conflict and reconcile it; never force a restore over new state. The backup journal restores package files only, not later user state changes.

## Check a candidate

```sh
python3 tools/validate_collection.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
```

These checks cover metadata, package references and selected helper regressions. They do not prove that Muse can discover the installed skills or produce a good result. Run representative work in Muse and inspect the actual deliverables before accepting a release.

## License

MIT. See [LICENSE](LICENSE). Adapted from the MIT-licensed plugins at https://github.com/Israelmusondaayliffe/plugins.
