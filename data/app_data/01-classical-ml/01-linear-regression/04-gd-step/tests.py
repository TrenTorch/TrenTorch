"""
pytest data/app_data/01-classical-ml/01-linear-regression/04-gd-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gd_step = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).gd_step


def test_matches_hand_computed_update():
    new_weight, new_bias = gd_step(
        np.array([1.0, 2.0]), np.array([0.5]), np.array([0.1, -0.2]), np.array([0.05]), lr=10.0
    )
    assert np.allclose(new_weight, [0.0, 4.0])
    assert np.allclose(new_bias, [0.0])


def test_zero_gradient_leaves_parameters_unchanged():
    weight, bias = np.array([3.0, -1.0]), np.array([2.0])
    new_weight, new_bias = gd_step(weight, bias, np.zeros(2), np.array([0.0]), lr=0.5)
    assert np.allclose(new_weight, weight) and np.allclose(new_bias, bias)


def test_bias_none_returns_updated_bias_none():
    # No bias parameter means there's nothing to step -- must stay None,
    # not a fabricated zero-stepped value.
    weight = np.array([1.0, 2.0])
    new_weight, new_bias = gd_step(weight, None, np.array([0.1, 0.1]), None, lr=1.0)
    assert new_bias is None
    assert np.allclose(new_weight, [0.9, 1.9])


def test_works_on_matrix_shaped_weight():
    # weight/grad_weight generalize to the (out_features, in_features)
    # shape 01-hypothesis-function actually produces, not just 1-D.
    weight = np.array([[1.0, 2.0], [3.0, 4.0]])
    grad_weight = np.ones((2, 2))
    new_weight, _ = gd_step(weight, None, grad_weight, None, lr=0.5)
    assert np.allclose(new_weight, [[0.5, 1.5], [2.5, 3.5]])


def test_does_not_mutate_input_arrays_in_place():
    # A real, common bug: modifying weight in place silently corrupts
    # the caller's "before" value -- breaks any before/after comparison,
    # like the loss-decrease test in the training-loop question.
    weight = np.array([1.0, 1.0])
    original = weight.copy()
    gd_step(weight, None, np.array([1.0, 1.0]), None, lr=1.0)
    assert np.allclose(weight, original)


def test_larger_learning_rate_moves_further():
    small, _ = gd_step(np.array([0.0]), None, np.array([1.0]), None, lr=0.01)
    large, _ = gd_step(np.array([0.0]), None, np.array([1.0]), None, lr=1.0)
    assert abs(large[0]) > abs(small[0])
