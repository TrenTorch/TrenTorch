"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [1.0, 1.0]), [0.9640275800758169, 1.5231883119115297], atol=1e-9)


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([0.0, 0.0], [[0.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [1.0, 1.0]), [0.0], atol=1e-9)


def test_all_negative_values():
    np.testing.assert_allclose(solve([-1.0, 0.0], [[-1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [1.0, 1.0]), [-0.9640275800758169], atol=1e-9)


def test_singleton_boundary():
    np.testing.assert_allclose(solve([1.0], [[1.0]], [[1.0]], [[1.0]], [1.0]), [0.9640275800758169], atol=1e-9)


def test_mixed_signs():
    np.testing.assert_allclose(solve([1.0, -1.0], [[1.0, -1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [1.0, -1.0]), [1.9280551601516338], atol=1e-9)


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([1e-08, 0.0], [[1e-08, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [1.0, 1.0]), [1.9999999999999997e-08], atol=1e-9)


def test_large_n_1e5():
    query = [0.0, 0.0]
    keys = np.zeros((100000, 2))
    Wq = [[1.0, 0.0], [0.0, 1.0]]
    Wk = [[1.0, 0.0], [0.0, 1.0]]
    v = [1.0, 1.0]
    out = solve(query, keys, Wq, Wk, v)
    assert out.shape == (100000,)
    np.testing.assert_allclose(out, np.zeros(100000))
