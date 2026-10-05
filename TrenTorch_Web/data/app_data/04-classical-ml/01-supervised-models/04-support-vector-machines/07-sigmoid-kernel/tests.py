"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sigmoid_kernel = _module.sigmoid_kernel


def test_known_value_with_unit_inputs():
    X = np.array([[1.0]])
    Y = np.array([[1.0]])
    assert np.isclose(sigmoid_kernel(X, Y, gamma=1.0, coef0=0.0)[0, 0], np.tanh(1.0))


def test_defaults_are_gamma_one_and_offset_zero():
    X = np.array([[0.5, 0.5]])
    Y = np.array([[1.0, 1.0]])
    assert np.isclose(sigmoid_kernel(X, Y)[0, 0], np.tanh(1.0))


def test_zero_inputs_give_tanh_of_the_offset():
    X = np.zeros((2, 3))
    Y = np.zeros((4, 3))
    assert np.allclose(sigmoid_kernel(X, Y, gamma=2.0, coef0=0.5), np.tanh(0.5))


def test_gamma_zero_gives_tanh_of_the_offset_everywhere():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(3, 2))
    Y = rng.normal(size=(5, 2))
    assert np.allclose(sigmoid_kernel(X, Y, gamma=0.0, coef0=-0.3), np.tanh(-0.3))


def test_offset_is_added_inside_the_tanh():
    # gamma * dot + coef0 = 2 * 1 + 0.5 = 2.5
    X = np.array([[1.0]])
    Y = np.array([[1.0]])
    assert np.isclose(sigmoid_kernel(X, Y, gamma=2.0, coef0=0.5)[0, 0], np.tanh(2.5))


def test_values_lie_strictly_inside_minus_one_and_one():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(10, 4)) * 0.5
    K = sigmoid_kernel(X, X, gamma=1.0)
    assert np.all(K > -1.0)
    assert np.all(K < 1.0)


def test_negative_alignment_gives_a_negative_value():
    X = np.array([[1.0, 0.0]])
    Y = np.array([[-1.0, 0.0]])
    assert sigmoid_kernel(X, Y, gamma=1.0, coef0=0.0)[0, 0] < 0.0


def test_output_shape_is_n_by_m_when_sizes_differ():
    X = np.ones((2, 3))
    Y = np.ones((6, 3))
    assert sigmoid_kernel(X, Y).shape == (2, 6)


def test_matches_an_explicit_double_loop():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(4, 3))
    Y = rng.normal(size=(3, 3))
    gamma, coef0 = 0.4, -0.2
    expected = np.empty((4, 3))
    for i in range(4):
        for j in range(3):
            expected[i, j] = np.tanh(gamma * np.dot(X[i], Y[j]) + coef0)
    assert np.allclose(sigmoid_kernel(X, Y, gamma=gamma, coef0=coef0), expected)


def test_self_kernel_is_symmetric():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(5, 2))
    K = sigmoid_kernel(X, X, gamma=0.7, coef0=0.1)
    assert np.allclose(K, K.T)


def test_large_positive_alignment_saturates_near_one():
    X = np.array([[100.0]])
    Y = np.array([[100.0]])
    assert np.isclose(sigmoid_kernel(X, Y, gamma=1.0)[0, 0], 1.0)


def test_swapping_the_arguments_transposes_the_kernel():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(3, 2))
    Y = rng.normal(size=(5, 2))
    assert np.allclose(sigmoid_kernel(X, Y, gamma=0.6, coef0=0.2), sigmoid_kernel(Y, X, gamma=0.6, coef0=0.2).T)
