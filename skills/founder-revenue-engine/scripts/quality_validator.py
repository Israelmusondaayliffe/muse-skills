#!/usr/bin/env python3
"""
LinkedIn Quality Validator (V3)

Automated detection of:
- AI tells and cliches (expanded with V3 taxonomy)
- Copula avoidance patterns
- Trailing -ing constructions
- Significance inflation
- Sycophantic/chatbot artifacts
- Generic positive conclusions
- Negative parallelisms, rule of three, curly quotes
- Hedge words, business jargon, banned openings
- Em-dashes (all variants)

Plus positive voice markers (bonuses):
- Lowercase emphasis, fragments, contractions
- Specific numbers, economic thinking, varied rhythm

Scoring: 100-point system (deductions + bonuses).

Usage:
    python quality_validator.py <text>
    python quality_validator.py --file <filepath>
    python quality_validator.py --file <filepath> --verbose
"""

import re
import sys
from pathlib import Path

# ============================================================
# BANNED PATTERNS
# ============================================================

AI_CLICHES = [
    'delve', 'delving', 'leverage', 'leveraging', 'unlock', 'unlocking',
    'journey', 'game-changer', 'game-changing', 'paradigm shift',
    'deep dive', 'diving deep', 'nuanced', 'robust', 'synergy',
    'disruptive', 'disruption', 'innovative', 'cutting-edge',
    'state-of-the-art', 'groundbreaking', 'revolutionary', 'transformative',
    # V3 additions
    'vibrant', 'nestled', 'breathtaking', 'stunning', 'renowned',
    'tapestry', 'beacon', 'cornerstone', 'myriad', 'plethora',
    'holistic', 'pivotal', 'unparalleled', 'harness', 'harnessing',
    'elevate', 'elevating', 'interplay', 'intricacies', 'intricate',
    'enduring', 'testament', 'landscape', 'realm', 'garner', 'garnered',
    'showcasing', 'fostering', 'underscoring',
]

BUSINESS_JARGON = [
    'scalable', 'scalability', 'bandwidth', 'circle back', 'touch base',
    'move the needle', 'low-hanging fruit', 'think outside the box',
    'drill down', 'take it offline', 'boil the ocean',
]

HEDGE_WORDS = [
    'kind of', 'sort of', 'probably', 'maybe', 'could be', 'might be',
    'perhaps', 'possibly', 'arguably', 'somewhat', 'relatively',
    'fairly', 'quite', 'rather',
]

BANNED_OPENINGS = [
    "let's talk about", "here's why", "here's the thing", "the truth is",
    "at the end of the day", "when it comes to", "in today's world",
    "it's no secret that", "we all know that",
]

# V3: Copula avoidance patterns
COPULA_AVOIDANCE = [
    'serves as', 'stands as', 'functions as', 'acts as',
    'boasts a', 'boasts an', 'boasts the',
    'features a', 'features an', 'features the',
    'offers a', 'offers an',
    'represents a', 'represents an',
]

# V3: Significance inflation
SIGNIFICANCE_PHRASES = [
    'marking a pivotal', 'marking a significant', 'marking a key',
    'setting the stage for', 'a testament to', 'is a testament',
    'reflects broader', 'contributing to the', 'indelible mark',
    'deeply rooted', 'enduring legacy', 'key turning point',
    'evolving landscape', 'focal point of',
    'plays a crucial role', 'plays a vital role',
    'plays a significant role', 'plays a pivotal role',
    'underscores the importance', 'highlights the significance',
    'symbolizing its', 'part of a broader',
]

# V3: Sycophantic artifacts
SYCOPHANCY = [
    'great question', 'excellent question', 'wonderful question',
    "you're absolutely right", "that's an excellent point",
    "that's a great point", "that's a fantastic",
    'i hope this helps', "let me know if you'd like",
    "let me know if you would like",
    'here is a comprehensive', 'here is an overview',
    'of course!', 'certainly!', 'absolutely!',
    'would you like me to',
]

# V3: Generic positive conclusions
GENERIC_CONCLUSIONS = [
    'the future looks bright', 'exciting times lie ahead',
    'exciting times ahead', 'continue their journey',
    'step in the right direction', 'poised to',
    'poised for growth', 'poised for success',
    'looking ahead', 'as we look to the future',
    'the possibilities are endless', 'only time will tell',
]

# V3: Negative parallelisms
NEGATIVE_PARALLELISMS = [
    'not only', "it's not just about", "it's not just a",
    "it's not merely", 'more than just a', 'more than just an',
]

# V3: Trailing -ing verbs
ING_VERBS = [
    'highlighting', 'underscoring', 'emphasizing', 'ensuring',
    'reflecting', 'symbolizing', 'contributing', 'cultivating',
    'fostering', 'encompassing', 'showcasing', 'demonstrating',
    'illustrating', 'reinforcing', 'signaling', 'representing',
]

# V3: Fluff phrases (overlaps with banned openings, kept separate for scoring)
FLUFF_PHRASES = [
    "it's worth noting", "it's important to note",
    "it is worth noting", "it is important to note",
    "in order to", "due to the fact that",
    "at this point in time", "now more than ever",
    "in terms of", "the fact of the matter",
]


def find_all(text_lower, pattern):
    """Find all occurrences of pattern in text."""
    if ' ' in pattern:
        return [m.start() for m in re.finditer(re.escape(pattern), text_lower)]
    else:
        return [m.start() for m in re.finditer(r'\b' + re.escape(pattern) + r'\b', text_lower)]


def count_violations(text):
    """Count all quality violations across all categories."""
    text_lower = text.lower()

    v = {
        'emdashes': 0,
        'ai_cliches': [],
        'business_jargon': [],
        'hedge_words': [],
        'banned_openings': [],
        # V3 additions
        'copula': [],
        'significance': [],
        'ing_constructions': [],
        'sycophancy': [],
        'generic_conclusions': [],
        'negative_parallelisms': [],
        'curly_quotes': 0,
        'fluff': [],
        'rule_of_three': 0,
    }

    # Em-dashes (all variants)
    v['emdashes'] = len(re.findall(r'[—–]', text)) + len(re.findall(r'(?<!\-)--(?!\-)', text))

    # AI cliches
    for c in AI_CLICHES:
        if find_all(text_lower, c):
            v['ai_cliches'].append(c)

    # Business jargon
    for j in BUSINESS_JARGON:
        if find_all(text_lower, j):
            v['business_jargon'].append(j)

    # Hedge words
    for h in HEDGE_WORDS:
        if find_all(text_lower, h):
            v['hedge_words'].append(h)

    # Banned openings
    for o in BANNED_OPENINGS:
        if text_lower.strip().startswith(o):
            v['banned_openings'].append(o)

    # V3: Copula avoidance
    for c in COPULA_AVOIDANCE:
        if find_all(text_lower, c):
            v['copula'].append(c)

    # V3: Significance inflation
    for s in SIGNIFICANCE_PHRASES:
        if s in text_lower:
            v['significance'].append(s)

    # V3: Trailing -ing constructions
    for verb in ING_VERBS:
        if re.search(rf',\s+{verb}\b', text_lower):
            v['ing_constructions'].append(verb)

    # V3: Sycophancy
    for s in SYCOPHANCY:
        if s in text_lower:
            v['sycophancy'].append(s)

    # V3: Generic conclusions
    for g in GENERIC_CONCLUSIONS:
        if g in text_lower:
            v['generic_conclusions'].append(g)

    # V3: Negative parallelisms
    for n in NEGATIVE_PARALLELISMS:
        if n in text_lower:
            v['negative_parallelisms'].append(n)

    # V3: Curly quotes
    v['curly_quotes'] = len(re.findall(r'[\u201c\u201d\u2018\u2019]', text))

    # V3: Fluff phrases
    for f in FLUFF_PHRASES:
        if f in text_lower:
            v['fluff'].append(f)

    # V3: Rule of three (multiple forced triplets)
    triplets = list(re.finditer(r'\b\w+,\s+\w+,\s+and\s+\w+', text_lower))
    if len(triplets) >= 2:
        for i in range(len(triplets) - 1):
            if triplets[i + 1].start() - triplets[i].end() < 200:
                v['rule_of_three'] = 1
                break

    return v


def check_voice_markers(text):
    """Check for positive voice markers."""
    return {
        'lowercase_emphasis': bool(re.search(r'\bi\b', text)),
        'fragments': bool(re.search(r'\b[A-Za-z]+\.$', text, re.MULTILINE)),
        'contractions': bool(re.search(r"n't|'s|'re|'ve|'ll", text)),
        'specific_numbers': bool(re.search(r'\$\d+|[\d,]+%|\d+ [a-z]+', text)),
        'economic_thinking': any(w in text.lower() for w in
            ['pays', 'cost', 'saves', 'captures', 'offload', 'subsidiz', 'rent', 'price', 'spent', 'invest']),
    }


def check_rhythm(text):
    """Analyze sentence length variety."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) < 2:
        return False
    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    return variance > 10


def calculate_score(v, voice, rhythm):
    """Calculate quality score out of 100."""
    score = 100

    # === DEDUCTIONS ===
    # Original categories
    score -= v['emdashes'] * 10
    score -= len(v['ai_cliches']) * 5
    score -= len(v['business_jargon']) * 3
    score -= len(v['hedge_words']) * 2
    score -= len(v['banned_openings']) * 15

    # V3 categories
    score -= len(v['copula']) * 5
    score -= len(v['significance']) * 5
    score -= len(v['ing_constructions']) * 4
    score -= len(v['sycophancy']) * 10
    score -= len(v['generic_conclusions']) * 5
    score -= len(v['negative_parallelisms']) * 2
    score -= v['curly_quotes'] * 1
    score -= len(v['fluff']) * 2
    score -= v['rule_of_three'] * 3

    # === BONUSES ===
    if voice['lowercase_emphasis']:
        score += 5
    if voice['fragments']:
        score += 5
    if voice['contractions']:
        score += 5
    if voice['specific_numbers']:
        score += 5
    if voice['economic_thinking']:
        score += 10
    if rhythm:
        score += 10

    return max(0, min(100, score))


def print_report(text, v, voice, rhythm, verbose=False):
    """Print quality report."""
    score = calculate_score(v, voice, rhythm)

    print("=" * 60)
    print("LINKEDIN QUALITY VALIDATION REPORT (V3)")
    print("=" * 60)

    print(f"\nOVERALL SCORE: {score}/100")
    if score >= 90:
        print("✓ Excellent. Ship it.")
    elif score >= 80:
        print("⚠ Good. Minor tweaks recommended.")
    elif score >= 70:
        print("⚠ Acceptable. Needs revision.")
    else:
        print("✗ Poor. Regenerate recommended.")

    # Count total violations
    total_original = (
        v['emdashes'] + len(v['ai_cliches']) + len(v['business_jargon']) +
        len(v['hedge_words']) + len(v['banned_openings'])
    )
    total_v3 = (
        len(v['copula']) + len(v['significance']) + len(v['ing_constructions']) +
        len(v['sycophancy']) + len(v['generic_conclusions']) +
        len(v['negative_parallelisms']) + v['curly_quotes'] +
        len(v['fluff']) + v['rule_of_three']
    )

    if total_original > 0 or total_v3 > 0:
        print(f"\nVIOLATIONS ({total_original + total_v3} total):")

        if v['emdashes'] > 0:
            print(f"  Em-dashes: {v['emdashes']} (-{v['emdashes'] * 10}pts)")
        if v['ai_cliches']:
            print(f"  AI cliches: {len(v['ai_cliches'])} (-{len(v['ai_cliches']) * 5}pts)")
            if verbose:
                for c in v['ai_cliches']:
                    print(f"    - {c}")
        if v['business_jargon']:
            print(f"  Business jargon: {len(v['business_jargon'])} (-{len(v['business_jargon']) * 3}pts)")
            if verbose:
                for j in v['business_jargon']:
                    print(f"    - {j}")
        if v['hedge_words']:
            print(f"  Hedge words: {len(v['hedge_words'])} (-{len(v['hedge_words']) * 2}pts)")
            if verbose:
                for h in v['hedge_words']:
                    print(f"    - {h}")
        if v['banned_openings']:
            print(f"  Banned openings: {len(v['banned_openings'])} (-{len(v['banned_openings']) * 15}pts)")

        # V3 violations
        if v['copula']:
            print(f"  Copula avoidance: {len(v['copula'])} (-{len(v['copula']) * 5}pts)")
            if verbose:
                for c in v['copula']:
                    print(f"    - \"{c}\" -> use \"is\" or \"has\"")
        if v['significance']:
            print(f"  Significance inflation: {len(v['significance'])} (-{len(v['significance']) * 5}pts)")
            if verbose:
                for s in v['significance']:
                    print(f"    - \"{s}\"")
        if v['ing_constructions']:
            print(f"  -ing constructions: {len(v['ing_constructions'])} (-{len(v['ing_constructions']) * 4}pts)")
            if verbose:
                for i in v['ing_constructions']:
                    print(f"    - \", {i}...\" -> delete or make own sentence")
        if v['sycophancy']:
            print(f"  Sycophancy/chatbot: {len(v['sycophancy'])} (-{len(v['sycophancy']) * 10}pts)")
            if verbose:
                for s in v['sycophancy']:
                    print(f"    - \"{s}\"")
        if v['generic_conclusions']:
            print(f"  Generic conclusions: {len(v['generic_conclusions'])} (-{len(v['generic_conclusions']) * 5}pts)")
            if verbose:
                for g in v['generic_conclusions']:
                    print(f"    - \"{g}\"")
        if v['negative_parallelisms']:
            print(f"  Negative parallelisms: {len(v['negative_parallelisms'])} (-{len(v['negative_parallelisms']) * 2}pts)")
        if v['curly_quotes'] > 0:
            print(f"  Curly quotes: {v['curly_quotes']} (-{v['curly_quotes']}pts)")
        if v['fluff']:
            print(f"  Fluff phrases: {len(v['fluff'])} (-{len(v['fluff']) * 2}pts)")
        if v['rule_of_three'] > 0:
            print(f"  Rule of three: forced triplets detected (-3pts)")

    else:
        print("\n✓ NO VIOLATIONS FOUND")

    # Voice markers
    print(f"\nVOICE MARKERS:")
    print(f"  Lowercase emphasis: {'✓ +5' if voice['lowercase_emphasis'] else '✗'}")
    print(f"  Fragments: {'✓ +5' if voice['fragments'] else '✗'}")
    print(f"  Contractions: {'✓ +5' if voice['contractions'] else '✗'}")
    print(f"  Specific numbers: {'✓ +5' if voice['specific_numbers'] else '✗'}")
    print(f"  Economic thinking: {'✓ +10' if voice['economic_thinking'] else '✗'}")
    print(f"  Varied rhythm: {'✓ +10' if rhythm else '✗'}")

    # Recommendations
    print(f"\nRECOMMENDATIONS:")
    if v['emdashes'] > 0:
        print("  -> Run emdash_replacer.py to fix em-dashes")
    if v['copula']:
        print("  -> Replace copula avoidance: 'serves as' -> 'is', 'boasts' -> 'has'")
    if v['significance']:
        print("  -> Delete significance inflation claims")
    if v['ing_constructions']:
        print("  -> Remove trailing -ing clauses or make them separate sentences")
    if v['sycophancy']:
        print("  -> Remove all chatbot language from content")
    if v['generic_conclusions']:
        print("  -> Replace generic conclusion with specific fact or question")
    if v['ai_cliches']:
        print("  -> Remove AI cliches and rewrite affected sections")
    if v['hedge_words'] and len(v['hedge_words']) > 3:
        print("  -> Too much hedge language. Commit to clear stance.")
    if not voice['economic_thinking']:
        print("  -> Add economic/structural insight (who pays? who wins?)")
    if not rhythm:
        print("  -> Vary sentence length. Mix short and long.")
    if not voice['lowercase_emphasis']:
        print("  -> Add lowercase emphasis for personality")

    if (total_original + total_v3) == 0 and score >= 85:
        print("  No changes needed. Output is high quality.")

    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python quality_validator.py <text>")
        print("       python quality_validator.py --file <filepath> [--verbose]")
        sys.exit(1)

    verbose = '--verbose' in sys.argv

    if sys.argv[1] == '--file':
        if len(sys.argv) < 3:
            print("Error: --file requires filepath argument")
            sys.exit(1)
        filepath = sys.argv[2]
        try:
            text = Path(filepath).read_text(encoding='utf-8')
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found")
            sys.exit(1)
    else:
        text = ' '.join([arg for arg in sys.argv[1:] if arg not in ('--verbose',)])

    v = count_violations(text)
    voice = check_voice_markers(text)
    rhythm = check_rhythm(text)
    print_report(text, v, voice, rhythm, verbose)

    score = calculate_score(v, voice, rhythm)
    sys.exit(0 if score >= 80 else 1)


if __name__ == '__main__':
    main()
