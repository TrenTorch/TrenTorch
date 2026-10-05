import numpy as np
from _load import load_solution


_module = load_solution(__file__)
softplus = _module.softplus


def test_zero():
    result = softplus(np.array(0.0))
    expected = np.log(2.0)
    np.testing.assert_allclose(result, expected, atol=1e-6)


def test_positive():
    result = softplus(np.array(2.0))
    expected = np.log(1.0 + np.exp(2.0))
    np.testing.assert_allclose(result, expected, atol=1e-6)


def test_negative():
    result = softplus(np.array(-2.0))
    expected = np.log(1.0 + np.exp(-2.0))
    np.testing.assert_allclose(result, expected, atol=1e-6)


def test_always_positive():
    x = np.linspace(-10.0, 10.0, 100)
    result = softplus(x)
    assert np.all(result > 0.0)


def test_large_positive_approaches_x():
    x = np.array(100.0)
    result = softplus(x)
    assert np.isclose(result, x, rtol=0.01)


def test_large_negative_approaches_zero():
    x = np.array(-100.0)
    result = softplus(x)
    assert result < 1e-40


def test_beta_steepens():
    x = np.array(1.0)
    result1 = softplus(x, beta=1.0)
    result2 = softplus(x, beta=2.0)
    assert result2 > result1


def test_vector():
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    result = softplus(x)
    assert result.shape == (5,)
    assert np.all(result > 0.0)


def test_2d_shape():
    x = np.array([[0.0, 1.0], [-1.0, 2.0]])
    result = softplus(x)
    assert result.shape == (2, 2)


def test_smooth_derivative():
    x = np.linspace(-2.0, 2.0, 10)
    result = softplus(x)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]


def test_input_not_modified():
    x = np.array([-1.0, 0.0, 1.0])
    x_before = x.copy()
    softplus(x)
    assert np.array_equal(x, x_before)


def test_custom_beta():
    x = np.array(0.0)
    result = softplus(x, beta=2.0)
    expected = (1.0 / 2.0) * np.log(2.0)
    np.testing.assert_allclose(result, expected, atol=1e-6)
