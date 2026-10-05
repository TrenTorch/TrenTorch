"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
linear_kernel = _module.linear_kernel


def test_known_values_on_a_small_example():
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    Y = np.array([[5.0, 6.0]])
    expected = np.array([[17.0], [39.0]])
    assert np.allclose(linear_kernel(X, Y), expected)


def test_output_shape_is_n_by_m_when_sizes_differ():
    X = np.ones((2, 3))
    Y = np.ones((4, 3))
    assert linear_kernel(X, Y).shape == (2, 4)


def test_shape_is_correct_when_the_feature_dimension_is_one():
    X = np.array([[2.0], [3.0], [4.0]])
    Y = np.array([[5.0], [6.0]])
    result = linear_kernel(X, Y)
    assert result.shape == (3, 2)
    assert np.allclose(result, [[10.0, 12.0], [15.0, 18.0], [20.0, 24.0]])


def test_matches_an_explicit_double_loop():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(5, 4))
    Y = rng.normal(size=(7, 4))
    expected = np.empty((5, 7))
    for i in range(5):
        for j in range(7):
            expected[i, j] = np.sum(X[i] * Y[j])
    assert np.allclose(linear_kernel(X, Y), expected)


def test_entry_is_the_dot_product_of_the_matching_rows():
    X = np.array([[1.0, -2.0, 0.5]])
    Y = np.array([[0.0, 3.0, 4.0], [2.0, 2.0, 2.0]])
    result = linear_kernel(X, Y)
    assert np.isclose(result[0, 0], -6.0 + 2.0)
    assert np.isclose(result[0, 1], 2.0 - 4.0 + 1.0)


def test_self_kernel_is_symmetric():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(6, 3))
    K = linear_kernel(X, X)
    assert np.allclose(K, K.T)


def test_orthogonal_points_have_zero_similarity():
    X = np.array([[1.0, 0.0]])
    Y = np.array([[0.0, 5.0]])
    assert np.isclose(linear_kernel(X, Y)[0, 0], 0.0)


def test_identical_unit_vectors_have_similarity_one():
    X = np.array([[0.6, 0.8]])
    assert np.isclose(linear_kernel(X, X)[0, 0], 1.0)


def test_scaling_one_input_scales_the_kernel_linearly():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(4, 2))
    Y = rng.normal(size=(3, 2))
    assert np.allclose(linear_kernel(3.0 * X, Y), 3.0 * linear_kernel(X, Y))


def test_does_not_modify_its_inputs():
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    Y = np.array([[5.0, 6.0]])
    X_before, Y_before = X.copy(), Y.copy()
    linear_kernel(X, Y)
    assert np.array_equal(X, X_before)
    assert np.array_equal(Y, Y_before)


def test_zero_rows_give_a_zero_kernel():
    X = np.zeros((2, 3))
    Y = np.ones((4, 3))
    assert np.array_equal(linear_kernel(X, Y), np.zeros((2, 4)))


def test_permuting_rows_of_x_permutes_rows_of_the_kernel():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(5, 3))
    Y = rng.normal(size=(4, 3))
    order = [4, 2, 0, 3, 1]
    assert np.allclose(linear_kernel(X[order], Y), linear_kernel(X, Y)[order])
