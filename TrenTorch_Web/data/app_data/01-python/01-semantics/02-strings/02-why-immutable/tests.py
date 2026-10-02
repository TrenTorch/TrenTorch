"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
replace_char_at = _module.replace_char_at
insert_at = _module.insert_at


def test_replace_at_various_positions():
    assert replace_char_at("hello", 0, "J") == "Jello"
    assert replace_char_at("hello", 2, "X") == "heXlo"
    assert replace_char_at("hello", 4, "!") == "hell!"
    assert replace_char_at("hello", -1, "!") == "hell!"


def test_out_of_range_returns_original():
    assert replace_char_at("hello", 5, "X") == "hello"
    assert replace_char_at("hello", -6, "X") == "hello"


def test_original_untouched():
    s = "hello"
    replace_char_at(s, 0, "J")
    assert s == "hello"


def test_multi_character_and_empty_replacement():
    assert replace_char_at("hello", 1, "XYZ") == "hXYZllo"
    assert replace_char_at("hello", 1, "") == "hllo"


def test_insert_at_boundary_and_clamping():
    assert insert_at("abc", 0, "X") == "Xabc"
    assert insert_at("abc", 3, "X") == "abcX"
    assert insert_at("abc", 99, "X") == "abcX"
    assert insert_at("abc", -99, "X") == "Xabc"
    assert insert_at("abc", 1, "X") == "aXbc"
    assert insert_at("abc", -1, "X") == "abXc"
