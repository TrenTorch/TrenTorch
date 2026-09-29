"""
pytest data/app_data/00-python/02-strings/04-case-methods/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
sentence_case = _module.sentence_case
swap_first_char_case = _module.swap_first_char_case
equal_ignoring_case = _module.equal_ignoring_case
case_kind = _module.case_kind


def test_sentence_case_lowercases_the_tail():
    assert sentence_case("pyTHON") == "Python"
    assert sentence_case("hELLO wORLD") == "Hello world"


def test_swap_first_char_case_leaves_rest_untouched():
    assert swap_first_char_case("python") == "Python"
    assert swap_first_char_case("PYthon") == "pYthon"
    assert swap_first_char_case("") == ""


def test_equal_ignoring_case_handles_sharp_s():
    assert equal_ignoring_case("Straße", "STRASSE") is True
    assert equal_ignoring_case("Hello", "HELLO") is True
    assert equal_ignoring_case("Hello", "World") is False


def test_case_kind_classification():
    assert case_kind("ABC") == "upper"
    assert case_kind("abc") == "lower"
    assert case_kind("Hello World") == "title"
    assert case_kind("hELLo") == "mixed"
    assert case_kind("123") == "mixed"
    assert case_kind("") == "mixed"


def test_originals_unchanged():
    s = "pyTHON"
    sentence_case(s)
    swap_first_char_case(s)
    assert s == "pyTHON"
