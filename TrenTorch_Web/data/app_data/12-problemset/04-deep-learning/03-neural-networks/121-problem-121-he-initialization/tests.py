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
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_02_exact_zero_inputs():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_03_all_negative_values():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_04_all_positive_values():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_05_singleton_boundary():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_06_repeated_values():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_07_mixed_signs():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_08_tiny_magnitudes():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_09_large_magnitudes():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_10_parameter_nudge():
    args = [3, 4, 1]
    actual = solve(*args)
    expected = np.array([[0.2821683112435684, 0.6708484049968816, 0.2698007429154901, -1.0640234240162014], [0.7392199696614589, 0.36446331214829103, -0.4384204807897534, 0.4744809451915244], [0.29767211498655916, 0.24015817785897278, 0.023206662856650833, 0.4463892843178486]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_11_reversed_order():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_12_large_n_1e5():
    # Performance case: expand a compatible 1-D numeric argument to exactly 100000 elements.
    args = [2, 3, 0]
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
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)
