"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([1.0, 2.0], lambda v: v * 2), [3.0, 6.0])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([0.0, 0.0], lambda v: v + 1), [1.0, 1.0])


def test_all_negative_values():
    np.testing.assert_allclose(solve([-1.0, -2.0], lambda v: v), [-2.0, -4.0])


def test_all_positive_values():
    np.testing.assert_allclose(solve([1.0, 2.0], lambda v: v), [2.0, 4.0])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([5.0], lambda v: v * 0), [5.0])


def test_repeated_values():
    np.testing.assert_allclose(solve([3.0, 3.0], lambda v: v), [6.0, 6.0])


def test_mixed_signs():
    np.testing.assert_allclose(solve([-1.0, 1.0], lambda v: -v), [0.0, 0.0])


def test_identity_sublayer_doubles_input():
    np.testing.assert_allclose(solve([2.0, -3.0], lambda v: v), [4.0, -6.0])


def test_zero_sublayer_is_identity():
    np.testing.assert_allclose(solve([2.0, -3.0], lambda v: v * 0), [2.0, -3.0])


def test_large_n_1e5():
    x = np.ones(100000)
    np.testing.assert_allclose(solve(x, lambda v: v), np.full(100000, 2.0))


def test_empty_or_degenerate_input():
    out = solve(np.zeros(0), lambda v: v)
    assert out.shape == (0,)
