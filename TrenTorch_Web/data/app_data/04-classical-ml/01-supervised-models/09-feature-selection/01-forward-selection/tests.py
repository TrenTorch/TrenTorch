"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
forward_selection = _module.forward_selection


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _orthonormal_columns():
    # Columns are the first four standard basis vectors of R^6, so they are orthogonal.
    return np.eye(6)[:, :4]


def test_exact_linear_target_picks_its_only_column_first():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(30, 4))
    y = X[:, 2]
    assert forward_selection(X, y, 1) == [2]


def test_two_orthogonal_terms_are_picked_in_order_of_contribution():
    # y = 2 * e3 - e1: feature 3 explains more variance than feature 1.
    X = _orthonormal_columns()
    y = 2.0 * X[:, 3] - X[:, 1]
    assert forward_selection(X, y, 2) == [3, 1]


def test_returns_k_distinct_indices():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(25, 5))
    y = rng.normal(size=25)
    picks = forward_selection(X, y, 3)
    assert len(picks) == 3 and len(set(picks)) == 3


def test_all_features_selected_when_k_equals_d():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(20, 4))
    y = rng.normal(size=20)
    assert sorted(forward_selection(X, y, 4)) == [0, 1, 2, 3]


def test_constant_target_still_returns_indices_without_error():
    X = np.arange(12.0).reshape(6, 2)
    y = np.ones(6)
    assert sorted(forward_selection(X, y, 2)) == [0, 1]


def test_ties_go_to_the_smallest_index():
    # Two identical columns give identical scores; the first must be chosen.
    rng = np.random.default_rng(3)
    base = rng.normal(size=15)
    X = np.column_stack([base, base, rng.normal(size=15)])
    y = 3.0 * base + 0.1 * rng.normal(size=15)
    assert forward_selection(X, y, 1) == [0]


def test_each_step_increases_the_in_sample_fit():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(40, 4))
    y = X[:, 0] + 0.5 * X[:, 3] + 0.05 * rng.normal(size=40)
    order = forward_selection(X, y, 4)
    scores = []
    for m in range(1, 5):
        A = np.column_stack([np.ones(40), X[:, order[:m]]])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        scores.append(1.0 - np.sum((y - A @ coef) ** 2) / np.sum((y - y.mean()) ** 2))
    assert all(b >= a - 1e-12 for a, b in zip(scores, scores[1:]))


def test_k_zero_raises():
    assert _raises_value_error(forward_selection, np.zeros((5, 2)), np.zeros(5), 0)


def test_k_larger_than_d_raises():
    assert _raises_value_error(forward_selection, np.zeros((5, 2)), np.zeros(5), 3)


def test_does_not_modify_inputs():
    rng = np.random.default_rng(5)
    X = rng.normal(size=(10, 3))
    y = rng.normal(size=10)
    X0, y0 = X.copy(), y.copy()
    forward_selection(X, y, 2)
    assert np.array_equal(X, X0) and np.array_equal(y, y0)


def test_returns_python_ints():
    rng = np.random.default_rng(6)
    X = rng.normal(size=(12, 3))
    y = rng.normal(size=12)
    assert all(isinstance(j, int) for j in forward_selection(X, y, 2))
