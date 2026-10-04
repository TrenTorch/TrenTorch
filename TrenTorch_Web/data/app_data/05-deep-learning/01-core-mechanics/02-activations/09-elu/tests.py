import numpy as np
from _load import load_solution


_module = load_solution(__file__)
elu = _module.elu


def test_zero():
    result = elu(np.array(0.0))
    np.testing.assert_allclose(result, 0.0)


def test_positive():
    result = elu(np.array(2.0))
    np.testing.assert_allclose(result, 2.0)


def test_small_negative():
    result = elu(np.array(-0.5))
    expected = 1.0 * (np.exp(-0.5) - 1)
    np.testing.assert_allclose(result, expected)


def test_large_negative():
    result = elu(np.array(-10.0))
    expected = 1.0 * (np.exp(-10.0) - 1)
    np.testing.assert_allclose(result, expected)


def test_large_negative_approaches_minus_alpha():
    result = elu(np.array(-100.0))
    assert result < -0.99


def test_custom_alpha():
    result = elu(np.array(-1.0), alpha=2.0)
    expected = 2.0 * (np.exp(-1.0) - 1)
    np.testing.assert_allclose(result, expected)


def test_vector():
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    result = elu(x)
    expected = np.where(x < 0, np.exp(x) - 1, x)
    np.testing.assert_allclose(result, expected)


def test_2d_shape():
    x = np.array([[0.0, 2.0], [-1.0, 1.0]])
    result = elu(x)
    assert result.shape == (2, 2)


def test_negative_region_smooth():
    x = np.linspace(-3.0, -0.1, 10)
    result = elu(x)
    assert np.all(result < 0)
    assert np.all(result > -1.0)


def test_positive_region_identity():
    x = np.linspace(0.1, 3.0, 10)
    result = elu(x)
    np.testing.assert_allclose(result, x)


def test_input_not_modified():
    x = np.array([-1.0, 0.0, 1.0])
    x_before = x.copy()
    elu(x)
    assert np.array_equal(x, x_before)


def test_alpha_scales_negative():
    x = np.array(-1.0)
    result1 = elu(x, alpha=1.0)
    result2 = elu(x, alpha=2.0)
    assert np.isclose(result2, 2.0 * result1)
