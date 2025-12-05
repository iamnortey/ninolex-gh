import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DIST_DIR = ROOT / "dist"
DICTIONARY_DIR = DIST_DIR / "dictionary"

# Source files with their domain assignments
SOURCE_FILES = [
    ("data/core/core_terms.csv", "core"),
    ("data/places/regions.csv", "places"),
    ("data/places/towns.csv", "places"),
    ("data/places/constituencies.csv", "places"),
    ("data/sports/football_clubs.csv", "sports"),
    ("data/people/public_figures.csv", "people"),
    ("data/people/complex_names.csv", "people"),
]

# Unified dictionary schema
DICTIONARY_FIELDS = [
    "grapheme",
    "phoneme",
    "domain",
    "category",
    "region",
    "city",
    "alias",
    "notes",
    "source_file",
]


def ensure_directories():
    """Create dist/dictionary if it doesn't exist."""
    DIST_DIR.mkdir(exist_ok=True)
    DICTIONARY_DIR.mkdir(exist_ok=True)


def load_and_normalize(csv_path, domain):
    """
    Load entries from a CSV and normalize them to the unified schema.
    Returns a list of dictionaries with DICTIONARY_FIELDS keys.
    """
    entries = []
    full_path = ROOT / csv_path

    if not full_path.exists():
        return entries

    with full_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grapheme = row.get("grapheme", "").strip()
            phoneme = row.get("phoneme", "").strip()

            # Skip invalid entries
            if not grapheme or not phoneme:
                continue

            # Build normalized entry
            entry = {
                "grapheme": grapheme,
                "phoneme": phoneme,
                "domain": domain,
                "category": row.get("category", "").strip(),
                "region": row.get("region", "").strip(),
                "city": row.get("city", "").strip(),
                "alias": row.get("alias", "").strip(),
                "notes": row.get("notes", "").strip(),
                "source_file": csv_path,
            }
            entries.append(entry)

    return entries


def build_dictionary():
    """
    Merge all domain CSVs into a single unified dictionary file.
    Returns the number of entries written.
    """
    ensure_directories()

    all_entries = []
    files_processed = 0

    for csv_path, domain in SOURCE_FILES:
        entries = load_and_normalize(csv_path, domain)
        if entries:
            all_entries.extend(entries)
            files_processed += 1

    # Write unified dictionary
    output_path = DICTIONARY_DIR / "ninolex_gh_dictionary.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=DICTIONARY_FIELDS)
        writer.writeheader()
        writer.writerows(all_entries)

    print(f"Built {output_path} with {len(all_entries)} entries from {files_processed} source files")
    return len(all_entries)


if __name__ == "__main__":
    build_dictionary()

