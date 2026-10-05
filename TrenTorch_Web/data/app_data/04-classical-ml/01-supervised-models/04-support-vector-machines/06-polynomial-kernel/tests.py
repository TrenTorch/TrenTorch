"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
polynomial_kernel = _module.polynomial_kernel


def test_degree_one_with_no_offset_is_the_linear_kernel():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(4, 3))
    Y = rng.normal(size=(5, 3))
    assert np.allclose(polynomial_kernel(X, Y, degree=1, coef0=0.0, gamma=1.0), X @ Y.T)


def test_known_value_with_degree_two_and_offset_one():
    # dot = 1*3 + 2*4 = 11, so (11 + 1) ** 2 = 144
    X = np.array([[1.0, 2.0]])
    Y = np.array([[3.0, 4.0]])
    assert np.isclose(polynomial_kernel(X, Y, degree=2, coef0=1.0, gamma=1.0)[0, 0], 144.0)


def test_defaults_are_degree_three_offset_one_gamma_one():
    # dot = 11, so (11 + 1) ** 3 = 1728
    X = np.array([[1.0, 2.0]])
    Y = np.array([[3.0, 4.0]])
    assert np.isclose(polynomial_kernel(X, Y)[0, 0], 1728.0)


def test_gamma_scales_the_dot_product_before_the_power():
    # gamma * dot = 0.5 * 11 = 5.5, and with coef0 = 0 and degree 2: 5.5 ** 2 = 30.25
    X = np.array([[1.0, 2.0]])
    Y = np.array([[3.0, 4.0]])
    result = polynomial_kernel(X, Y, degree=2, coef0=0.0, gamma=0.5)
    assert np.isclose(result[0, 0], 30.25)


def test_offset_is_added_before_the_power_not_after():
    # Correct form is (gamma * dot + coef0) ** degree, not gamma * (dot + coef0) ** degree.
    # dot = 2, gamma = 2, coef0 = 1, degree = 2: (2 * 2 + 1) ** 2 = 25, while the wrong form gives 2 * (2 + 1) ** 2 = 18.
    X = np.array([[2.0]])
    Y = np.array([[1.0]])
    assert np.isclose(polynomial_kernel(X, Y, degree=2, coef0=1.0, gamma=2.0)[0, 0], 25.0)


def test_coef0_changes_the_result():
    X = np.array([[1.0, 0.0]])
    Y = np.array([[1.0, 0.0]])
    without_offset = polynomial_kernel(X, Y, degree=2, coef0=0.0)[0, 0]
    with_offset = polynomial_kernel(X, Y, degree=2, coef0=1.0)[0, 0]
    assert np.isclose(without_offset, 1.0)
    assert np.isclose(with_offset, 4.0)


def test_output_shape_is_n_by_m_when_sizes_differ():
    X = np.ones((2, 3))
    Y = np.ones((5, 3))
    assert polynomial_kernel(X, Y).shape == (2, 5)


def test_matches_an_explicit_double_loop():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(3, 2))
    Y = rng.normal(size=(4, 2))
    degree, coef0, gamma = 3, 0.5, 0.8
    expected = np.empty((3, 4))
    for i in range(3):
        for j in range(4):
            expected[i, j] = (gamma * np.dot(X[i], Y[j]) + coef0) ** degree
    assert np.allclose(polynomial_kernel(X, Y, degree=degree, coef0=coef0, gamma=gamma), expected)


def test_even_degree_gives_nonnegative_values():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(6, 3))
    K = polynomial_kernel(X, X, degree=2, coef0=0.0, gamma=1.0)
    assert np.all(K >= 0.0)


def test_self_kernel_is_symmetric():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(5, 2))
    K = polynomial_kernel(X, X, degree=3)
    assert np.allclose(K, K.T)


def test_odd_degree_keeps_the_sign_of_the_base():
    # dot = -2, base = -2 + 1 = -1, (-1) ** 3 = -1
    X = np.array([[-2.0]])
    Y = np.array([[1.0]])
    assert np.isclose(polynomial_kernel(X, Y, degree=3, coef0=1.0, gamma=1.0)[0, 0], -1.0)


def test_zero_gamma_gives_coef0_to_the_power_of_degree_everywhere():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(3, 2))
    Y = rng.normal(size=(4, 2))
    assert np.allclose(polynomial_kernel(X, Y, degree=3, coef0=2.0, gamma=0.0), 8.0)
