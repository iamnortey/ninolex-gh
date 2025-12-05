# Changelog

All notable changes to this project will be documented in this file.

## [v0.1.0] - 2025-12-05

### Added

- Initial unified pronunciation dictionary for Ghanaian English and Ghanaian proper nouns.
- Domain-based CSV sources under `data/`:
  - `data/core/` – core terms (exams, institutions, foods, slang, etc.)
  - `data/places/` – regions, towns, constituencies
  - `data/sports/` – football clubs and sports-related entities
  - `data/people/` – public figures and complex personal names
  - `data/education/` – placeholder for secondary schools and related entities
- Unified dictionary exports:
  - CSV: `dist/dictionary/ninolex_gh_dictionary.csv`
  - JSON: `dist/dictionary/ninolex_gh_dictionary.json`
  - PLS: `exports/ninolex_gh_core.pls` (for TTS engines such as ElevenLabs)
- Build scripts:
  - `build/build_dictionary.py`
  - `build/generate_json.py`
  - `build/generate_pls.py`
- Documentation:
  - `README.md` – overview, quick starts, repository structure and usage
  - `ROADMAP.md` – vision and planned milestones
  - `CONTRIBUTING.md` – contributor workflow and IPA guidelines
- Licensing and repo hygiene:
  - MIT License in `LICENSE`
  - Basic `.gitignore` for Python, macOS, and IDE files

### Notes

- This release establishes Ninolex-GH as a v0.1.0 "foundation" for Ghanaian pronunciation coverage.
- Future releases will expand schools, constituencies, public figures, and sports coverage as described in the roadmap.
