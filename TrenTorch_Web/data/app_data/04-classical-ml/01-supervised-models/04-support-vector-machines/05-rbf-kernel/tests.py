"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
rbf_kernel = _module.rbf_kernel


def test_known_value_for_a_3_4_5_triangle():
    # squared distance is 25, so exp(-0.1 * 25) = exp(-2.5)
    X = np.array([[0.0, 0.0]])
    Y = np.array([[3.0, 4.0]])
    assert np.isclose(rbf_kernel(X, Y, gamma=0.1)[0, 0], np.exp(-2.5))


def test_default_gamma_is_one():
    X = np.array([[0.0]])
    Y = np.array([[2.0]])
    assert np.isclose(rbf_kernel(X, Y)[0, 0], np.exp(-4.0))


def test_self_kernel_diagonal_is_exactly_one():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(8, 3))
    K = rbf_kernel(X, X, gamma=2.0)
    assert np.allclose(np.diag(K), 1.0, atol=1e-12)
    assert np.all(K <= 1.0 + 1e-12)


def test_output_shape_is_n_by_m_when_sizes_differ():
    X = np.zeros((2, 3))
    Y = np.ones((5, 3))
    assert rbf_kernel(X, Y).shape == (2, 5)


def test_matches_an_explicit_double_loop():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(4, 2))
    Y = rng.normal(size=(6, 2))
    gamma = 0.7
    expected = np.empty((4, 6))
    for i in range(4):
        for j in range(6):
            expected[i, j] = np.exp(-gamma * np.sum((X[i] - Y[j]) ** 2))
    assert np.allclose(rbf_kernel(X, Y, gamma=gamma), expected)


def test_values_lie_in_zero_to_one():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(10, 4))
    K = rbf_kernel(X, X, gamma=0.5)
    assert np.all(K > 0.0)
    assert np.all(K <= 1.0 + 1e-12)


def test_kernel_is_symmetric_for_the_same_point_set():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(6, 3))
    K = rbf_kernel(X, X, gamma=1.3)
    assert np.allclose(K, K.T)


def test_gamma_zero_gives_all_ones():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(3, 2))
    Y = rng.normal(size=(4, 2))
    assert np.allclose(rbf_kernel(X, Y, gamma=0.0), np.ones((3, 4)))


def test_larger_gamma_gives_a_smaller_similarity_for_the_same_pair():
    X = np.array([[0.0, 0.0]])
    Y = np.array([[1.0, 1.0]])
    narrow = rbf_kernel(X, Y, gamma=5.0)[0, 0]
    wide = rbf_kernel(X, Y, gamma=0.1)[0, 0]
    assert narrow < wide


def test_translating_both_inputs_leaves_the_kernel_unchanged():
    rng = np.random.default_rng(5)
    X = rng.normal(size=(4, 2))
    Y = rng.normal(size=(3, 2))
    shift = np.array([10.0, -3.0])
    assert np.allclose(rbf_kernel(X + shift, Y + shift), rbf_kernel(X, Y))


def test_farther_points_are_less_similar_than_closer_ones():
    origin = np.array([[0.0, 0.0]])
    near = np.array([[0.5, 0.0]])
    far = np.array([[2.0, 0.0]])
    assert rbf_kernel(origin, near)[0, 0] > rbf_kernel(origin, far)[0, 0]


def test_result_is_finite_for_large_distances():
    X = np.array([[0.0, 0.0]])
    Y = np.array([[1000.0, 1000.0]])
    result = rbf_kernel(X, Y, gamma=1.0)
    assert np.all(np.isfinite(result))
    assert result[0, 0] == 0.0
