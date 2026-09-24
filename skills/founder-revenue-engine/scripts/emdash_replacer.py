#!/usr/bin/env python3
"""
Em-Dash Replacer

Systematically replaces em-dashes with appropriate punctuation.
- New sentence: period + capitalize next word
- Continuation: comma + keep lowercase

Usage:
    python emdash_replacer.py input.txt [output.txt]
    python emdash_replacer.py input.txt --in-place
    python emdash_replacer.py --text "Content with — dashes"
"""

import argparse
import re
import sys
from pathlib import Path


def is_likely_sentence(text: str) -> bool:
    """
    Determine if text following em-dash could be a standalone sentence.
    
    Heuristics:
    - Has a subject (starts with pronoun, noun, or article)
    - Has a verb
    - Is long enough to be a sentence (3+ words typically)
    """
    text = text.strip()
    if not text:
        return False
    
    words = text.split()
    if len(words) < 2:
        return False
    
    # Common sentence starters (pronouns, articles, demonstratives)
    sentence_starters = {
        'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'this', 'that', 'these', 'those',
        'the', 'a', 'an',
        'there', 'here',
        'my', 'your', 'his', 'her', 'its', 'our', 'their',
        'what', 'which', 'who', 'how', 'why', 'when', 'where',
    }
    
    first_word = words[0].lower().strip('.,!?;:')
    
    # Strong signal: starts with sentence starter
    if first_word in sentence_starters:
        return True
    
    # Strong signal: starts with capitalized proper noun or name
    if words[0][0].isupper() and first_word not in sentence_starters:
        # Could be proper noun at start of sentence
        return True
    
    # Check for verb presence (simple heuristic)
    common_verbs = {
        'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'having',
        'do', 'does', 'did', 'doing',
        'will', 'would', 'could', 'should', 'may', 'might', 'must',
        'can', 'shall',
        'get', 'gets', 'got', 'make', 'makes', 'made',
        'know', 'knows', 'knew', 'think', 'thinks', 'thought',
        'see', 'sees', 'saw', 'want', 'wants', 'wanted',
        'use', 'uses', 'used', 'find', 'finds', 'found',
        'give', 'gives', 'gave', 'tell', 'tells', 'told',
        'work', 'works', 'worked', 'seem', 'seems', 'seemed',
        'feel', 'feels', 'felt', 'try', 'tries', 'tried',
        'leave', 'leaves', 'left', 'call', 'calls', 'called',
        'need', 'needs', 'needed', 'keep', 'keeps', 'kept',
        'let', 'lets', 'help', 'helps', 'helped',
        'show', 'shows', 'showed', 'hear', 'hears', 'heard',
        'play', 'plays', 'played', 'run', 'runs', 'ran',
        'move', 'moves', 'moved', 'live', 'lives', 'lived',
        'believe', 'believes', 'believed', 'hold', 'holds', 'held',
        'bring', 'brings', 'brought', 'happen', 'happens', 'happened',
        'write', 'writes', 'wrote', 'provide', 'provides', 'provided',
        'sit', 'sits', 'sat', 'stand', 'stands', 'stood',
        'lose', 'loses', 'lost', 'pay', 'pays', 'paid',
        'meet', 'meets', 'met', 'include', 'includes', 'included',
        'continue', 'continues', 'continued', 'set', 'sets',
        'learn', 'learns', 'learned', 'change', 'changes', 'changed',
        'lead', 'leads', 'led', 'understand', 'understands', 'understood',
        'watch', 'watches', 'watched', 'follow', 'follows', 'followed',
        'stop', 'stops', 'stopped', 'create', 'creates', 'created',
        'speak', 'speaks', 'spoke', 'read', 'reads',
        'allow', 'allows', 'allowed', 'add', 'adds', 'added',
        'spend', 'spends', 'spent', 'grow', 'grows', 'grew',
        'open', 'opens', 'opened', 'walk', 'walks', 'walked',
        'win', 'wins', 'won', 'offer', 'offers', 'offered',
        'remember', 'remembers', 'remembered', 'love', 'loves', 'loved',
        'consider', 'considers', 'considered', 'appear', 'appears', 'appeared',
        'buy', 'buys', 'bought', 'wait', 'waits', 'waited',
        'serve', 'serves', 'served', 'die', 'dies', 'died',
        'send', 'sends', 'sent', 'expect', 'expects', 'expected',
        'build', 'builds', 'built', 'stay', 'stays', 'stayed',
        'fall', 'falls', 'fell', 'cut', 'cuts',
        'reach', 'reaches', 'reached', 'kill', 'kills', 'killed',
        'remain', 'remains', 'remained', 'suggest', 'suggests', 'suggested',
        'raise', 'raises', 'raised', 'pass', 'passes', 'passed',
        'sell', 'sells', 'sold', 'require', 'requires', 'required',
        'report', 'reports', 'reported', 'decide', 'decides', 'decided',
        'pull', 'pulls', 'pulled'
    }
    
    text_lower = text.lower()
    has_verb = any(f' {verb} ' in f' {text_lower} ' for verb in common_verbs)
    
    # If has sentence starter AND verb, definitely sentence
    if first_word in sentence_starters and has_verb:
        return True
    
    # If 5+ words and has verb, likely sentence
    if len(words) >= 5 and has_verb:
        return True
    
    # Short fragments without clear sentence structure -> continuation
    if len(words) <= 3:
        return False
    
    # Default: if starts with lowercase and no clear indicators, continuation
    if text[0].islower():
        return False
    
    # Default for ambiguous cases: treat as sentence (safer)
    return True


def replace_emdashes(text: str) -> tuple[str, int]:
    """
    Replace em-dashes with period or comma based on context.
    
    Returns:
        tuple: (processed_text, count_of_replacements)
    """
    # Match em-dash variants: —, –, --
    # Pattern: captures text before and after em-dash
    emdash_pattern = r'(\S)\s*[—–]|(\S)\s*--\s*'
    
    count = 0
    result = text
    
    # Find all em-dashes
    emdash_chars = ['—', '–', '--']
    
    for emdash in emdash_chars:
        while emdash in result:
            # Find position
            pos = result.find(emdash)
            if pos == -1:
                break
            
            # Get text after em-dash
            after_pos = pos + len(emdash)
            # Skip any whitespace
            while after_pos < len(result) and result[after_pos] in ' \t':
                after_pos += 1
            
            # Get remaining text
            remaining = result[after_pos:] if after_pos < len(result) else ""
            
            # Determine replacement
            if is_likely_sentence(remaining):
                # Period + capitalize
                replacement = '. '
                # Find first letter and capitalize
                if remaining:
                    first_letter_idx = 0
                    while first_letter_idx < len(remaining) and not remaining[first_letter_idx].isalpha():
                        first_letter_idx += 1
                    if first_letter_idx < len(remaining):
                        remaining = (remaining[:first_letter_idx] + 
                                   remaining[first_letter_idx].upper() + 
                                   remaining[first_letter_idx + 1:])
            else:
                # Comma + keep lowercase
                replacement = ', '
                # Ensure lowercase
                if remaining and remaining[0].isupper():
                    # Check if it's a proper noun (keep uppercase) vs regular word
                    first_word = remaining.split()[0] if remaining.split() else ""
                    # Simple heuristic: if all caps or mixed case in middle, keep
                    # Otherwise lowercase
                    if first_word and not first_word.isupper():
                        remaining = remaining[0].lower() + remaining[1:]
            
            # Strip whitespace before em-dash
            before = result[:pos].rstrip()
            
            # Reconstruct
            result = before + replacement + remaining
            count += 1
    
    return result, count


def process_file(input_path: str, output_path: str = None, in_place: bool = False) -> dict:
    """
    Process a file and replace em-dashes.
    
    Returns:
        dict with 'count', 'input', 'output' keys
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    text = input_file.read_text(encoding='utf-8')
    processed, count = replace_emdashes(text)
    
    if in_place:
        output_file = input_file
    elif output_path:
        output_file = Path(output_path)
    else:
        output_file = input_file.with_suffix('.processed' + input_file.suffix)
    
    output_file.write_text(processed, encoding='utf-8')
    
    return {
        'count': count,
        'input': str(input_file),
        'output': str(output_file)
    }


def main():
    parser = argparse.ArgumentParser(
        description='Replace em-dashes with appropriate punctuation'
    )
    parser.add_argument('input', nargs='?', help='Input file path')
    parser.add_argument('output', nargs='?', help='Output file path (optional)')
    parser.add_argument('--in-place', '-i', action='store_true',
                       help='Modify file in place')
    parser.add_argument('--text', '-t', help='Process text directly instead of file')
    
    args = parser.parse_args()
    
    if args.text:
        processed, count = replace_emdashes(args.text)
        print(f"Processed text ({count} em-dashes replaced):")
        print(processed)
        return
    
    if not args.input:
        parser.print_help()
        sys.exit(1)
    
    try:
        result = process_file(args.input, args.output, args.in_place)
        print(f"Em-dash replacement complete:")
        print(f"  Input: {result['input']}")
        print(f"  Output: {result['output']}")
        print(f"  Replacements: {result['count']}")
        
        if result['count'] == 0:
            print("  Status: No em-dashes found ✓")
        else:
            print(f"  Status: {result['count']} em-dashes replaced ✓")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
