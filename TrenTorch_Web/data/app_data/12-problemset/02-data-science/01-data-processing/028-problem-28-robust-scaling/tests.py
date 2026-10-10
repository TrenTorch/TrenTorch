"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[1.0], [2.0], [3.0], [4.0]]), [[-1.0], [-0.3333333333333333], [0.3333333333333333], [1.0]])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[0.0], [0.0], [0.0]]), [[0.0], [0.0], [0.0]])


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-4.0], [-3.0], [-2.0], [-1.0]]), [[-1.0], [-0.3333333333333333], [0.3333333333333333], [1.0]])


def test_all_positive_values():
    np.testing.assert_allclose(solve([[2.0], [4.0], [6.0], [8.0]]), [[-1.0], [-0.3333333333333333], [0.3333333333333333], [1.0]])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[5.0]]), [[0.0]])


def test_repeated_values():
    np.testing.assert_allclose(solve([[3.0], [3.0], [3.0]]), [[0.0], [0.0], [0.0]])


def test_mixed_signs():
    np.testing.assert_allclose(solve([[-2.0], [0.0], [2.0], [4.0]]), [[-1.0], [-0.3333333333333333], [0.3333333333333333], [1.0]])


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08], [2e-08], [3e-08], [4e-08]]), [[-1.0], [-0.33333333333333326], [0.33333333333333326], [1.0000000000000002]])


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[1000000.0], [2000000.0], [3000000.0], [4000000.0]]), [[-1.0], [-0.3333333333333333], [0.3333333333333333], [1.0]])


def test_parameter_nudge():
    base = solve([[1.0], [2.0], [3.0], [4.0]])
    scaled = solve([[10.0], [20.0], [30.0], [40.0]])
    np.testing.assert_allclose(base, scaled)


def test_reversed_order():
    X = [[1.0], [2.0], [3.0], [4.0]]
    np.testing.assert_allclose(solve(X)[::-1], solve(X[::-1]))


def test_large_n_1e5():
    X = np.arange(100000, dtype=float).reshape(-1, 1)
    assert solve(X).shape == (100000, 1)


def test_empty_or_degenerate_input():
    with pytest.raises(IndexError):
        solve(np.zeros((0, 1)))
