"""
pytest data/app_data/00-python/07-functions/02-positional-vs-keyword/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/07-functions/{Path(__file__).resolve().parent.name}")
build_point = _module.build_point
configure_model = _module.configure_model
format_record = _module.format_record


def test_all_positional_calls():
    assert build_point(3, 4) == (3, 4)
    assert configure_model("db", 128, "cosine") == {
        "name": "db",
        "dimensions": 128,
        "metric": "cosine",
    }


def test_all_keyword_calls():
    assert build_point(x=3, y=4) == (3, 4)
    assert format_record(identifier=7, value=3.5, label="score") == "7=3.5 [score]"


def test_mixed_calls():
    assert configure_model("db", dimensions=128, metric="cosine") == {
        "name": "db",
        "dimensions": 128,
        "metric": "cosine",
    }


def test_keyword_order_does_not_matter():
    assert build_point(y=4, x=3) == (3, 4)
    assert configure_model(metric="cosine", name="db", dimensions=128) == {
        "name": "db",
        "dimensions": 128,
        "metric": "cosine",
    }


def test_returned_structure():
    assert format_record(7, 3.5, "score") == "7=3.5 [score]"
    result = configure_model("db", 128, "cosine")
    assert type(result) is dict
