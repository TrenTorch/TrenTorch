import numpy as np
from _load import load_solution


_module = load_solution(__file__)
hardtanh = _module.hardtanh


def test_zero():
    result = hardtanh(np.array(0.0))
    np.testing.assert_allclose(result, 0.0)


def test_within_range_positive():
    result = hardtanh(np.array(0.5))
    np.testing.assert_allclose(result, 0.5)


def test_within_range_negative():
    result = hardtanh(np.array(-0.5))
    np.testing.assert_allclose(result, -0.5)


def test_boundary_lower():
    result = hardtanh(np.array(-1.0))
    np.testing.assert_allclose(result, -1.0)


def test_boundary_upper():
    result = hardtanh(np.array(1.0))
    np.testing.assert_allclose(result, 1.0)


def test_large_negative():
    result = hardtanh(np.array(-100.0))
    np.testing.assert_allclose(result, -1.0)


def test_large_positive():
    result = hardtanh(np.array(100.0))
    np.testing.assert_allclose(result, 1.0)


def test_vector():
    x = np.array([-10.0, -0.5, 0.0, 0.5, 10.0])
    result = hardtanh(x)
    expected = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    np.testing.assert_allclose(result, expected)


def test_2d_shape():
    x = np.array([[0.0, 2.0], [-2.0, 0.5]])
    result = hardtanh(x)
    assert result.shape == (2, 2)


def test_range_bounded():
    x = np.linspace(-100.0, 100.0, 201)
    result = hardtanh(x)
    assert np.all(result >= -1.0)
    assert np.all(result <= 1.0)


def test_monotonic():
    x = np.linspace(-5.0, 5.0, 11)
    result = hardtanh(x)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]


def test_input_not_modified():
    x = np.array([-0.5, 0.0, 0.5])
    x_before = x.copy()
    hardtanh(x)
    assert np.array_equal(x, x_before)


def test_identity_in_range():
    x = np.linspace(-0.8, 0.8, 9)
    result = hardtanh(x)
    np.testing.assert_allclose(result, x)
