"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/01-xgboost/03-logistic-gradients/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-xgboost-logistic-grads")
xgb_logistic_grad_hess = _module.xgb_logistic_grad_hess


def test_1_positive_class_with_p_point_seven():
    g, h = xgb_logistic_grad_hess(1, 0.7)
    assert abs(g - (-0.3)) < 1e-12 and abs(h - 0.21) < 1e-12


def test_2_negative_class_at_one_half():
    g, h = xgb_logistic_grad_hess(0, 0.5)
    assert abs(g - 0.5) < 1e-12 and abs(h - 0.25) < 1e-12


def test_3_hessian_is_largest_at_one_half():
    assert xgb_logistic_grad_hess(1, 0.5)[1] > xgb_logistic_grad_hess(1, 0.9)[1]


def test_4_hessian_is_never_negative():
    for p in [0.0, 0.2, 0.8, 1.0]:
        assert xgb_logistic_grad_hess(1, p)[1] >= 0


def test_5_gradient_points_toward_the_label():
    assert xgb_logistic_grad_hess(1, 0.2)[0] < 0


def test_6_works_on_arrays():
    g, h = xgb_logistic_grad_hess(__import__("numpy").array([1, 0]), __import__("numpy").array([0.7, 0.5]))
    assert g.shape == (2,) and h.shape == (2,)

