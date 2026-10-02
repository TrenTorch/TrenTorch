"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

cost_sensitive_error = load_solution(__file__).cost_sensitive_error


def test_zero_one_cost_is_error_rate():
    y = np.array([0, 1, 1, 0, 1])
    p = np.array([0, 1, 0, 0, 0])
    assert np.isclose(cost_sensitive_error(y, p, 1.0 - np.eye(2)), 2 / 5)


def test_asymmetric_costs():
    cost = np.array([[0.0, 1.0], [5.0, 0.0]])
    y = np.array([0, 0, 1, 1])
    p = np.array([1, 0, 0, 1])
    # one false positive (1) + one false negative (5), over 4 samples
    assert np.isclose(cost_sensitive_error(y, p, cost), 6 / 4)


def test_perfect_predictions_cost_nothing():
    y = np.array([0, 1, 2, 1])
    assert cost_sensitive_error(y, y, 5.0 * (1.0 - np.eye(3))) == 0.0


def test_three_class_matrix():
    cost = np.array([[0, 2, 9], [1, 0, 3], [4, 6, 0]], dtype=float)
    y = np.array([0, 1, 2])
    p = np.array([2, 2, 1])
    assert np.isclose(cost_sensitive_error(y, p, cost), (9 + 3 + 6) / 3)


def test_empty_input_is_zero():
    assert cost_sensitive_error(np.array([], dtype=int), np.array([], dtype=int), np.eye(2)) == 0.0


def test_returns_python_float():
    assert isinstance(cost_sensitive_error(np.array([0]), np.array([1]), np.ones((2, 2))), float)
