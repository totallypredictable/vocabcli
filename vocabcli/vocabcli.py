"""This module provides the vocabcli model-controller."""
# vocabcli/vocabcli.py

from pathlib import Path
from typing import Any, Dict, NamedTuple

from vocabcli.database import DatabaseHandler


class CurrentWord(NamedTuple):
    word: Dict[str, Any]
    error: int


class Worder:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
