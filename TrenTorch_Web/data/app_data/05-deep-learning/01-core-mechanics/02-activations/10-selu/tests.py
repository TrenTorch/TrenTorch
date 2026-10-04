import numpy as np
from _load import load_solution


_module = load_solution(__file__)
selu = _module.selu


LAMBDA = 1.0507
ALPHA = 1.6733


def test_zero():
    result = selu(np.array(0.0))
    np.testing.assert_allclose(result, 0.0)


def test_positive():
    result = selu(np.array(2.0))
    expected = LAMBDA * 2.0
    np.testing.assert_allclose(result, expected)


def test_negative():
    result = selu(np.array(-1.0))
    expected = LAMBDA * ALPHA * (np.exp(-1.0) - 1)
    np.testing.assert_allclose(result, expected)


def test_large_positive():
    result = selu(np.array(5.0))
    expected = LAMBDA * 5.0
    np.testing.assert_allclose(result, expected)


def test_large_negative():
    result = selu(np.array(-10.0))
    expected = LAMBDA * ALPHA * (np.exp(-10.0) - 1)
    np.testing.assert_allclose(result, expected)


def test_vector():
    x = np.array([-1.0, 0.0, 1.0])
    result = selu(x)
    expected = LAMBDA * np.where(
        x < 0,
        ALPHA * (np.exp(x) - 1),
        x,
    )
    np.testing.assert_allclose(result, expected)


def test_2d_shape():
    x = np.array([[0.0, 1.0], [-1.0, 2.0]])
    result = selu(x)
    assert result.shape == (2, 2)


def test_positive_scaled_by_lambda():
    x = np.array(1.0)
    result = selu(x)
    assert np.isclose(result, LAMBDA)


def test_negative_scaled():
    x = np.array(-0.5)
    result = selu(x)
    expected = LAMBDA * ALPHA * (np.exp(-0.5) - 1)
    np.testing.assert_allclose(result, expected)


def test_input_not_modified():
    x = np.array([-1.0, 0.0, 1.0])
    x_before = x.copy()
    selu(x)
    assert np.array_equal(x, x_before)


def test_negative_region_bounded():
    x = np.linspace(-5.0, -0.1, 10)
    result = selu(x)
    lower = LAMBDA * ALPHA * (-1.0)
    assert np.all(result > lower * 1.01)
    assert np.all(result < 0.0)


def test_positive_region_identity_scaled():
    x = np.linspace(0.1, 5.0, 10)
    result = selu(x)
    expected = LAMBDA * x
    np.testing.assert_allclose(result, expected)


def test_monotonic():
    x = np.linspace(-5.0, 5.0, 100)
    result = selu(x)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]
