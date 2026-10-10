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
    _close(solve([1.0, 2.0, 3.0, 4.0], 2), np.array([float('nan'), 1.5, 2.5, 3.5]))


def test_02_readme_example_2():
    _close(solve([2.0, 4.0, 6.0, 8.0, 10.0], 3), np.array([float('nan'), float('nan'), 4.0, 6.0, 8.0]))


def test_03_random_valid_case_1():
    _close(solve([2.66, 1.74, 1.92, 0.72, 4.87, 3.67, 0.31, 2.32, 4.84, 2.37, 2.89, 3.0], 5), np.array([float('nan'), float('nan'), float('nan'), float('nan'), 2.382, 2.584, 2.298, 2.378, 3.2020000000000004, 2.7020000000000004, 2.5460000000000003, 3.0840000000000005]))


def test_04_random_valid_case_2():
    _close(solve([1.88, 1.45, -0.18, 2.56, 1.64, 2.77, 2.4, 0.29, -2.26, 1.19, 2.23, 0.66], 5), np.array([float('nan'), float('nan'), float('nan'), float('nan'), 1.47, 1.6479999999999997, 1.8379999999999999, 1.9319999999999997, 0.9679999999999996, 0.8779999999999996, 0.7699999999999995, 0.42199999999999943]))


def test_05_random_valid_case_3():
    _close(solve([-0.22, -3.6, -0.6, 4.89, 4.19, -0.11, -2.13, 1.3, 0.18, 5.0, 3.95, -3.3], 1), np.array([-0.22, -3.6, -0.6000000000000001, 4.889999999999999, 4.189999999999999, -0.1100000000000021, -2.130000000000002, 1.2999999999999978, 0.17999999999999772, 4.999999999999998, 3.9499999999999993, -3.3000000000000007]))


def test_06_random_valid_case_4():
    _close(solve([-3.49, -3.55, 2.2, 1.5, 3.07, 2.36, -0.16, 3.84, -1.96, -0.24, 2.13, 1.2], 1), np.array([-3.49, -3.55, 2.2, 1.5, 3.0700000000000003, 2.36, -0.16000000000000014, 3.84, -1.96, -0.2400000000000002, 2.13, 1.2000000000000002]))


def test_07_random_valid_case_5():
    _close(solve([1.14, -1.69, -4.39, 3.53, 4.75, 4.91, 0.87, -3.39, 3.89, 1.05, 2.56, 0.98], 2), np.array([float('nan'), -0.275, -3.0399999999999996, -0.4299999999999997, 4.140000000000001, 4.830000000000001, 2.8900000000000006, -1.2599999999999996, 0.2500000000000005, 2.4700000000000006, 1.8050000000000008, 1.770000000000001]))


def test_08_random_valid_case_6():
    _close(solve([-1.37, 0.49, -1.98, 2.33, 1.07, 4.44, -4.58, 0.69, 3.77, -0.8, 0.03, 3.72], 1), np.array([-1.37, 0.49, -1.98, 2.33, 1.0700000000000003, 4.44, -4.58, 0.69, 3.77, -0.8000000000000003, 0.029999999999999805, 3.72]))


def test_09_random_valid_case_7():
    _close(solve([-0.7, 3.5, -2.92, -4.06, 3.64, -3.93, 0.46, 0.98, -0.27, 2.0, 1.32, -1.06], 1), np.array([-0.7, 3.5, -2.92, -4.06, 3.64, -3.93, 0.45999999999999996, 0.98, -0.27, 2.0, 1.3200000000000003, -1.0599999999999998]))


def test_10_random_valid_case_8():
    _close(solve([-3.17, -0.37, 4.4, -2.81, 1.55, 1.73, 0.16, 4.73, -1.73, -1.77, 1.77, 3.04], 4), np.array([float('nan'), float('nan'), float('nan'), -0.48749999999999993, 0.6925000000000001, 1.2175, 0.15749999999999997, 2.0425, 1.2225, 0.3474999999999999, 0.7499999999999999, 0.3274999999999997]))


def test_11_random_valid_case_9():
    _close(solve([3.81, 0.85, 4.15, -0.82, 4.66, -2.18, -2.24, 4.17, 0.33, -3.0, -2.93, 4.22], 2), np.array([float('nan'), 2.33, 2.5, 1.6649999999999998, 1.92, 1.2399999999999998, -2.2100000000000004, 0.9649999999999996, 2.25, -1.335, -2.965, 0.645]))


def test_12_random_valid_case_10():
    _close(solve([2.17, -1.21, -4.22, -4.69, 3.43, 0.06, -2.29, -0.37, 0.1, -3.32, 3.26, -2.0], 5), np.array([float('nan'), float('nan'), float('nan'), float('nan'), -0.9039999999999999, -1.326, -1.542, -0.772, 0.18600000000000003, -1.1640000000000001, -0.5240000000000001, -0.4660000000000002]))
