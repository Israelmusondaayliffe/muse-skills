#!/usr/bin/env python3
"""
Voice Profiler

Extracts voice markers from sample text to create voice preservation profile.

Usage:
    python3 bin/voice_profile.py sample.txt
    python3 bin/voice_profile.py sample.txt --output profile.json
    python3 bin/voice_profile.py sample.txt --verbose
"""

import argparse
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict
from collections import Counter


@dataclass
class VoiceProfile:
    """Voice profile extracted from text."""
    tone: str = "neutral"
    sentence_style: str = "varied"
    structure: str = "hybrid"
    
    characteristic_phrases: List[str] = field(default_factory=list)
    common_transitions: List[str] = field(default_factory=list)
    
    avg_sentence_length: float = 0.0
    sentence_length_variance: str = "medium"
    
    question_frequency: float = 0.0
    contraction_frequency: float = 0.0
    first_person_frequency: float = 0.0
    
    emphasis_method: str = "structural"
    
    confidence: str = "medium"
    word_count: int = 0
    sentence_count: int = 0


def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def analyze_sentence_style(sentences: List[str]) -> tuple:
    """Analyze sentence length patterns."""
    if not sentences:
        return 0.0, "unknown"
    
    lengths = [count_words(s) for s in sentences]
    avg = sum(lengths) / len(lengths)
    
    # Calculate variance
    if len(lengths) > 1:
        variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5
        
        if std_dev < 3:
            variance_desc = "low"
        elif std_dev < 7:
            variance_desc = "medium"
        else:
            variance_desc = "high"
    else:
        variance_desc = "unknown"
    
    # Determine style
    if avg < 10:
        style = "short-punchy"
    elif avg < 18:
        style = "medium"
    else:
        style = "flowing"
    
    # Adjust for variance
    if variance_desc == "high":
        style = "varied"
    
    return avg, style


def analyze_tone(text: str, sentences: List[str]) -> str:
    """Analyze overall tone of text."""
    text_lower = text.lower()
    
    # Count indicators
    contractions = len(re.findall(r"\b\w+'\w+\b", text))
    questions = text.count('?')
    exclamations = text.count('!')
    
    first_person = len(re.findall(r'\b(I|me|my|mine|we|us|our|ours)\b', text, re.I))
    second_person = len(re.findall(r'\b(you|your|yours)\b', text, re.I))
    
    # Formal indicators
    formal_words = ['therefore', 'consequently', 'furthermore', 'moreover', 
                   'nevertheless', 'notwithstanding', 'hereby', 'wherein']
    formal_count = sum(1 for w in formal_words if w in text_lower)
    
    # Casual indicators
    casual_patterns = ['yeah', 'yep', 'nope', 'gonna', 'wanna', 'kinda', 
                      'sorta', 'gotta', 'btw', 'tbh', 'imo', 'imho']
    casual_count = sum(1 for p in casual_patterns if p in text_lower)
    
    word_count = count_words(text)
    if word_count == 0:
        return "neutral"
    
    # Calculate ratios
    contraction_ratio = contractions / (word_count / 100)
    question_ratio = questions / len(sentences) if sentences else 0
    first_person_ratio = first_person / (word_count / 100)
    
    # Determine tone
    if formal_count > 2 or (contraction_ratio < 0.5 and first_person_ratio < 1):
        return "formal"
    elif casual_count > 1 or contraction_ratio > 3:
        return "casual"
    elif question_ratio > 0.3:
        return "curious"
    elif first_person_ratio > 3 and contraction_ratio > 1:
        return "conversational"
    elif first_person_ratio < 0.5:
        return "objective"
    else:
        return "direct"


def extract_repeated_phrases(text: str, min_length: int = 3, max_length: int = 6) -> List[str]:
    """Extract phrases that appear multiple times (potential signature phrases)."""
    words = text.lower().split()
    phrases = []
    
    for length in range(min_length, max_length + 1):
        for i in range(len(words) - length + 1):
            phrase = ' '.join(words[i:i + length])
            phrases.append(phrase)
    
    # Count phrases
    counter = Counter(phrases)
    
    # Filter to phrases that appear more than once
    repeated = [phrase for phrase, count in counter.items() if count >= 2]
    
    # Remove subphrases of longer phrases
    filtered = []
    repeated_sorted = sorted(repeated, key=len, reverse=True)
    
    for phrase in repeated_sorted:
        if not any(phrase in longer and phrase != longer for longer in filtered):
            filtered.append(phrase)
    
    return filtered[:10]  # Top 10


def extract_transitions(text: str) -> List[str]:
    """Extract common transition patterns used."""
    common_transitions = [
        'but', 'and', 'so', 'then', 'however', 'moreover', 'furthermore',
        'additionally', 'also', 'yet', 'still', 'though', 'although',
        'because', 'since', 'therefore', 'thus', 'hence', 'meanwhile',
        "here's the thing", "the point is", "what matters is",
        "in other words", "that said", "on the other hand"
    ]
    
    found = []
    text_lower = text.lower()
    
    for trans in common_transitions:
        # Look for at sentence starts
        pattern = rf'[.!?]\s*{re.escape(trans)}\b'
        if re.search(pattern, text_lower, re.I):
            found.append(trans)
    
    return found


def analyze_structure(text: str) -> str:
    """Analyze structure preference (prose vs lists vs hybrid)."""
    bullet_count = text.count('- ') + text.count('• ') + text.count('* ')
    numbered_count = len(re.findall(r'\n\d+\.', text))
    header_count = len(re.findall(r'\n#{1,6}\s', text))
    
    paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
    
    total_structure = bullet_count + numbered_count + header_count
    
    if total_structure > paragraph_count:
        return "list-dominant"
    elif total_structure == 0:
        return "prose-dominant"
    else:
        return "hybrid"


def analyze_emphasis(text: str) -> str:
    """Analyze how emphasis is typically applied."""
    bold_count = len(re.findall(r'\*\*[^*]+\*\*', text))
    caps_count = len(re.findall(r'\b[A-Z]{3,}\b', text))
    
    # Check for short emphatic paragraphs
    paragraphs = text.split('\n\n')
    short_paras = len([p for p in paragraphs if p.strip() and count_words(p) < 10])
    
    if bold_count > 3:
        return "bold"
    elif caps_count > 2:
        return "caps"
    elif short_paras > len(paragraphs) * 0.3:
        return "structural"
    else:
        return "none"


def determine_confidence(word_count: int) -> str:
    """Determine confidence level based on sample size."""
    if word_count < 100:
        return "low"
    elif word_count < 500:
        return "medium"
    else:
        return "high"


def create_voice_profile(text: str) -> VoiceProfile:
    """Create complete voice profile from text."""
    sentences = split_sentences(text)
    word_count = count_words(text)
    
    avg_length, sentence_style = analyze_sentence_style(sentences)
    
    # Calculate frequencies
    contraction_count = len(re.findall(r"\b\w+'\w+\b", text))
    question_count = text.count('?')
    first_person_count = len(re.findall(r'\b(I|me|my|mine|we|us|our|ours)\b', text, re.I))
    
    return VoiceProfile(
        tone=analyze_tone(text, sentences),
        sentence_style=sentence_style,
        structure=analyze_structure(text),
        characteristic_phrases=extract_repeated_phrases(text),
        common_transitions=extract_transitions(text),
        avg_sentence_length=round(avg_length, 1),
        sentence_length_variance="high" if sentence_style == "varied" else "medium",
        question_frequency=round(question_count / len(sentences) if sentences else 0, 2),
        contraction_frequency=round(contraction_count / (word_count / 100) if word_count else 0, 2),
        first_person_frequency=round(first_person_count / (word_count / 100) if word_count else 0, 2),
        emphasis_method=analyze_emphasis(text),
        confidence=determine_confidence(word_count),
        word_count=word_count,
        sentence_count=len(sentences)
    )


def format_profile_report(profile: VoiceProfile) -> str:
    """Format profile as human-readable report."""
    lines = [
        "VOICE PROFILE ANALYSIS",
        "=" * 50,
        "",
        f"Confidence: {profile.confidence.upper()}",
        f"Sample size: {profile.word_count} words, {profile.sentence_count} sentences",
        "",
        "VOICE CHARACTERISTICS:",
        f"  Tone: {profile.tone}",
        f"  Sentence style: {profile.sentence_style}",
        f"  Structure preference: {profile.structure}",
        f"  Emphasis method: {profile.emphasis_method}",
        "",
        "METRICS:",
        f"  Avg sentence length: {profile.avg_sentence_length} words",
        f"  Question frequency: {profile.question_frequency:.0%} of sentences",
        f"  Contraction frequency: {profile.contraction_frequency:.1f} per 100 words",
        f"  First-person frequency: {profile.first_person_frequency:.1f} per 100 words",
        "",
    ]
    
    if profile.characteristic_phrases:
        lines.append("CHARACTERISTIC PHRASES:")
        for phrase in profile.characteristic_phrases[:5]:
            lines.append(f"  • {phrase}")
        lines.append("")
    
    if profile.common_transitions:
        lines.append("COMMON TRANSITIONS:")
        for trans in profile.common_transitions:
            lines.append(f"  • {trans}")
        lines.append("")
    
    lines.append("PRESERVATION GUIDANCE:")
    
    if profile.tone == "conversational":
        lines.append("  • Maintain contractions and first-person perspective")
    elif profile.tone == "formal":
        lines.append("  • Preserve formal register, avoid contractions")
    elif profile.tone == "curious":
        lines.append("  • Preserve embedded questions and exploratory language")
    elif profile.tone == "direct":
        lines.append("  • Maintain decisive, direct statements")
    
    if profile.sentence_style == "short-punchy":
        lines.append("  • Keep sentences short, preserve fragments")
    elif profile.sentence_style == "flowing":
        lines.append("  • Maintain longer, connected sentence structure")
    elif profile.sentence_style == "varied":
        lines.append("  • Preserve rhythm variation in sentence length")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Extract voice profile from sample text'
    )
    parser.add_argument('input', help='Input file path')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed analysis')
    
    args = parser.parse_args()
    
    try:
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        
        text = input_file.read_text(encoding='utf-8')
        profile = create_voice_profile(text)
        
        if args.output:
            output_file = Path(args.output)
            output_file.write_text(
                json.dumps(asdict(profile), indent=2),
                encoding='utf-8'
            )
            print(f"Profile saved to: {args.output}")
        
        if args.verbose or not args.output:
            print(format_profile_report(profile))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
