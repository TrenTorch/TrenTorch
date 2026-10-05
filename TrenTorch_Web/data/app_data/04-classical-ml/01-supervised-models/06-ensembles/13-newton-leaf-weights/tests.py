"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

solution = load_solution(__file__)
logistic_grad_hess = solution.logistic_grad_hess
leaf_weight = solution.leaf_weight
split_gain = solution.split_gain


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_gradient_at_zero_score_for_positive_label():
    g, _ = logistic_grad_hess(np.array([1]), np.array([0.0]))
    assert np.isclose(g[0], -0.5)


def test_hessian_at_zero_score_is_a_quarter():
    _, h = logistic_grad_hess(np.array([1, 0]), np.array([0.0, 0.0]))
    assert np.allclose(h, 0.25)


def test_gradient_is_positive_for_negative_label_at_zero():
    g, _ = logistic_grad_hess(np.array([0]), np.array([0.0]))
    assert np.isclose(g[0], 0.5)


def test_hessian_is_small_for_confident_scores():
    _, h = logistic_grad_hess(np.array([1]), np.array([20.0]))
    assert h[0] < 1e-6


def test_gradient_and_hessian_shapes_match_input():
    y = np.array([0, 1, 1, 0])
    g, h = logistic_grad_hess(y, np.array([0.1, -0.2, 0.3, 0.0]))
    assert g.shape == (4,) and h.shape == (4,)


def test_labels_other_than_zero_one_raise():
    assert _raises_value_error(logistic_grad_hess, np.array([2]), np.array([0.0]))


def test_leaf_weight_matches_formula():
    assert np.isclose(leaf_weight(-4.0, 2.0, 1.0), 4.0 / 3.0)


def test_leaf_weight_sign_opposes_gradient_sum():
    assert leaf_weight(3.0, 1.0, 0.5) < 0
    assert leaf_weight(-3.0, 1.0, 0.5) > 0


def test_regularization_shrinks_leaf_weight():
    assert abs(leaf_weight(-4.0, 2.0, 10.0)) < abs(leaf_weight(-4.0, 2.0, 0.1))


def test_nonpositive_lambda_raises():
    assert _raises_value_error(leaf_weight, -1.0, 1.0, 0.0)
    assert _raises_value_error(split_gain, 1.0, 1.0, 1.0, 1.0, -1.0, 0.0)


def test_split_gain_matches_hand_computed_value():
    gain = split_gain(-4.0, 2.0, 4.0, 2.0, lam=1.0, gamma=0.0)
    assert np.isclose(gain, 16.0 / 3.0)


def test_gamma_subtracts_from_gain():
    base = split_gain(-4.0, 2.0, 4.0, 2.0, lam=1.0, gamma=0.0)
    penalized = split_gain(-4.0, 2.0, 4.0, 2.0, lam=1.0, gamma=1.0)
    assert np.isclose(base - penalized, 1.0)


def test_split_gain_is_symmetric_in_left_and_right():
    a = split_gain(-4.0, 2.0, 1.0, 3.0, lam=1.0, gamma=0.0)
    b = split_gain(1.0, 3.0, -4.0, 2.0, lam=1.0, gamma=0.0)
    assert np.isclose(a, b)


def test_identical_halves_give_negative_gain_from_the_lambda_penalty():
    gain = split_gain(2.0, 1.0, 2.0, 1.0, lam=1.0, gamma=0.0)
    assert np.isclose(gain, 0.5 * (2.0 + 2.0 - 16.0 / 3.0))
    assert gain < 0


def test_same_input_gives_same_output():
    y = np.array([0, 1, 1])
    raw = np.array([0.2, -0.1, 0.4])
    a = logistic_grad_hess(y, raw)
    b = logistic_grad_hess(y, raw)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])
