"""
pytest data/app_data/00-python/05-dictionaries/03-removing-entries/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
remove_keys = _module.remove_keys
take_last = _module.take_last
remove_and_return = _module.remove_and_return
clear_and_report = _module.clear_and_report


def test_remove_keys_returns_exact_count():
    d = {"a": 1, "b": 2}
    result = remove_keys(d, ["a", "z", "a"])
    assert result == 1
    assert d == {"b": 2}


def test_remove_keys_mutates_in_place():
    d = {"a": 1, "b": 2}
    before_id = id(d)
    remove_keys(d, ["a"])
    assert id(d) == before_id


def test_take_last_respects_insertion_order():
    d = {"a": 1, "b": 2}
    assert take_last(d) == ("b", 2)
    d["a_again"] = 3
    d.pop("a")
    d["a"] = 4
    assert take_last(d) == ("a", 4)


def test_take_last_on_empty_dictionary():
    assert take_last({}) is None


def test_remove_and_return_with_stored_none_and_absent():
    d = {"a": None}
    assert remove_and_return(d, "a", "missing") is None
    assert "a" not in d
    d2 = {"a": 1}
    assert remove_and_return(d2, "z", "missing") == "missing"
    assert d2 == {"a": 1}


def test_clear_and_report_counts_before_clearing():
    d = {"a": 1, "b": 2}
    before_id = id(d)
    count = clear_and_report(d)
    assert count == 2
    assert d == {}
    assert id(d) == before_id
