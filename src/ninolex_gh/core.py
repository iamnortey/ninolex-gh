"""
Ninolex-GH Core Module
======================

Provides the primary lookup interface for the Ghanaian pronunciation dictionary.

This module is designed for infrastructure use in TTS engines, voice assistants,
and language applications requiring canonical Ghanaian pronunciations.

Architecture:
    - Data is loaded lazily on first access via _load_data()
    - A module-level cache (_CACHE) avoids repeated file I/O
    - All lookups are case-insensitive and Unicode-normalized (NFC)

Thread Safety:
    The module is safe for concurrent reads after initial load.
    The _CACHE is populated on first access and remains immutable thereafter.
"""

from __future__ import annotations

import json
import unicodedata
from importlib import resources
from typing import Any, Dict, List, Union

from .exceptions import WordNotFound

# ==============================================================================
# SENTINEL & CACHE
# ==============================================================================

# Sentinel object for distinguishing "no default provided" from "default is None"
_MISSING: Any = object()

# Module-level cache for dictionary data
# Structure: { normalized_grapheme: entry_dict, ... }
_CACHE: Union[Dict[str, Dict[str, Any]], None] = None

# Raw entries list (preserved for iteration and entry count)
_RAW_ENTRIES: Union[List[Dict[str, Any]], None] = None


# ==============================================================================
# INTERNAL HELPERS
# ==============================================================================

def _normalize_key(text: str) -> str:
    """
    Normalize a grapheme string for dictionary lookup.
    
    Applies:
        1. Unicode NFC normalization (canonical composition)
        2. Whitespace stripping (leading/trailing)
        3. Case folding to lowercase
    
    This ensures consistent lookups regardless of:
        - Composed vs decomposed Unicode (e.g., é vs e + combining acute)
        - Leading/trailing whitespace
        - Case variations (Accra, ACCRA, accra)
    
    Args:
        text: The raw grapheme string.
    
    Returns:
        Normalized key string suitable for dictionary lookup.
    """
    return unicodedata.normalize("NFC", text).strip().lower()


def _load_data() -> Dict[str, Dict[str, Any]]:
    """
    Load and cache the dictionary data from the bundled JSON file.
    
    Uses importlib.resources (Python 3.9+) to load from the installed package,
    ensuring compatibility with various installation methods:
        - Regular pip install
        - Editable installs (pip install -e .)
        - Zipapps and frozen applications
        - System packages
    
    The data is cached in the module-level _CACHE variable to avoid
    repeated file I/O on subsequent lookups.
    
    Returns:
        dict: Mapping of normalized graphemes to entry dictionaries.
        
    Note:
        This function is idempotent; calling it multiple times returns
        the same cached dictionary instance.
    """
    global _CACHE, _RAW_ENTRIES
    
    if _CACHE is not None:
        return _CACHE
    
    # Load JSON from package resources (Python 3.9+ API)
    # This works regardless of how the package is installed
    data_files = resources.files("ninolex_gh.data")
    json_file = data_files.joinpath("ninolex_gh_dictionary.json")
    
    with json_file.open("r", encoding="utf-8") as f:
        _RAW_ENTRIES = json.load(f)
    
    # Build lookup cache with normalized keys
    _CACHE = {
        _normalize_key(entry["grapheme"]): entry
        for entry in _RAW_ENTRIES
    }
    
    return _CACHE


# ==============================================================================
# PUBLIC API
# ==============================================================================

def lookup(word: str, default: Any = _MISSING) -> Dict[str, Any]:
    """
    Look up a word in the Ninolex-GH dictionary.
    
    This is the primary API for accessing pronunciation data. Lookups are
    case-insensitive and Unicode-normalized (NFC).
    
    Args:
        word: The grapheme (spelling) to look up. Case-insensitive.
              Examples: "Kumasi", "WASSCE", "dumsor"
        
        default: Value to return if word is not found.
                 - If not provided: raises WordNotFound
                 - If provided (including None, [], {}, etc.): returns that value
    
    Returns:
        dict: The full entry dictionary when found, containing:
            - grapheme (str): Original spelling
            - phoneme (str): IPA transcription
            - domain (str): Category domain (core, places, people, etc.)
            - category (str): Subcategory (city, food, public_figure, etc.)
            - region (str): Geographic region if applicable
            - city (str): City if applicable
            - alias (str): Alternative names/spellings
            - notes (str): Additional context
            - source_file (str): Origin CSV file
        
        Or returns `default` if provided and word not found.
    
    Raises:
        WordNotFound: If word is not in dictionary and no default was provided.
    
    Examples:
        >>> import ninolex_gh
        
        >>> # Basic lookup
        >>> entry = ninolex_gh.lookup("dumsor")
        >>> entry["phoneme"]
        'ˈdum.sɔ'
        
        >>> # Case-insensitive
        >>> ninolex_gh.lookup("KUMASI")["phoneme"]
        'kuˈmɑːsi'
        
        >>> # With explicit default (including None)
        >>> ninolex_gh.lookup("xyz", default=None)
        None
        
        >>> ninolex_gh.lookup("xyz", default={"phoneme": "unknown"})
        {'phoneme': 'unknown'}
        
        >>> # Raises exception if no default provided
        >>> ninolex_gh.lookup("nonexistent")
        Traceback (most recent call last):
            ...
        ninolex_gh.WordNotFound: Grapheme not found in Ninolex-GH: 'nonexistent'
    """
    mapping = _load_data()
    key = _normalize_key(word)
    
    if key in mapping:
        return mapping[key]
    
    # Word not found - check if a default was explicitly provided
    if default is not _MISSING:
        return default
    
    raise WordNotFound(f"Grapheme not found in Ninolex-GH: {word!r}")


def get_entry_count() -> int:
    """
    Return the total number of entries in the dictionary.
    
    Useful for validation, testing, CI checks, and informational purposes.
    
    Returns:
        int: Number of entries in the loaded dictionary.
    
    Example:
        >>> import ninolex_gh
        >>> count = ninolex_gh.get_entry_count()
        >>> count > 100  # Should have many entries
        True
    """
    mapping = _load_data()
    return len(mapping)


def list_graphemes() -> List[str]:
    """
    Return a list of all graphemes (original spellings) in the dictionary.
    
    The returned list preserves original casing from the source data.
    Useful for autocomplete, iteration, validation, or building indexes.
    
    Returns:
        list[str]: All graphemes in the dictionary (original case preserved).
    
    Example:
        >>> import ninolex_gh
        >>> graphemes = ninolex_gh.list_graphemes()
        >>> "Accra" in graphemes
        True
        >>> len(graphemes) == ninolex_gh.get_entry_count()
        True
    """
    # Ensure data is loaded
    _load_data()
    
    # Return original graphemes from raw entries (preserves order and case)
    return [entry["grapheme"] for entry in _RAW_ENTRIES]
