"""
Ninolex-GH: Canonical Ghanaian Pronunciation Dictionary
========================================================

A machine-readable pronunciation lexicon for Ghanaian proper nouns,
designed for TTS engines, voice assistants, and language applications.

Installation
------------
::

    pip install ninolex-gh

Quick Start
-----------
::

    import ninolex_gh
    
    # Look up a pronunciation
    entry = ninolex_gh.lookup("Kumasi")
    print(entry["phoneme"])  # 'kuˈmɑːsi'
    
    # Case-insensitive lookups
    ninolex_gh.lookup("WASSCE")["phoneme"]  # 'ˈwasi'
    
    # Handle missing words with a default
    entry = ninolex_gh.lookup("unknown_word", default=None)
    print(entry)  # None
    
    # Or let it raise an exception (default behavior)
    ninolex_gh.lookup("nonexistent")
    # Raises: ninolex_gh.WordNotFound

API Reference
-------------
**lookup(word, default=<missing>)**
    Look up a word's pronunciation.
    
    - Returns the entry dict if found
    - Returns ``default`` if provided and not found (even if default is None)
    - Raises ``WordNotFound`` if not found and no default provided

**get_entry_count()**
    Return the total number of entries in the dictionary.

**list_graphemes()**
    Return a list of all graphemes (spellings) in the dictionary.

Entry Structure
---------------
Each entry is a dict with the following keys:

- **grapheme**: Original spelling (str)
- **phoneme**: IPA transcription (str)
- **domain**: Category domain - core, places, people, sports, education (str)
- **category**: Subcategory - city, food, public_figure, shs, etc. (str)
- **region**: Geographic region if applicable (str)
- **city**: City if applicable (str)
- **alias**: Alternative names/spellings (str)
- **notes**: Additional context (str)
- **source_file**: Origin CSV file path (str)

Exceptions
----------
**NinolexError**
    Base exception for all Ninolex-GH errors.

**WordNotFound**
    Raised when a grapheme is not found and no default is provided.

Version
-------
``__version__`` contains the current package version.

Currently using semantic versioning (0.x.y) during initial development.
Future releases will adopt CalVer (e.g., 2025.12.05) to reflect data snapshots.

Links
-----
- Repository: https://github.com/iamnortey/ninolex-gh
- Documentation: See README.md and IPA_GUIDE.md in the repository

License
-------
MIT License - see LICENSE file for details.
"""

from .core import get_entry_count, list_graphemes, lookup
from .exceptions import NinolexError, WordNotFound

__all__ = [
    # Primary API
    "lookup",
    # Utility functions
    "get_entry_count",
    "list_graphemes",
    # Exceptions
    "NinolexError",
    "WordNotFound",
]

# Package version
# ---------------
# Currently using semantic versioning (0.x.y) during initial development.
# Will transition to CalVer (YYYY.MM.DD) when publishing stable releases
# to make data currency immediately clear to consumers.
__version__ = "0.1.0"
