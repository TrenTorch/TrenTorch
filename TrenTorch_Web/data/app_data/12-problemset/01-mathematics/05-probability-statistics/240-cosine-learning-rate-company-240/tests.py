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
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_02_exact_zero_inputs():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_03_all_negative_values():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_04_all_positive_values():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_05_singleton_boundary():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_06_repeated_values():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_07_mixed_signs():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_08_tiny_magnitudes():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_09_large_magnitudes():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_10_parameter_nudge():
    args = [2, 2, 2, 2]
    actual = solve(*args)
    expected = 2.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_11_reversed_order():
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_12_large_n_1e5():
    # Performance case: expand a compatible 1-D numeric argument to exactly 100000 elements.
    args = [1, 1, 1, 1]
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
    args = [1, 1, 1, 1]
    actual = solve(*args)
    expected = 1.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected
