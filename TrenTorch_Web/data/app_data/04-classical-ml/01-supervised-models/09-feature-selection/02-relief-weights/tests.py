"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
relief_weights = _module.relief_weights


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_informative_feature_gets_weight_one_and_constant_gets_zero():
    # y equals feature 0; feature 1 is constant, so its weight is exactly 0.
    X = np.array([[0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [1.0, 0.0]])
    y = np.array([0, 0, 1, 1])
    assert np.allclose(relief_weights(X, y), [1.0, 0.0])


def test_constant_feature_always_has_zero_weight():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(12, 3))
    X[:, 2] = 5.0
    y = rng.integers(0, 2, size=12)
    assert relief_weights(X, y)[2] == 0.0


def test_output_has_one_weight_per_feature():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(10, 4))
    y = rng.integers(0, 2, size=10)
    assert relief_weights(X, y).shape == (4,)


def test_scaling_every_feature_by_the_same_factor_does_not_change_weights():
    # Distances and feature ranges both scale by c, so every ratio is unchanged.
    rng = np.random.default_rng(2)
    X = rng.normal(size=(15, 3))
    y = (X[:, 0] > 0).astype(int)
    assert np.allclose(relief_weights(7.0 * X, y), relief_weights(X, y))


def test_relevant_feature_is_weighted_above_irrelevant_one():
    rng = np.random.default_rng(3)
    X = rng.uniform(size=(60, 2))
    y = (X[:, 0] > 0.5).astype(int)
    w = relief_weights(X, y)
    assert w[0] > w[1]


def test_clean_separation_gives_weight_one():
    X = np.array([[0.0], [0.0], [0.0], [1.0], [1.0], [1.0]])
    y = np.array([0, 0, 0, 1, 1, 1])
    assert np.isclose(relief_weights(X, y)[0], 1.0)


def test_label_renaming_does_not_change_the_weights():
    X = np.array([[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0], [0.5, 0.5]])
    y = np.array([0, 0, 1, 1, 0])
    assert np.allclose(relief_weights(X, y), relief_weights(X, 9 - y))


def test_single_class_gives_zero_weights():
    X = np.array([[0.0], [1.0], [2.0]])
    y = np.array([0, 0, 0])
    assert np.allclose(relief_weights(X, y), [0.0])


def test_matches_a_plain_loop_implementation():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(8, 3))
    y = rng.integers(0, 2, size=8)
    spread = X.max(0) - X.min(0)
    expected = np.zeros(3)
    for i in range(8):
        hit_d, miss_d = np.inf, np.inf
        hit, miss = None, None
        for k in range(8):
            if k == i:
                continue
            dd = np.sqrt(np.sum((X[i] - X[k]) ** 2))
            if y[k] == y[i] and dd < hit_d:
                hit_d, hit = dd, k
            if y[k] != y[i] and dd < miss_d:
                miss_d, miss = dd, k
        if hit is None or miss is None:
            continue
        expected += (np.abs(X[i] - X[miss]) - np.abs(X[i] - X[hit])) / spread
    assert np.allclose(relief_weights(X, y), expected / 8)


def test_wrong_shape_raises():
    assert _raises_value_error(relief_weights, np.zeros(5), np.zeros(5))


def test_label_length_mismatch_raises():
    assert _raises_value_error(relief_weights, np.zeros((4, 2)), np.zeros(3))


def test_single_sample_raises():
    assert _raises_value_error(relief_weights, np.zeros((1, 2)), np.zeros(1))


def test_does_not_modify_inputs():
    X = np.array([[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]])
    y = np.array([0, 0, 1, 1])
    X0, y0 = X.copy(), y.copy()
    relief_weights(X, y)
    assert np.array_equal(X, X0) and np.array_equal(y, y0)
