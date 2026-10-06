"""Executable tests: 13 categories for the causal mask.

The mask is an n-by-n boolean matrix whose entry (i, j) is True exactly when j <= i.
Categories that do not apply to a non-negative size parameter are skipped with that reason.
"""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def expected_mask(n):
    rows = np.arange(n)[:, None]
    cols = np.arange(n)[None, :]
    return cols <= rows


def test_01_basic_example():
    expected = np.array([[True, False, False], [True, True, False], [True, True, True]])
    assert np.array_equal(solve(3), expected)


def test_02_exact_zero_inputs():
    out = solve(0)
    assert out.shape == (0, 0)
    assert out.dtype == bool


def test_04_all_positive_values():
    assert np.array_equal(solve(4), expected_mask(4))


def test_05_singleton_boundary():
    assert np.array_equal(solve(1), np.array([[True]]))


def test_09_large_magnitudes():
    n = 1000
    out = solve(n)
    assert out.shape == (n, n)
    assert int(out.sum()) == n * (n + 1) // 2


def test_10_parameter_nudge():
    assert np.array_equal(solve(3)[:2, :2], solve(2))
    assert np.array_equal(solve(4)[:3, :3], solve(3))


def test_13_empty_or_degenerate_input():
    assert solve(0).size == 0
