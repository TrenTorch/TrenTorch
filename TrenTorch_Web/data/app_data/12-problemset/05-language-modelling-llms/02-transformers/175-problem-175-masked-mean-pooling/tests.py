"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[[1.0, 1.0], [3.0, 3.0]]], [[True, True]]), [[2.0, 2.0]])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[[0.0, 0.0], [0.0, 0.0]]], [[True, True]]), [[0.0, 0.0]])


def test_all_negative_values():
    np.testing.assert_allclose(solve([[[-1.0, -1.0], [-3.0, -3.0]]], [[True, True]]), [[-2.0, -2.0]])


def test_all_positive_values():
    np.testing.assert_allclose(solve([[[2.0, 2.0], [4.0, 4.0]]], [[True, True]]), [[3.0, 3.0]])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[[5.0, 5.0]]], [[True]]), [[5.0, 5.0]])


def test_repeated_values():
    np.testing.assert_allclose(solve([[[2.0, 2.0], [2.0, 2.0]]], [[True, True]]), [[2.0, 2.0]])


def test_mixed_signs():
    np.testing.assert_allclose(solve([[[-1.0, 1.0], [1.0, -1.0]]], [[True, True]]), [[0.0, 0.0]])


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[[1e-08, 1e-08], [2e-08, 2e-08]]], [[True, True]]), [[1.5000000000000002e-08, 1.5000000000000002e-08]])


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[[1000000.0, 1000000.0], [2000000.0, 2000000.0]]], [[True, True]]), [[1500000.0, 1500000.0]])


def test_all_masked_row_is_zero():
    np.testing.assert_allclose(solve([[[1.0, 1.0], [3.0, 3.0]]], [[False, False]]), [[0.0, 0.0]])


def test_partial_mask_averages_only_unmasked():
    np.testing.assert_allclose(solve([[[1.0, 1.0], [3.0, 3.0]]], [[True, False]]), [[1.0, 1.0]])


def test_large_n_1e5():
    emb = np.ones((1, 100000, 2))
    mask = np.ones((1, 100000), dtype=bool)
    np.testing.assert_allclose(solve(emb, mask), [[1.0, 1.0]])


def test_empty_or_degenerate_input():
    out = solve(np.zeros((0, 2, 3)), np.zeros((0, 2), dtype=bool))
    assert out.shape == (0, 3)
