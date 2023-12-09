"""This module provides the vocabcli model-controller."""
# vocabcli/vocabcli.py

from typing import Any, Dict, NamedTuple

class CurrentWord(NamedTuple):
    word: Dict[str, Any]
    error: int
