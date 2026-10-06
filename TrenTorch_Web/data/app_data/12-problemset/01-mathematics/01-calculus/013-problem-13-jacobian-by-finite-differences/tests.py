"""Executable tests: 13 categories for the Jacobian by finite differences.

f(z) = [z0**2, z0*z1] has Jacobian [[2*z0, 0], [z1, z0]], used as the analytic reference.
"""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def f(z):
    z = np.asarray(z, dtype=float)
    return np.array([z[0] ** 2, z[0] * z[1]])


def jacobian(x0, x1):
    return np.array([[2 * x0, 0.0], [x1, x0]])


def test_01_basic_example():
    np.testing.assert_allclose(solve(f, [1.0, 2.0], 1e-5), jacobian(1.0, 2.0), atol=1e-6, rtol=1e-6)


def test_02_exact_zero_inputs():
    np.testing.assert_allclose(solve(f, [0.0, 0.0]), jacobian(0.0, 0.0), atol=1e-6)


def test_03_all_negative_values():
    np.testing.assert_allclose(solve(f, [-1.0, -2.0]), jacobian(-1.0, -2.0), atol=1e-6, rtol=1e-6)


def test_04_all_positive_values():
    np.testing.assert_allclose(solve(f, [3.0, 4.0]), jacobian(3.0, 4.0), atol=1e-6, rtol=1e-6)


@pytest.mark.skip(reason="Not applicable: f needs two inputs, so there is no single-element case")
def test_05_singleton_boundary():
    pass


def test_06_repeated_values():
    np.testing.assert_allclose(solve(f, [2.0, 2.0]), jacobian(2.0, 2.0), atol=1e-6, rtol=1e-6)


def test_07_mixed_signs():
    np.testing.assert_allclose(solve(f, [-1.0, 2.0]), jacobian(-1.0, 2.0), atol=1e-6, rtol=1e-6)


def test_08_tiny_magnitudes():
    np.testing.assert_allclose(solve(f, [1e-8, 1e-8]), jacobian(1e-8, 1e-8), atol=1e-6)


def test_09_large_magnitudes():
    np.testing.assert_allclose(solve(f, [1e4, 1e4]), jacobian(1e4, 1e4), rtol=1e-6, atol=1e-2)


def test_10_parameter_nudge():
    np.testing.assert_allclose(solve(f, [1.0, 2.0], 1e-3), jacobian(1.0, 2.0), atol=1e-6, rtol=1e-6)


def test_11_reversed_order():
    np.testing.assert_allclose(solve(f, [2.0, 1.0]), jacobian(2.0, 1.0), atol=1e-6, rtol=1e-6)


@pytest.mark.skip(reason="Not applicable: the Jacobian size is fixed by f, not by a sample count")
def test_12_large_n_1e5():
    pass


def test_13_empty_or_degenerate_input():
    with pytest.raises(IndexError):
        solve(f, [])
