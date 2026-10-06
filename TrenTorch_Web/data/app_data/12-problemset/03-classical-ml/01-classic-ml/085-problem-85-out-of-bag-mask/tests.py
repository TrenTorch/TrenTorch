"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    expected = np.array([False, False, False] + [True] * 7)
    np.testing.assert_array_equal(solve(10, [0, 1, 2]), expected)


def test_02_empty_bootstrap_is_all_out_of_bag():
    np.testing.assert_array_equal(solve(3, []), [True, True, True])


def test_03_duplicates_do_not_change_mask():
    np.testing.assert_array_equal(solve(5, [0, 2, 2]), [False, True, False, True, True])


def test_04_all_drawn_gives_no_out_of_bag():
    np.testing.assert_array_equal(solve(3, [2, 0, 1, 1]), [False, False, False])


def test_05_singleton_boundary():
    np.testing.assert_array_equal(solve(1, [0]), [False])


def test_06_zero_samples_gives_empty_mask():
    assert solve(0, []).shape == (0,)
