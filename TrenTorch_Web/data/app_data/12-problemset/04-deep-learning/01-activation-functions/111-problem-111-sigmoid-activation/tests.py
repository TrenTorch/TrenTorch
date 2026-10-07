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
    _close(solve([0.0]), np.array([0.5]))


def test_02_readme_example_2():
    _close(solve([2.0, -2.0]), np.array([0.8807970779778823, 0.11920292202211755]))


def test_03_readme_example_3():
    _close(solve([800.0, -800.0]), np.array([1.0, 0.0]))


def test_04_random_valid_case_1():
    _close(solve([778.45, 687.94, 373.41, 796.3, -4.36, 271.3]), np.array([1.0, 1.0, 1.0, 1.0, 0.012617160679338692, 1.0]))


def test_05_random_valid_case_2():
    _close(solve([352.07, 28.5, 672.52, -199.99, -18.59, 60.29]), np.array([1.0, 0.9999999999995806, 1.0, 1.3978049180576288e-87, 8.442393247174089e-09, 1.0]))


def test_06_random_valid_case_3():
    _close(solve([391.22, 425.89, 539.52, -464.8, 592.02, -9.29]), np.array([1.0, 1.0, 1.0, 1.3801453018157451e-202, 1.0, 9.233453382664761e-05]))


def test_07_random_valid_case_4():
    _close(solve([433.92, -787.36, 142.7, 398.84, 593.05, 78.08]), np.array([1.0, 0.0, 1.0, 1.0, 1.0, 1.0]))


def test_08_random_valid_case_5():
    _close(solve([503.76, -90.79, 99.3, -197.45, 111.29, -349.68]), np.array([1.0, 3.718809981875991e-40, 1.0, 1.7723706442384504e-86, 1.0, 1.3674314623180087e-152]))


def test_09_random_valid_case_6():
    _close(solve([-248.23, 600.46, 685.4, 797.13, -129.59, 361.4]), np.array([1.5670424349080211e-108, 1.0, 1.0, 1.0, 5.2453936982458e-57, 1.0]))


def test_10_random_valid_case_7():
    _close(solve([297.76, 597.49, 770.34, 675.25, 27.39, -372.21]), np.array([1.0, 1.0, 1.0, 1.0, 0.9999999999987275, 2.245178583025998e-162]))


def test_11_random_valid_case_8():
    _close(solve([-13.01, 476.53, -111.38, 128.44, 421.69, -365.7]), np.array([2.237833745688869e-06, 1.0, 4.2489400707232255e-49, 1.0, 1.0, 1.5083702842865913e-159]))


def test_12_random_valid_case_9():
    _close(solve([-220.55, 278.69, 777.95, 88.28, 769.97, -350.91]), np.array([1.6457051046552748e-96, 1.0, 1.0, 1.0, 1.0, 3.9969006692283046e-153]))
