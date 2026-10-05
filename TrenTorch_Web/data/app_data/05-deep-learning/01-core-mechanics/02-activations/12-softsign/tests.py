import numpy as np
from _load import load_solution


_module = load_solution(__file__)
softsign = _module.softsign


def test_zero():
    result = softsign(np.array(0.0))
    np.testing.assert_allclose(result, 0.0)


def test_positive():
    result = softsign(np.array(1.0))
    expected = 1.0 / 2.0
    np.testing.assert_allclose(result, expected)


def test_negative():
    result = softsign(np.array(-1.0))
    expected = -1.0 / 2.0
    np.testing.assert_allclose(result, expected)


def test_range_bounded():
    x = np.linspace(-100.0, 100.0, 201)
    result = softsign(x)
    assert np.all(result > -1.0)
    assert np.all(result < 1.0)


def test_odd_function():
    x = np.array(2.0)
    result_pos = softsign(x)
    result_neg = softsign(-x)
    np.testing.assert_allclose(result_neg, -result_pos)


def test_large_positive():
    result = softsign(np.array(100.0))
    expected = 100.0 / 101.0
    np.testing.assert_allclose(result, expected)


def test_large_negative():
    result = softsign(np.array(-100.0))
    expected = -100.0 / 101.0
    np.testing.assert_allclose(result, expected)


def test_vector():
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    result = softsign(x)
    expected = x / (1.0 + np.abs(x))
    np.testing.assert_allclose(result, expected)


def test_2d_shape():
    x = np.array([[0.0, 1.0], [-1.0, 2.0]])
    result = softsign(x)
    assert result.shape == (2, 2)


def test_monotonic():
    x = np.linspace(-5.0, 5.0, 100)
    result = softsign(x)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]


def test_approaches_one():
    x = np.linspace(10.0, 1000.0, 10)
    result = softsign(x)
    assert np.all(result > 0.99)
    assert np.all(result < 1.0)


def test_input_not_modified():
    x = np.array([-1.0, 0.0, 1.0])
    x_before = x.copy()
    softsign(x)
    assert np.array_equal(x, x_before)


def test_small_input():
    x = np.array(0.01)
    result = softsign(x)
    expected = 0.01 / 1.01
    np.testing.assert_allclose(result, expected, atol=1e-6)
