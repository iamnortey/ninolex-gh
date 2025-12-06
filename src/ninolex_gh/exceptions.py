"""
Ninolex-GH Exceptions

Custom exception classes for the Ninolex-GH pronunciation dictionary.
"""


class NinolexError(Exception):
    """Base exception for Ninolex-GH."""


class WordNotFound(NinolexError):
    """Raised when a grapheme is not found in the dictionary."""
