#!/usr/bin/env python3
"""
Smoke Test for Ninolex-GH Package

Validates that the package imports correctly and the API works as expected.
This script should pass before any release or CI merge.

Usage:
    cd /path/to/ninolex-gh
    PYTHONPATH=src python tools/smoke_test_package.py
    
    # Or after pip install -e .
    python tools/smoke_test_package.py

Exit Codes:
    0 - All tests passed
    1 - One or more tests failed
"""

import sys


def main():
    """Run smoke tests and return exit code."""
    print("=" * 60)
    print("Ninolex-GH Package Smoke Test")
    print("=" * 60)
    print()
    
    errors = []
    
    # Test 1: Import the package
    try:
        import ninolex_gh
        print(f"✅ Package imported successfully")
        print(f"   Version: {ninolex_gh.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import ninolex_gh: {e}")
        errors.append("import")
        # Can't continue without import
        return 1
    
    print()
    
    # Test 2: Check entry count
    try:
        count = ninolex_gh.get_entry_count()
        print(f"✅ get_entry_count() returned: {count}")
        
        # Sanity check: should have at least a few entries
        if count < 1:
            print(f"   ⚠️  Warning: Entry count is very low ({count})")
            errors.append("entry_count_low")
    except Exception as e:
        print(f"❌ get_entry_count() failed: {e}")
        errors.append("entry_count")
    
    print()
    
    # Test 3: Basic lookup
    test_words = ["dumsor", "Accra", "waakye"]
    print("Lookup tests:")
    for word in test_words:
        try:
            entry = ninolex_gh.lookup(word)
            if entry and "phoneme" in entry:
                print(f"   ✅ lookup({word!r}) → {entry['phoneme']}")
            else:
                print(f"   ⚠️  lookup({word!r}) returned unexpected: {entry}")
        except ninolex_gh.WordNotFound:
            print(f"   ⚠️  lookup({word!r}) → NOT FOUND (may not be in sample data)")
        except Exception as e:
            print(f"   ❌ lookup({word!r}) failed: {e}")
            errors.append(f"lookup_{word}")
    
    print()
    
    # Test 4: WordNotFound exception
    try:
        ninolex_gh.lookup("__nonexistent_word_xyz_123__")
        print("❌ lookup() should have raised WordNotFound")
        errors.append("wordnotfound")
    except ninolex_gh.WordNotFound as e:
        print(f"✅ WordNotFound raised correctly: {e}")
    except Exception as e:
        print(f"❌ Wrong exception type: {type(e).__name__}: {e}")
        errors.append("exception_type")
    
    print()
    
    # Test 5: Default parameter
    try:
        result = ninolex_gh.lookup("__nonexistent__", default={"phoneme": "N/A"})
        if result == {"phoneme": "N/A"}:
            print("✅ lookup() with default works correctly")
        else:
            print(f"❌ lookup() with default returned unexpected: {result}")
            errors.append("default")
    except Exception as e:
        print(f"❌ lookup() with default failed: {e}")
        errors.append("default")
    
    print()
    
    # Test 6: list_graphemes()
    try:
        graphemes = ninolex_gh.list_graphemes()
        if isinstance(graphemes, list) and len(graphemes) > 0:
            print(f"✅ list_graphemes() returned {len(graphemes)} graphemes")
            print(f"   Sample: {graphemes[:3]}...")
        else:
            print(f"⚠️  list_graphemes() returned: {graphemes}")
    except Exception as e:
        print(f"❌ list_graphemes() failed: {e}")
        errors.append("list_graphemes")
    
    print()
    
    # Summary
    print("=" * 60)
    if errors:
        print(f"❌ FAILED - {len(errors)} error(s): {', '.join(errors)}")
        return 1
    else:
        print("✅ All smoke tests passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
