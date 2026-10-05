"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
replace_char_at = _module.replace_char_at
insert_at = _module.insert_at
join_with_separator = _module.join_with_separator
repeat_text = _module.repeat_text
total_chars_copied = _module.total_chars_copied


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


def test_separator_placement():
    assert join_with_separator(["a"], "-") == "a"
    assert join_with_separator(["a", "b"], "-") == "a-b"
    assert join_with_separator(["a", "b", "c"], "-") == "a-b-c"


def test_empty_and_single_element_input():
    assert join_with_separator([], "-") == ""
    assert join_with_separator(["x"], "-") == "x"


def test_empty_separator_and_empty_parts():
    assert join_with_separator(["a", "b"], "") == "ab"
    assert join_with_separator(["", "x", ""], "-") == "-x-"


def test_repeat_text_zero_and_negative():
    assert repeat_text("ab", 0) == ""
    assert repeat_text("ab", -3) == ""
    assert repeat_text("ab", 3) == "ababab"


def test_total_chars_copied_matches_formula():
    assert total_chars_copied(0, 5) == 0
    assert total_chars_copied(1, 5) == 5
    assert total_chars_copied(3, 2) == 12
    assert total_chars_copied(10000, 1) == 1 * 10000 * 10001 // 2
