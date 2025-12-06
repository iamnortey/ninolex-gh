#!/usr/bin/env python3
"""
IPA Validation Script for Ninolex-GH

This script validates that all phoneme values in the unified dictionary
contain only allowed IPA characters and separators.

Usage:
    python3 tests/validate_ipa.py

Exit codes:
    0 - All phonemes are valid
    1 - One or more phonemes contain invalid characters
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICTIONARY_PATH = ROOT / "dist" / "dictionary" / "ninolex_gh_dictionary.json"

# ==============================================================================
# ALLOWED IPA CHARACTER SET FOR NINOLEX-GH
# ==============================================================================
# This defines the subset of IPA symbols approved for Ghanaian English
# transcriptions. See IPA_GUIDE.md for full conventions.

# Vowels (monophthongs and common diphthong components)
VOWELS = set("aeiouɪʊɛɔəɑæʌ")

# Long vowel marker
LENGTH = set("ː")

# Consonants
CONSONANTS = set(
    "bdfghjklmnpqrstvwxyzŋʃʒθðɲɾʔ"
)

# Affricates and special consonants (individual characters)
# tʃ, dʒ, tɕ, dʑ are composed of these
AFFRICATE_PARTS = set("tɕdʑ")

# Labial-velars (k͡p, ɡ͡b) - component characters
# The tie bar ͡ (U+0361) joins them
LABIAL_VELAR_PARTS = set("ɡ͡")

# Stress and prosody markers
STRESS_MARKERS = set("ˈˌ")

# Syllable separators and spacing
SEPARATORS = set(". -")

# Nasalization and other diacritics
DIACRITICS = set("̃̀́̂̄")  # combining tilde, combining accents

# Whitespace (for multi-word entries)
WHITESPACE = set(" ")

# Combine all allowed characters
ALLOWED_CHARS = (
    VOWELS
    | LENGTH
    | CONSONANTS
    | AFFRICATE_PARTS
    | LABIAL_VELAR_PARTS
    | STRESS_MARKERS
    | SEPARATORS
    | DIACRITICS
    | WHITESPACE
)


def load_dictionary():
    """Load the unified dictionary JSON."""
    if not DICTIONARY_PATH.exists():
        print(f"Error: Dictionary not found at {DICTIONARY_PATH}")
        print("Run 'python3 build/build_dictionary.py' and 'python3 build/generate_json.py' first.")
        sys.exit(1)

    with DICTIONARY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def validate_phoneme(phoneme):
    """
    Check if a phoneme string contains only allowed characters.
    
    Returns:
        A set of invalid characters found, or empty set if valid.
    """
    invalid = set()
    for char in phoneme:
        if char not in ALLOWED_CHARS:
            invalid.add(char)
    return invalid


def main():
    """Run IPA validation on all dictionary entries."""
    print("=" * 60)
    print("Ninolex-GH IPA Validation")
    print("=" * 60)
    print()

    entries = load_dictionary()
    print(f"Loaded {len(entries)} entries from dictionary")
    print()

    errors = []

    for entry in entries:
        grapheme = entry.get("grapheme", "")
        phoneme = entry.get("phoneme", "")
        
        invalid_chars = validate_phoneme(phoneme)
        
        if invalid_chars:
            errors.append({
                "grapheme": grapheme,
                "phoneme": phoneme,
                "invalid_chars": invalid_chars,
                "source_file": entry.get("source_file", "unknown"),
            })

    if errors:
        print(f"❌ Found {len(errors)} entries with invalid IPA characters:")
        print("-" * 60)
        
        for err in errors:
            print(f"  Grapheme: {err['grapheme']}")
            print(f"  Phoneme:  {err['phoneme']}")
            print(f"  Invalid:  {sorted(err['invalid_chars'])}")
            print(f"  Source:   {err['source_file']}")
            print()
        
        print("-" * 60)
        print(f"Total errors: {len(errors)}")
        print()
        print("Please review IPA_GUIDE.md and correct these entries.")
        print("If a character is legitimately needed, add it to ALLOWED_CHARS")
        print("in tests/validate_ipa.py")
        sys.exit(1)
    else:
        print("✅ All phonemes contain only allowed IPA characters")
        print()
        print(f"Validated {len(entries)} entries successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
