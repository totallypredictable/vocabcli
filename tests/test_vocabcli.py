# tests/test_vocabcli.py
import json

import pytest
from typer.testing import CliRunner

from vocabcli import (
        DB_READ_ERROR,
        SUCCESS,
        __app_name__,
        __version__,
        cli,
        vocabcli,
)


runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    word = [{"word": "Rasierer", "article": "der", "gender": "Masculine", "typ": "Noun"}]
    db_file = tmp_path / "vocab.json"
    with db_file.open("w") as db:
        json.dump(word, db, indent=4)
    return db_file

test_data1 = {
        "name": "Zeit",
        "article": "die",
        "gender": "Feminine",
        "typ": "Noun",
        "word": {

            "name": "Zeit",
            "article": "die",
            "gender": "Feminine",
            "typ": "Noun",
        },
}

test_data2 = {
        "name": "Alkohol",
        "article": "der",
        "gender": "Masculine",
        "typ": "Noun",
        "word": {

            "name": "Alkohol",
            "article": "der",
            "gender": "Masculine",
            "typ": "Noun",
        },
}

@pytest.mark.parametrize(
        "name, article, gender, typ, expected",
        [
            pytest.param(
                test_data1["name"],
                test_data1["article"],
                test_data1["gender"],
                test_data1["typ"],
                (test_data1["word"], SUCCESS),
            ),
            pytest.param(
                test_data2["name"],
                test_data2["article"],
                test_data2["gender"],
                test_data2["typ"],
                (test_data2["word"], SUCCESS),
            ),
        ],
)

def test_add(mock_json_file, name, article, gender, typ, expected):
    worder = vocabcli.Worder(mock_json_file)
    assert worder.add(name, article, gender, typ) == expected
    read = worder._db_handler.read_words()
    assert len(read.word_list) == 2
