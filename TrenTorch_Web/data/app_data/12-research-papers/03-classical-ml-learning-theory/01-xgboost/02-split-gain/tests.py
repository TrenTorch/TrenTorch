"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/01-xgboost/02-split-gain/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-xgboost-split-gain")
xgb_split_gain = _module.xgb_split_gain


def test_1_matches_a_hand_value():
    assert abs(xgb_split_gain(1.0, 1.0, -1.0, 1.0, 0.0, 0.0) - 1.0) < 1e-12


def test_2_gamma_subtracts_a_fixed_penalty():
    assert abs(xgb_split_gain(1.0, 1.0, -1.0, 1.0, 0.0, 0.3) - 0.7) < 1e-12


def test_3_empty_children_give_zero_gain():
    assert abs(xgb_split_gain(0.0, 0.0, 0.0, 0.0, 1.0, 0.0)) < 1e-12


def test_4_swapping_children_leaves_gain_unchanged():
    a = xgb_split_gain(2.0, 3.0, -1.0, 2.0, 1.0, 0.0)
    b = xgb_split_gain(-1.0, 2.0, 2.0, 3.0, 1.0, 0.0)
    assert abs(a - b) < 1e-12


def test_5_regularization_reduces_gain():
    assert xgb_split_gain(2.0, 3.0, -1.0, 2.0, 5.0, 0.0) < xgb_split_gain(2.0, 3.0, -1.0, 2.0, 0.0, 0.0)


def test_6_returns_a_float():
    assert isinstance(xgb_split_gain(1.0, 1.0, 1.0, 1.0, 1.0, 0.0), float)

