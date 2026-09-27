# NOTICE

## Attribution

This skill repackages and consolidates selected skills by Matt Pocock,
originally published under the MIT License.

- Upstream: https://github.com/mattpocock/skills
- Pinned commit: c55ee46073ed923f86ce59a5eb3b6d895095d1b7

Portions of this skill are derived from that upstream work, verbatim or in
condensed form, and remain under the upstream MIT License.

## Ported upstream paths

references/ (verbatim; format files de-dashed):

- engineering/domain-modeling/CONTEXT-FORMAT.md -> references/domain-modeling-context-format.md
- engineering/domain-modeling/ADR-FORMAT.md -> references/domain-modeling-adr-format.md
- engineering/ask-matt/PHASE-BOUNDARIES.md -> references/ask-matt-phase-boundaries.md
- engineering/prototype/LOGIC.md -> references/prototype-logic.md
- engineering/prototype/UI.md -> references/prototype-ui.md
- engineering/improve-codebase-architecture/HTML-REPORT.md -> references/html-report-format.md
- productivity/teach/MISSION-FORMAT.md + productivity/teach/LEARNING-RECORD-FORMAT.md -> references/teach-formats.md (concatenated; minor appendices skipped)
- engineering/codebase-design/DEEPENING.md -> references/codebase-design-deepening.md
- engineering/codebase-design/DESIGN-IT-TWICE.md -> references/codebase-design-design-it-twice.md
- engineering/tdd/tests.md -> references/tdd-tests.md
- engineering/tdd/mocking.md -> references/tdd-mocking.md

bin/ (verbatim):

- engineering/wizard/template.sh -> bin/wizard-template.sh
- engineering/diagnosing-bugs/scripts/hitl-loop.template.sh -> bin/hitl-loop.template.sh (kept from the previous package, which ported it from upstream diagnosing-bugs scripts; the dropped usage/safety note about `capture` was restored in this revision)
- misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh -> bin/block-dangerous-git.sh
- in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs -> bin/dependency-cruiser.config.cjs

assets/ (verbatim setup seed templates):

- engineering/setup-matt-pocock-skills/domain.md -> assets/setup-seeds/domain.md
- engineering/setup-matt-pocock-skills/issue-tracker-github.md -> assets/setup-seeds/issue-tracker-github.md
- engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md -> assets/setup-seeds/issue-tracker-gitlab.md
- engineering/setup-matt-pocock-skills/issue-tracker-local.md -> assets/setup-seeds/issue-tracker-local.md
- engineering/setup-matt-pocock-skills/triage-labels.md -> assets/setup-seeds/triage-labels.md

assets/ (template extracts from upstream SKILL.md files):

- engineering/to-spec/SKILL.md (<spec-template>) -> assets/spec-template.md
- engineering/to-tickets/SKILL.md (<local-ticket-template> + <issue-template>) -> assets/issue-template.md
- productivity/to-questionnaire/SKILL.md (<questionnaire-template>) -> assets/questionnaire-template.md
- productivity/handoff/SKILL.md (summary structure) -> assets/handoff-template.md

## Consolidation mapping

Upstream skill names folded into this skill's named subagents:

- decision-mapping -> wayfinder
- diagnose -> diagnosing-bugs
- batch-grill-me -> grilling
- ubiquitous-language -> domain-modeling
- writing-great-skills -> writing-for-agents
