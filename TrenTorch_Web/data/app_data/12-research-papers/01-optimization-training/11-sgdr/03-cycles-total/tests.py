"""
pytest data/app_data/12-research-papers/01-optimization-and-training/11-sgdr/03-cycles-total/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sgdr-cycles-total")
cycles_total = _module.cycles_total


def test_1_hand_case():
    assert cycles_total(10, 2, 3) == 70


def test_2_one_cycle_is_first_length():
    assert cycles_total(7, 3, 1) == 7


def test_3_zero_cycles_is_zero():
    assert cycles_total(10, 2, 0) == 0


def test_4_constant_cycles():
    assert cycles_total(5, 1, 4) == 20


def test_5_increases_with_more_cycles():
    assert cycles_total(10, 2, 4) > cycles_total(10, 2, 3)


def test_6_matches_geometric_sum():
    assert cycles_total(3, 2, 4) == 3 * (2**4 - 1)

