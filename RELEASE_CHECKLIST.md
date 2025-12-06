# Ninolex-GH Release Checklist

This checklist must be completed before cutting a release tag or publishing to PyPI.

---

## Pre-Release Validation

### 1. Run the Full Build Pipeline

```bash
cd /path/to/ninolex-gh

# Build unified dictionary from source CSVs
python build/build_dictionary.py

# Generate JSON export
python build/generate_json.py

# Generate PLS export
python build/generate_pls.py
```

**Expected output:**
- `dist/dictionary/ninolex_gh_dictionary.csv` created
- `dist/dictionary/ninolex_gh_dictionary.json` created
- `exports/ninolex_gh_core.pls` created

---

### 2. Run IPA Validator

```bash
python tests/validate_ipa.py
```

**Required outcome:**
- [ ] Character errors: **0**
- [ ] Tie-bar warnings: **0** (or explicitly acknowledged)
- [ ] Exit code: **0**

---

### 3. Sync Package Data

The package ships a snapshot of the dictionary. After rebuilding, sync the data:

```bash
cp dist/dictionary/ninolex_gh_dictionary.json \
   src/ninolex_gh/data/ninolex_gh_dictionary.json
```

**Verify sync:**
```bash
diff dist/dictionary/ninolex_gh_dictionary.json \
     src/ninolex_gh/data/ninolex_gh_dictionary.json
```

Should return no output (files are identical).

---

### 4. Run Package Smoke Test

```bash
PYTHONPATH=src python tools/smoke_test_package.py
```

**Required outcome:**
- [ ] All tests pass
- [ ] Exit code: **0**

---

### 5. Verify Entry Count

```bash
python -c "
import json
with open('dist/dictionary/ninolex_gh_dictionary.json') as f:
    print(f'Total entries: {len(json.load(f))}')
"
```

**Record the count:** ______ entries

- [ ] Entry count is ≥ 100 (production minimum)
- [ ] Entry count matches expectations for this release

---

### 6. Update Documentation

#### CHANGELOG.md

Add a new section at the top:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Data Changes
- Added: [list new entries or domains]
- Modified: [list significant phoneme corrections]
- Removed: [list removed entries, if any]

### Package Changes
- [list any API or tooling changes]

### Entry Count
- Total: NNN entries (+/- NN from previous)
```

#### Version Numbers

Update version in **both** locations:

1. `pyproject.toml`:
   ```toml
   version = "X.Y.Z"
   ```

2. `src/ninolex_gh/__init__.py`:
   ```python
   __version__ = "X.Y.Z"
   ```

**Verify versions match:**
```bash
grep 'version' pyproject.toml
grep '__version__' src/ninolex_gh/__init__.py
```

---

### 7. Final Validation

Run all checks one more time:

```bash
# Full pipeline
python build/build_dictionary.py
python build/generate_json.py
python build/generate_pls.py

# Validation
python tests/validate_ipa.py
PYTHONPATH=src python tools/smoke_test_package.py

# Quick API check
python -c "import ninolex_gh; print(ninolex_gh.lookup('Accra'))"
```

---

## Commit and Tag

```bash
git add -A
git commit -m "Release vX.Y.Z: NNN entries, [brief summary]"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main --tags
```

---

## PyPI Publishing (Future)

> **Note:** Only proceed with PyPI publishing after the package has been
> validated internally. These steps are for future reference.

### 1. Build Distribution Artifacts

```bash
# Install build tools
pip install build twine

# Build wheel and sdist
python -m build
```

**Verify output:**
```bash
ls -la dist/
# Should see:
#   ninolex_gh-X.Y.Z-py3-none-any.whl
#   ninolex_gh-X.Y.Z.tar.gz
```

### 2. Inspect Built Artifacts

```bash
# Check wheel contents include the JSON data
unzip -l dist/ninolex_gh-X.Y.Z-py3-none-any.whl | grep json
```

**Must see:** `ninolex_gh/data/ninolex_gh_dictionary.json`

### 3. Test in Clean Environment

```bash
# Create fresh virtualenv
python -m venv /tmp/ninolex-test
source /tmp/ninolex-test/bin/activate

# Install from local wheel
pip install dist/ninolex_gh-X.Y.Z-py3-none-any.whl

# Verify it works
python -c "
import ninolex_gh
print('Version:', ninolex_gh.__version__)
print('Entries:', ninolex_gh.get_entry_count())
print('Lookup dumsor:', ninolex_gh.lookup('dumsor'))
"

# Cleanup
deactivate
rm -rf /tmp/ninolex-test
```

### 4. Upload to PyPI

```bash
# Test PyPI first (optional but recommended)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

### 5. Verify PyPI Installation

```bash
pip install ninolex-gh
python -c "import ninolex_gh; print(ninolex_gh.lookup('dumsor'))"
```

---

## Post-Release

- [ ] Verify GitHub release page shows the tag
- [ ] Verify PyPI page shows correct version (if published)
- [ ] Announce release in ANNOUNCEMENTS.md (if significant)
- [ ] Update any downstream projects that depend on Ninolex-GH

---

## Quick Reference: Minimum Release Requirements

| Check | Requirement |
|-------|-------------|
| IPA Validation | 0 errors |
| Smoke Test | All pass |
| Entry Count | ≥ 100 |
| Package Data Sync | Identical to dist/ |
| Version Updated | pyproject.toml + __init__.py |
| CHANGELOG Updated | Data summary included |
