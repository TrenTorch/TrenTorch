"""
pytest data/app_data/12-research-papers/07-agentic-systems/02-chain-of-thought/03-answers-match/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-cot-answers-match")
answers_match = _module.answers_match


def test_1_thousands_separator_is_ignored():
    assert answers_match("1,000", "1000") is True


def test_2_numeric_values_compare_by_value():
    assert answers_match("3.0", "3") is True


def test_3_different_numbers_do_not_match():
    assert answers_match("4", "5") is False


def test_4_text_compares_case_insensitively():
    assert answers_match("Yes", "yes") is True


def test_5_different_text_does_not_match():
    assert answers_match("a", "b") is False


def test_6_returns_a_bool():
    assert isinstance(answers_match("1", "1"), bool)

