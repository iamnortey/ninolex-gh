#!/usr/bin/env python3
"""
Smoke Test for Ninolex-GH Package

Quick validation that the package imports and basic lookup works.

Usage:
    cd /path/to/ninolex-gh
    pip install -e .
    python tools/smoke_test_package.py
"""

import ninolex_gh


def main():
    print("Ninolex-GH version:", getattr(ninolex_gh, "__version__", "unknown"))
    try:
        entry = ninolex_gh.lookup("dumsor", default=None)
        print("Lookup 'dumsor':", entry)
    except Exception as e:
        print("Error during lookup:", e)


if __name__ == "__main__":
    main()
