"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    h_new, cell = solve([0.5], [0.5], [0.0], [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]], [0.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(h_new, [0.11308555459718517], atol=1e-9)
    np.testing.assert_allclose(cell, [0.19946529748821443], atol=1e-9)


def test_exact_zero_inputs():
    h_new, cell = solve([0.0], [0.0], [0.0], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [0.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(h_new, [0.0], atol=1e-9)
    np.testing.assert_allclose(cell, [0.0], atol=1e-9)


def test_all_negative_values():
    h_new, cell = solve([-0.5], [-0.5], [-1.0], [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]], [0.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(h_new, [-0.23767359898722454], atol=1e-9)
    np.testing.assert_allclose(cell, [-0.6306496674545327], atol=1e-9)


def test_repeated_values():
    h_new, cell = solve([1.0], [1.0], [1.0], [[0.2, 0.2], [0.2, 0.2], [0.2, 0.2], [0.2, 0.2]], [0.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(h_new, [0.40615441537483654], atol=1e-9)
    np.testing.assert_allclose(cell, [0.8261584152871869], atol=1e-9)


def test_mixed_signs():
    h_new, cell = solve([1.0], [-1.0], [0.5], [[0.1, -0.1], [-0.2, 0.2], [0.3, -0.3], [-0.4, 0.4]], [0.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(h_new, [-0.10523366960536037], atol=1e-9)
    np.testing.assert_allclose(cell, [-0.16445382181506502], atol=1e-9)


def test_tiny_magnitudes():
    h_new, cell = solve([1e-08], [1e-08], [0.0], [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]], [0.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(h_new, [2.0000000080000005e-09], atol=1e-9)
    np.testing.assert_allclose(cell, [4.000000004000001e-09], atol=1e-9)


def test_large_magnitudes():
    h_new, cell = solve([10.0], [10.0], [10.0], [[0.01, 0.01], [0.01, 0.01], [0.01, 0.01], [0.01, 0.01]], [0.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(h_new, [0.5498191654444256], atol=1e-9)
    np.testing.assert_allclose(cell, [5.606863634414869], atol=1e-9)


def test_large_n_1e5():
    x = np.ones(1)
    h = np.zeros(1)
    c = np.zeros(1)
    W = np.zeros((4, 2))
    b = np.zeros(4)
    h_new, cell = solve(x, h, c, W, b)
    assert h_new.shape == (1,) and cell.shape == (1,)
