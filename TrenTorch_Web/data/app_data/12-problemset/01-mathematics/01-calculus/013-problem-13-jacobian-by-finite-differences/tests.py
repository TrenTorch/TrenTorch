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
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([1.0, 2.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[2.0000000000131024, 1.0000000000065512], [1.0000000000065512, -4.000000000026205]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_02_exact_zero_inputs():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([0.0, 0.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_03_all_negative_values():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([-2.0, -3.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[-4.000000000026205, 1.0000000000065512], [0.9999999999621422, 6.000000000039306]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_04_all_positive_values():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([2.0, 3.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[4.000000000026205, 0.9999999999621422], [0.9999999999621422, -6.000000000039306]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_05_singleton_boundary():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([1.0], dtype=float), 1e-05]
    with pytest.raises(IndexError):
        solve(*args)

def test_06_repeated_values():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([2.0, 2.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[4.000000000026205, 0.9999999999621422], [1.0000000000065512, -4.000000000026205]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_07_mixed_signs():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([-2.0, 2.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[-4.000000000026205, 0.9999999999621422], [0.9999999999621422, -4.000000000026205]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_08_tiny_magnitudes():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([1e-08, 1e-08], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[2.0000000000006135e-08, 1.0], [1.0, -2.0000000000006135e-08]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_09_large_magnitudes():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([1000.0, 1000.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[1999.9999960418788, 0.9999959729611873], [0.9999959729611873, -1999.9999960418788]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_10_parameter_nudge():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([1.0, 2.0], dtype=float), 1.00001]
    actual = solve(*args)
    expected = np.array([[2.0, 0.9999999999999998], [0.9999999999999998, -4.0]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_11_reversed_order():
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([2.0, 1.0], dtype=float), 1e-05]
    actual = solve(*args)
    expected = np.array([[4.000000000026205, 0.9999999999621422], [1.0000000000065512, -2.000000000002]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_12_large_n_1e5():
    # Performance case: expand a compatible 1-D numeric argument to exactly 100000 elements.
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([1.0, 2.0], dtype=float), 1e-05]
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
    args = [lambda z: np.sum(np.asarray(z, dtype=float) ** 2), np.array([], dtype=float), 1e-05]
    with pytest.raises(IndexError):
        solve(*args)
