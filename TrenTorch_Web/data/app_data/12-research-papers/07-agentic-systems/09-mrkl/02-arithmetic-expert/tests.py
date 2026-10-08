"""
pytest data/app_data/12-research-papers/07-agentic-systems/09-mrkl/02-arithmetic-expert/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mrkl-arithmetic")
arithmetic_expert = _module.arithmetic_expert


def test_1_addition():
    assert arithmetic_expert("2 + 3") == 5.0


def test_2_subtraction_with_negative_number():
    assert arithmetic_expert("-2 - 3") == -5.0


def test_3_multiplication():
    assert arithmetic_expert("4 * 2.5") == 10.0


def test_4_invalid_expression_returns_none():
    assert arithmetic_expert("two plus three") is None


def test_5_unsupported_operator_returns_none():
    assert arithmetic_expert("8 / 2") is None


def test_6_returns_a_float():
    assert isinstance(arithmetic_expert("1 + 1"), float)

