"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]]), [[1.0, 1.0], [1.0, 1.0]], atol=1e-9)


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-1.0, -2.0], [-2.0, -4.0], [-3.0, -5.0]]), [[1.0, 0.9819805060619656], [0.9819805060619656, 1.0]], atol=1e-9)


def test_all_positive_values():
    np.testing.assert_allclose(solve([[1.0, 3.0], [2.0, 2.0], [3.0, 1.0]]), [[1.0, -1.0], [-1.0, 1.0]], atol=1e-9)


def test_repeated_values():
    # Constant columns have zero std, so correlation is 0/0 = NaN
    assert np.all(np.isnan(solve([[2.0, 2.0], [2.0, 2.0], [2.0, 2.0]])))


def test_mixed_signs():
    np.testing.assert_allclose(solve([[-1.0, 1.0], [0.0, 0.0], [1.0, -1.0]]), [[1.0, -1.0], [-1.0, 1.0]], atol=1e-9)


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08, 2e-08], [2e-08, 4e-08], [3e-08, 6e-08]]), [[1.0, 1.0], [1.0, 1.0]], atol=1e-9)


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[1000000.0, 2000000.0], [2000000.0, 4000000.0], [3000000.0, 6000000.0]]), [[1.0, 1.0], [1.0, 1.0]], atol=1e-9)


def test_reversed_order():
    X = [[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]]
    np.testing.assert_allclose(solve(X), solve(X[::-1]))


def test_diagonal_is_one():
    out = solve([[1.0, 5.0], [2.0, 3.0], [3.0, 1.0]])
    np.testing.assert_allclose(np.diag(out), [1.0, 1.0])


def test_large_n_1e5():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((100000, 2))
    out = solve(X)
    assert out.shape == (2, 2)
    np.testing.assert_allclose(np.diag(out), [1.0, 1.0], atol=1e-9)
