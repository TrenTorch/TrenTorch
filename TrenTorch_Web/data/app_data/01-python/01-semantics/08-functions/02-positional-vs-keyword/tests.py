"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
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
