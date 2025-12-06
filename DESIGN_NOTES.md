# Ninolex-GH Design Notes

This document captures high-level design decisions and rationale for Ninolex-GH. It's intended for maintainers and contributors who want to understand the "why" behind the current architecture.

---

## Schema design

### Current schema (v0.1.x)

The unified dictionary uses these fields:

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `grapheme` | string | Yes | The written form (spelling) |
| `phoneme` | string | Yes | IPA transcription |
| `domain` | string | Yes | Category group (core, places, people, sports, education) |
| `category` | string | No | Subcategory (e.g. "shs", "city", "public_figure") |
| `region` | string | No | Ghana region (for places/institutions) |
| `city` | string | No | City or town |
| `alias` | string | No | Common abbreviation or nickname |
| `notes` | string | No | Additional context |
| `source_file` | string | Auto | Path to source CSV (for traceability) |

### Why this schema?

1. **Simplicity**: Flat structure, no nested objects, easy to consume in any language.
2. **Domain separation**: The `domain` field allows filtering by category while keeping a single unified export.
3. **TTS focus**: `grapheme` and `phoneme` are the primary fields; everything else is metadata.
4. **Traceability**: `source_file` lets consumers trace entries back to their source CSV.

### Future schema extensions

We're considering these optional fields for future versions:

- **`variant_lang`**: Language family code (e.g. `ak` for Akan, `ee` for Ewe)
- **`confidence_score`**: Transcription quality indicator (0.0–1.0)

Any new fields will be:

- **Additive**: Existing fields remain unchanged
- **Optional**: Empty/null values for entries without the new data
- **Documented**: Added to this file and the schema docs

---

## IPA conventions

### Why a strict character set?

TTS engines vary in their IPA support. By defining a conservative character set:

1. We ensure broad compatibility across engines (ElevenLabs, AWS Polly, Google TTS, etc.)
2. We avoid exotic symbols that might be rendered incorrectly
3. We maintain consistency across contributors

### Ghana-specific choices

- **Labial-velars**: We use `kp` and `gb` (not `k͡p`, `ɡ͡b`) for readability
- **Affricates**: We use `tʃ` and `dʒ` (not `tɕ`, `dʑ`) for Ghanaian palatal sounds
- **Stress marking**: Always mark primary stress with `ˈ` for polysyllabic words
- **Syllable dots**: Use `.` for readability, not phonological claims

See [IPA_GUIDE.md](IPA_GUIDE.md) for the full convention set.

---

## Build pipeline

### Why separate build scripts?

```
build_dictionary.py → CSV (unified)
generate_json.py    → JSON
generate_pls.py     → PLS
```

1. **Single source of truth**: All domain CSVs merge into one unified CSV
2. **Multiple formats**: Downstream consumers choose their preferred format
3. **Incremental builds**: You can regenerate just JSON or PLS without re-merging

### Why standard library only?

- Zero dependencies = zero friction for contributors
- Works on any Python 3.x installation
- No `requirements.txt` to maintain

If we ever need dependencies (e.g. for advanced validation), we'll document them clearly.

---

## Backwards compatibility

Once we publish packages (PyPI, npm), backwards compatibility becomes critical:

1. **Schema stability**: Core fields (`grapheme`, `phoneme`) will never change
2. **Additive changes only**: New fields are optional; old consumers ignore them
3. **Semantic versioning**: Breaking changes require major version bumps
4. **Migration guides**: Any breaking change will include upgrade instructions

---

## Why not a database?

We considered SQLite or other databases, but chose flat files because:

1. **Git-friendly**: CSV files diff cleanly and merge reasonably
2. **No dependencies**: No database server or ORM required
3. **Transparency**: Anyone can open a CSV in Excel or a text editor
4. **Portability**: Files work on any platform without setup

For consumers who want database-style queries, the JSON export can be loaded into any in-memory store.

---

## Future API considerations

If we build a hosted API:

1. **Read-only**: The API would serve lookups, not accept edits
2. **Versioned**: API versions would map to dictionary versions
3. **Cached**: Heavy caching since data changes infrequently
4. **SSML output**: Primary use case is generating SSML for TTS

This is a long-term vision, not a v0.x commitment.

---

## Contact

For architecture questions or proposals, open a GitHub issue or reach out to the maintainers.
