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
    _close(solve([[1, 2], [3, 4], [9, 9]], [1, 1, 0]), np.array([2.0, 3.0]))


def test_02_readme_example_2():
    _close(solve([[5.0, 5.0]], [0]), np.array([0.0, 0.0]))


def test_03_random_valid_case_1():
    _close(solve([[2.7, -2.43, -0.41], [1.48, 4.71, -1.99], [-3.56, 0.02, 0.59], [-1.62, 4.17, 3.67], [0.6, -0.2, 0.14], [-1.5, 2.17, 2.68]], [True, True, False, True, True, False]), np.array([0.7899999999999999, 1.5624999999999998, 0.35250000000000004]))


def test_04_random_valid_case_2():
    _close(solve([[-2.14, 0.5, 1.39], [3.42, -2.2, 3.81], [-0.42, 4.86, -0.95], [3.94, -2.12, 0.64], [-2.8, 1.38, 2.3], [3.79, 4.24, -1.42]], [True, False, True, False, True, False]), np.array([-1.7866666666666664, 2.2466666666666666, 0.9133333333333332]))


def test_05_random_valid_case_3():
    _close(solve([[-3.32, 3.76, 3.11], [1.85, -1.3, 1.66], [3.18, 3.24, -4.47], [0.3, -2.63, -2.8], [0.77, -0.16, 2.13], [-3.24, 2.99, -4.77]], [True, True, False, True, True, False]), np.array([-0.09999999999999992, -0.08249999999999999, 1.025]))


def test_06_random_valid_case_4():
    _close(solve([[3.6, -2.28, -2.17], [4.64, 2.26, 4.88], [-0.33, 4.13, -0.69], [0.74, 0.1, -4.07], [1.04, 1.7, -4.7], [0.57, 3.23, -1.55]], [False, True, False, False, False, False]), np.array([4.64, 2.26, 4.88]))


def test_07_random_valid_case_5():
    _close(solve([[0.88, 2.16, -1.14], [-0.12, -0.62, 2.98], [-2.4, 3.97, 2.78], [-3.1, -3.32, 2.35], [-1.79, 2.57, 4.86], [3.92, 3.81, -0.89]], [False, True, True, True, False, True]), np.array([-0.42500000000000004, 0.9600000000000001, 1.805]))


def test_08_random_valid_case_6():
    _close(solve([[-3.19, -1.42, 4.74], [4.21, 4.61, 2.56], [4.58, 1.31, -3.53], [1.4, 0.21, -4.42], [4.62, 1.53, -0.67], [-1.0, -3.58, -0.57]], [False, True, False, True, True, False]), np.array([3.41, 2.1166666666666667, -0.8433333333333333]))


def test_09_random_valid_case_7():
    _close(solve([[1.69, -4.03, 2.84], [4.53, -3.51, 1.91], [-4.07, -0.74, 3.42], [-0.55, 2.44, 2.07], [-4.04, 0.66, 3.05], [4.04, -2.82, 4.41]], [True, False, True, True, False, True]), np.array([0.27749999999999986, -1.2875, 3.185]))


def test_10_random_valid_case_8():
    _close(solve([[0.49, -0.14, 0.05], [2.59, -4.74, 1.2], [1.77, -3.56, 0.37], [-2.74, -2.27, -4.17], [4.85, 3.59, -1.83], [0.98, 2.88, -4.86]], [True, False, False, True, True, False]), np.array([0.8666666666666666, 0.39333333333333326, -1.9833333333333334]))


def test_11_random_valid_case_9():
    _close(solve([[-4.48, 1.87, 4.41], [4.46, 3.68, 4.94], [-1.47, 1.08, 1.72], [-3.06, -4.04, -4.28], [-0.66, -2.49, 2.0], [-0.59, -0.61, 4.57]], [False, True, True, False, True, True]), np.array([0.43500000000000005, 0.4149999999999999, 3.3075]))


def test_12_random_valid_case_10():
    _close(solve([[-4.1, 3.27, 1.32], [-1.94, -1.95, 1.35], [4.61, -4.36, -4.36], [-2.18, 1.4, -3.81], [-1.54, 3.77, 0.35], [1.61, -0.15, 1.63]], [False, True, True, True, False, False]), np.array([0.1633333333333334, -1.6366666666666667, -2.2733333333333334]))
