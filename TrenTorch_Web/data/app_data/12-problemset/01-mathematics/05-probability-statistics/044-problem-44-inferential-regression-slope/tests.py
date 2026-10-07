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
    _close(solve([1.0, 2.0, 3.0], [2.0, 4.0, 5.0]), (1.5, 0.6666666666666665))


def test_02_readme_example_2():
    _close(solve([0.0, 1.0, 2.0, 3.0], [1.0, 3.0, 5.0, 7.0]), (2.0, 1.0))


def test_03_random_valid_case_1():
    _close(solve([-3.9, -3.86, 0.94, 4.05, 3.23, 1.67, 1.12, -0.77, 1.01], [-1.83, 3.88, 3.02, -1.34, 0.5, 2.0, 3.39, 3.58, 2.66]), (-0.12709090388852326, 1.8115052505078828))


def test_04_random_valid_case_2():
    _close(solve([-1.16, 4.96, 2.18, 3.88, -1.64, -1.57, -3.31, 1.73, 3.3], [0.5, 3.3, 2.74, 0.65, -4.51, 0.0, 2.42, 1.93, 1.34]), (0.34792550107852166, 0.6064292839969748))


def test_05_random_valid_case_3():
    _close(solve([0.23, -2.13, 0.02, 4.87, -2.29, 1.65, 4.63, 1.94, 3.47], [-3.71, -4.43, 2.4, 1.2, 4.3, -4.38, -4.88, 1.21, -2.96]), (-0.312268191334474, -0.8201107899295408))


def test_06_random_valid_case_4():
    _close(solve([3.09, 1.22, 1.08, 2.57, 2.79, 4.04, -2.43, -3.51, -4.84], [0.86, 4.92, 4.81, 1.37, 1.09, -2.59, -3.85, 3.04, 4.78]), (-0.2528040388898314, 1.7159715773275808))


def test_07_random_valid_case_5():
    _close(solve([0.1, -1.26, -3.34, 2.45, -3.06, -0.4, 4.9, -0.71, -2.24], [-3.39, 0.02, 0.44, -2.16, 0.57, 3.23, 2.78, 0.48, 0.27]), (0.06028855136090508, 0.2727363603160913))


def test_08_random_valid_case_6():
    _close(solve([0.93, -3.84, -2.83, -0.52, 2.23, 2.68, -2.03, -3.01, 0.27], [0.69, 4.59, 4.13, 2.9, 4.02, 2.96, -2.36, -2.29, 4.48]), (0.2794246013283883, 2.3144531733477485))


def test_09_random_valid_case_7():
    _close(solve([-3.9, 2.59, -0.01, 0.32, -4.75, 2.0, 4.51, -2.08, -0.56], [2.65, 2.6, -3.4, -1.58, 0.19, -3.69, -4.02, 2.61, -0.71]), (-0.500667087398927, -0.6990282360344426))


def test_10_random_valid_case_8():
    _close(solve([4.65, -1.54, 0.41, 3.22, 3.54, 4.62, -4.92, 2.77, -2.29], [0.45, -4.8, 2.48, -1.22, -0.07, 1.54, -4.32, 4.82, -2.16]), (0.6083567439797116, -1.0714901713364204))


def test_11_random_valid_case_9():
    _close(solve([3.35, -1.81, 4.48, -0.16, -0.83, -1.86, 4.21, 1.47, -2.79], [2.44, -1.81, -1.11, -3.49, 4.31, 3.84, 0.82, 2.53, 1.5]), (-0.10873903850041232, 1.0765509525902772))


def test_12_random_valid_case_10():
    _close(solve([-1.45, -0.09, 1.84, 1.96, 4.57, -0.05, 2.93, 4.92, -4.62], [4.02, -2.78, 4.38, -4.84, 1.21, 1.02, -4.48, -3.7, 0.27]), (-0.3913173243830494, -0.10921262032507506))
