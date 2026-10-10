"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    dX, dW, db = solve([[1.0, 2.0]], [[1.0, 2.0]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[1.0, 2.0]])
    np.testing.assert_allclose(dW, [[1.0, 2.0], [2.0, 4.0]])
    np.testing.assert_allclose(db, [1.0, 2.0])


def test_exact_zero_inputs():
    dX, dW, db = solve([[0.0, 0.0]], [[0.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[0.0, 0.0]])
    np.testing.assert_allclose(dW, [[0.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(db, [0.0, 0.0])


def test_all_negative_values():
    dX, dW, db = solve([[-1.0, -2.0]], [[-1.0, -2.0]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[-1.0, -2.0]])
    np.testing.assert_allclose(dW, [[1.0, 2.0], [2.0, 4.0]])
    np.testing.assert_allclose(db, [-1.0, -2.0])


def test_all_positive_values():
    dX, dW, db = solve([[2.0, 3.0]], [[1.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[1.0, 1.0]])
    np.testing.assert_allclose(dW, [[2.0, 2.0], [3.0, 3.0]])
    np.testing.assert_allclose(db, [1.0, 1.0])


def test_singleton_boundary():
    dX, dW, db = solve([[2.0]], [[3.0]], [[4.0]])
    np.testing.assert_allclose(dX, [[12.0]])
    np.testing.assert_allclose(dW, [[6.0]])
    np.testing.assert_allclose(db, [3.0])


def test_repeated_values():
    dX, dW, db = solve([[1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[1.0, 1.0], [1.0, 1.0]])
    np.testing.assert_allclose(dW, [[2.0, 2.0], [2.0, 2.0]])
    np.testing.assert_allclose(db, [2.0, 2.0])


def test_mixed_signs():
    dX, dW, db = solve([[1.0, -1.0]], [[-1.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[-1.0, 1.0]])
    np.testing.assert_allclose(dW, [[-1.0, 1.0], [1.0, -1.0]])
    np.testing.assert_allclose(db, [-1.0, 1.0])


def test_tiny_magnitudes():
    dX, dW, db = solve([[1e-08, 2e-08]], [[1e-08, 1e-08]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[1e-08, 1e-08]])
    np.testing.assert_allclose(dW, [[1.0000000000000001e-16, 1.0000000000000001e-16], [2.0000000000000002e-16, 2.0000000000000002e-16]])
    np.testing.assert_allclose(db, [1e-08, 1e-08])


def test_large_magnitudes():
    dX, dW, db = solve([[10000.0, 20000.0]], [[1.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(dX, [[1.0, 1.0]])
    np.testing.assert_allclose(dW, [[10000.0, 10000.0], [20000.0, 20000.0]])
    np.testing.assert_allclose(db, [1.0, 1.0])


def test_parameter_nudge():
    X = [[1.0, 2.0]]
    dY1 = [[1.0, 0.0]]
    dY2 = [[2.0, 0.0]]
    W = [[1.0, 0.0], [0.0, 1.0]]
    dX1, dW1, db1 = solve(X, dY1, W)
    dX2, dW2, db2 = solve(X, dY2, W)
    np.testing.assert_allclose(dX2, 2 * np.array(dX1))
    np.testing.assert_allclose(dW2, 2 * np.array(dW1))


def test_reversed_order():
    X = [[1.0, 2.0], [3.0, 4.0]]
    dY = [[1.0, 0.0], [0.0, 1.0]]
    W = [[1.0, 0.0], [0.0, 1.0]]
    dX, dW, db = solve(X, dY, W)
    dX_r, dW_r, db_r = solve(X[::-1], dY[::-1], W)
    np.testing.assert_allclose(dX_r, dX[::-1])
    np.testing.assert_allclose(dW_r, dW)
    np.testing.assert_allclose(db_r, db)


def test_large_n_1e5():
    X = np.ones((100000, 1))
    dY = np.ones((100000, 1))
    W = np.array([[2.0]])
    dX, dW, db = solve(X, dY, W)
    assert dX.shape == (100000, 1)
    np.testing.assert_allclose(dW, [[100000.0]])
    np.testing.assert_allclose(db, [100000.0])


def test_empty_or_degenerate_input():
    dX, dW, db = solve(np.zeros((0, 2)), np.zeros((0, 2)), np.eye(2))
    assert dX.shape == (0, 2) and dW.shape == (2, 2) and db.shape == (2,)
