"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[[1.0, 2.0, 3.0, 4.0]]], 2), [[[[1.0, 2.0]], [[3.0, 4.0]]]])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[[0.0, 0.0, 0.0, 0.0]]], 2), [[[[0.0, 0.0]], [[0.0, 0.0]]]])


def test_all_negative_values():
    np.testing.assert_allclose(solve([[[-1.0, -2.0, -3.0, -4.0]]], 2), [[[[-1.0, -2.0]], [[-3.0, -4.0]]]])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[[5.0]]], 1), [[[[5.0]]]])


def test_repeated_values():
    np.testing.assert_allclose(solve([[[2.0, 2.0, 2.0, 2.0]]], 4), [[[[2.0]], [[2.0]], [[2.0]], [[2.0]]]])


def test_mixed_signs():
    np.testing.assert_allclose(solve([[[-1.0, 1.0, -2.0, 2.0]]], 2), [[[[-1.0, 1.0]], [[-2.0, 2.0]]]])


def test_invalid_n_heads_raises():
    with pytest.raises(ValueError):
        solve([[[1.0, 2.0, 3.0]]], 2)


def test_zero_n_heads_raises():
    with pytest.raises(ValueError):
        solve([[[1.0, 2.0]]], 0)


def test_merge_is_inverse_of_split():
    X = np.arange(24, dtype=float).reshape(1, 2, 12)
    split = solve(X, 3)
    merged = split.transpose(0, 2, 1, 3).reshape(1, 2, 12)
    np.testing.assert_allclose(merged, X)


def test_large_n_1e5():
    X = np.ones((1, 100000, 4))
    out = solve(X, 2)
    assert out.shape == (1, 2, 100000, 2)
