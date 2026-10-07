"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[1.0, 3.0], [3.0, 5.0]]), [2.0, 4.0])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[0.0, 0.0], [0.0, 0.0]]), [0.0, 0.0])


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-1.0, -2.0], [-3.0, -4.0]]), [-2.0, -3.0])


def test_all_positive_values():
    np.testing.assert_allclose(solve([[2.0, 4.0], [4.0, 6.0]]), [3.0, 5.0])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[5.0, 5.0]]), [5.0, 5.0])


def test_repeated_values():
    np.testing.assert_allclose(solve([[2.0, 2.0], [2.0, 2.0]]), [2.0, 2.0])


def test_mixed_signs():
    np.testing.assert_allclose(solve([[-1.0, 1.0], [1.0, -1.0]]), [0.0, 0.0])


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08, 2e-08], [3e-08, 4e-08]]), [2e-08, 3.0000000000000004e-08])


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[1000000.0, 2000000.0], [3000000.0, 4000000.0]]), [2000000.0, 3000000.0])


def test_reversed_order():
    grads = [[1.0, 2.0], [3.0, 4.0]]
    np.testing.assert_allclose(solve(grads), solve(grads[::-1]))


def test_single_microbatch_is_identity():
    np.testing.assert_allclose(solve([[7.0, -2.0]]), [7.0, -2.0])


def test_large_n_1e5():
    grads = np.ones((100000, 2))
    np.testing.assert_allclose(solve(grads), [1.0, 1.0])


def test_empty_or_degenerate_input():
    assert np.isnan(solve([]))
