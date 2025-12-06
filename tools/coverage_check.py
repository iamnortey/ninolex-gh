#!/usr/bin/env python3
"""
Coverage Check Script for Ninolex-GH

This script estimates dictionary coverage against a sample text file.
It extracts candidate proper nouns and checks how many are in the dictionary.

Usage:
    python3 tools/coverage_check.py path/to/news_article.txt

Example:
    python3 tools/coverage_check.py samples/ghanaweb_article.txt

Output:
    - Total tokens in the text
    - Candidate proper nouns extracted
    - Matches found in Ninolex-GH
    - Coverage percentage
    - List of unmatched candidates (for gap analysis)

Notes:
    - Uses a simple heuristic: tokens starting with uppercase, containing lowercase
    - Not perfect NLP; intended for internal gap analysis
    - Works best with clean text (not HTML)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICTIONARY_PATH = ROOT / "dist" / "dictionary" / "ninolex_gh_dictionary.json"


def load_dictionary():
    """Load the unified dictionary and return a set of lowercase graphemes."""
    if not DICTIONARY_PATH.exists():
        print(f"Error: Dictionary not found at {DICTIONARY_PATH}")
        print("Run 'python3 build/build_dictionary.py' and 'python3 build/generate_json.py' first.")
        sys.exit(1)

    with DICTIONARY_PATH.open(encoding="utf-8") as f:
        entries = json.load(f)

    # Build a set of lowercase graphemes for case-insensitive matching
    graphemes = set()
    for entry in entries:
        grapheme = entry.get("grapheme", "").strip()
        if grapheme:
            graphemes.add(grapheme.lower())
            # Also add aliases (semicolon-separated)
            alias = entry.get("alias", "").strip()
            if alias:
                for a in alias.split(";"):
                    a = a.strip()
                    if a:
                        graphemes.add(a.lower())

    return graphemes


def extract_candidates(text):
    """
    Extract candidate proper nouns from text using a simple heuristic.
    
    Criteria:
    - Starts with uppercase letter
    - Contains at least one lowercase letter (filters out all-caps acronyms like "THE")
    - At least 2 characters
    
    Returns a list of unique candidates (preserving original case for display).
    """
    # Tokenize: split on whitespace and punctuation, keeping words
    tokens = re.findall(r"[A-Za-zÀ-ÿ'']+", text)
    
    candidates = []
    seen = set()
    
    for token in tokens:
        # Must start with uppercase
        if not token[0].isupper():
            continue
        
        # Must contain at least one lowercase letter
        if not any(c.islower() for c in token):
            continue
        
        # Must be at least 2 characters
        if len(token) < 2:
            continue
        
        # Skip common English words that often appear capitalized
        common_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "shall", "can", "this", "that",
            "these", "those", "it", "its", "he", "she", "they", "we", "you", "i",
            "his", "her", "their", "our", "your", "my", "who", "which", "what",
            "when", "where", "why", "how", "if", "then", "so", "as", "not", "no",
            "yes", "all", "some", "any", "each", "every", "both", "few", "many",
            "more", "most", "other", "such", "only", "also", "just", "now", "new",
            "first", "last", "one", "two", "three", "said", "says", "told", "according",
            "president", "minister", "chief", "dr", "mr", "mrs", "ms", "prof",
            "january", "february", "march", "april", "may", "june", "july",
            "august", "september", "october", "november", "december",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        }
        
        if token.lower() in common_words:
            continue
        
        # Deduplicate (case-insensitive)
        key = token.lower()
        if key not in seen:
            seen.add(key)
            candidates.append(token)
    
    return candidates


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/coverage_check.py <path/to/text_file.txt>")
        print()
        print("Example:")
        print("    python3 tools/coverage_check.py samples/ghanaweb_article.txt")
        sys.exit(1)

    text_path = Path(sys.argv[1])
    
    if not text_path.exists():
        print(f"Error: File not found: {text_path}")
        sys.exit(1)

    # Load dictionary
    print("Loading Ninolex-GH dictionary...")
    dictionary = load_dictionary()
    print(f"  {len(dictionary)} unique graphemes/aliases loaded")
    print()

    # Load and process text
    print(f"Processing: {text_path}")
    with text_path.open(encoding="utf-8") as f:
        text = f.read()

    # Basic stats
    all_tokens = re.findall(r"[A-Za-zÀ-ÿ'']+", text)
    total_tokens = len(all_tokens)

    # Extract candidates
    candidates = extract_candidates(text)
    total_candidates = len(candidates)

    # Check coverage
    matched = []
    unmatched = []

    for candidate in candidates:
        if candidate.lower() in dictionary:
            matched.append(candidate)
        else:
            unmatched.append(candidate)

    matched_count = len(matched)
    coverage = (matched_count / total_candidates * 100) if total_candidates > 0 else 0

    # Report
    print()
    print("=" * 60)
    print("COVERAGE REPORT")
    print("=" * 60)
    print(f"  Total tokens in text:      {total_tokens:,}")
    print(f"  Candidate proper nouns:    {total_candidates:,}")
    print(f"  Matched in Ninolex-GH:     {matched_count:,}")
    print(f"  Coverage:                  {coverage:.2f}%")
    print()

    if matched:
        print("-" * 60)
        print("MATCHED CANDIDATES")
        print("-" * 60)
        for m in sorted(matched, key=str.lower):
            print(f"  ✓ {m}")
        print()

    if unmatched:
        print("-" * 60)
        print("UNMATCHED CANDIDATES (potential gaps)")
        print("-" * 60)
        for u in sorted(unmatched, key=str.lower):
            print(f"  ✗ {u}")
        print()
        print(f"Total unmatched: {len(unmatched)}")
        print("Review these for potential additions to the dictionary.")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
