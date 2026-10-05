"""
pytest tests.py
"""

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
is_negative_definite = _module.is_negative_definite
is_negative_semidefinite = _module.is_negative_semidefinite
quadratic_maximizer = _module.quadratic_maximizer


def _random_nd(n, seed):
    b = np.random.default_rng(seed).normal(size=(n, n))
    return -(b @ b.T + np.eye(n))


# ---- 1-6: negative definite ----


def test_1_diagonal_with_negative_entries_is_negative_definite():
    assert is_negative_definite(np.diag([-1.0, -2.0, -3.0]))


def test_2_random_negated_gram_matrices_are_negative_definite():
    for seed in range(5):
        assert is_negative_definite(_random_nd(4, seed))


def test_3_a_zero_eigenvalue_is_not_negative_definite():
    assert not is_negative_definite(np.array([[-1.0, 0.0], [0.0, 0.0]]))


def test_4_a_positive_eigenvalue_is_not_negative_definite():
    assert not is_negative_definite(np.array([[-1.0, 0.0], [0.0, 1.0]]))
    assert not is_negative_definite(np.eye(3))


def test_5_non_symmetric_and_non_square_are_not_negative_definite():
    assert not is_negative_definite(np.array([[-2.0, 1.0], [0.0, -2.0]]))
    assert not is_negative_definite(-np.ones((2, 3)))


def test_6_matches_negation_of_positive_definiteness():
    a = _random_nd(4, 7)
    assert is_negative_definite(a) and not is_negative_definite(-a)


# ---- 7-11: negative semi-definite ----


def test_7_negative_definite_is_also_semidefinite():
    assert is_negative_semidefinite(np.diag([-1.0, -5.0]))


def test_8_singular_negative_semidefinite_passes():
    a = np.array([[-1.0, 1.0], [1.0, -1.0]])  # eigenvalues -2 and 0
    assert is_negative_semidefinite(a)
    assert not is_negative_definite(a)


def test_9_zero_matrix_is_negative_semidefinite_but_not_definite():
    assert is_negative_semidefinite(np.zeros((3, 3)))
    assert not is_negative_definite(np.zeros((3, 3)))


def test_10_tolerance_separates_rounding_error_from_real_curvature():
    assert is_negative_semidefinite(np.array([[-1.0, 0.0], [0.0, 1e-12]]))
    assert not is_negative_semidefinite(np.array([[-1.0, 0.0], [0.0, 1e-3]]))
    assert not is_negative_semidefinite(np.array([[-1.0, 0.0], [0.0, 1e-12]]), tol=0.0)


def test_11_positive_definite_and_non_symmetric_are_not_negative_semidefinite():
    assert not is_negative_semidefinite(np.eye(2))
    assert not is_negative_semidefinite(np.array([[-1.0, 3.0], [0.0, -1.0]]))


# ---- 12-16: the maximizer ----


def test_12_hand_computed_one_dimensional_peak():
    # f(x) = -x^2 + 4x peaks at x = 2 (a = [[-2]], b = [4])
    np.testing.assert_allclose(quadratic_maximizer(np.array([[-2.0]]), np.array([4.0])), [2.0])


def test_13_gradient_is_zero_at_the_maximizer():
    a = _random_nd(5, 8)
    b = np.random.default_rng(9).normal(size=5)
    x = quadratic_maximizer(a, b)
    np.testing.assert_allclose(a @ x + b, np.zeros(5), atol=1e-10)


def test_14_value_at_the_maximizer_beats_nearby_points():
    a = _random_nd(3, 10)
    b = np.array([1.0, -2.0, 0.5])
    f = lambda x: 0.5 * x @ a @ x + b @ x
    best = quadratic_maximizer(a, b)
    rng = np.random.default_rng(11)
    for _ in range(50):
        assert f(best) >= f(best + rng.normal(size=3) * 0.5)


def test_15_non_negative_definite_matrices_raise_value_error():
    b = np.array([1.0, 1.0])
    for a in (np.eye(2), np.zeros((2, 2)), np.array([[-1.0, 0.0], [0.0, 0.0]]), np.array([[-1.0, 0.0], [0.0, 1.0]])):
        with pytest.raises(ValueError):
            quadratic_maximizer(a, b)


def test_16_inputs_are_not_modified():
    a, b = _random_nd(3, 12), np.array([1.0, 2.0, 3.0])
    a_copy, b_copy = a.copy(), b.copy()
    quadratic_maximizer(a, b)
    np.testing.assert_array_equal(a, a_copy)
    np.testing.assert_array_equal(b, b_copy)
