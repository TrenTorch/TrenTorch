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
    _close(solve([3.0, 5.0, 7.0], [2.5, 5.0, 8.0]), np.array([0.5, 0.0, -1.0]))


def test_02_readme_example_2():
    _close(solve([1.0, 1.0], [1.0, 1.0]), np.array([0.0, 0.0]))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], [0.5, 2.5, 2.0])


def test_04_random_valid_case_1():
    _close(solve([4.4, -2.7, -0.53, 2.0, 1.55, -1.51], [3.24, 2.28, -4.94, -2.1, -0.9, 1.37]), np.array([1.1600000000000001, -4.98, 4.41, 4.1, 2.45, -2.88]))


def test_05_random_valid_case_2():
    _close(solve([0.22, 0.1, 2.92, 2.03, 1.76, -3.59], [0.03, -0.18, -4.03, 4.14, -2.48, 3.32]), np.array([0.19, 0.28, 6.95, -2.11, 4.24, -6.91]))


def test_06_random_valid_case_3():
    _close(solve([0.06, -2.91, 1.5, 2.66, 0.89, -0.71], [4.42, -3.31, 4.33, 0.07, 2.55, -4.36]), np.array([-4.36, 0.3999999999999999, -2.83, 2.5900000000000003, -1.6599999999999997, 3.6500000000000004]))


def test_07_random_valid_case_4():
    _close(solve([4.25, 0.05, 3.52, -1.0, 3.65, -1.98], [3.78, 0.21, -4.15, -2.21, 1.15, -2.8]), np.array([0.4700000000000002, -0.15999999999999998, 7.67, 1.21, 2.5, 0.8199999999999998]))


def test_08_random_valid_case_5():
    _close(solve([-3.22, 1.67, 3.5, -0.74, 1.18, 0.07], [0.96, 4.31, -0.93, 3.16, 0.14, -3.44]), np.array([-4.18, -2.6399999999999997, 4.43, -3.9000000000000004, 1.04, 3.51]))


def test_09_random_valid_case_6():
    _close(solve([1.78, 2.57, 0.46, -3.0, 3.32, -1.83], [-4.87, -1.02, 0.29, 4.41, 1.89, 2.64]), np.array([6.65, 3.59, 0.17000000000000004, -7.41, 1.43, -4.470000000000001]))


def test_10_random_valid_case_7():
    _close(solve([4.89, -3.04, 1.3, 3.15, -3.6, 3.33], [-2.28, 3.06, -1.87, 2.58, -4.15, -3.71]), np.array([7.17, -6.1, 3.17, 0.5699999999999998, 0.5500000000000003, 7.04]))


def test_11_random_valid_case_8():
    _close(solve([4.54, 3.94, -2.72, -4.53, 4.99, 3.74], [-1.07, 1.75, 2.41, -1.07, 0.64, 0.18]), np.array([5.61, 2.19, -5.130000000000001, -3.46, 4.3500000000000005, 3.56]))


def test_12_random_valid_case_9():
    _close(solve([-2.56, 3.41, 1.41, -2.69, -0.18, 3.29], [2.88, 0.89, 0.63, -3.21, 4.28, 2.41]), np.array([-5.4399999999999995, 2.52, 0.7799999999999999, 0.52, -4.46, 0.8799999999999999]))
