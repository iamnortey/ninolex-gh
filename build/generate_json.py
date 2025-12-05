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
    """
    ensure_dictionary()

    entries = []
    with CSV_PATH.open(encoding="utf-8") as f:
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
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Wrote {JSON_PATH} with {len(entries)} entries")


if __name__ == "__main__":
    generate_json()

