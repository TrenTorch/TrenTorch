"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_array_equal(solve([1, 2, 0, 0], 0), [True, True, False, False])


def test_exact_zero_inputs():
    np.testing.assert_array_equal(solve([0, 0, 0], 0), [False, False, False])


def test_all_negative_values():
    np.testing.assert_array_equal(solve([-1, -2, -3], 0), [True, True, True])


def test_all_positive_values():
    np.testing.assert_array_equal(solve([1, 2, 3], 0), [True, True, True])


def test_singleton_boundary():
    np.testing.assert_array_equal(solve([5], 0), [True])


def test_repeated_values():
    np.testing.assert_array_equal(solve([3, 3, 3], 3), [False, False, False])


def test_mixed_signs():
    np.testing.assert_array_equal(solve([-1, 0, 1], 0), [True, False, True])


def test_parameter_nudge():
    np.testing.assert_array_equal(solve([1, 2, 3], 2), [True, False, True])


def test_reversed_order():
    ids = [1, 2, 0]
    np.testing.assert_array_equal(solve(ids, 0)[::-1], solve(ids[::-1], 0))


def test_large_n_1e5():
    ids = np.concatenate([np.ones(50000, dtype=int), np.zeros(50000, dtype=int)])
    out = solve(ids, 0)
    assert out.shape == (100000,)
    assert int(out.sum()) == 50000


def test_empty_or_degenerate_input():
    out = solve([], 0)
    assert out.shape == (0,)
