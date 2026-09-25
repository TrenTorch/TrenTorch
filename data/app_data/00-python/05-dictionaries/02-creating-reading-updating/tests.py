"""
pytest data/app_data/00-python/05-dictionaries/02-creating-reading-updating/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
word_frequencies = _module.word_frequencies
safe_lookup = _module.safe_lookup
increment = _module.increment
dict_from_two_lists = _module.dict_from_two_lists


def test_word_frequencies_counts_and_case():
    assert word_frequencies("a b a") == {"a": 2, "b": 1}
    assert word_frequencies("The the") == {"The": 1, "the": 1}
    assert word_frequencies("") == {}


def test_safe_lookup_does_not_insert():
    d = {"a": 1}
    result = safe_lookup(d, "z", 99)
    assert result == 99
    assert d == {"a": 1}


def test_safe_lookup_with_stored_none():
    d = {"a": None}
    assert safe_lookup(d, "a", 99) is None


def test_increment_mutates_in_place():
    d = {"a": 5}
    before_id = id(d)
    increment(d, "a", 3)
    assert d["a"] == 8
    assert id(d) == before_id
    increment(d, "b", -2)
    assert d["b"] == -2


def test_dict_from_two_lists_repeated_keys_and_empty():
    assert dict_from_two_lists(["a", "a"], [1, 2]) == {"a": 2}
    assert dict_from_two_lists([], []) == {}
    assert dict_from_two_lists(["a", "b"], [1, 2]) == {"a": 1, "b": 2}
