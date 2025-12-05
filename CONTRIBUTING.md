# Contributing to Ninolex-GH

Thank you for your interest in improving Ninolex-GH. This project is intended to be a high-quality, curated pronunciation dictionary for Ghanaian English and Ghanaian proper nouns.

---

## How the data is organised

- **Source of truth**: CSV files under `data/`
  - `data/core/` – core terms (exams, institutions, foods, slang, etc.)
  - `data/places/` – regions, towns, constituencies
  - `data/sports/` – football clubs and sports-related entities
  - `data/people/` – public figures and complex personal names
- **Unified dictionary**: built under `dist/dictionary/` via:
  - `python3 build/build_dictionary.py`
- **Exports**:
  - JSON: `dist/dictionary/ninolex_gh_dictionary.json`
  - PLS: `exports/ninolex_gh_core.pls`

Contributors should **edit only the CSV files under `data/`**. The unified dictionary and exports are generated.

---

## Workflow for making changes

1. **Fork** the repository on GitHub and clone your fork.

2. Create a **feature branch**, for example:

```bash
git checkout -b feature/add-ashanti-schools
```

3. Edit the relevant CSV file(s) under `data/`:
   - Keep the header row unchanged.
   - Add new rows at the bottom.
   - Avoid duplicate grapheme values within the same file.

4. Regenerate the dictionary and exports:

```bash
python3 build/build_dictionary.py
python3 build/generate_json.py
python3 build/generate_pls.py
```

5. Optionally run any basic checks (e.g. ensure no obvious encoding issues or broken CSV syntax).

6. Commit your changes and push your branch to your fork.

7. Open a **Pull Request** against the `main` branch of the upstream repository with:
   - A clear title (e.g. "Add more constituencies in Volta Region")
   - A short description of what you changed and why.

---

## IPA and pronunciation guidelines

Ninolex-GH uses IPA (`alphabet="ipa"`) in the `phoneme` column.

### General rules

- Use consistent IPA notations for Ghanaian English vowels and consonants.
- Reflect Ghanaian usage and stress patterns, not British or American defaults.
- For multi-word entries, use a reasonable segmentation with dots if helpful, for example:
  - `ˈdum.sɔ` for "dumsor"
  - `əˈkraː` for "Accra"
- Avoid over-complicating phonetic detail; aim for a practical balance that TTS engines can use reliably.
- If you are unsure about a particular name, open an issue or PR and explain your reasoning so maintainers can help refine the IPA.

---

## Code and scripts

If you modify any of the Python build scripts under `build/`:

- Keep the code simple and dependency-free (standard library only).
- Make sure the scripts still run on a plain Python 3.x installation.
- Test by re-running the three core commands:

```bash
python3 build/build_dictionary.py
python3 build/generate_json.py
python3 build/generate_pls.py
```

---

## Reporting issues

Use GitHub Issues to report:

- Incorrect or unnatural pronunciations
- Missing categories (e.g. important schools, towns, institutions)
- Bugs in the build scripts
- Ideas for new features or exports

Please include specific examples (grapheme, expected pronunciation, and any references) when reporting pronunciation issues.

