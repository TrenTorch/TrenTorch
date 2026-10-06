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
    args = [[1.0, 2.0, 3.0], [0.5, 0.5, 0.5], 0.1]
    actual = solve(*args)
    expected = np.array([1.05, 2.05, 3.05], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_02_exact_zero_inputs():
    args = [[0, 0, 0], [0, 0, 0], 0.1]
    actual = solve(*args)
    expected = np.array([0.0, 0.0, 0.0], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_03_all_negative_values():
    args = [[-2.0, -3.0, -4.0], [-1.5, -1.5, -1.5], 0.1]
    actual = solve(*args)
    expected = np.array([-2.15, -3.15, -4.15], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_04_all_positive_values():
    args = [[2.0, 3.0, 4.0], [1.5, 1.5, 1.5], 0.1]
    actual = solve(*args)
    expected = np.array([2.15, 3.15, 4.15], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_05_singleton_boundary():
    args = [[1.0], [0.5], 0.1]
    actual = solve(*args)
    expected = np.array([1.05], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_06_repeated_values():
    args = [[2, 2, 2], [2, 2, 2], 0.1]
    actual = solve(*args)
    expected = np.array([2.2, 2.2, 2.2], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_07_mixed_signs():
    args = [[-2.0, 0.0, 2.0], [-2.0, 0.0, 2.0], 0.1]
    actual = solve(*args)
    expected = np.array([-2.2, 0.0, 2.2], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_08_tiny_magnitudes():
    args = [[1e-08, 1e-08, 1e-08], [1e-08, 1e-08, 1e-08], 0.1]
    actual = solve(*args)
    expected = np.array([1.1000000000000001e-08, 1.1000000000000001e-08, 1.1000000000000001e-08], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_09_large_magnitudes():
    args = [[1000.0, 1000.0, 1000.0], [1000.0, 1000.0, 1000.0], 0.1]
    actual = solve(*args)
    expected = np.array([1100.0, 1100.0, 1100.0], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_10_parameter_nudge():
    args = [[1.0, 2.0, 3.0], [0.5, 0.5, 0.5], 1.1]
    actual = solve(*args)
    expected = np.array([1.55, 2.55, 3.55], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_11_reversed_order():
    args = [[3.0, 2.0, 1.0], [0.5, 0.5, 0.5], 0.1]
    actual = solve(*args)
    expected = np.array([3.05, 2.05, 1.05], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_12_large_n_1e5():
    # Performance case: expand a compatible 1-D numeric argument to exactly 100000 elements.
    args = [[1.0, 2.0, 3.0], [0.5, 0.5, 0.5], 0.1]
    expanded = False
    for i, arg in enumerate(args):
        if isinstance(arg, np.ndarray) and arg.ndim == 1 and arg.size > 1 and np.issubdtype(arg.dtype, np.number):
            args[i] = np.resize(arg.astype(float), 100000)
            expanded = True
            break
        if isinstance(arg, list) and len(arg) > 1 and all(isinstance(x, (int, float, np.number)) and not isinstance(x, bool) for x in arg):
            args[i] = np.resize(np.asarray(arg, dtype=float), 100000)
            expanded = True
            break
    if not expanded:
        pytest.skip("No compatible 1-D numeric argument for the 1e5 performance category")
    actual = solve(*args)
    assert actual is not None
    if isinstance(actual, np.ndarray):
        assert actual.size >= 1

def test_13_empty_or_degenerate_input():
    args = [[], [0.5, 0.5, 0.5], 0.1]
    with pytest.raises(ValueError):
        solve(*args)
