"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

gaussian_random_projection = load_solution(__file__).gaussian_random_projection


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _data():
    return np.random.default_rng(0).normal(size=(12, 200))


def test_output_shape_is_n_by_k():
    assert gaussian_random_projection(_data(), 30).shape == (12, 30)


def test_same_seed_gives_same_projection():
    X = _data()
    assert np.array_equal(gaussian_random_projection(X, 30, seed=7),
                          gaussian_random_projection(X, 30, seed=7))


def test_different_seeds_give_different_projections():
    X = _data()
    a = gaussian_random_projection(X, 30, seed=1)
    b = gaussian_random_projection(X, 30, seed=2)
    assert not np.allclose(a, b)


def test_projection_is_linear():
    X = _data()
    Y = np.random.default_rng(5).normal(size=X.shape)
    a = gaussian_random_projection(X + Y, 20, seed=3)
    b = gaussian_random_projection(X, 20, seed=3) + gaussian_random_projection(Y, 20, seed=3)
    assert np.allclose(a, b)


def test_pairwise_squared_distances_are_roughly_preserved():
    X = _data()
    Z = gaussian_random_projection(X, 120, seed=0)
    orig = np.sum((X[:, None] - X[None]) ** 2, axis=2)
    proj = np.sum((Z[:, None] - Z[None]) ** 2, axis=2)
    mask = ~np.eye(len(X), dtype=bool)
    ratio = proj[mask] / orig[mask]
    assert abs(np.mean(ratio) - 1.0) < 0.1


def test_zero_input_stays_zero():
    Z = gaussian_random_projection(np.zeros((4, 10)), 3, seed=0)
    assert np.allclose(Z, 0.0)


def test_k_below_one_raises():
    assert _raises_value_error(gaussian_random_projection, _data(), 0)


def test_does_not_modify_the_data():
    X = _data()
    before = X.copy()
    gaussian_random_projection(X, 10)
    assert np.array_equal(X, before)
