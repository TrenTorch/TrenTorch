"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    ids, labels = solve([1, 2, 3, 4], [False, True, False, True], -100)
    np.testing.assert_array_equal(ids, [1, 2, 3, 4])
    np.testing.assert_array_equal(labels, [-100, 2, -100, 4])


def test_exact_zero_inputs():
    ids, labels = solve([0, 0, 0], [True, True, True], -100)
    np.testing.assert_array_equal(ids, [0, 0, 0])
    np.testing.assert_array_equal(labels, [0, 0, 0])


def test_all_negative_values():
    ids, labels = solve([-1, -2, -3], [True, False, True], -100)
    np.testing.assert_array_equal(ids, [-1, -2, -3])
    np.testing.assert_array_equal(labels, [-1, -100, -3])


def test_all_positive_values():
    ids, labels = solve([1, 2, 3], [True, True, False], -100)
    np.testing.assert_array_equal(ids, [1, 2, 3])
    np.testing.assert_array_equal(labels, [1, 2, -100])


def test_singleton_boundary():
    ids, labels = solve([5], [True], -100)
    np.testing.assert_array_equal(ids, [5])
    np.testing.assert_array_equal(labels, [5])


def test_repeated_values():
    ids, labels = solve([2, 2, 2], [False, True, False], -100)
    np.testing.assert_array_equal(ids, [2, 2, 2])
    np.testing.assert_array_equal(labels, [-100, 2, -100])


def test_mixed_signs():
    ids, labels = solve([-1, 0, 1], [True, False, True], -100)
    np.testing.assert_array_equal(ids, [-1, 0, 1])
    np.testing.assert_array_equal(labels, [-1, -100, 1])


def test_tiny_magnitudes():
    ids, labels = solve([1, 2], [True, True], -1)
    np.testing.assert_array_equal(ids, [1, 2])
    np.testing.assert_array_equal(labels, [1, 2])


def test_no_positions_masked_gives_all_ignore():
    ids, labels = solve([1, 2, 3], [False, False, False])
    np.testing.assert_array_equal(labels, [-100, -100, -100])


def test_all_positions_masked_keeps_original_ids_as_labels():
    ids, labels = solve([1, 2, 3], [True, True, True])
    np.testing.assert_array_equal(labels, ids)


def test_large_n_1e5():
    ids = np.arange(100000)
    mask = np.zeros(100000, dtype=bool)
    mask[::2] = True
    _, labels = solve(ids, mask)
    assert int((labels != -100).sum()) == 50000


def test_empty_or_degenerate_input():
    ids, labels = solve(np.array([], dtype=int), np.array([], dtype=bool))
    assert ids.shape == (0,) and labels.shape == (0,)
