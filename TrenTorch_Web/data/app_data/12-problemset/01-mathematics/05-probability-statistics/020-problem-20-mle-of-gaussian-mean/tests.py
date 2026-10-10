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
    _close(solve([1.0, 2.0, 3.0]), 2.0)


def test_02_readme_example_2():
    _close(solve([-1.0, 1.0]), 0.0)


def test_03_random_valid_case_1():
    _close(solve([2.3, 4.65, -0.13, -1.37, -4.9, 2.71, 0.61, 4.23]), 1.0125000000000002)


def test_04_random_valid_case_2():
    _close(solve([-1.52, -0.87, 3.65, 0.98, -3.4, -1.18, 1.04, 1.6]), 0.03749999999999998)


def test_05_random_valid_case_3():
    _close(solve([-1.16, -2.09, 4.15, 1.91, 2.0, 1.8, -3.72, -0.35]), 0.3175)


def test_06_random_valid_case_4():
    _close(solve([3.22, -1.01, -2.57, 2.67, 0.8, -1.53, 4.87, 0.77]), 0.9025000000000001)


def test_07_random_valid_case_5():
    _close(solve([-0.6, -4.62, 3.01, 4.06, -3.9, 1.72, 4.69, -2.97]), 0.17375000000000002)


def test_08_random_valid_case_6():
    _close(solve([-3.92, -1.23, -4.3, 2.24, 3.51, 2.76, 0.4, -4.14]), -0.585)


def test_09_random_valid_case_7():
    _close(solve([2.91, 3.01, 0.58, -3.12, 1.1, 4.59, -3.18, -4.19]), 0.2124999999999998)


def test_10_random_valid_case_8():
    _close(solve([2.75, 1.83, 2.86, -0.08, 3.9, 1.31, -0.39, -1.13]), 1.3812499999999999)


def test_11_random_valid_case_9():
    _close(solve([3.5, 0.25, 1.29, 0.98, -2.44, -0.28, -4.56, 1.14]), -0.015000000000000013)


def test_12_random_valid_case_10():
    _close(solve([4.24, 1.67, 2.99, -0.91, -0.19, 0.63, 3.34, -1.94]), 1.22875)
