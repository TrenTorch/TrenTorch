"""
pytest data/app_data/00-python/02-strings/03-concatenation-cost/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
join_with_separator = _module.join_with_separator
repeat_text = _module.repeat_text
total_chars_copied = _module.total_chars_copied


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
