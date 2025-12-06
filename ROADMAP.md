# Ninolex-GH Roadmap

## Vision

Ninolex-GH aims to be the canonical, open pronunciation dictionary for Ghanaian English and Ghanaian proper nouns – optimised for TTS engines, LLMs, and education products.

The long-term goal is to provide high-quality, machine-readable pronunciations for:

- Ghanaian names (Akan, Ewe, Ga, etc.)
- Towns, regions, constituencies and localities
- Secondary schools, universities and institutions
- Public figures, MPs, judges, footballers and cultural icons
- Foods, slang, and exam-related terms

---

## Current status (v0.1.x)

- Core exam terms (WASSCE, BECE, etc.)
- Selected foods and slang (waakye, dumsor, etc.)
- Regions and key towns
- Seed set of constituencies
- Seed set of football clubs
- Seed set of public figures and complex personal names
- **Seed set of SHS and universities** (new)
- Unified dictionary export (CSV + JSON)
- PLS export for TTS engines
- **IPA validation tooling with tie-bar checks** (enhanced)
- **IPA style guide with accent policy** (enhanced)
- **Quality tooling stubs** (coverage check, Golden 100 template)

---

## Near-term milestones

### v0.2.0 – Education & geography expansion

- Add full list of SHS names and common abbreviations
- Add richer metadata for regions and towns
- Expand town coverage to more district capitals
- Normalise IPA conventions for common name patterns (e.g. "Nii", "Osei", "Adwoa")
- Improve IPA validation with more comprehensive character checks
- Begin populating the "Golden 100" reference list

### v0.3.0 – Politics & governance

- Add all constituencies with standard IPA
- Add all presidents and vice presidents
- Add a curated list of MPs and key public officials
- Add Supreme Court justices (past and present)

### v0.4.0 – Sports & culture

- Expand Ghana Premier League and historical clubs
- Add extended list of Black Stars / Black Queens players and coaches
- Add culturally significant figures (musicians, authors, etc.)

---

## Data model enhancements (future)

These fields are under consideration for future schema versions:

### `variant_lang`

A language code indicating the origin language of a name:

- `ak` – Akan (Twi, Fante)
- `ee` – Ewe
- `ga` – Ga
- `dag` – Dagbani
- `en` – English

This would help consumers filter or style pronunciations by language family.

### `confidence_score`

A numeric score (0.0–1.0) indicating transcription confidence:

- `1.0` – Verified by native speaker or linguist
- `0.8` – High confidence, standard pattern
- `0.5` – Inferred or auto-generated, needs review

This would help downstream users prioritise verified entries.

### Backwards compatibility

Any schema changes will be additive. Existing fields (`grapheme`, `phoneme`, `domain`, etc.) will remain stable. New optional fields will be introduced with sensible defaults or empty values.

---

## Packaging & distribution (future)

### Versioning scheme

- Define and adopt a **CalVer-style versioning scheme** (e.g. `2025.12.05`) for packaged releases so that data snapshots are clearly identifiable
- Code-only changes may share the same data version with a patch suffix (e.g. `2025.12.05.1`)
- See [DESIGN_NOTES.md](DESIGN_NOTES.md) for rationale

### PyPI package

A Python package (`ninolex-gh`) exposing:

- `load_dictionary()` – Returns all entries as a list of dicts
- `lookup(grapheme)` – Returns phoneme and metadata for a term
- `search(query)` – Fuzzy search across graphemes

Installation:

```bash
pip install ninolex-gh
```

### npm package

A JavaScript/TypeScript package (`ninolex-gh`) exposing:

- Full dictionary as JSON
- "Lite" dictionary with just grapheme/phoneme pairs
- TypeScript types for dictionary entries

Installation:

```bash
npm install ninolex-gh
```

### Versioned releases

Each package version would correspond to a tagged Git release using CalVer.

---

## Quality & coverage tooling (future)

### Golden 100

A curated list of 100 high-priority entries that should have:

- Human-verified IPA transcriptions
- Optional: reference audio recordings for pronunciation validation

Template available at `tools/golden_100_template.txt`.

### Coverage estimation

A script (`tools/coverage_check.py`) to estimate dictionary coverage against sample Ghanaian news text. Helps identify gaps in coverage.

### Audio reference (long-term)

Future consideration: recording reference audio for Golden 100 entries to validate TTS output quality.

---

## Hosted API (future vision)

A future Ninolex API could:

- Accept text input and return SSML with IPA tags for recognized entities
- Provide pronunciation lookups via REST or GraphQL
- Support batch processing for large documents

This is a long-term goal, not committed for v0.x releases.

---

## Contributions welcome

If you want to help:

- See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new entries and follow IPA rules.
- See [IPA_GUIDE.md](IPA_GUIDE.md) for transcription conventions.
- Open issues for specific gaps (e.g. "Add all schools in Ashanti Region", "Add Ewe given names").
