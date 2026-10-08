"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/01-xgboost/01-leaf-weight/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-xgboost-leaf-weight")
xgb_leaf_weight = _module.xgb_leaf_weight


def test_1_matches_a_hand_value():
    assert abs(xgb_leaf_weight(2.0, 3.0, 1.0) - (-0.5)) < 1e-12


def test_2_zero_gradient_gives_zero_weight():
    assert xgb_leaf_weight(0.0, 5.0, 1.0) == 0.0


def test_3_no_regularization_is_the_plain_newton_step():
    assert abs(xgb_leaf_weight(4.0, 2.0, 0.0) - (-2.0)) < 1e-12


def test_4_regularization_shrinks_the_weight():
    assert abs(xgb_leaf_weight(2.0, 3.0, 10.0)) < abs(xgb_leaf_weight(2.0, 3.0, 0.0))


def test_5_weight_points_against_the_gradient():
    assert xgb_leaf_weight(-4.0, 2.0, 0.0) > 0


def test_6_returns_a_float():
    assert isinstance(xgb_leaf_weight(1.0, 1.0, 1.0), float)

