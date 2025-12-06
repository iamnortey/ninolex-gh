# Ninolex-GH IPA Guide

This guide defines the subset of IPA (International Phonetic Alphabet) and transcription conventions used in Ninolex-GH for Ghanaian English and Ghanaian proper nouns.

The goal is **practical TTS correctness**, not academic phonetic perfection. We aim for transcriptions that help text-to-speech engines produce natural-sounding Ghanaian pronunciations.

---

## Target accent and scope

Ninolex-GH encodes pronunciations in **formal Ghanaian English** – roughly the accent you would hear from a newsreader on national TV/radio (e.g. GBC, Joy News, Citi FM).

For local names (Twi, Ga, Ewe, etc.), we aim to capture how they are pronounced **in this register**, not in fully localized vernacular speech. The goal is practical intelligibility for TTS and educational tools, not a full phonological description of every Ghanaian language.

### Anglicized vs local forms

When there is a strong Anglicized form versus a local form (e.g. "Osei", "Accra"), prefer the form actually used by educated Ghanaian English speakers in formal contexts.

If both are relevant, you may:

- Use the main `grapheme` for the dominant formal pronunciation
- Use `alias` or `notes` to document alternative vernacular forms (for future expansion)

Example: "Osei" might be pronounced slightly differently in rural Ashanti Twi versus formal Ghanaian English on a news broadcast. We encode the latter.

---

## Accent baseline

Ninolex-GH uses **Ghanaian English** as the baseline accent, with influences from:

- British English (historical colonial influence)
- Local Ghanaian language phonology (Akan, Ewe, Ga, etc.)

When in doubt, favour the pronunciation a well-educated Ghanaian speaker would use in formal contexts (news broadcasts, academic settings, etc.).

---

## Vowels

| Symbol | Example (Ghanaian English) | Notes |
|--------|---------------------------|-------|
| `i` | "machine", "see" | High front unrounded |
| `ɪ` | "bit", "sit" | Near-high front (lax) |
| `e` | "say", "play" | Mid front (can be pure or diphthongal) |
| `ɛ` | "bed", "set" | Open-mid front |
| `æ` | Rare in Ghanaian English | Use sparingly; often replaced by `a` or `ɛ` |
| `a` | "father", "car" | Open front/central |
| `ɑ` | Alternative to `a` | Use consistently if preferred |
| `ɔ` | "bought", "law" | Open-mid back rounded (common in Ghanaian English) |
| `o` | "go", "show" | Mid back rounded |
| `u` | "food", "blue" | High back rounded |
| `ʊ` | "put", "book" | Near-high back rounded (lax) |
| `ə` | "about", "sofa" | Schwa (unstressed syllables) |
| `ʌ` | Rare | Often replaced by `ɔ` or `a` in Ghanaian English |

### Long vowels

Use `ː` after a vowel to indicate length:

- `iː` – "see"
- `uː` – "food"
- `ɔː` – "bought" (if distinguishing length)
- `aː` – extended "a" sound

### Diphthongs

Transcribe diphthongs as vowel sequences:

- `aɪ` – "buy", "my"
- `aʊ` – "now", "how"
- `ɔɪ` – "boy", "toy"
- `eɪ` – "say", "day"
- `oʊ` – "go", "show"

---

## Consonants

### Standard consonants

| Symbol | Example | Notes |
|--------|---------|-------|
| `p` | "pen" | Voiceless bilabial plosive |
| `b` | "bed" | Voiced bilabial plosive |
| `t` | "ten" | Voiceless alveolar plosive |
| `d` | "den" | Voiced alveolar plosive |
| `k` | "cat" | Voiceless velar plosive |
| `g` | "go" | Voiced velar plosive |
| `f` | "fat" | Voiceless labiodental fricative |
| `v` | "van" | Voiced labiodental fricative |
| `s` | "sit" | Voiceless alveolar fricative |
| `z` | "zoo" | Voiced alveolar fricative |
| `ʃ` | "ship" | Voiceless postalveolar fricative |
| `ʒ` | "measure" | Voiced postalveolar fricative |
| `h` | "hat" | Voiceless glottal fricative |
| `m` | "man" | Bilabial nasal |
| `n` | "no" | Alveolar nasal |
| `ŋ` | "sing" | Velar nasal |
| `l` | "let" | Alveolar lateral |
| `r` | "red" | Alveolar approximant (or tap `ɾ`) |
| `w` | "wet" | Labio-velar approximant |
| `j` | "yes" | Palatal approximant |

### Affricates

| Symbol | Example | Notes |
|--------|---------|-------|
| `tʃ` | "church", "Kyebi" | Voiceless postalveolar affricate |
| `dʒ` | "judge", "Adwoa" | Voiced postalveolar affricate |

**Convention**: Use `tʃ` and `dʒ` for Ghanaian "Ky-" and "Gy-" sounds respectively. Avoid `tɕ` and `dʑ` unless specifically needed for a more palatal quality.

### Ghana-specific consonants

#### Labial-velars

Ghanaian languages feature labial-velar consonants. These are **single articulations**, not sequences.

| Symbol | Example | Notes |
|--------|---------|-------|
| `k͡p` | "Kpando" | Voiceless labial-velar plosive |
| `ɡ͡b` | "Agbogbloshie" | Voiced labial-velar plosive |

**Convention**: Use the tie bar (`k͡p`, `ɡ͡b`) to explicitly mark these as single segments. The validator will warn if bare `kp` or `gb` sequences are found without tie-bars.

Alternative tie-bar: `͜` (U+035C) is also acceptable: `k͜p`, `ɡ͜b`.

#### Palatal nasal

| Symbol | Example | Notes |
|--------|---------|-------|
| `ɲ` | "Sunyani" | Palatal nasal (like Spanish "ñ") |

### Syllabic consonants and difficult clusters

Names like "Nkansah" and "Mampong" can involve syllabic nasals or implied vowels.

For now, Ninolex-GH uses a practical approach for TTS:

- We may prefer slightly "smoothed" pronunciations that TTS engines can handle reliably
- Where syllabic consonants are clearly needed, we use the IPA syllabic marker `̩` (combining vertical line below)

Example: A syllabic `n` would be written as `n̩`.

Contributors should follow existing patterns in the dictionary and, when in doubt, open an issue for discussion.

---

## Stress and syllabification

### Primary stress

Mark primary stress with `ˈ` (U+02C8) **before** the stressed syllable:

- `əˈkraː` – Accra
- `kuˈmɑːsi` – Kumasi
- `ˈdum.sɔ` – dumsor

**Important**: Do NOT use the ASCII apostrophe `'` (U+0027). The validator will reject it.

### Secondary stress (optional)

Use `ˌ` (U+02CC) for secondary stress in longer words:

- `ˌableˈkuma` – Ablekuma

### Syllable separators

Use `.` (dot) to separate syllables for readability:

- `ˈdum.sɔ` – dumsor
- `ˈwa.tʃe` – waakye

This is for **readability**, not a strict phonological claim. Use dots where they help TTS engines parse multi-syllable words.

---

## Examples

| Grapheme | Phoneme | Notes |
|----------|---------|-------|
| dumsor | `ˈdum.sɔ` | Power outages (slang) |
| waakye | `ˈwa.tʃe` | Rice and beans dish |
| Accra | `əˈkraː` | Capital city |
| Kumasi | `kuˈmɑːsi` | Ashanti regional capital |
| Sunyani | `suˈɲani` | Bono regional capital |
| Kwame | `ˈkwame` | Akan male day name (Saturday) |
| Adwoa | `ˈadʒwa` | Akan female day name (Monday) |
| Dzigbordi | `dʒiɡˈbɔːdi` | Ewe female name |
| PRESEC | `ˈprɛsɛk` | Presbyterian Boys' Secondary School |
| Kpando | `k͡panˈdo` | Town in Volta Region (labial-velar) |

---

## Validation

All phoneme values are validated using:

```bash
python3 tests/validate_ipa.py
```

This script performs two checks:

1. **Character validation**: Ensures only approved IPA characters are used
2. **Tie-bar check**: Warns about labial-velar sequences (`kp`, `gb`) that lack tie-bars

If you need to add a new symbol, update both this guide and the `ALLOWED_CHARS` set in `tests/validate_ipa.py`.

---

## Contributing IPA transcriptions

1. Read this guide before adding or editing phoneme values.
2. Use consistent symbols from the approved set.
3. For labial-velars, always use tie-bars: `k͡p`, `ɡ͡b`.
4. Use `ˈ` (U+02C8) for stress, never `'` (U+0027).
5. When uncertain, open an issue or PR with your reasoning.
6. Maintainers will run `python3 tests/validate_ipa.py` on contributions.

For more details on the contribution workflow, see [CONTRIBUTING.md](CONTRIBUTING.md).
