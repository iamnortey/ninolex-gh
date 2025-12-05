# GitHub Issues Seed – Ninolex-GH

This file contains suggested issues that can be created on GitHub to grow Ninolex-GH in line with the roadmap.

---

## Issue 1 – Expand SHS and education coverage

**Title:** Add full SHS list and common abbreviations

**Labels:** enhancement, data, education

**Description:**

Add a comprehensive list of Ghanaian secondary schools (SHS) and their common abbreviations to the `data/education/` domain.

- Add or update a CSV under `data/education/` (for example `shs.csv`).
- Include at least:
  - Official school name
  - Common abbreviation or nickname (if any)
  - Region
  - City/town
  - Suggested IPA for the school name
- Regenerate the unified dictionary and exports using:

  ```bash
  python3 build/build_dictionary.py
  python3 build/generate_json.py
  python3 build/generate_pls.py
  ```

---

## Issue 2 – Complete constituencies coverage

**Title:** Expand and validate Ghanaian constituencies in data/places/constituencies.csv

**Labels:** enhancement, data, geography

**Description:**

Expand `data/places/constituencies.csv` to cover all Ghanaian constituencies with consistent IPA.

- Ensure each row includes:
  - Constituency name
  - Region
  - Optional notes (e.g. major town)
  - IPA pronunciation for the constituency name
- Validate for duplicates and obvious spelling errors.
- Regenerate unified dictionary and exports.

---

## Issue 3 – Presidents and vice presidents

**Title:** Add all Ghanaian presidents and vice presidents to data/people/public_figures.csv

**Labels:** enhancement, data, people

**Description:**

Add all Ghanaian presidents and vice presidents to the public figures dataset.

- For each person, include:
  - Full name
  - Role (e.g. President, Vice President)
  - Approximate period in office (for notes)
  - IPA for the full name using Ghanaian pronunciation conventions
- Regenerate unified dictionary and exports.

---

## Issue 4 – Supreme Court justices (seed set)

**Title:** Add key Ghanaian Supreme Court justices to public figures

**Labels:** enhancement, data, people

**Description:**

Add a curated list of current and notable past Supreme Court justices.

- Extend `data/people/public_figures.csv` or a new relevant people CSV.
- Include:
  - Full name
  - Role/title
  - Notes (e.g. "Chief Justice 20XX–20YY")
  - IPA for the full name
- Regenerate unified dictionary and exports.

---

## Issue 5 – Black Stars / Black Queens players

**Title:** Expand football coverage with Black Stars and Black Queens players

**Labels:** enhancement, data, sports

**Description:**

Add a wider list of notable Black Stars and Black Queens players.

- Extend `data/people/complex_names.csv` or `data/sports/` with player names.
- Include:
  - Full name
  - Role (e.g. striker, midfielder)
  - Notes (optional: club, era)
  - IPA for the full name
- Regenerate unified dictionary and exports.

---

## Issue 6 – CLI lookup tool (optional)

**Title:** Add a simple CLI lookup for Ninolex-GH

**Labels:** enhancement, tooling

**Description:**

Add a small Python CLI tool to query the unified dictionary from the terminal.

- A script (for example under `tools/` or `cli/`) that:
  - Loads `dist/dictionary/ninolex_gh_dictionary.json`
  - Accepts a search term (grapheme) and prints:
    - grapheme
    - phoneme
    - domain
    - any notes
- Document usage briefly in the README.
