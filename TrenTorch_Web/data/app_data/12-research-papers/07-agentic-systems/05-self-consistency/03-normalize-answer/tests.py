"""
pytest data/app_data/12-research-papers/07-agentic-systems/05-self-consistency/03-normalize-answer/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sc-normalize-answer")
normalize_answer = _module.normalize_answer


def test_1_lowercases_and_removes_punctuation():
    assert normalize_answer("The Answer, 42!") == "the answer 42"


def test_2_collapses_repeated_whitespace():
    assert normalize_answer("a    b\t c") == "a b c"


def test_3_strips_surrounding_space():
    assert normalize_answer("  yes  ") == "yes"


def test_4_is_idempotent():
    once = normalize_answer("Hello, World!")
    assert normalize_answer(once) == once


def test_5_returns_a_string():
    assert isinstance(normalize_answer("x"), str)


def test_6_empty_string_stays_empty():
    assert normalize_answer("!!!") == ""

