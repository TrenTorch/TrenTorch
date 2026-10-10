"""Tests with varied inputs. Expected values were checked against independent references (SciPy, scikit-learn, PyTorch or a first-principles formula)."""
import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def _close(actual, expected, rtol=1e-6, atol=1e-8):
    if isinstance(expected, dict):
        assert set(actual) == set(expected)
        for k in expected:
            _close(actual[k], expected[k], rtol, atol)
        return
    if isinstance(expected, (tuple, list)) and not (len(expected) and isinstance(expected[0], (int, float, np.number)) and not isinstance(expected, tuple)):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            _close(a, e, rtol, atol)
        return
    a, e = np.asarray(actual), np.asarray(expected)
    assert a.shape == e.shape, (a.shape, e.shape)
    if a.dtype.kind in "biufc" and e.dtype.kind in "biufc":
        np.testing.assert_allclose(a, e, rtol=rtol, atol=atol, equal_nan=True)
    else:
        assert a.tolist() == e.tolist()


def test_01_readme_example_1():
    _close(solve([1, 3], [2, 2]), 1.0)


def test_02_readme_example_2():
    _close(solve([2.0, 2.0], [2.0, 2.0]), 0.0)


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], [1.0, 4.0])


def test_04_random_valid_case_1():
    _close(solve([-4.2, 3.2, 4.59, -2.5, -2.65, 0.47, -1.66, 0.89], [2.54, 3.92, 2.06, -2.32, 4.03, 1.11, 4.61, 0.72]), 17.094137500000002)


def test_05_random_valid_case_2():
    _close(solve([2.85, 1.79, 1.9, 3.2, 0.77, 2.09, -2.14, -4.71], [3.62, 4.13, -2.59, 3.82, 0.49, -0.94, -0.32, 4.01]), 14.402887499999997)


def test_06_random_valid_case_3():
    _close(solve([-3.72, 4.3, -0.11, 1.4, 3.32, 4.45, -3.56, 4.66], [0.29, 2.14, 2.0, 3.59, 3.19, -1.57, -1.77, -1.92]), 14.0939625)


def test_07_random_valid_case_4():
    _close(solve([-3.63, 4.58, 0.7, -1.02, 3.55, 3.72, 2.76, -0.37], [4.72, -1.99, 3.24, 0.45, 3.14, -0.11, 0.14, 0.05]), 17.9222125)


def test_08_random_valid_case_5():
    _close(solve([3.95, -2.65, 4.96, 5.0, -0.95, 3.64, -2.2, -1.2], [3.64, -2.1, -3.52, -0.36, -2.85, 0.92, 3.67, 1.94]), 19.545437500000002)


def test_09_random_valid_case_6():
    _close(solve([3.71, 3.69, 1.59, -0.42, 4.75, 4.65, 0.8, 4.03], [2.69, 2.45, -0.98, -2.44, -0.85, -1.28, -4.45, -2.8]), 19.24995)


def test_10_random_valid_case_7():
    _close(solve([-2.91, -1.82, -0.61, 4.9, -1.12, -1.84, 3.96, 0.21], [2.17, 1.01, 3.28, 1.18, 4.11, 0.65, 4.94, -1.77]), 12.652450000000002)


def test_11_random_valid_case_8():
    _close(solve([1.76, 2.66, -1.96, -4.42, 2.65, -0.46, 2.08, 2.42], [1.34, 0.93, 0.68, -3.35, -1.41, 2.99, 4.62, 3.94]), 6.0539875)


def test_12_random_valid_case_9():
    _close(solve([-2.74, -1.39, -0.9, 4.03, 0.72, 1.69, 1.17, 2.95], [4.06, 0.98, 2.86, 2.42, -4.87, -4.9, -1.67, -4.66]), 26.1550625)
