import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS_DIR = ROOT / "exports"
DICTIONARY_PATH = ROOT / "dist" / "dictionary" / "ninolex_gh_dictionary.csv"

EXPORTS_DIR.mkdir(exist_ok=True)


def ensure_dictionary():
    """
    Ensure the unified dictionary exists.
    If not, build it by importing build_dictionary.
    """
    if not DICTIONARY_PATH.exists():
        print("Dictionary not found. Building from source CSVs...")
        from build_dictionary import build_dictionary
        build_dictionary()


def load_entries_from_dictionary():
    """
    Load entries from the unified dictionary CSV.
    Returns a list of (grapheme, phoneme) tuples.
    """
    entries = []
    with DICTIONARY_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grapheme = row.get("grapheme", "").strip()
            phoneme = row.get("phoneme", "").strip()
            if not grapheme or not phoneme:
                continue
            entries.append((grapheme, phoneme))
    return entries


def write_pls(entries, output_path, lang="en-GH"):
    """Write entries to a W3C PLS file."""
    with output_path.open("w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(
            f'<lexicon version="1.0" alphabet="ipa" xml:lang="{lang}" '
            'xmlns="http://www.w3.org/2005/01/pronunciation-lexicon">\n\n'
        )
        for grapheme, phoneme in entries:
            f.write(
                f'  <lexeme><grapheme>{grapheme}</grapheme>'
                f'<phoneme>{phoneme}</phoneme></lexeme>\n'
            )
        f.write('\n</lexicon>\n')


def build_core():
    """
    Build the core PLS file from the unified dictionary.
    Deduplicates by grapheme (case-insensitive).
    """
    # Ensure dictionary exists
    ensure_dictionary()

    # Load and deduplicate entries
    entries = []
    seen = set()

    for grapheme, phoneme in load_entries_from_dictionary():
        key = grapheme.lower()
        if key in seen:
            continue
        seen.add(key)
        entries.append((grapheme, phoneme))

    # Write PLS
    out = EXPORTS_DIR / "ninolex_gh_core.pls"
    write_pls(entries, out)
    print(f"Wrote {out} with {len(entries)} entries")


if __name__ == "__main__":
    build_core()
