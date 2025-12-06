"""
Ninolex-GH Core Module

Provides the primary lookup interface for the Ghanaian pronunciation dictionary.
"""

import json
import unicodedata
from importlib import resources

from .exceptions import WordNotFound

_CACHE = None


def _load_data():
    """
    Load and cache the dictionary data from the bundled JSON file.
    
    Uses importlib.resources to load from the installed package,
    ensuring compatibility with various installation methods (pip, zipapps, etc.).
    
    Returns:
        dict: Mapping of normalized graphemes to entry dictionaries.
    """
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    with resources.files("ninolex_gh.data").joinpath("ninolex_gh_dictionary.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

    _CACHE = {
        unicodedata.normalize("NFC", entry["grapheme"]).strip().lower(): entry
        for entry in data
    }
    return _CACHE


def lookup(word: str, default=None):
    """
    Look up a word in the Ninolex-GH dictionary.
    
    Args:
        word: The grapheme (spelling) to look up. Case-insensitive.
        default: Value to return if word is not found. If None and word
                 is missing, raises WordNotFound.
    
    Returns:
        dict: The full entry dictionary containing phoneme, domain, category,
              notes, etc. Or `default` if provided and word not found.
    
    Raises:
        WordNotFound: If word is not in dictionary and default is None.
    
    Example:
        >>> import ninolex_gh
        >>> entry = ninolex_gh.lookup("dumsor")
        >>> print(entry["phoneme"])
        'ˈdum.sɔ'
    """
    mapping = _load_data()
    key = unicodedata.normalize("NFC", word).strip().lower()
    if key in mapping:
        return mapping[key]
    if default is not None:
        return default
    raise WordNotFound(f"Grapheme not found in Ninolex-GH: {word!r}")
