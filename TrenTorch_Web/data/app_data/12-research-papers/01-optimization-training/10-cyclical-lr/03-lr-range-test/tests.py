"""
pytest data/app_data/12-research-papers/01-optimization-and-training/10-cyclical-lr/03-lr-range-test/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clr-range-test")
lr_range_test = _module.lr_range_test


def test_1_first_iteration_is_min_lr():
    assert abs(lr_range_test(0, 1e-4, 2.0) - 1e-4) < 1e-18


def test_2_hand_case():
    assert abs(lr_range_test(3, 1e-4, 2.0) - 8e-4) < 1e-15


def test_3_growth_factor_one_is_constant():
    assert lr_range_test(10, 0.01, 1.0) == 0.01


def test_4_increasing_in_iteration():
    assert lr_range_test(5, 0.001, 1.5) > lr_range_test(4, 0.001, 1.5)


def test_5_returns_a_float():
    assert isinstance(lr_range_test(2, 0.1, 2.0), float)


def test_6_geometric_ratio_between_steps():
    a = lr_range_test(2, 0.01, 3.0)
    b = lr_range_test(3, 0.01, 3.0)
    assert abs(b / a - 3.0) < 1e-12

