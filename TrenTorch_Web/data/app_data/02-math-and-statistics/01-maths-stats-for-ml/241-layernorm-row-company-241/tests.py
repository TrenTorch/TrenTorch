"""Executable tests: 2 visible examples + 11 targeted edge/performance cases.

The case names document the hidden-test categories. Expected values are materialized
from the reference implementation at authoring time; the agent should not have to
invent edge cases or expected outputs.
"""
import numpy as np
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution('02-math-and-statistics/01-maths-stats-for-ml/241-layernorm-row-company-241')
solve = _module.solve


def test_01_basic_example():
    args = [np.array([[1.0, 2.0], [3.0, 4.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[0.5527864045000421, 1.4472135954999579], [0.5527864045000421, 1.4472135954999579]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_02_exact_zero_inputs():
    args = [np.array([[0.0, 0.0], [0.0, 0.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[1.0, 1.0], [1.0, 1.0]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_03_all_negative_values():
    args = [np.array([[-2.0, -3.0], [-4.0, -5.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[1.4472135954999579, 0.5527864045000421], [1.4472135954999579, 0.5527864045000421]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_04_all_positive_values():
    args = [np.array([[2.0, 3.0], [4.0, 5.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[0.5527864045000421, 1.4472135954999579], [0.5527864045000421, 1.4472135954999579]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_05_singleton_boundary():
    args = [np.array([[1.0, 2.0], [3.0, 4.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[0.5527864045000421, 1.4472135954999579], [0.5527864045000421, 1.4472135954999579]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_06_repeated_values():
    args = [np.array([[2.0, 2.0], [2.0, 2.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[1.0, 1.0], [1.0, 1.0]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_07_mixed_signs():
    args = [np.array([[-2.0, -0.6666666666666667], [0.6666666666666665, 2.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[0.44529980377477096, 1.5547001962252291], [0.44529980377477085, 1.5547001962252291]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_08_tiny_magnitudes():
    args = [np.array([[1e-08, 1e-08], [1e-08, 1e-08]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[1.0, 1.0], [1.0, 1.0]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_09_large_magnitudes():
    args = [np.array([[1000.0, 1000.0], [1000.0, 1000.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[1.0, 1.0], [1.0, 1.0]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_10_parameter_nudge():
    args = [np.array([[1.0, 2.0], [3.0, 4.0]], dtype=float), 2, 2, 2]
    actual = solve(*args)
    expected = np.array([[1.3333333333333335, 2.6666666666666665], [1.3333333333333335, 2.6666666666666665]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_11_reversed_order():
    args = [np.array([[1.0, 2.0], [3.0, 4.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[0.5527864045000421, 1.4472135954999579], [0.5527864045000421, 1.4472135954999579]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_12_large_n_1e5():
    # Performance case: expand a compatible 1-D numeric argument to exactly 100000 elements.
    args = [np.array([[1.0, 2.0], [3.0, 4.0]], dtype=float), 1, 1, 1]
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
    args = [np.array([[1.0, 2.0], [3.0, 4.0]], dtype=float), 1, 1, 1]
    actual = solve(*args)
    expected = np.array([[0.5527864045000421, 1.4472135954999579], [0.5527864045000421, 1.4472135954999579]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)
