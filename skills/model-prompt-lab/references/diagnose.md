# Diagnose a Prompt Failure

Diagnose the observed failure before adding instructions. The troubleshooter
checks for duplication first; additions come only after consolidation and removal
have failed.

## Procedure

1. **Restate the symptom** exactly as the user reported it.
2. **Classify it** (categories below), then identify the root cause in terms of
   the target model's actual behavior — not the folklore of older models.
3. **Run the duplication check** before anything else: repeated instructions,
   repeated approval language, stacked brevity nudges, XML blocks beyond five.
   Use `scripts/validate_prompt.py` on the prompt text.
4. **Consolidate or remove first;** add new instructions only if a measured gap
   remains.
5. **Specify a test scenario** with a concrete input that should now produce a
   different output, and a fallback diagnostic step if the fix fails.

## Failure categories

| Category | Signature | Usual fix |
|---|---|---|
| TOO_BRIEF | Required caveats or evidence missing in short answers | Must-include contract for short answers, or remove the stacked brevity nudges |
| APPROVAL_NOISE | Asks permission for safe, expected actions | Consolidate ask-first language into one compact autonomy policy |
| APPROVAL_GAP | Skips confirmation where the user wanted it | Name the specific confirmation-required actions; add ambiguity triggers |
| SCOPE_DRIFT | Refactors, tidies, gold-plates beyond the ask | Scope-restraint snippet (Fable 5) or equivalent boundary |
| OVERPLANNING | Re-derives facts, surveys options it will not pursue | Act-when-ready instruction; reduce effort if measured |
| EARLY_STOPPING | Text-only intent without the tool call; permission-asking mid-run | Checkpoint discipline; autonomous reminder for unattended pipelines; "continue" nudge |
| FABRICATED_PROGRESS | Status claims with no tool-result backing | Evidence-grounded progress instruction (non-optional on long runs) |
| UNREQUESTED_ACTIONS | Applies fixes when assessment was asked | Assessment-vs-action boundary |
| VERBOSITY | Option surveys, long essays, structured bloat | Lead-with-outcome instruction; selectivity over compression |
| RETRIEVAL_DRIFT | Over- or under-searching | Explicit retrieval budget |
| PTC_MISROUTE / PTC_ROUTING_VAGUE | Programmatic tool calling final answers empty or wrong stage | Task-specific `<tool_orchestration>`; test program_output and final message separately |
| CACHE_COST | Surprise cache bills | Review caching config; track cached_tokens and cache_write_tokens |
| PRO_MODE_MISUSE | "Think harder", candidate generation, invented pro slugs | Use `reasoning.mode: "pro"`, reserve for measured quality gains |
| SAFEGUARD_FRICTION | Blocks or mid-stream pauses on legitimate dual-use work | safety_identifier; state legitimate purpose; reframe, never evade |
| OVER_PROMPTING | Many XML blocks; prompt-shaped output | Measured subtraction: one group per eval cycle |
| HALLUCINATED_SPECIFICS | Invented slugs, prices, parameters | Source-check; mark unverified; deliver against evidence |
| REASONING_EXTRACTION_REFUSAL | stop_reason refusal on "show your thinking" lineage | Remove reasoning-echo instructions; use structured thinking blocks |

## Delivery format

```
### Diagnosis
- Symptom: [user's report]
- Category: [from the table]
- Root cause: [model behavior, not folklore]
- Duplication check: [run first — yes, and what was found]

### Fix Applied
- [Specific change, copy-pasteable; consolidation and removal first]

### Test Scenario
- [Concrete input that should now produce a different output]

### If This Doesn't Fix It
- [Next diagnostic step / alternative fix]
```
