"""
Ninolex-GH: Canonical Ghanaian Pronunciation Dictionary

A machine-readable pronunciation lexicon for Ghanaian proper nouns,
designed for TTS engines, voice assistants, and language applications.

Usage:
    >>> import ninolex_gh
    >>> entry = ninolex_gh.lookup("Kumasi")
    >>> print(entry["phoneme"])
    'kuˈmɑːsi'
    
    >>> # With default for missing words
    >>> entry = ninolex_gh.lookup("unknown", default=None)
    >>> print(entry)
    None

    >>> # Raises WordNotFound if no default
    >>> ninolex_gh.lookup("nonexistent")
    Traceback (most recent call last):
        ...
    ninolex_gh.WordNotFound: Grapheme not found in Ninolex-GH: 'nonexistent'
"""

from .core import lookup
from .exceptions import NinolexError, WordNotFound

__all__ = ["lookup", "NinolexError", "WordNotFound"]

# Temporary version placeholder; we will align with CalVer later
__version__ = "0.1.0"
