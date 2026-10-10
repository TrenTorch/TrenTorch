"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[2.0, 0.0], [0.0, 2.0]], [1.0, 1.0], [0.0, 0.0]), [2.0, 2.0])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0], [0.0, 0.0]), [0.0, 0.0])


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-2.0, 0.0], [0.0, -2.0]], [1.0, 1.0], [0.0, 0.0]), [-2.0, -2.0])


def test_all_positive_values():
    np.testing.assert_allclose(solve([[2.0, 0.0], [0.0, 2.0]], [2.0, 2.0], [0.0, 0.0]), [4.0, 4.0])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[3.0]], [2.0], [1.0]), [7.0])


def test_repeated_values():
    np.testing.assert_allclose(solve([[1.0, 1.0], [1.0, 1.0]], [1.0, 1.0], [0.0, 0.0]), [2.0, 2.0])


def test_mixed_signs():
    np.testing.assert_allclose(solve([[1.0, 2.0], [2.0, 1.0]], [1.0, -1.0], [0.0, 0.0]), [-1.0, 1.0])


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08, 0.0], [0.0, 1e-08]], [1.0, 1.0], [0.0, 0.0]), [1e-08, 1e-08])


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[10000.0, 0.0], [0.0, 10000.0]], [1.0, 1.0], [0.0, 0.0]), [10000.0, 10000.0])


def test_parameter_nudge():
    A = [[1.0, 2.0], [2.0, 1.0]]
    x = [1.0, -1.0]
    b1 = [0.0, 0.0]
    b2 = [0.001, 0.001]
    np.testing.assert_allclose(np.array(solve(A, x, b2)) - np.array(solve(A, x, b1)), [0.001, 0.001])


def test_reversed_order():
    A = [[1.0, 2.0], [2.0, 1.0]]
    x = [1.0, -1.0]
    b = [0.0, 0.0]
    A_rev = [[1.0, 2.0], [2.0, 1.0]]
    x_rev = [-1.0, 1.0]
    np.testing.assert_allclose(solve(A, x, b), solve(A_rev, x_rev, b)[::-1])


@pytest.mark.skip(reason="Not applicable: a 1e5 x 1e5 dense matrix cannot be materialised")
def test_large_n_1e5():
    pass


def test_empty_or_degenerate_input():
    assert solve(np.zeros((0, 0)), np.array([]), np.array([])).shape == (0,)
