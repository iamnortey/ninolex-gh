# Ninolex GH – The Ghanaian Pronunciation Dictionary

**Ninolex GH** is an open, machine-readable pronunciation dictionary focused on **Ghanaian English and Ghanaian proper nouns**.

The goal is simple:

> Make text-to-speech systems pronounce Ghanaian names, places, schools, foods and institutions the way real Ghanaians do.

This project is maintained by Ninobyte and the community, and is designed to be:

- **LLM-friendly** – easy to consume from AI/ML pipelines  
- **TTS-friendly** – exportable to W3C PLS (`.pls`) for engines like ElevenLabs  
- **Country-scalable** – future variants like `Ninolex-NG`, `Ninolex-KE`, etc.

---

## Repository structure

```text
data/
  core/
    core_terms.csv         # exams, institutions, food, slang, generic Ghana terms
  places/
    regions.csv            # regions
    towns.csv              # capitals + major towns
    constituencies.csv     # electoral constituencies
  people/
    public_figures.csv     # presidents, Big Six, judges, footballers
    complex_names.csv      # Ghanaian names often mispronounced by TTS
  sports/
    football_clubs.csv     # Ghana Premier League clubs
  education/
    shs.csv                # secondary schools + nicknames (coming soon)

build/
  build_dictionary.py      # script to merge domain CSVs → unified dictionary
  generate_pls.py          # script to compile dictionary → PLS exports
  generate_json.py         # script to export dictionary as JSON

dist/
  dictionary/
    ninolex_gh_dictionary.csv    # unified dictionary (auto-generated)
    ninolex_gh_dictionary.json   # JSON export (auto-generated)

exports/
  # generated PLS files will be written here
  # e.g. ninolex_gh_core.pls
```

### Dictionary view vs domain sources

All canonical entries are maintained in domain-specific CSVs under `data/` (core terms, places, people, sports, etc.).
These are merged into a single unified dictionary file.

The unified dictionary is available in both CSV and JSON formats:

- CSV: `dist/dictionary/ninolex_gh_dictionary.csv`
- JSON: `dist/dictionary/ninolex_gh_dictionary.json`

Tooling such as PLS exports read from this unified dictionary, so downstream users can treat Ninolex-GH as one dictionary, while maintainers still benefit from organized domain files.

To rebuild the dictionary:

```bash
python3 build/build_dictionary.py
```

To generate the PLS export (will auto-build dictionary if missing):

```bash
python3 build/generate_pls.py
```

To generate the JSON export (will auto-build dictionary if missing):

```bash
python3 build/generate_json.py
```
