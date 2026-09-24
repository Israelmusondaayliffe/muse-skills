#!/usr/bin/env python3
"""
Consensus Detector Script

Checks if generated content falls into consensus zone (p > 0.90).
Flags common patterns, overused vocabulary, and generic structures.

Usage:
    python consensus_detector.py <text>
    python consensus_detector.py --file <filepath>
"""

import re
import sys
from collections import Counter

# Common consensus markers
CONSENSUS_PHRASES = [
    'is important', 'is essential', 'is crucial', 'is key',
    'the key is', 'the secret is', 'the truth is',
    'you need to', 'you should', 'you must',
    'it\'s important to', 'it\'s essential to',
    'can help you', 'will help you',
    'benefits and challenges', 'pros and cons',
    'on one hand', 'on the other hand',
    'both X and Y', 'it depends on',
    'there are many', 'there are several',
    'in today\'s world', 'in this day and age',
    'as we all know', 'everyone knows',
    'the future of', 'the power of',
    'best practices', 'tips and tricks'
]

ASPIRATIONAL_PHRASES = [
    'freedom and flexibility', 'work-life balance',
    'follow your passion', 'find your purpose',
    'be authentic', 'be yourself',
    'continuous learning', 'growth mindset',
    'think outside the box', 'push the envelope',
    'make a difference', 'change the world'
]

GENERIC_ADVICE_PATTERNS = [
    r'\b(start|begin|try|consider|focus on|work on|build|create|develop)\b',
    r'\b(improve|enhance|optimize|maximize|increase|boost)\b',
    r'\b(learn|study|practice|master|understand)\b',
    r'\b(network|connect|collaborate|engage|interact)\b'
]

def detect_consensus_markers(text):
    """Detect consensus language patterns."""
    text_lower = text.lower()
    
    markers = {
        'consensus_phrases': [],
        'aspirational_phrases': [],
        'generic_advice_count': 0,
        'hedge_count': 0,
        'questions_to_statements_ratio': 0
    }
    
    # Check consensus phrases
    for phrase in CONSENSUS_PHRASES:
        if phrase.lower() in text_lower:
            markers['consensus_phrases'].append(phrase)
    
    # Check aspirational phrases
    for phrase in ASPIRATIONAL_PHRASES:
        if phrase.lower() in text_lower:
            markers['aspirational_phrases'].append(phrase)
    
    # Count generic advice patterns
    for pattern in GENERIC_ADVICE_PATTERNS:
        markers['generic_advice_count'] += len(re.findall(pattern, text_lower))
    
    # Count hedge words
    hedge_words = ['maybe', 'perhaps', 'possibly', 'probably', 'might', 'could', 'may']
    for hedge in hedge_words:
        markers['hedge_count'] += len(re.findall(rf'\b{hedge}\b', text_lower))
    
    # Questions vs statements
    questions = len(re.findall(r'\?', text))
    sentences = len(re.findall(r'[.!?]', text))
    if sentences > 0:
        markers['questions_to_statements_ratio'] = questions / sentences
    
    return markers

def check_vocabulary_originality(text):
    """Check if vocabulary is overused/generic."""
    # Extract words (lowercase, no punctuation)
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    word_counts = Counter(words)
    
    # Common overused words in content
    overused_words = [
        'important', 'essential', 'need', 'help', 'work', 'time',
        'thing', 'way', 'make', 'good', 'great', 'best',
        'people', 'want', 'know', 'think', 'just', 'really'
    ]
    
    overused_found = {word: count for word, count in word_counts.items() if word in overused_words}
    
    return {
        'total_words': len(words),
        'unique_words': len(word_counts),
        'uniqueness_ratio': len(word_counts) / len(words) if words else 0,
        'overused_words': overused_found
    }

def check_structure_originality(text):
    """Check if structure follows generic patterns."""
    text_lower = text.lower().strip()
    
    issues = []
    
    # Check for list-based structure
    if re.search(r'(here are|these are|following are).*(:\s*)?[\n\s]*\d+\.', text_lower):
        issues.append("Generic numbered list structure detected")
    
    # Check for how-to structure
    if re.search(r'how to|steps to|ways to|tips for', text_lower):
        issues.append("Generic how-to/tips structure detected")
    
    # Check for question-answer structure
    if re.search(r'what (is|are)|why (do|does)|how (can|do)', text_lower):
        q_count = len(re.findall(r'\?', text))
        if q_count > 2:
            issues.append("Q&A structure (often generic)")
    
    # Check for benefit listing
    if re.search(r'benefits of|advantages of|pros of', text_lower):
        issues.append("Generic benefits listing detected")
    
    return issues

def calculate_consensus_score(markers, vocab, structure_issues):
    """Calculate probability that content is in consensus zone (0-100)."""
    score = 0
    
    # Consensus phrases (5 points each, cap at 30)
    score += min(30, len(markers['consensus_phrases']) * 5)
    
    # Aspirational phrases (10 points each, cap at 30)
    score += min(30, len(markers['aspirational_phrases']) * 10)
    
    # Generic advice patterns (2 points each, cap at 20)
    score += min(20, markers['generic_advice_count'] * 2)
    
    # Hedge words (3 points each, cap at 15)
    score += min(15, markers['hedge_count'] * 3)
    
    # Low vocabulary uniqueness (up to 20 points)
    if vocab['uniqueness_ratio'] < 0.6:
        score += 20
    elif vocab['uniqueness_ratio'] < 0.7:
        score += 10
    
    # Overused words (2 points each, cap at 10)
    score += min(10, sum(vocab['overused_words'].values()) * 2)
    
    # Structure issues (5 points each, cap at 15)
    score += min(15, len(structure_issues) * 5)
    
    return min(100, score)

def print_report(text, markers, vocab, structure_issues):
    """Print consensus detection report."""
    consensus_score = calculate_consensus_score(markers, vocab, structure_issues)
    
    # Invert to show tail probability (p < 0.10 = score < 10)
    tail_score = 100 - consensus_score
    
    print("=" * 60)
    print("CONSENSUS DETECTION REPORT")
    print("=" * 60)
    
    print(f"\nCONSENSUS SCORE: {consensus_score}/100")
    print(f"TAIL PROBABILITY: p ≈ {tail_score/100:.2f}")
    
    if consensus_score >= 70:
        print("❌ HIGH CONSENSUS - Content is generic/mainstream")
        print("   Recommendation: Regenerate with stronger contrarian angles")
    elif consensus_score >= 40:
        print("⚠ MODERATE CONSENSUS - Some generic elements")
        print("   Recommendation: Revise to strengthen contrarian perspective")
    elif consensus_score >= 20:
        print("✓ LOW CONSENSUS - Reasonably contrarian")
        print("   Recommendation: Minor refinements acceptable")
    else:
        print("✓✓ TAIL CONTENT - Strong contrarian perspective")
        print("   Recommendation: Maintain this approach")
    
    # Details
    if markers['consensus_phrases']:
        print(f"\n⚠ CONSENSUS PHRASES ({len(markers['consensus_phrases'])}):")
        for phrase in markers['consensus_phrases'][:5]:
            print(f"  - '{phrase}'")
        if len(markers['consensus_phrases']) > 5:
            print(f"  ... and {len(markers['consensus_phrases']) - 5} more")
    
    if markers['aspirational_phrases']:
        print(f"\n⚠ ASPIRATIONAL PHRASES ({len(markers['aspirational_phrases'])}):")
        for phrase in markers['aspirational_phrases']:
            print(f"  - '{phrase}'")
    
    if markers['generic_advice_count'] > 5:
        print(f"\n⚠ GENERIC ADVICE PATTERNS: {markers['generic_advice_count']} instances")
        print("   (start, improve, learn, etc.)")
    
    if markers['hedge_count'] > 3:
        print(f"\n⚠ HEDGE WORDS: {markers['hedge_count']} instances")
        print("   (maybe, perhaps, possibly, etc.)")
    
    if vocab['uniqueness_ratio'] < 0.7:
        print(f"\n⚠ LOW VOCABULARY UNIQUENESS: {vocab['uniqueness_ratio']:.1%}")
        print("   More varied vocabulary needed")
    
    if vocab['overused_words']:
        print(f"\n⚠ OVERUSED WORDS:")
        for word, count in sorted(vocab['overused_words'].items(), key=lambda x: -x[1])[:5]:
            print(f"  - '{word}': {count} times")
    
    if structure_issues:
        print(f"\n⚠ STRUCTURE ISSUES:")
        for issue in structure_issues:
            print(f"  - {issue}")
    
    print("\n" + "=" * 60)
    
    # Recommendations
    print("\n📋 RECOMMENDATIONS:")
    if consensus_score >= 70:
        print("  1. Regenerate Phase 2 (Tail Angles) with stronger economic/structural focus")
        print("  2. Remove all aspirational language")
        print("  3. Replace generic advice with specific insights")
        print("  4. Add concrete numbers/examples")
    elif consensus_score >= 40:
        print("  1. Remove consensus phrases")
        print("  2. Replace aspirational language with structural insight")
        print("  3. Reduce hedge words - commit to clear stance")
        print("  4. Vary vocabulary more")
    elif consensus_score >= 20:
        print("  1. Minor cleanup of remaining consensus markers")
        print("  2. Consider adding more specific examples")
    else:
        print("  • Content is sufficiently contrarian - proceed to PRISM refinement")
    
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python consensus_detector.py <text>")
        print("       python consensus_detector.py --file <filepath>")
        sys.exit(1)
    
    if sys.argv[1] == '--file':
        if len(sys.argv) < 3:
            print("Error: --file requires filepath argument")
            sys.exit(1)
        
        filepath = sys.argv[2]
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found")
            sys.exit(1)
    else:
        text = ' '.join(sys.argv[1:])
    
    # Run detection
    markers = detect_consensus_markers(text)
    vocab = check_vocabulary_originality(text)
    structure_issues = check_structure_originality(text)
    
    # Print report
    print_report(text, markers, vocab, structure_issues)

if __name__ == '__main__':
    main()
