# Ninolex-GH IPA Guide

This guide defines the subset of IPA (International Phonetic Alphabet) and transcription conventions used in Ninolex-GH for Ghanaian English and Ghanaian proper nouns.

The goal is **practical TTS correctness**, not academic phonetic perfection. We aim for transcriptions that help text-to-speech engines produce natural-sounding Ghanaian pronunciations.

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

Ghanaian languages feature labial-velar consonants. Transcribe these as:

| Symbol | Example | Notes |
|--------|---------|-------|
| `kp` | "Kpando" | Voiceless labial-velar plosive |
| `gb` | "Agbogbloshie" | Voiced labial-velar plosive |

Optionally use the tie bar (`k͡p`, `ɡ͡b`) for explicit notation, but `kp` and `gb` are acceptable for readability.

#### Palatal nasal

| Symbol | Example | Notes |
|--------|---------|-------|
| `ɲ` | "Sunyani" | Palatal nasal (like Spanish "ñ") |

---

## Stress and syllabification

### Primary stress

Mark primary stress with `ˈ` **before** the stressed syllable:

- `əˈkraː` – Accra
- `kuˈmɑːsi` – Kumasi
- `ˈdum.sɔ` – dumsor

### Secondary stress (optional)

Use `ˌ` for secondary stress in longer words:

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

---

## Validation

All phoneme values are validated using:

```bash
python3 tests/validate_ipa.py
```

This script checks that only approved IPA characters are used. If you need to add a new symbol, update both this guide and the `ALLOWED_CHARS` set in `tests/validate_ipa.py`.

---

## Contributing IPA transcriptions

1. Read this guide before adding or editing phoneme values.
2. Use consistent symbols from the approved set.
3. When uncertain, open an issue or PR with your reasoning.
4. Maintainers may run `python3 tests/validate_ipa.py` on contributions.

For more details on the contribution workflow, see [CONTRIBUTING.md](CONTRIBUTING.md).
