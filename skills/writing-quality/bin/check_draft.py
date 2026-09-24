#!/usr/bin/env python3
"""
Quality Validator V5

Objective quality scoring for content.
Checks AI tells, cliches, hedge language, em-dashes,
copula avoidance, -ing constructions, significance inflation,
sycophantic tone, curly quotes, negative parallelisms, rule of three,
generic positive conclusions, and modern structural slop.

Based on Wikipedia's WikiProject AI Cleanup taxonomy + V2 detection.

Usage:
    python3 bin/check_draft.py draft.txt
    python3 bin/check_draft.py draft.txt --verbose
    python3 bin/check_draft.py draft.txt --json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple


@dataclass
class Issue:
    """Represents a detected quality issue."""
    line: int
    text: str
    category: str
    severity: str  # 'high', 'medium', 'low'
    suggestion: str = ""


@dataclass
class ValidationResult:
    """Complete validation results."""
    emdash_count: int = 0
    emdash_issues: List[Issue] = field(default_factory=list)

    ai_tell_count: int = 0
    ai_tell_issues: List[Issue] = field(default_factory=list)

    cliche_count: int = 0
    cliche_issues: List[Issue] = field(default_factory=list)

    hedge_count: int = 0
    hedge_issues: List[Issue] = field(default_factory=list)

    # V3 additions
    copula_count: int = 0
    copula_issues: List[Issue] = field(default_factory=list)

    ing_count: int = 0
    ing_issues: List[Issue] = field(default_factory=list)

    significance_count: int = 0
    significance_issues: List[Issue] = field(default_factory=list)

    sycophancy_count: int = 0
    sycophancy_issues: List[Issue] = field(default_factory=list)

    curly_quote_count: int = 0
    curly_quote_issues: List[Issue] = field(default_factory=list)

    negative_parallelism_count: int = 0
    negative_parallelism_issues: List[Issue] = field(default_factory=list)

    rule_of_three_count: int = 0
    rule_of_three_issues: List[Issue] = field(default_factory=list)

    generic_conclusion_count: int = 0
    generic_conclusion_issues: List[Issue] = field(default_factory=list)

    structural_slop_count: int = 0
    structural_slop_issues: List[Issue] = field(default_factory=list)

    technical_score: float = 0.0

    def to_dict(self) -> dict:
        return {
            'emdash_count': self.emdash_count,
            'ai_tell_count': self.ai_tell_count,
            'cliche_count': self.cliche_count,
            'hedge_count': self.hedge_count,
            'copula_count': self.copula_count,
            'ing_count': self.ing_count,
            'significance_count': self.significance_count,
            'sycophancy_count': self.sycophancy_count,
            'curly_quote_count': self.curly_quote_count,
            'negative_parallelism_count': self.negative_parallelism_count,
            'rule_of_three_count': self.rule_of_three_count,
            'generic_conclusion_count': self.generic_conclusion_count,
            'structural_slop_count': self.structural_slop_count,
            'technical_score': self.technical_score,
            'issues': {
                'emdash': [{'line': i.line, 'text': i.text} for i in self.emdash_issues],
                'ai_tells': [{'line': i.line, 'text': i.text, 'suggestion': i.suggestion} for i in self.ai_tell_issues],
                'cliches': [{'line': i.line, 'text': i.text, 'suggestion': i.suggestion} for i in self.cliche_issues],
                'hedges': [{'line': i.line, 'text': i.text} for i in self.hedge_issues],
                'copula': [{'line': i.line, 'text': i.text, 'suggestion': i.suggestion} for i in self.copula_issues],
                'ing_constructions': [{'line': i.line, 'text': i.text} for i in self.ing_issues],
                'significance': [{'line': i.line, 'text': i.text} for i in self.significance_issues],
                'sycophancy': [{'line': i.line, 'text': i.text} for i in self.sycophancy_issues],
                'curly_quotes': [{'line': i.line, 'text': i.text} for i in self.curly_quote_issues],
                'negative_parallelisms': [{'line': i.line, 'text': i.text} for i in self.negative_parallelism_issues],
                'rule_of_three': [{'line': i.line, 'text': i.text} for i in self.rule_of_three_issues],
                'generic_conclusions': [{'line': i.line, 'text': i.text} for i in self.generic_conclusion_issues],
                'structural_slop': [
                    {
                        'line': i.line,
                        'text': i.text,
                        'severity': i.severity,
                        'suggestion': i.suggestion,
                    }
                    for i in self.structural_slop_issues
                ],
            }
        }


# === V2 DETECTION PATTERNS (unchanged) ===

HIGH_SEVERITY_AI_TELLS = {
    'delve': 'explore',
    'delving': 'exploring',
    'delved': 'explored',
    'leverage': 'use',
    'leveraging': 'using',
    'leveraged': 'used',
    'unlock': 'enable',
    'unlocking': 'enabling',
    'unlocked': 'enabled',
    'journey': 'process',
    'tapestry': '[remove or be specific]',
    'landscape': 'field',
    'realm': 'area',
    'testament': 'evidence',
    'beacon': '[remove or be specific]',
    'cornerstone': 'foundation',
    'myriad': 'many',
    'plethora': 'many',
    'nuanced': '[remove or be specific]',
    'holistic': '[explain specifically]',
    'pivotal': 'important',
    'groundbreaking': '[replace with evidence or remove]',
    'robust': '[describe the strength specifically]',
    'unparalleled': '[remove hyperbole]',
    'harness': 'use',
    'harnessing': 'using',
    'elevate': 'improve',
    'elevating': 'improving',
    # V3 additions from humanizer taxonomy
    'vibrant': '[be specific or remove]',
    'nestled': '[remove, state location directly]',
    'breathtaking': '[remove or be specific]',
    'stunning': '[remove or be specific]',
    'renowned': '[cite specific recognition]',
    'showcasing': '[remove -ing or rewrite]',
    'fostering': '[remove -ing or rewrite]',
    'garner': 'get',
    'garnered': 'got',
    'underscore': 'show',
    'underscoring': '[remove -ing or rewrite]',
    'interplay': 'relationship',
    'intricacies': 'details',
    'intricate': 'detailed',
    'enduring': 'lasting',
}

MEDIUM_SEVERITY_AI_TELLS = {
    'however': '[use "but" or restructure]',
    'moreover': '[remove or use "and"]',
    'furthermore': '[remove or use "also"]',
    'additionally': '[remove or use "also"]',
    'in conclusion': '[remove]',
    'to summarize': '[remove]',
    'firstly': 'first',
    'secondly': 'second',
    'thirdly': 'third',
}

MEDIUM_PHRASES = [
    "it's worth noting",
    "it's important to note",
    "it is worth noting",
    "it is important to note",
    "that being said",
    "at the end of the day",
    "when all is said and done",
    "in today's fast-paced world",
    "now more than ever",
    "the fact of the matter",
    "in terms of",
    "in order to",
]

BUSINESS_CLICHES = {
    'game-changer': '[be specific about impact]',
    'paradigm shift': '[describe the change]',
    'low-hanging fruit': '[name the easy wins]',
    'move the needle': '[quantify the impact]',
    'circle back': 'follow up',
    'touch base': 'connect',
    'synergy': '[explain the benefit]',
    'synergize': '[explain specifically]',
    'disruptive': '[explain how]',
    'best-in-class': '[provide evidence]',
    'world-class': '[provide evidence]',
    'cutting-edge': '[explain specifically]',
    'state-of-the-art': '[explain specifically]',
    'next-generation': '[explain specifically]',
    'value-add': 'benefit',
    'actionable insights': 'recommendations',
    'deep dive': 'analysis',
}

HEDGE_WORDS = [
    'perhaps',
    'maybe',
    'possibly',
    'probably',
    'might',
    'could be',
    'may be',
    'kind of',
    'sort of',
    'somewhat',
    'it depends',
    'on one hand',
    'on the other hand',
    'could potentially',
    'might possibly',
]


# === V3 DETECTION PATTERNS (new from humanizer taxonomy) ===

COPULA_AVOIDANCE = {
    'serves as': 'is',
    'stands as': 'is',
    'functions as': 'is',
    'acts as': 'is',
    'boasts a': 'has a',
    'boasts an': 'has an',
    'boasts the': 'has the',
    'features a': 'has a',
    'features an': 'has an',
    'features the': 'has the',
    'offers a': 'has a',
    'offers an': 'has an',
    'represents a': 'is a',
    'represents an': 'is an',
}

SIGNIFICANCE_PHRASES = [
    "marking a pivotal",
    "marking a significant",
    "marking a key",
    "marks a pivotal",
    "marks a significant",
    "marks a key",
    "setting the stage for",
    "a testament to",
    "is a testament",
    "reflects broader",
    "contributing to the",
    "indelible mark",
    "deeply rooted",
    "enduring legacy",
    "key turning point",
    "evolving landscape",
    "focal point of",
    "plays a crucial role",
    "plays a vital role",
    "plays a significant role",
    "plays a pivotal role",
    "plays a key role",
    "underscores the importance",
    "highlights the significance",
    "symbolizing its",
    "part of a broader",
]

SYCOPHANTIC_PHRASES = [
    "great question",
    "excellent question",
    "wonderful question",
    "you're absolutely right",
    "that's an excellent point",
    "that's a great point",
    "that's a fantastic",
    "i hope this helps",
    "let me know if you'd like",
    "let me know if you would like",
    "here is a comprehensive",
    "here is an overview",
    "of course!",
    "certainly!",
    "absolutely!",
    "would you like me to",
]

NEGATIVE_PARALLELISM_PHRASES = [
    "not only",
    "it's not just about",
    "it's not just a",
    "it's not merely",
    "more than just a",
    "more than just an",
    "it is not just",
    "it is not merely",
]

GENERIC_CONCLUSION_PHRASES = [
    "the future looks bright",
    "exciting times lie ahead",
    "exciting times ahead",
    "continue their journey",
    "step in the right direction",
    "poised to",
    "poised for growth",
    "poised for success",
    "looking ahead",
    "as we look to the future",
    "the possibilities are endless",
    "only time will tell",
]

STRUCTURAL_SLOP_PATTERNS = [
    (
        r"(?im)^\s*(?:here[’']s the thing|here[’']s what i mean|let me be clear|i[’']ll be honest|the uncomfortable truth is)\b",
        "throat-clearing opener",
        "medium",
        "Cut the setup and start with the claim unless the phrase carries real voice or context.",
    ),
    (
        r"(?i)\b(?:what most people get wrong|what nobody tells you|the part everyone misses|this is the part most people skip)\b",
        "faux-insight setup",
        "high",
        "Remove the exclusivity claim and state the supported point directly.",
    ),
    (
        r"(?im)^\s*(?:the best part|the key|the secret|the detail that makes it work):\s+[a-z]",
        "colon reveal",
        "medium",
        "Rewrite as a plain sentence. Keep colons for lists, labels, and quotations.",
    ),
    (
        r"(?i)(?:\bwhat if i told you\b|\bthink about it:|\bplot twist:)",
        "rhetorical setup",
        "medium",
        "Drop the setup and state the point.",
    ),
    (
        r"(?i)\b(?:that[’']s it\.\s+that[’']s the whole thing|not an? [^.!?]{1,50}\.\s+not an? [^.!?]{1,50}\.\s+an? [^.!?]{1,50}[.!?])",
        "dramatic fragmentation",
        "medium",
        "State the point in a complete sentence unless the fragments are a real voice marker.",
    ),
    (
        r"(?im)^\s*(?:in conclusion|ultimately|overall),",
        "summary-recap ending",
        "medium",
        "Cut the recap cue and end on a concrete point, decision, or next action.",
    ),
    (
        r"(?i)\b(?:the rest of this (?:essay|article|section)|in the next section|what follows will)\b",
        "meta joiner",
        "medium",
        "Delete the announcement and let the writing move to the next point.",
    ),
    (
        r"(?i)\b(?:the implications are significant|the reasons are structural|this is concerning|this matters)\b",
        "vague declarative",
        "medium",
        "Name the supported implication, reason, mechanism, or next action.",
    ),
    (
        r"(?i)\b(?:decision|strategy|framework|system|document|plan|analysis)\s+(?:believes|decides|discovers|wants|hopes)\b",
        "false agency",
        "medium",
        "Name the actual person or process when known.",
    ),
]


def find_pattern_in_text(text: str, pattern: str, case_insensitive: bool = True) -> List[Tuple[int, int]]:
    """Find all occurrences of pattern in text, return (start, end) positions."""
    flags = re.IGNORECASE if case_insensitive else 0
    if ' ' in pattern:
        regex = re.compile(re.escape(pattern), flags)
    else:
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', flags)
    return [(m.start(), m.end()) for m in regex.finditer(text)]


def get_line_number(text: str, position: int) -> int:
    """Get line number for a character position in text."""
    return text[:position].count('\n') + 1


def get_context(text: str, start: int, end: int, window: int = 20) -> str:
    """Get surrounding context for a match."""
    ctx_start = max(0, start - window)
    ctx_end = min(len(text), end + window)
    return text[ctx_start:ctx_end].replace('\n', ' ')


# === V2 CHECKS (unchanged logic) ===

def check_emdashes(text: str) -> List[Issue]:
    """Check for em-dashes."""
    issues = []
    for match in re.finditer(r'[—–]', text):
        line_num = get_line_number(text, match.start())
        context = get_context(text, match.start(), match.end())
        issues.append(Issue(
            line=line_num, text=context, category='emdash',
            severity='high', suggestion='Replace with period + capitalize OR comma'
        ))
    for match in re.finditer(r'(?<!\-)--(?!\-)', text):
        line_num = get_line_number(text, match.start())
        context = get_context(text, match.start(), match.end())
        issues.append(Issue(
            line=line_num, text=context, category='emdash',
            severity='high', suggestion='Replace with period + capitalize OR comma'
        ))
    return issues


def check_ai_tells(text: str) -> List[Issue]:
    """Check for AI tell words and phrases."""
    issues = []
    for word, suggestion in HIGH_SEVERITY_AI_TELLS.items():
        for start, end in find_pattern_in_text(text, word):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end, 15)
            issues.append(Issue(
                line=line_num, text=context, category='ai_tell',
                severity='high', suggestion=f'Replace "{word}" with "{suggestion}"'
            ))
    for word, suggestion in MEDIUM_SEVERITY_AI_TELLS.items():
        for start, end in find_pattern_in_text(text, word):
            before = text[:start].rstrip()
            if before and before[-1] in '.!?':
                line_num = get_line_number(text, start)
                context = get_context(text, start, end)
                issues.append(Issue(
                    line=line_num, text=context, category='ai_tell',
                    severity='medium', suggestion=suggestion
                ))
    for phrase in MEDIUM_PHRASES:
        for start, end in find_pattern_in_text(text, phrase):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end, 10)
            issues.append(Issue(
                line=line_num, text=context, category='ai_tell',
                severity='medium', suggestion='Remove or rephrase'
            ))
    return issues


def check_cliches(text: str) -> List[Issue]:
    """Check for business cliches."""
    issues = []
    for cliche, suggestion in BUSINESS_CLICHES.items():
        for start, end in find_pattern_in_text(text, cliche):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end, 15)
            issues.append(Issue(
                line=line_num, text=context, category='cliche',
                severity='medium', suggestion=f'Replace with "{suggestion}"'
            ))
    return issues


def check_hedges(text: str) -> List[Issue]:
    """Check for hedge language."""
    issues = []
    for hedge in HEDGE_WORDS:
        for start, end in find_pattern_in_text(text, hedge):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end)
            issues.append(Issue(
                line=line_num, text=context, category='hedge',
                severity='medium', suggestion='Remove or make decisive statement'
            ))
    return issues


# === V3 CHECKS (new from humanizer taxonomy) ===

def check_copula_avoidance(text: str) -> List[Issue]:
    """Check for copula avoidance patterns (serves as, stands as, boasts)."""
    issues = []
    for pattern, suggestion in COPULA_AVOIDANCE.items():
        for start, end in find_pattern_in_text(text, pattern):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end)
            issues.append(Issue(
                line=line_num, text=context, category='copula',
                severity='high', suggestion=f'Replace "{pattern}" with "{suggestion}"'
            ))
    return issues


def check_ing_constructions(text: str) -> List[Issue]:
    """Check for superficial -ing analysis phrases tacked onto sentences."""
    issues = []
    # Pattern: comma + space + -ing word at clause boundaries
    ing_verbs = [
        'highlighting', 'underscoring', 'emphasizing', 'ensuring',
        'reflecting', 'symbolizing', 'contributing', 'cultivating',
        'fostering', 'encompassing', 'showcasing', 'demonstrating',
        'illustrating', 'reinforcing', 'signaling', 'representing',
    ]
    for verb in ing_verbs:
        pattern = rf',\s+{verb}\b'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line_num = get_line_number(text, match.start())
            context = get_context(text, match.start(), match.end(), 30)
            issues.append(Issue(
                line=line_num, text=context, category='ing_construction',
                severity='high',
                suggestion=f'Remove ", {verb}..." clause or make it a separate sentence'
            ))
    return issues


def check_significance_inflation(text: str) -> List[Issue]:
    """Check for undue emphasis on significance, legacy, broader trends."""
    issues = []
    for phrase in SIGNIFICANCE_PHRASES:
        for start, end in find_pattern_in_text(text, phrase):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end, 25)
            issues.append(Issue(
                line=line_num, text=context, category='significance',
                severity='high',
                suggestion='Remove significance claim or replace with specific fact'
            ))
    return issues


def check_sycophancy(text: str) -> List[Issue]:
    """Check for sycophantic/servile tone and chatbot artifacts."""
    issues = []
    for phrase in SYCOPHANTIC_PHRASES:
        for start, end in find_pattern_in_text(text, phrase):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end)
            issues.append(Issue(
                line=line_num, text=context, category='sycophancy',
                severity='high',
                suggestion='Remove chatbot language from content'
            ))
    return issues


def check_curly_quotes(text: str) -> List[Issue]:
    """Check for curly quotation marks (ChatGPT artifact)."""
    issues = []
    for match in re.finditer(r'[\u201c\u201d\u2018\u2019]', text):
        line_num = get_line_number(text, match.start())
        context = get_context(text, match.start(), match.end())
        issues.append(Issue(
            line=line_num, text=context, category='curly_quote',
            severity='low',
            suggestion='Replace curly quote with straight quote'
        ))
    return issues


def check_negative_parallelisms(text: str) -> List[Issue]:
    """Check for overused negative parallelism structures."""
    issues = []
    for phrase in NEGATIVE_PARALLELISM_PHRASES:
        for start, end in find_pattern_in_text(text, phrase):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end, 30)
            issues.append(Issue(
                line=line_num, text=context, category='negative_parallelism',
                severity='medium',
                suggestion='State the point directly without rhetorical contrast'
            ))
    return issues


def check_rule_of_three(text: str) -> List[Issue]:
    """Check for forced triplet structures."""
    issues = []
    # Detect patterns like "X, Y, and Z" appearing multiple times in close proximity
    triplet_pattern = r'\b\w+,\s+\w+,\s+and\s+\w+'
    matches = list(re.finditer(triplet_pattern, text, re.IGNORECASE))

    # Only flag if multiple triplets in same paragraph or within 200 chars
    if len(matches) >= 2:
        for i in range(len(matches) - 1):
            if matches[i + 1].start() - matches[i].end() < 200:
                line_num = get_line_number(text, matches[i].start())
                context = get_context(text, matches[i].start(), matches[i].end(), 10)
                issues.append(Issue(
                    line=line_num, text=context, category='rule_of_three',
                    severity='medium',
                    suggestion='Multiple triplet structures nearby. Use natural grouping sizes.'
                ))
                break  # flag once per cluster
    return issues


def check_generic_conclusions(text: str) -> List[Issue]:
    """Check for vague positive conclusion language."""
    issues = []
    for phrase in GENERIC_CONCLUSION_PHRASES:
        for start, end in find_pattern_in_text(text, phrase):
            line_num = get_line_number(text, start)
            context = get_context(text, start, end, 25)
            issues.append(Issue(
                line=line_num, text=context, category='generic_conclusion',
                severity='high',
                suggestion='Replace with specific fact or delete'
            ))
    return issues


def check_structural_slop(text: str) -> List[Issue]:
    """Check explicit structural patterns added in the no-ai-slop parity review."""
    issues = []
    for pattern, name, severity, suggestion in STRUCTURAL_SLOP_PATTERNS:
        for match in re.finditer(pattern, text):
            line_num = get_line_number(text, match.start())
            context = get_context(text, match.start(), match.end(), 30)
            issues.append(Issue(
                line=line_num,
                text=context,
                category="structural_slop",
                severity=severity,
                suggestion=f"{name}: {suggestion}",
            ))
    return issues


# === SCORING ===

def calculate_technical_score(result: ValidationResult) -> float:
    """
    Calculate technical score 0-10.

    V5 scoring (expanded from V4):
    - Em-dash elimination: 1.5 points (1.5=zero, 0.75=1-2, 0=3+)
    - AI-tell elimination: 2 points (2=zero, 1.5=1-2, 0.5=3-5, 0=6+)
    - Cliche elimination: 1 point (1=zero, 0.5=1-2, 0=3+)
    - Hedge elimination: 1 point (1=zero, 0.5=1-2, 0=3+)
    - Copula avoidance: 1 point (1=zero, 0.5=1-2, 0=3+)
    - -ing constructions: 1 point (1=zero, 0.5=1-2, 0=3+)
    - Significance inflation: 1 point (1=zero, 0.5=1-2, 0=3+)
    - Sycophancy/chatbot artifacts: 0.5 points (0.5=zero, 0=any)
    - Base: 1 point
    - Structural slop: subtract 0.5 per issue, up to 2 points
    """
    score = 1.0

    # Em-dash scoring
    if result.emdash_count == 0:
        score += 1.5
    elif result.emdash_count <= 2:
        score += 0.75

    # AI-tell scoring (high severity)
    high_ai_tells = len([i for i in result.ai_tell_issues if i.severity == 'high'])
    if high_ai_tells == 0:
        score += 2.0
    elif high_ai_tells <= 2:
        score += 1.5
    elif high_ai_tells <= 5:
        score += 0.5

    # Cliche scoring
    if result.cliche_count == 0:
        score += 1.0
    elif result.cliche_count <= 2:
        score += 0.5

    # Hedge scoring
    if result.hedge_count == 0:
        score += 1.0
    elif result.hedge_count <= 2:
        score += 0.5

    # V3: Copula avoidance scoring
    if result.copula_count == 0:
        score += 1.0
    elif result.copula_count <= 2:
        score += 0.5

    # V3: -ing construction scoring
    if result.ing_count == 0:
        score += 1.0
    elif result.ing_count <= 2:
        score += 0.5

    # V3: Significance inflation scoring
    if result.significance_count == 0:
        score += 1.0
    elif result.significance_count <= 2:
        score += 0.5

    # V3: Sycophancy scoring
    if result.sycophancy_count == 0:
        score += 0.5

    score -= min(2.0, result.structural_slop_count * 0.5)
    return max(0.0, min(10.0, score))


def validate_content(text: str) -> ValidationResult:
    """Run full validation on content."""
    result = ValidationResult()

    # V2 checks
    result.emdash_issues = check_emdashes(text)
    result.emdash_count = len(result.emdash_issues)

    result.ai_tell_issues = check_ai_tells(text)
    result.ai_tell_count = len(result.ai_tell_issues)

    result.cliche_issues = check_cliches(text)
    result.cliche_count = len(result.cliche_issues)

    result.hedge_issues = check_hedges(text)
    result.hedge_count = len(result.hedge_issues)

    # V3 checks
    result.copula_issues = check_copula_avoidance(text)
    result.copula_count = len(result.copula_issues)

    result.ing_issues = check_ing_constructions(text)
    result.ing_count = len(result.ing_issues)

    result.significance_issues = check_significance_inflation(text)
    result.significance_count = len(result.significance_issues)

    result.sycophancy_issues = check_sycophancy(text)
    result.sycophancy_count = len(result.sycophancy_issues)

    result.curly_quote_issues = check_curly_quotes(text)
    result.curly_quote_count = len(result.curly_quote_issues)

    result.negative_parallelism_issues = check_negative_parallelisms(text)
    result.negative_parallelism_count = len(result.negative_parallelism_issues)

    result.rule_of_three_issues = check_rule_of_three(text)
    result.rule_of_three_count = len(result.rule_of_three_issues)

    result.generic_conclusion_issues = check_generic_conclusions(text)
    result.generic_conclusion_count = len(result.generic_conclusion_issues)

    result.structural_slop_issues = check_structural_slop(text)
    result.structural_slop_count = len(result.structural_slop_issues)

    # Calculate technical score
    result.technical_score = calculate_technical_score(result)

    return result


def format_report(result: ValidationResult, verbose: bool = False) -> str:
    """Format validation results as readable report."""
    lines = [
        "QUALITY VALIDATION REPORT (V5)",
        "=" * 50,
        "",
        f"Technical Score: {result.technical_score:.1f}/10",
        "",
        "COMPONENT SCORES:",
        f"  Em-dashes:              {result.emdash_count} found {'✓' if result.emdash_count == 0 else '✗'}",
        f"  AI tells:               {result.ai_tell_count} found {'✓' if result.ai_tell_count == 0 else '⚠' if result.ai_tell_count <= 2 else '✗'}",
        f"  Cliches:                {result.cliche_count} found {'✓' if result.cliche_count == 0 else '⚠' if result.cliche_count <= 2 else '✗'}",
        f"  Hedges:                 {result.hedge_count} found {'✓' if result.hedge_count == 0 else '⚠' if result.hedge_count <= 2 else '✗'}",
        f"  Copula avoidance:       {result.copula_count} found {'✓' if result.copula_count == 0 else '⚠' if result.copula_count <= 2 else '✗'}",
        f"  -ing constructions:     {result.ing_count} found {'✓' if result.ing_count == 0 else '⚠' if result.ing_count <= 2 else '✗'}",
        f"  Significance inflation: {result.significance_count} found {'✓' if result.significance_count == 0 else '⚠' if result.significance_count <= 2 else '✗'}",
        f"  Sycophancy/chatbot:     {result.sycophancy_count} found {'✓' if result.sycophancy_count == 0 else '✗'}",
        f"  Curly quotes:           {result.curly_quote_count} found {'✓' if result.curly_quote_count == 0 else '⚠'}",
        f"  Negative parallelisms:  {result.negative_parallelism_count} found {'✓' if result.negative_parallelism_count == 0 else '⚠'}",
        f"  Rule of three:          {result.rule_of_three_count} found {'✓' if result.rule_of_three_count == 0 else '⚠'}",
        f"  Generic conclusions:    {result.generic_conclusion_count} found {'✓' if result.generic_conclusion_count == 0 else '✗'}",
        f"  Structural slop:        {result.structural_slop_count} found {'✓' if result.structural_slop_count == 0 else '✗'}",
        "",
    ]

    if verbose:
        all_issues = (
            [('EM-DASH', result.emdash_issues)] +
            [('AI TELL', result.ai_tell_issues)] +
            [('CLICHE', result.cliche_issues)] +
            [('HEDGE', result.hedge_issues)] +
            [('COPULA AVOIDANCE', result.copula_issues)] +
            [('-ING CONSTRUCTION', result.ing_issues)] +
            [('SIGNIFICANCE INFLATION', result.significance_issues)] +
            [('SYCOPHANCY', result.sycophancy_issues)] +
            [('CURLY QUOTE', result.curly_quote_issues)] +
            [('NEGATIVE PARALLELISM', result.negative_parallelism_issues)] +
            [('RULE OF THREE', result.rule_of_three_issues)] +
            [('GENERIC CONCLUSION', result.generic_conclusion_issues)] +
            [('STRUCTURAL SLOP', result.structural_slop_issues)]
        )

        for category_name, issues in all_issues:
            if issues:
                lines.append(f"{category_name} ISSUES:")
                for issue in issues:
                    lines.append(f"  Line {issue.line} [{issue.severity}]: ...{issue.text}...")
                    if issue.suggestion:
                        lines.append(f"    -> {issue.suggestion}")
                lines.append("")

    # Overall assessment
    lines.append("ASSESSMENT:")
    if result.technical_score >= 9:
        lines.append("  ✓ Excellent - Ready to ship")
    elif result.technical_score >= 8:
        lines.append("  ✓ Good - Meets the quality floor")
    elif result.technical_score >= 5:
        lines.append("  ⚠ Below threshold - Revision recommended")
    else:
        lines.append("  ✗ Poor - Major revision needed")

    lines.append("")
    lines.append("NOTE: Voice consistency, proportional editing, and source-backed texture require manual assessment.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Validate content quality objectively (V5 - merged Unslop taxonomy)'
    )
    parser.add_argument('input', help='Input file path')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed issue list')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output as JSON')

    args = parser.parse_args()

    try:
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        text = input_file.read_text(encoding='utf-8')
        result = validate_content(text)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(format_report(result, verbose=args.verbose))

        # Exit code based on score
        if result.technical_score >= 8:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
