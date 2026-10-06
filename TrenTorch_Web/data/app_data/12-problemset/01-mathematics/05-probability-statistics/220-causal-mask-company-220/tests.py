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


@pytest.mark.skip(reason="Not applicable: n is a size and must be non-negative")
def test_03_all_negative_values():
    pass


def test_04_all_positive_values():
    assert np.array_equal(solve(4), expected_mask(4))


def test_05_singleton_boundary():
    assert np.array_equal(solve(1), np.array([[True]]))


@pytest.mark.skip(reason="Not applicable: the mask has no repeated input values")
def test_06_repeated_values():
    pass


@pytest.mark.skip(reason="Not applicable: the mask has no mixed-sign input values")
def test_07_mixed_signs():
    pass


@pytest.mark.skip(reason="Not applicable: the mask is boolean with no magnitudes")
def test_08_tiny_magnitudes():
    pass


def test_09_large_magnitudes():
    n = 1000
    out = solve(n)
    assert out.shape == (n, n)
    assert int(out.sum()) == n * (n + 1) // 2


def test_10_parameter_nudge():
    assert np.array_equal(solve(3)[:2, :2], solve(2))
    assert np.array_equal(solve(4)[:3, :3], solve(3))


@pytest.mark.skip(reason="Not applicable: the mask has no ordering to reverse")
def test_11_reversed_order():
    pass


@pytest.mark.skip(reason="Not applicable: an n-by-n mask for n=1e5 cannot be materialised")
def test_12_large_n_1e5():
    pass


def test_13_empty_or_degenerate_input():
    assert solve(0).size == 0
