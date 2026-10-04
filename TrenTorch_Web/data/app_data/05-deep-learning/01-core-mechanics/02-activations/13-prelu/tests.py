import numpy as np
from _load import load_solution


_module = load_solution(__file__)
prelu = _module.prelu


def test_zero():
    result = prelu(np.array(0.0), alpha=0.01)
    np.testing.assert_allclose(result, 0.0)


def test_positive():
    result = prelu(np.array(2.0), alpha=0.01)
    np.testing.assert_allclose(result, 2.0)


def test_negative_with_scalar_alpha():
    result = prelu(np.array(-2.0), alpha=0.01)
    expected = -0.02
    np.testing.assert_allclose(result, expected)


def test_alpha_zero_is_relu():
    x = np.array([-1.0, 0.0, 1.0])
    result = prelu(x, alpha=0.0)
    expected = np.array([0.0, 0.0, 1.0])
    np.testing.assert_allclose(result, expected)


def test_alpha_one_is_identity():
    x = np.array([-2.0, 0.0, 2.0])
    result = prelu(x, alpha=1.0)
    np.testing.assert_allclose(result, x)


def test_scalar_alpha():
    x = np.array([-2.0, 1.0])
    result = prelu(x, alpha=0.1)
    expected = np.array([-0.2, 1.0])
    np.testing.assert_allclose(result, expected)


def test_vector_alpha():
    x = np.array([-1.0, -2.0])
    alpha = np.array([0.1, 0.2])
    result = prelu(x, alpha)
    expected = np.array([-0.1, -0.4])
    np.testing.assert_allclose(result, expected)


def test_2d_shape():
    x = np.array([[0.0, 1.0], [-1.0, 2.0]])
    result = prelu(x, alpha=0.01)
    assert result.shape == (2, 2)


def test_2d_with_scalar_alpha():
    x = np.array([[0.0, 2.0], [-2.0, 1.0]])
    result = prelu(x, alpha=0.1)
    expected = np.array([[0.0, 2.0], [-0.2, 1.0]])
    np.testing.assert_allclose(result, expected)


def test_monotonic_positive_region():
    x = np.linspace(0.0, 5.0, 10)
    result = prelu(x, alpha=0.01)
    np.testing.assert_allclose(result, x)


def test_negative_region_scaled():
    x = np.linspace(-5.0, -0.1, 10)
    result = prelu(x, alpha=0.1)
    expected = 0.1 * x
    np.testing.assert_allclose(result, expected)


def test_input_not_modified():
    x = np.array([-1.0, 0.0, 1.0])
    x_before = x.copy()
    prelu(x, alpha=0.01)
    assert np.array_equal(x, x_before)


def test_large_alpha():
    x = np.array(-1.0)
    result1 = prelu(x, alpha=0.1)
    result2 = prelu(x, alpha=0.5)
    assert result2 < result1


def test_alpha_array_broadcast():
    x = np.array([-1.0, -2.0, -3.0])
    alpha = np.array([0.1, 0.2, 0.3])
    result = prelu(x, alpha)
    expected = alpha * x
    np.testing.assert_allclose(result, expected)
