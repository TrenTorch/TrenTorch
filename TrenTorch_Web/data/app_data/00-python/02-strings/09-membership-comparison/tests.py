"""
pytest data/app_data/00-python/02-strings/09-membership-comparison/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
compare_strings = _module.compare_strings
compare_ignoring_case = _module.compare_ignoring_case
caesar_shift = _module.caesar_shift


def test_decision_at_first_differing_character():
    assert compare_strings("apple", "banana") == -1
    assert compare_strings("b", "a") == 1


def test_prefix_ordering_and_equality():
    assert compare_strings("app", "apple") == -1
    assert compare_strings("apple", "app") == 1
    assert compare_strings("apple", "apple") == 0


def test_uppercase_before_lowercase():
    assert compare_strings("Zebra", "apple") == -1


def test_digits_compare_as_text():
    assert compare_strings("10", "9") == -1


def test_compare_ignoring_case():
    assert compare_ignoring_case("Zebra", "apple") == 1
    assert compare_ignoring_case("APPLE", "apple") == 0


def test_caesar_shift_wrap_case_and_non_letters():
    assert caesar_shift("Abc, xyz!", 3) == "Def, abc!"
    assert caesar_shift("Hello", 0) == "Hello"
    assert caesar_shift("Hello", 26) == "Hello"
    assert caesar_shift("Def, abc!", -3) == "Abc, xyz!"
