"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    dX, dW1, db1, dW2, db2 = solve([[1.0, 2.0]], [[1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0], [1.0]], ([[1.0, 2.0]], [[1.0, 2.0]]))
    np.testing.assert_allclose(dX, [[1.0, 1.0]])
    np.testing.assert_allclose(dW1, [[1.0, 1.0], [2.0, 2.0]])
    np.testing.assert_allclose(db1, [1.0, 1.0])
    np.testing.assert_allclose(dW2, [[1.0], [2.0]])
    np.testing.assert_allclose(db2, [1.0])


def test_exact_zero_inputs():
    dX, dW1, db1, dW2, db2 = solve([[0.0, 0.0]], [[0.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0], [1.0]], ([[0.0, 0.0]], [[0.0, 0.0]]))
    np.testing.assert_allclose(dX, [[0.0, 0.0]])
    np.testing.assert_allclose(dW1, [[0.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(db1, [0.0, 0.0])
    np.testing.assert_allclose(dW2, [[0.0], [0.0]])
    np.testing.assert_allclose(db2, [0.0])


def test_all_negative_values():
    dX, dW1, db1, dW2, db2 = solve([[-1.0, -2.0]], [[1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0], [1.0]], ([[-1.0, -2.0]], [[0.0, 0.0]]))
    np.testing.assert_allclose(dX, [[0.0, 0.0]])
    np.testing.assert_allclose(dW1, [[0.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(db1, [0.0, 0.0])
    np.testing.assert_allclose(dW2, [[0.0], [0.0]])
    np.testing.assert_allclose(db2, [1.0])


def test_singleton_boundary():
    dX, dW1, db1, dW2, db2 = solve([[2.0]], [[1.0]], [[1.0]], [[1.0]], ([[2.0]], [[2.0]]))
    np.testing.assert_allclose(dX, [[1.0]])
    np.testing.assert_allclose(dW1, [[2.0]])
    np.testing.assert_allclose(db1, [1.0])
    np.testing.assert_allclose(dW2, [[2.0]])
    np.testing.assert_allclose(db2, [1.0])


def test_repeated_values():
    dX, dW1, db1, dW2, db2 = solve([[1.0, 1.0]], [[1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0], [1.0]], ([[1.0, 1.0]], [[1.0, 1.0]]))
    np.testing.assert_allclose(dX, [[1.0, 1.0]])
    np.testing.assert_allclose(dW1, [[1.0, 1.0], [1.0, 1.0]])
    np.testing.assert_allclose(db1, [1.0, 1.0])
    np.testing.assert_allclose(dW2, [[1.0], [1.0]])
    np.testing.assert_allclose(db2, [1.0])


def test_mixed_signs():
    dX, dW1, db1, dW2, db2 = solve([[1.0, -1.0]], [[1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0], [1.0]], ([[1.0, -1.0]], [[1.0, 0.0]]))
    np.testing.assert_allclose(dX, [[1.0, 0.0]])
    np.testing.assert_allclose(dW1, [[1.0, 0.0], [-1.0, 0.0]])
    np.testing.assert_allclose(db1, [1.0, 0.0])
    np.testing.assert_allclose(dW2, [[1.0], [0.0]])
    np.testing.assert_allclose(db2, [1.0])


def test_relu_blocks_negative_preactivation():
    dX, dW1, db1, dW2, db2 = solve([[1.0, 2.0]], [[5.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0], [1.0]], ([[-1.0, 2.0]], [[0.0, 2.0]]))
    np.testing.assert_allclose(dX, [[0.0, 5.0]])
    np.testing.assert_allclose(dW1, [[0.0, 5.0], [0.0, 10.0]])
    np.testing.assert_allclose(db1, [0.0, 5.0])
    np.testing.assert_allclose(dW2, [[0.0], [10.0]])
    np.testing.assert_allclose(db2, [5.0])


def test_large_n_1e5():
    X = np.ones((100000, 1))
    W1 = np.array([[1.0]])
    W2 = np.array([[1.0]])
    z1 = X @ W1
    h = np.maximum(z1, 0)
    dY = np.ones((100000, 1))
    dX, dW1, db1, dW2, db2 = solve(X, dY, W1, W2, (z1, h))
    assert dX.shape == (100000, 1)
    np.testing.assert_allclose(dW2, [[100000.0]])


def test_empty_or_degenerate_input():
    dX, dW1, db1, dW2, db2 = solve(np.zeros((0, 1)), np.zeros((0, 1)), np.array([[1.0]]), np.array([[1.0]]), (np.zeros((0, 1)), np.zeros((0, 1))))
    assert dX.shape == (0, 1)
