import numpy as np
from _load import load_solution


_module = load_solution(__file__)
hard_sigmoid = _module.hard_sigmoid


def test_zero_input():
    x = np.array(0.0)
    result = hard_sigmoid(x)
    expected = 0.5
    np.testing.assert_allclose(result, expected)


def test_negative_input_in_linear_region():
    x = np.array(-1.0)
    result = hard_sigmoid(x)
    expected = (-1.0 + 2.5) / 5.0
    np.testing.assert_allclose(result, expected)


def test_positive_input_in_linear_region():
    x = np.array(1.5)
    result = hard_sigmoid(x)
    expected = (1.5 + 2.5) / 5.0
    np.testing.assert_allclose(result, expected)


def test_large_negative_input():
    x = np.array(-10.0)
    result = hard_sigmoid(x)
    expected = 0.0
    np.testing.assert_allclose(result, expected)


def test_large_positive_input():
    x = np.array(10.0)
    result = hard_sigmoid(x)
    expected = 1.0
    np.testing.assert_allclose(result, expected)


def test_boundary_lower():
    x = np.array(-2.5)
    result = hard_sigmoid(x)
    expected = 0.0
    np.testing.assert_allclose(result, expected)


def test_boundary_upper():
    x = np.array(2.5)
    result = hard_sigmoid(x)
    expected = 1.0
    np.testing.assert_allclose(result, expected)


def test_vector_input():
    x = np.array([-10.0, -1.0, 0.0, 1.0, 10.0])
    result = hard_sigmoid(x)
    expected = np.array([0.0, 0.3, 0.5, 0.7, 1.0])
    np.testing.assert_allclose(result, expected)


def test_2d_shape_preserved():
    x = np.array([[0.0, 1.0], [-1.0, 2.0]])
    result = hard_sigmoid(x)
    assert result.shape == (2, 2)


def test_input_not_modified():
    x = np.array([-1.0, 0.0, 1.0])
    x_before = x.copy()
    hard_sigmoid(x)
    assert np.array_equal(x, x_before)


def test_monotonic_increasing():
    x = np.linspace(-5.0, 5.0, 11)
    result = hard_sigmoid(x)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]


def test_range_bounded():
    x = np.linspace(-100.0, 100.0, 201)
    result = hard_sigmoid(x)
    assert np.all(result >= 0.0)
    assert np.all(result <= 1.0)


def test_matches_sigmoid_in_linear_region():
    x = np.linspace(-0.5, 0.5, 5)
    result = hard_sigmoid(x)
    assert np.all(result >= 0.4)
    assert np.all(result <= 0.6)
