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
    _close(solve([1.0, -2.0], 0.1, 0.2), 0.8)


def test_02_readme_example_2():
    _close(solve([0.0, 0.0, 0.0], 1.0, 1.0), 0.0)


def test_03_random_valid_case_1():
    _close(solve([-2.9, 3.63, 0.4, -0.6, 3.73], 0.14, 0.13), 3.9176870000000004)


def test_04_random_valid_case_2():
    _close(solve([3.71, -3.71, 0.04, 2.23, 0.79], 0.86, 0.7), 20.60718)


def test_05_random_valid_case_3():
    _close(solve([2.21, 2.93, 4.76, 3.22, 0.82], 0.03, 0.47), 11.502539)


def test_06_random_valid_case_4():
    _close(solve([-2.39, 2.83, 3.51, 4.36, 0.81], 0.85, 0.72), 28.269448000000004)


def test_07_random_valid_case_5():
    _close(solve([1.22, 3.86, 4.13, -4.41, 4.02], 0.44, 0.88), 38.145095999999995)


def test_08_random_valid_case_6():
    _close(solve([-1.92, 1.65, -3.03, 4.3, 4.34], 0.51, 0.62), 24.176173999999996)


def test_09_random_valid_case_7():
    _close(solve([-0.2, -0.92, 3.09, 4.41, 2.07], 0.23, 0.81), 16.2965375)


def test_10_random_valid_case_8():
    _close(solve([-2.88, 4.05, -2.85, 1.04, 0.6], 0.94, 0.23), 14.674815)


def test_11_random_valid_case_9():
    _close(solve([1.35, -2.74, -0.25, 2.62, 1.39], 0.53, 0.08), 5.1530640000000005)


def test_12_random_valid_case_10():
    _close(solve([2.28, 1.44, -0.5, -4.83, -1.55], 0.41, 0.88), 18.977496000000002)
