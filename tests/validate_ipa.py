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

Checks performed:
    1. Character validation against approved IPA subset
    2. Tie-bar check for labial-velars (kp, gb should use k͡p, ɡ͡b)
    3. Stress marker validation (no ASCII apostrophe allowed)
"""

import json
import re
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
# Includes ɒ (U+0252) and ɜ (U+025C) for British English-influenced Ghanaian pronunciations
VOWELS = set("aeiouɪʊɛɔəɑæʌɒɜ")

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
# Tie bars: ͡ (U+0361) and ͜ (U+035C) join them
# Also include both 'g' (U+0067) and 'ɡ' (U+0261) for flexibility
TIE_BARS = set("͜͡")
LABIAL_VELAR_PARTS = set("ɡ") | TIE_BARS

# Stress and prosody markers
# ˈ (U+02C8) - primary stress
# ˌ (U+02CC) - secondary stress
# NOTE: ASCII apostrophe ' (U+0027) is NOT allowed
STRESS_MARKERS = set("ˈˌ")

# Syllable separators and spacing
SEPARATORS = set(". -")

# Nasalization and other diacritics
# Including syllabic marker ̩ (U+0329) for syllabic consonants like n̩
DIACRITICS = set("̩̃̀́̂̄")  # combining tilde, accents, syllabic marker

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

# ==============================================================================
# FORBIDDEN CHARACTERS
# ==============================================================================
# These characters are explicitly forbidden and should trigger errors

# ASCII apostrophe - often mistakenly used instead of IPA stress marker
FORBIDDEN_CHARS = set("'")  # U+0027


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
        # Check for explicitly forbidden characters first
        if char in FORBIDDEN_CHARS:
            invalid.add(char)
        elif char not in ALLOWED_CHARS:
            invalid.add(char)
    return invalid


def check_tiebar_labial_velars(phoneme):
    """
    Check for labial-velar sequences (kp, gb) that lack a tie-bar.
    
    Proper forms: k͡p, k͜p, ɡ͡b, g͡b, ɡ͜b, g͜b
    Suspicious forms: kp, gb (without tie-bar between them)
    
    Returns:
        A list of suspicious sequences found, or empty list if clean.
    """
    issues = []
    
    # Pattern for kp without tie-bar
    # Match 'k' followed by 'p' but NOT with a tie-bar in between
    if re.search(r'k(?![͜͡])p', phoneme):
        issues.append("'kp' without tie-bar (should be 'k͡p' or 'k͜p')")
    
    # Pattern for gb without tie-bar
    # Match 'g' or 'ɡ' followed by 'b' but NOT with a tie-bar in between
    if re.search(r'[gɡ](?![͜͡])b', phoneme):
        issues.append("'gb' without tie-bar (should be 'ɡ͡b' or 'g͡b')")
    
    return issues


def main():
    """Run IPA validation on all dictionary entries."""
    print("=" * 70)
    print("Ninolex-GH IPA Validation")
    print("=" * 70)
    print()

    entries = load_dictionary()
    print(f"Loaded {len(entries)} entries from dictionary")
    print()

    char_errors = []
    tiebar_warnings = []

    for entry in entries:
        grapheme = entry.get("grapheme", "")
        phoneme = entry.get("phoneme", "")
        source_file = entry.get("source_file", "unknown")
        
        # Check 1: Invalid characters
        invalid_chars = validate_phoneme(phoneme)
        if invalid_chars:
            char_errors.append({
                "grapheme": grapheme,
                "phoneme": phoneme,
                "invalid_chars": invalid_chars,
                "source_file": source_file,
            })
        
        # Check 2: Tie-bar for labial-velars
        tiebar_issues = check_tiebar_labial_velars(phoneme)
        if tiebar_issues:
            tiebar_warnings.append({
                "grapheme": grapheme,
                "phoneme": phoneme,
                "issues": tiebar_issues,
                "source_file": source_file,
            })

    # ==== Report: Character validation ====
    print("-" * 70)
    print("1. CHARACTER VALIDATION")
    print("-" * 70)
    
    if char_errors:
        print(f"❌ Found {len(char_errors)} entries with invalid IPA characters:")
        print()
        
        for err in char_errors:
            print(f"  Grapheme: {err['grapheme']}")
            print(f"  Phoneme:  {err['phoneme']}")
            # Show hex codes for debugging
            invalid_with_codes = [f"'{c}' (U+{ord(c):04X})" for c in sorted(err['invalid_chars'])]
            print(f"  Invalid:  {', '.join(invalid_with_codes)}")
            print(f"  Source:   {err['source_file']}")
            print()
        
        print(f"Total character errors: {len(char_errors)}")
        print()
        print("Note: If ' (U+0027 ASCII apostrophe) appears, replace with ˈ (U+02C8)")
    else:
        print("✅ All phonemes contain only allowed IPA characters")
    
    print()
    
    # ==== Report: Tie-bar check ====
    print("-" * 70)
    print("2. TIE-BAR CHECK (labial-velars)")
    print("-" * 70)
    
    if tiebar_warnings:
        print(f"⚠️  Found {len(tiebar_warnings)} entries with potential labial-velar issues:")
        print()
        
        for warn in tiebar_warnings:
            print(f"  Grapheme: {warn['grapheme']}")
            print(f"  Phoneme:  {warn['phoneme']}")
            for issue in warn['issues']:
                print(f"  Issue:    {issue}")
            print(f"  Source:   {warn['source_file']}")
            print()
        
        print(f"Total tie-bar warnings: {len(tiebar_warnings)}")
        print()
        print("These are warnings only. Review and add tie-bars if appropriate.")
        print("See IPA_GUIDE.md for labial-velar conventions.")
    else:
        print("✅ No labial-velar tie-bar issues detected")
    
    print()
    
    # ==== Summary ====
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Entries validated: {len(entries)}")
    print(f"  Character errors:  {len(char_errors)}")
    print(f"  Tie-bar warnings:  {len(tiebar_warnings)}")
    print()
    
    # Exit code based on character errors only (not warnings)
    if char_errors:
        print("Please review IPA_GUIDE.md and correct the errors above.")
        print("If a character is legitimately needed, add it to ALLOWED_CHARS")
        print("in tests/validate_ipa.py")
        sys.exit(1)
    else:
        print("✅ Validation passed (warnings may still need attention)")
        sys.exit(0)


if __name__ == "__main__":
    main()
