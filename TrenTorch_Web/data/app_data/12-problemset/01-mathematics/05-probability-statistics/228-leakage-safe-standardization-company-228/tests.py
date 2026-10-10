"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    tr, va = solve([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0]])
    np.testing.assert_allclose(tr, [[-1.0, -1.0], [1.0, 1.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[3.0, 3.0]], atol=1e-9)


def test_exact_zero_inputs():
    tr, va = solve([[0.0, 0.0], [0.0, 0.0]], [[1.0, 1.0]])
    np.testing.assert_allclose(tr, [[0.0, 0.0], [0.0, 0.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[1.0, 1.0]], atol=1e-9)


def test_all_negative_values():
    tr, va = solve([[-1.0, -2.0], [-3.0, -4.0]], [[-5.0, -6.0]])
    np.testing.assert_allclose(tr, [[1.0, 1.0], [-1.0, -1.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[-3.0, -3.0]], atol=1e-9)


def test_all_positive_values():
    tr, va = solve([[2.0, 4.0], [4.0, 6.0]], [[6.0, 8.0]])
    np.testing.assert_allclose(tr, [[-1.0, -1.0], [1.0, 1.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[3.0, 3.0]], atol=1e-9)


def test_singleton_boundary():
    tr, va = solve([[2.0, 2.0]], [[3.0, 3.0]])
    np.testing.assert_allclose(tr, [[0.0, 0.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[1.0, 1.0]], atol=1e-9)


def test_repeated_values():
    tr, va = solve([[1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0]])
    np.testing.assert_allclose(tr, [[0.0, 0.0], [0.0, 0.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[0.0, 0.0]], atol=1e-9)


def test_mixed_signs():
    tr, va = solve([[-1.0, 1.0], [1.0, -1.0]], [[0.0, 0.0]])
    np.testing.assert_allclose(tr, [[-1.0, 1.0], [1.0, -1.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[0.0, 0.0]], atol=1e-9)


def test_tiny_magnitudes():
    tr, va = solve([[1e-08, 1e-08], [2e-08, 2e-08]], [[3e-08, 3e-08]])
    np.testing.assert_allclose(tr, [[-1.0000000000000002, -1.0000000000000002], [0.9999999999999997, 0.9999999999999997]], atol=1e-9)
    np.testing.assert_allclose(va, [[2.999999999999999, 2.999999999999999]], atol=1e-9)


def test_large_magnitudes():
    tr, va = solve([[1000000.0, 1000000.0], [2000000.0, 2000000.0]], [[3000000.0, 3000000.0]])
    np.testing.assert_allclose(tr, [[-1.0, -1.0], [1.0, 1.0]], atol=1e-9)
    np.testing.assert_allclose(va, [[3.0, 3.0]], atol=1e-9)


def test_statistics_come_only_from_train():
    tr1, va1 = solve([[1.0], [3.0]], [[100.0]])
    tr2, va2 = solve([[1.0], [3.0]], [[-100.0]])
    np.testing.assert_allclose(tr1, tr2)


def test_reversed_order():
    train = [[1.0], [2.0], [3.0]]
    val = [[4.0]]
    tr, va = solve(train, val)
    tr_r, va_r = solve(train[::-1], val)
    np.testing.assert_allclose(tr_r, tr[::-1])
    np.testing.assert_allclose(va_r, va)


def test_large_n_1e5():
    train = np.arange(100000, dtype=float).reshape(-1, 1)
    val = np.array([[0.0]])
    tr, va = solve(train, val)
    assert tr.shape == (100000, 1)
    assert abs(tr.mean()) < 1e-6


def test_empty_or_degenerate_input():
    tr, va = solve(np.zeros((0, 1)), np.zeros((0, 1)))
    assert tr.shape == (0, 1) and va.shape == (0, 1)
