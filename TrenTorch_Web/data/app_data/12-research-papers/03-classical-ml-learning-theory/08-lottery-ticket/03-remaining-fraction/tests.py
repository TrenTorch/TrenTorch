"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/08-lottery-ticket/03-remaining-fraction/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lottery-remaining-fraction")
remaining_fraction = _module.remaining_fraction


def test_1_one_round_keeps_one_minus_p():
    assert abs(remaining_fraction(0.2, 1) - 0.8) < 1e-12


def test_2_zero_rounds_keep_everything():
    assert remaining_fraction(0.5, 0) == 1.0


def test_3_compounds_over_rounds():
    assert abs(remaining_fraction(0.5, 3) - 0.125) < 1e-12


def test_4_zero_pruning_keeps_everything():
    assert remaining_fraction(0.0, 10) == 1.0


def test_5_remaining_fraction_decreases_with_rounds():
    assert remaining_fraction(0.2, 4) < remaining_fraction(0.2, 2)


def test_6_returns_a_float():
    assert isinstance(remaining_fraction(0.1, 2), float)

