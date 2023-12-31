"""This module provides the vocabcli model-controller."""
# vocabcli/vocabcli.py

from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from vocabcli import DB_READ_ERROR
from vocabcli.database import DatabaseHandler


class CurrentWord(NamedTuple):
    word: Dict[str, Any]
    error: int


class Worder:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, name: str, article: str|None = None, gender: str|None = None, typ: str|None = None) -> CurrentWord:
        """Add a new word to the database."""
        if article == None:
            article = "NA"
        if gender == None:
            gender == "NA"
        if typ == None:
            typ == "NA"
        word = {
                "article": article,
                "gender": gender,
                "typ": typ,
        }
        read = self._db_handler.read_words()
        if read.error == DB_READ_ERROR:
            return CurrentWord(word, read.error)
        if name not in read.word_list:
            read.word_list[name] = word
        write = self._db_handler.write_words(read.word_list)
        return CurrentWord(word, write.error)

    def get_word_list(self) -> List[Dict[str, Any]]:
        """Return the current vocabulary."""
        read = self._db_handler.read_words()
        return read.word_list


