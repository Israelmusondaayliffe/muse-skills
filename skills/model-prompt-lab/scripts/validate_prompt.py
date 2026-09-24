#!/usr/bin/env python3
"""
Validate a GPT-5.6 prompt against production requirements.

Usage:
    python validate_prompt.py <prompt_file>
    python validate_prompt.py --text "<prompt_text>"

Checks:
- XML tag balance (when XML is used)
- Lean Markdown structure for long prompts
- Over-prompting detection (count of XML blocks > 5 = warning)
- Repeated-instruction detection (state-once discipline, NEW for 5.6)
- Approval-repetition detection (repeated ask-first language, NEW for 5.6)
- Brevity-without-contract detection (NEW for 5.6)
- Model string correctness (gpt-5.6 family; warns on legacy strings)
- Reasoning effort validity (none/low/medium/high/xhigh/max)
- Pro mode anti-patterns ("think harder", candidate generation, pro slugs, NEW for 5.6)
- PTC routing checks (task-specific orchestration when PTC present, NEW for 5.6)
- reasoning.context validity (auto/all_turns/current_turn, NEW for 5.6)
- Deprecated parameter detection (prompt_cache_retention, NEW for 5.6)
- Retrieval budget presence for search-using prompts
- Creative drafting guardrail for drafting tasks
- Phase parameter presence for multi-step prompts
- Preamble pattern for tool-heavy tasks
- Personality/collaboration split heuristic
- Absolute-word density on judgment calls
"""

import sys
import re
import argparse


def check_xml_balance(text):
    """Check that all XML-style tags are properly opened and closed."""
    issues = []
    open_tags = re.findall(r'<(\w[\w_-]*)(?:\s[^>]*)?>(?!</)', text)
    close_tags = re.findall(r'</(\w[\w_-]*)>', text)
    self_closing = re.findall(r'<(\w[\w_-]*)\s*/>', text)

    open_counts = {}
    for tag in open_tags:
        if tag not in self_closing:
            open_counts[tag] = open_counts.get(tag, 0) + 1

    close_counts = {}
    for tag in close_tags:
        close_counts[tag] = close_counts.get(tag, 0) + 1

    for tag in set(list(open_counts.keys()) + list(close_counts.keys())):
        o = open_counts.get(tag, 0)
        c = close_counts.get(tag, 0)
        if o > c:
            issues.append(f"FAIL: Tag <{tag}> opened {o} time(s) but closed {c} time(s)")
        elif c > o:
            issues.append(f"FAIL: Tag </{tag}> closed {c} time(s) but opened {o} time(s)")

    return issues


def count_xml_blocks(text):
    """Count distinct top-level XML blocks (used for over-prompting detection)."""
    open_tags = re.findall(r'<(\w[\w_-]*)(?:\s[^>]*)?>(?!</)', text)
    return len(set(open_tags)), set(open_tags)


def check_over_prompting(text):
    """Detect over-prompting: too many XML blocks suggests scaffolding the model can choose itself."""
    issues = []
    count, blocks = count_xml_blocks(text)
    if count > 5:
        issues.append(
            f"WARN: Found {count} distinct XML blocks ({', '.join(sorted(blocks))}). "
            f"GPT-5.6 prefers lean prompts. Consider whether each block is an invariant "
            f"or compensating for an older model's weakness. Run the measured subtraction "
            f"pass: remove one group at a time, rerun the same evals."
        )
    return issues


def check_repeated_instructions(text):
    """Detect duplicated instruction lines (state-once discipline). NEW for 5.6."""
    issues = []
    lines = [
        re.sub(r'^[\-\*\d\.\)\s]+', '', ln.strip()).lower()
        for ln in text.splitlines()
    ]
    lines = [ln for ln in lines if len(ln) > 30 and not ln.startswith('#') and not ln.startswith('<')]
    seen = {}
    for ln in lines:
        seen[ln] = seen.get(ln, 0) + 1
    dupes = [ln for ln, n in seen.items() if n > 1]
    if dupes:
        preview = dupes[0][:70]
        issues.append(
            f"WARN: {len(dupes)} instruction line(s) appear more than once "
            f"(e.g., \"{preview}...\"). On GPT-5.6, repetition is a behavior bug, "
            f"not emphasis. State each instruction once."
        )
    return issues


def check_approval_repetition(text):
    """Detect repeated ask-first/approval language. NEW for 5.6."""
    issues = []
    patterns = [
        r'ask\s+(?:the\s+user\s+)?(?:for\s+permission|first|before)',
        r'confirm\s+before',
        r'do\s+not\s+mutate',
        r'wait\s+for\s+(?:approval|confirmation|permission)',
        r'get\s+(?:explicit\s+)?(?:approval|permission|confirmation)',
        r'require\s+confirmation',
        r'ask\s+permission',
    ]
    total = 0
    for p in patterns:
        total += len(re.findall(p, text, re.IGNORECASE))
    if total > 3:
        issues.append(
            f"WARN: Found {total} approval-style instructions (ask first / confirm before / "
            f"wait for approval / require confirmation). Repeating these on GPT-5.6 causes "
            f"unnecessary approval requests for safe, expected actions. Consolidate into ONE "
            f"compact autonomy policy that names safe local actions and confirmation-required "
            f"actions. See autonomy-and-response-style.md."
        )
    return issues


def check_brevity_without_contract(text):
    """Detect broad brevity instructions without a must-include contract. NEW for 5.6."""
    issues = []
    text_lower = text.lower()
    brevity_signals = [
        "be concise", "keep it short", "keep it brief", "be brief",
        "keep responses short", "answer briefly", "short answers only",
    ]
    has_brevity = any(s in text_lower for s in brevity_signals)
    contract_signals = [
        "must include", "must still include", "lead with the conclusion",
        "keep all required", "preserve", "include the evidence", "material caveat",
    ]
    has_contract = any(s in text_lower for s in contract_signals)
    if has_brevity and not has_contract:
        issues.append(
            "WARN: Broad brevity instruction found without a must-include contract. "
            "GPT-5.6 is more concise by default than 5.5; 'be concise' style instructions "
            "can make responses too brief and drop required caveats or evidence. Either "
            "remove the instruction and re-test, or specify what a short answer must "
            "include. See autonomy-and-response-style.md."
        )
    return issues


def check_model_string(text):
    """Check for correct model string usage."""
    issues = []
    text_lower = text.lower()
    legacy = [
        "gpt-5.5", "gpt-5-5",
        "gpt-5.4", "gpt-5-4",
        "gpt-5.3", "gpt-5-3",
        "gpt-5.2", "gpt-5-2",
        "gpt-5.1", "gpt-5-1",
        "gpt-4.1", "gpt-4o",
        "o3-", "o4-mini",
    ]
    for dep in legacy:
        if dep in text_lower:
            issues.append(
                f"WARN: Found older model string '{dep}'. Confirm whether this is "
                f"intentional (migration source, comparison) or should be a gpt-5.6 "
                f"family string."
            )

    valid_56 = ["gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.6", "gpt-5-6"]
    if not any(v in text_lower for v in valid_56):
        issues.append("WARN: No GPT-5.6 model string found. Confirm this is a 5.6 prompt.")

    fabricated = re.findall(r'gpt-5\.6-(\w+)', text_lower)
    for suffix in set(fabricated):
        if suffix not in ("sol", "terra", "luna"):
            issues.append(
                f"FAIL: 'gpt-5.6-{suffix}' is not a documented variant. Valid strings: "
                f"gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna, or the gpt-5.6 alias. "
                f"Pro mode is reasoning.mode='pro', not a model slug."
            )
    return issues


def check_reasoning_effort(text):
    """Check reasoning effort configuration."""
    issues = []
    effort_match = re.search(r'effort["\']?\s*[:=]\s*["\'](\w+)["\']', text, re.IGNORECASE)
    if effort_match:
        effort = effort_match.group(1).lower()
        valid = ["none", "low", "medium", "high", "xhigh", "max"]
        if effort not in valid:
            issues.append(f"FAIL: Invalid reasoning effort '{effort}'. Valid: {valid}")
        elif effort in ("high", "xhigh", "max"):
            issues.append(
                f"INFO: Reasoning effort set to '{effort}'. For 5.6, preserve your current "
                f"setting as the baseline, then compare one level lower on representative "
                f"tasks. If migrating from xhigh, compare xhigh and max."
            )
    return issues


def check_pro_mode(text):
    """Check pro-mode configuration and anti-patterns. NEW for 5.6."""
    issues = []
    text_lower = text.lower()
    has_pro = bool(re.search(r'mode["\']?\s*[:=]\s*["\']pro["\']', text, re.IGNORECASE)) or "pro mode" in text_lower

    anti_patterns = ["think harder", "think more deeply", "use pro mode",
                     "generate several candidate", "generate multiple candidate",
                     "multiple candidate answers", "pick the best answer"]
    found_anti = [p for p in anti_patterns if p in text_lower]
    if has_pro and found_anti:
        issues.append(
            f"WARN: Pro-mode prompt contains mode-coaching language ({', '.join(found_anti)}). "
            f"Pro mode does the extra work itself; keep the same outcome-focused prompt as "
            f"standard mode. Remove these instructions."
        )

    if re.search(r'gpt-5\.6[\w\-]*pro', text_lower):
        issues.append(
            "FAIL: Found a pro model slug. There is no separate Pro model. Use "
            "reasoning.mode='pro' on gpt-5.6-sol/-terra/-luna."
        )
    return issues


def check_ptc_routing(text):
    """Check PTC prompts for task-specific routing. NEW for 5.6."""
    issues = []
    text_lower = text.lower()
    has_ptc = "programmatic_tool_calling" in text_lower or "programmatic tool calling" in text_lower
    if not has_ptc:
        return issues

    if "tool_orchestration" not in text_lower:
        issues.append(
            "WARN: Programmatic Tool Calling present without a <tool_orchestration> block. "
            "Generic instructions do not produce correct routing. State the bounded stage, "
            "eligible tools, output schema, limits, and which work stays direct. See "
            "programmatic-tool-calling.md."
        )
    else:
        if re.search(r'\[(?:bounded stage|eligible tools|output schema|condition)\]', text):
            issues.append(
                "FAIL: <tool_orchestration> block contains unfilled template brackets. "
                "Fill every bracket with the task's specifics."
            )
    if "allowed_callers" not in text_lower:
        issues.append(
            "INFO: PTC present without an allowed_callers mention. Confirm eligible tools "
            "are opted in and side-effecting tools stay direct-only."
        )
    generic = ["use programmatic tool calling efficiently", "use ptc efficiently",
               "use tools efficiently"]
    if any(g in text_lower for g in generic):
        issues.append(
            "WARN: Generic efficiency instruction found. Replace with task-specific routing."
        )
    return issues


def check_reasoning_context(text):
    """Validate reasoning.context values. NEW for 5.6."""
    issues = []
    m = re.search(r'context["\']?\s*[:=]\s*["\'](\w+)["\']', text, re.IGNORECASE)
    if m:
        val = m.group(1).lower()
        if val not in ("auto", "all_turns", "current_turn"):
            issues.append(
                f"FAIL: Invalid reasoning.context '{val}'. Valid: auto, all_turns, current_turn."
            )
    return issues


def check_deprecated_params(text):
    """Check for deprecated API parameters and legacy block names."""
    issues = []
    if "prompt_cache_retention" in text:
        issues.append(
            "FAIL: 'prompt_cache_retention' is deprecated on GPT-5.6. Replace with "
            "prompt_cache_options.ttl."
        )
    deprecated_blocks = {
        "default_follow_through_policy": "Replace with one compact autonomy policy (# Autonomy or <autonomy_policy>).",
        "personality_and_writing_controls": "Split into # Personality, # Collaboration style, # Autonomy, # Output.",
        "output_verbosity_spec": "Replace with # Output section, text.verbosity, and a must-include contract.",
        "dig_deeper_nudge": "Usually over-prompting on 5.6. Tighten # Success criteria instead.",
        "solution_persistence": "Replace with a high-initiative # Collaboration style bullet, only if evals demand it.",
    }
    for pattern, note in deprecated_blocks.items():
        if pattern in text:
            issues.append(f"INFO: Found '{pattern}'. {note}")
    return issues


def check_lean_structure(text):
    """Check for lean Markdown sections in long prompt bodies."""
    issues = []
    if len(text) < 400:
        return issues
    sections = ["# Goal", "# Success criteria", "# Constraints", "# Autonomy", "# Output", "# Stop rules"]
    found = [s for s in sections if s in text]
    if len(found) == 0 and len(text) > 600:
        issues.append(
            "INFO: No lean Markdown sections found (Goal, Success criteria, Constraints, "
            "Autonomy, Output, Stop rules). The 5.6 default prompt structure uses Markdown "
            "headers. Consider whether the body would be clearer with that scaffold."
        )
    return issues


def check_absolutes_on_judgment(text):
    """Detect aggressive ALWAYS/NEVER usage on what may be judgment calls."""
    issues = []
    always_count = len(re.findall(r'\bALWAYS\b', text))
    never_count = len(re.findall(r'\bNEVER\b', text))
    if always_count + never_count > 4:
        issues.append(
            f"INFO: Found {always_count} 'ALWAYS' and {never_count} 'NEVER' instructions. "
            f"GPT-5.6 prefers decision rules ('prefer', 'default to', 'when X, do Y') for "
            f"judgment calls. Reserve absolutes for true invariants."
        )
    return issues


def check_recommended_blocks(text):
    """Check for recommended patterns based on detected task type."""
    issues = []
    text_lower = text.lower()

    # Search/research prompts: retrieval budget check
    if any(w in text_lower for w in ["search", "browse", "web", "research"]):
        retrieval_signals = ["retrieval budget", "retrieval_budget", "stopping rule", "enough evidence", "make another retrieval call"]
        if not any(s in text_lower for s in retrieval_signals):
            issues.append(
                "WARN: Search-using prompt without an explicit retrieval budget. "
                "Define when enough evidence is enough to prevent search loops. "
                "See research-and-citations.md."
            )
        if "citation_rules" not in text and "cite" not in text_lower:
            issues.append("INFO: Research prompt without explicit citation handling. Citations may drift.")

    # Drafting tasks: creative guardrail check
    drafting_signals = ["slide", "blurb", "talk track", "outbound", "leadership", "newsletter", "draft", "summary for sharing"]
    if any(s in text_lower for s in drafting_signals):
        guardrail_signals = ["creative", "source-backed", "do not invent", "placeholder", "labeled assumption"]
        if not any(s in text_lower for s in guardrail_signals):
            issues.append(
                "WARN: Drafting prompt without a creative drafting guardrail. "
                "Distinguish source-backed facts from creative wording. "
                "See research-and-citations.md."
            )

    # Extraction prompts
    if any(w in text_lower for w in ["extract", "json schema", "parse"]):
        if "structured_output_contract" not in text and "extraction_spec" not in text and "schema" not in text_lower:
            issues.append("INFO: Extraction prompt without explicit structured output specification.")

    # High-impact actions
    if any(w in text_lower for w in ["refund", "cancel", "delete", "deploy", "production change"]):
        confirmation_signals = ["confirmation", "verification_loop", "action_safety", "autonomy"]
        if not any(s in text_lower for s in confirmation_signals):
            issues.append(
                "WARN: High-impact action prompt without a confirmation clause. Add an "
                "autonomy policy requiring confirmation for destructive actions (stated once)."
            )

    # Batch/list prompts
    if any(w in text_lower for w in ["batch", "all items", "paginated", "every record"]):
        if "completeness_contract" not in text and "# Success criteria" not in text:
            issues.append(
                "INFO: Batch/list prompt without completeness handling. Try coverage "
                "requirements in # Success criteria first."
            )

    # Agent prompts without an autonomy policy
    agent_signals = ["agent", "tool", "workflow", "multi-step"]
    action_signals = ["edit", "write", "send", "post", "execute", "run ", "change", "fix"]
    if any(w in text_lower for w in agent_signals) and any(w in text_lower for w in action_signals):
        if "# autonomy" not in text_lower and "autonomy_policy" not in text_lower and "without asking" not in text_lower:
            issues.append(
                "INFO: Action-taking agent prompt without an autonomy policy. GPT-5.6 is "
                "proactive on multi-step tasks; define what each request type authorizes. "
                "See autonomy-and-response-style.md."
            )

    return issues


def check_phase_parameter(text):
    """Check for phase parameter awareness in multi-step prompts."""
    issues = []
    text_lower = text.lower()
    is_multistep = any(w in text_lower for w in [
        "multi-step", "multi_step", "tool call", "agent", "workflow",
        "preamble", "commentary", "long-running"
    ])
    if is_multistep and "phase" not in text_lower:
        issues.append(
            "INFO: Multi-step prompt without phase parameter mention. Phase handling is "
            "preserved from 5.4/5.5 and prevents preamble-as-final-answer issues."
        )
    return issues


def check_preamble_pattern(text):
    """Check for preamble pattern in tool-heavy prompts."""
    issues = []
    text_lower = text.lower()
    tool_heavy = sum(1 for w in ["tool", "search", "fetch", "function call"] if w in text_lower) >= 2
    streaming_signals = ["streaming", "first token", "user-visible update", "progress"]
    has_preamble = any(s in text_lower for s in ["preamble", "before any tool calls", "intermediary update"])
    if tool_heavy and not has_preamble and not any(s in text_lower for s in streaming_signals):
        issues.append(
            "INFO: Tool-heavy prompt without preamble pattern. If users see streaming output, "
            "a short preamble improves perceived time-to-first-token. See api-parameters.md."
        )
    return issues


def check_personality_split(text):
    """Detect combined personality+collaboration block."""
    issues = []
    has_personality = "# Personality" in text or "<personality" in text
    has_collaboration = (
        "# Collaboration" in text
        or "collaboration style" in text.lower()
        or "collaboration_style" in text.lower()
    )
    if has_personality and not has_collaboration:
        section = re.search(r'#\s*Personality(.*?)(?=\n#\s|\Z)', text, re.DOTALL)
        if section:
            s = section.group(1).lower()
            task_signals = ["ask for clarification", "make assumption", "check work", "iterate", "tool", "verify"]
            if sum(1 for t in task_signals if t in s) >= 2:
                issues.append(
                    "INFO: Personality block appears to mix tone with task behavior. "
                    "Split into # Personality (how it sounds) and # Collaboration style "
                    "(how it works). See personality-and-collaboration.md."
                )
    return issues


def validate_prompt(text):
    """Run all validation checks."""
    all_issues = []
    all_issues.extend(check_xml_balance(text))
    all_issues.extend(check_over_prompting(text))
    all_issues.extend(check_repeated_instructions(text))
    all_issues.extend(check_approval_repetition(text))
    all_issues.extend(check_brevity_without_contract(text))
    all_issues.extend(check_model_string(text))
    all_issues.extend(check_reasoning_effort(text))
    all_issues.extend(check_pro_mode(text))
    all_issues.extend(check_ptc_routing(text))
    all_issues.extend(check_reasoning_context(text))
    all_issues.extend(check_deprecated_params(text))
    all_issues.extend(check_lean_structure(text))
    all_issues.extend(check_absolutes_on_judgment(text))
    all_issues.extend(check_recommended_blocks(text))
    all_issues.extend(check_phase_parameter(text))
    all_issues.extend(check_preamble_pattern(text))
    all_issues.extend(check_personality_split(text))

    fails = [i for i in all_issues if i.startswith("FAIL")]
    warns = [i for i in all_issues if i.startswith("WARN")]
    infos = [i for i in all_issues if i.startswith("INFO")]

    return {
        "passed": len(fails) == 0,
        "fails": fails,
        "warnings": warns,
        "info": infos,
        "total_issues": len(all_issues),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate GPT-5.6 prompt")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="Path to prompt file")
    group.add_argument("--text", help="Prompt text directly")
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        with open(args.file, "r") as f:
            text = f.read()

    result = validate_prompt(text)

    print(f"\n{'=' * 50}")
    print("GPT-5.6 Prompt Validation")
    print(f"{'=' * 50}")
    print(f"Status: {'PASS' if result['passed'] else 'FAIL'}")
    print(f"Issues: {result['total_issues']}")

    if result["fails"]:
        print(f"\nFAILURES ({len(result['fails'])}):")
        for f in result["fails"]:
            print(f"  {f}")

    if result["warnings"]:
        print(f"\nWARNINGS ({len(result['warnings'])}):")
        for w in result["warnings"]:
            print(f"  {w}")

    if result["info"]:
        print(f"\nINFO ({len(result['info'])}):")
        for i in result["info"]:
            print(f"  {i}")

    if not result["fails"] and not result["warnings"]:
        print("\nAll checks passed.")

    print(f"{'=' * 50}\n")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
