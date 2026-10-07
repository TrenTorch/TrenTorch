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
    _close(solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 1.0], 0.0), np.array([3.0, 7.0]))


def test_02_readme_example_2():
    _close(solve([[1.0], [2.0], [3.0]], [2.0], 1.0), np.array([3.0, 5.0, 7.0]))


def test_03_random_valid_case_1():
    _close(solve([[1.5, 4.06, -4.77], [-3.77, -0.62, 1.94], [-2.7, 2.69, 3.88], [2.74, 4.92, 4.03], [-2.07, 0.9, -4.33]], [0.1, -2.01, 2.66], 0.0), np.array([-20.6988, 6.0296, 4.6439, 1.1046000000000034, -13.533800000000001]))


def test_04_random_valid_case_2():
    _close(solve([[2.3, 3.21, -4.61], [2.79, 1.9, -4.6], [-1.45, 2.81, -3.93], [-4.9, -4.67, -1.55], [3.07, 4.49, 3.48]], [0.07, 3.48, 3.55], 0.09), np.array([-4.943700000000001, -9.432699999999999, -4.1842, -22.0071, 28.284100000000002]))


def test_05_random_valid_case_3():
    _close(solve([[-1.57, 4.93, -4.19], [-1.98, 4.25, -2.93], [-0.01, 2.4, 1.34], [1.65, 0.4, 4.7], [-2.58, -3.27, 1.64]], [1.74, -3.3, 0.19], 1.38), np.array([-18.4169, -16.6469, -6.3027999999999995, 3.824, 7.9933999999999985]))


def test_06_random_valid_case_4():
    _close(solve([[0.74, 0.91, 4.05], [2.32, 3.5, 4.09], [-4.57, 0.61, 4.9], [2.29, -1.15, 0.09], [-0.47, -0.88, -4.5]], [-0.44, -1.94, 3.09], 1.24), np.array([11.663499999999999, 6.067299999999999, 17.2084, 2.7415, -10.751]))


def test_07_random_valid_case_5():
    _close(solve([[4.01, -3.9, -3.11], [4.96, -2.19, -0.1], [3.24, 3.51, 4.16], [-0.52, -2.32, -2.68], [-3.84, 1.67, 2.57]], [1.62, 2.93, 2.94], 0.89), np.array([-13.184199999999999, 2.2145, 28.6535, -14.6292, 7.118099999999999]))


def test_08_random_valid_case_6():
    _close(solve([[4.96, 1.38, 3.23], [-1.56, 3.23, 0.3], [-2.48, -3.55, -2.33], [-2.7, -1.32, 3.54], [-2.5, -2.13, -0.86]], [0.09, 1.68, -1.76], 0.4), np.array([-2.5200000000000005, 5.158000000000001, -1.6864, -8.291, -1.8898000000000001]))


def test_09_random_valid_case_7():
    _close(solve([[4.89, -1.49, 1.06], [1.54, -2.29, -0.16], [1.79, -0.03, -3.47], [1.19, -4.07, 3.11], [2.85, 4.52, 2.71]], [2.04, 1.71, 2.01], 1.35), np.array([10.908299999999999, 0.2541000000000002, -2.024399999999999, 3.068999999999998, 20.3403]))


def test_10_random_valid_case_8():
    _close(solve([[1.13, 1.33, 0.42], [-4.89, 2.49, -0.16], [3.99, 1.07, 2.93], [-3.31, 4.54, -2.91], [-2.76, -3.05, 4.96]], [4.84, 3.78, -0.7], -1.41), np.array([8.792599999999998, -15.553399999999998, 19.895200000000003, 1.7678000000000014, -29.769399999999997]))


def test_11_random_valid_case_9():
    _close(solve([[-4.64, 4.02, -0.87], [3.58, -4.47, 1.66], [3.6, -2.41, 4.15], [-0.97, 4.77, 2.18], [2.05, 3.07, -3.94]], [-0.39, -3.3, -4.79], 0.28), np.array([-7.009099999999998, 5.683399999999998, -13.049500000000002, -25.5249, 8.222100000000001]))


def test_12_random_valid_case_10():
    _close(solve([[-0.43, 1.63, 0.1], [1.93, -0.48, 3.36], [-0.61, 1.45, 4.34], [-0.06, 3.7, 1.41], [1.55, -0.68, -3.42]], [3.23, -0.76, -3.65], -1.66), np.array([-4.6527, -7.3252999999999995, -20.5733, -9.8123, 16.3463]))
