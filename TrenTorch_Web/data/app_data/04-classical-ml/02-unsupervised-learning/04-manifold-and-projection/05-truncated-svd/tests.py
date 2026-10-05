"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

truncated_svd = load_solution(__file__).truncated_svd


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _rank_two():
    rng = np.random.default_rng(0)
    return rng.normal(size=(8, 2)) @ rng.normal(size=(2, 5))


def test_shapes_for_k_components():
    U, s, Vt = truncated_svd(_rank_two(), 2)
    assert U.shape == (8, 2)
    assert s.shape == (2,)
    assert Vt.shape == (2, 5)


def test_rank_two_matrix_is_reconstructed_exactly_with_k_two():
    X = _rank_two()
    U, s, Vt = truncated_svd(X, 2)
    assert np.allclose(U @ np.diag(s) @ Vt, X, atol=1e-8)


def test_singular_values_are_descending():
    rng = np.random.default_rng(1)
    _, s, _ = truncated_svd(rng.normal(size=(10, 6)), 4)
    assert np.all(np.diff(s) <= 1e-12)


def test_truncation_error_equals_next_singular_value():
    X = _rank_two() + 0.01 * np.random.default_rng(2).normal(size=(8, 5))
    full_s = np.linalg.svd(X, compute_uv=False)
    U, s, Vt = truncated_svd(X, 2)
    err = np.linalg.norm(X - U @ np.diag(s) @ Vt)
    assert np.isclose(err, np.sqrt(np.sum(full_s[2:] ** 2)), atol=1e-8)


def test_matches_numpy_leading_singular_values():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(9, 4))
    _, s, _ = truncated_svd(X, 3)
    assert np.allclose(s, np.linalg.svd(X, compute_uv=False)[:3])


def test_columns_of_u_are_orthonormal():
    U, _, _ = truncated_svd(_rank_two(), 2)
    assert np.allclose(U.T @ U, np.eye(2), atol=1e-8)


def test_data_is_not_centered():
    X = np.ones((4, 3)) * 5.0
    _, s, _ = truncated_svd(X, 1)
    assert np.isclose(s[0], np.linalg.norm(X))


def test_k_out_of_range_raises():
    X = _rank_two()
    assert _raises_value_error(truncated_svd, X, 0)
    assert _raises_value_error(truncated_svd, X, 6)


def test_same_input_gives_same_factors():
    X = _rank_two()
    a = truncated_svd(X, 2)
    b = truncated_svd(X, 2)
    assert all(np.array_equal(p, q) for p, q in zip(a, b))


def test_does_not_modify_the_data():
    X = _rank_two()
    before = X.copy()
    truncated_svd(X, 2)
    assert np.array_equal(X, before)
