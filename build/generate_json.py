#!/usr/bin/env python3
"""
Generate JSON export of the unified Ninolex-GH dictionary.

Reads dist/dictionary/ninolex_gh_dictionary.csv and writes
dist/dictionary/ninolex_gh_dictionary.json with proper UTF-8 encoding.
"""

from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent.parent
DICT_DIR = ROOT / "dist" / "dictionary"
CSV_PATH = DICT_DIR / "ninolex_gh_dictionary.csv"
JSON_PATH = DICT_DIR / "ninolex_gh_dictionary.json"


def ensure_dictionary():
    """
    Ensure the unified dictionary CSV exists.
    If not, build it by importing build_dictionary.
    """
    if not CSV_PATH.exists():
        print("Dictionary CSV not found. Building from source CSVs...")
        from build_dictionary import build_dictionary
        build_dictionary()


def generate_json():
    """
    Read the unified dictionary CSV and export it as JSON.
    Uses explicit UTF-8 encoding and proper newline handling.
    """
    ensure_dictionary()

    entries = []
    # Use utf-8 encoding with newline="" for proper CSV handling
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grapheme = row.get("grapheme", "").strip()
            phoneme = row.get("phoneme", "").strip()

            # Skip invalid entries
            if not grapheme or not phoneme:
                continue

            # Preserve all fields exactly as they appear
            entry = {
                "grapheme": grapheme,
                "phoneme": phoneme,
                "domain": row.get("domain", "").strip(),
                "category": row.get("category", "").strip(),
                "region": row.get("region", "").strip(),
                "city": row.get("city", "").strip(),
                "alias": row.get("alias", "").strip(),
                "notes": row.get("notes", "").strip(),
                "source_file": row.get("source_file", "").strip(),
            }
            entries.append(entry)

    # Write JSON with UTF-8 encoding and readable formatting
    # ensure_ascii=False preserves IPA characters correctly
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Wrote {JSON_PATH} with {len(entries)} entries")
    return len(entries)


if __name__ == "__main__":
    generate_json()
