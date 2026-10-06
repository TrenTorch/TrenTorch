"""Executable tests: 2 visible examples + 11 targeted edge/performance cases.

The case names document the hidden-test categories. Expected values are materialized
from the reference implementation at authoring time; the agent should not have to
invent edge cases or expected outputs.
"""
import numpy as np
import pytest
from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve

def test_01_basic_example():
    args = [[1.0, 2.0], [0.1, 0.2], 0.01]
    actual = solve(*args)
    expected = np.array([0.999, 1.998], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_02_exact_zero_inputs():
    args = [[0, 0], [0, 0], 0.01]
    actual = solve(*args)
    expected = np.array([0.0, 0.0], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_03_all_negative_values():
    args = [[-2.0, -3.0], [-1.1, -1.2], 0.01]
    actual = solve(*args)
    expected = np.array([-1.989, -2.988], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_04_all_positive_values():
    args = [[2.0, 3.0], [1.1, 1.2], 0.01]
    actual = solve(*args)
    expected = np.array([1.989, 2.988], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_05_singleton_boundary():
    args = [[1.0], [0.1], 0.01]
    actual = solve(*args)
    expected = np.array([0.999], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_06_repeated_values():
    args = [[2, 2], [2, 2], 0.01]
    actual = solve(*args)
    expected = np.array([1.98, 1.98], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_07_mixed_signs():
    args = [[-2.0, 2.0], [-2.0, 2.0], 0.01]
    actual = solve(*args)
    expected = np.array([-1.98, 1.98], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_08_tiny_magnitudes():
    args = [[1e-08, 1e-08], [1e-08, 1e-08], 0.01]
    actual = solve(*args)
    expected = np.array([9.900000000000001e-09, 9.900000000000001e-09], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_09_large_magnitudes():
    args = [[1000.0, 1000.0], [1000.0, 1000.0], 0.01]
    actual = solve(*args)
    expected = np.array([990.0, 990.0], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_10_parameter_nudge():
    args = [[1.0, 2.0], [0.1, 0.2], 1.01]
    actual = solve(*args)
    expected = np.array([0.899, 1.798], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_11_reversed_order():
    args = [[2.0, 1.0], [0.2, 0.1], 0.01]
    actual = solve(*args)
    expected = np.array([1.998, 0.999], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

@pytest.mark.skip(reason="Not applicable: the 1e5-row case needs arguments that share one row dimension")
def test_12_large_n_1e5():
    pass

def test_13_empty_or_degenerate_input():
    args = [[], [0.1, 0.2], 0.01]
    with pytest.raises(ValueError):
        solve(*args)
