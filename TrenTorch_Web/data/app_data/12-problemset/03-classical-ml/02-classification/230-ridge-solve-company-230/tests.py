"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[1.0, 0.0], [0.0, 1.0]], [1.0, 2.0], 0.0), [1.0, 2.0], atol=1e-6)


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0], 1.0), [0.0, 0.0], atol=1e-6)


def test_all_negative_values():
    np.testing.assert_allclose(solve([[1.0, 0.0], [0.0, 1.0]], [-1.0, -2.0], 0.0), [-1.0, -2.0], atol=1e-6)


def test_all_positive_values():
    np.testing.assert_allclose(solve([[1.0, 0.0], [0.0, 1.0]], [2.0, 3.0], 0.5), [1.3333333333333333, 2.0], atol=1e-6)


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[2.0]], [4.0], 0.0), [2.0], atol=1e-6)


def test_repeated_values():
    np.testing.assert_allclose(solve([[1.0, 0.0], [1.0, 0.0]], [2.0, 2.0], 0.1), [1.9047619047619047, 0.0], atol=1e-6)


def test_mixed_signs():
    np.testing.assert_allclose(solve([[1.0, 0.0], [0.0, 1.0]], [-1.0, 1.0], 0.0), [-1.0, 1.0], atol=1e-6)


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1.0, 0.0], [0.0, 1.0]], [1e-08, 2e-08], 0.0), [1e-08, 2e-08], atol=1e-6)


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[1.0, 0.0], [0.0, 1.0]], [1000000.0, 2000000.0], 0.0), [1000000.0, 2000000.0], atol=1e-6)


def test_parameter_nudge():
    X = [[1.0, 0.0], [1.0, 0.0]]
    y = [2.0, 2.0]
    no_reg = solve(X, y, 0.001)
    with_reg = solve(X, y, 10.0)
    assert not np.allclose(no_reg, with_reg)


def test_reversed_order():
    X = [[1.0, 0.0], [0.0, 1.0]]
    y = [1.0, 2.0]
    np.testing.assert_allclose(solve(X, y, 0.0), solve(X[::-1], y[::-1], 0.0), atol=1e-9)


def test_large_regularization_shrinks_toward_zero():
    X = [[1.0, 0.0], [0.0, 1.0]]
    y = [10.0, 10.0]
    out = solve(X, y, 1e6)
    assert np.all(np.abs(out) < 0.1)


def test_large_n_1e5():
    X = np.eye(2)
    X = np.tile(X, (50000, 1))
    y = np.tile([1.0, 2.0], 50000)
    out = solve(X, y, 0.0)
    np.testing.assert_allclose(out, [1.0, 2.0], atol=1e-6)
