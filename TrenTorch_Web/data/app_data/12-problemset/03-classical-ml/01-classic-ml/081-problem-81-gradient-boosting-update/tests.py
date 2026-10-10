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
    _close(solve([1.0, 2.0], [0.5, -1.0], 0.1), np.array([1.05, 1.9]))


def test_02_readme_example_2():
    _close(solve([0.0, 0.0], [4.0, 8.0], 0.5), np.array([2.0, 4.0]))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], [0.5, 0.5, 0.5], 0.1)


def test_04_random_valid_case_1():
    _close(solve([1.15, 3.95, 4.33, -2.87, 1.73, -0.55], [4.1, 1.16, 2.62, 2.99, 2.18, 0.0], 0.55), np.array([3.405, 4.588, 5.771000000000001, -1.2254999999999998, 2.9290000000000003, -0.55]))


def test_05_random_valid_case_2():
    _close(solve([-1.18, 3.4, 3.32, 4.27, 1.27, 0.8], [2.04, 0.93, -4.37, 3.87, -4.43, 1.37], 0.09), np.array([-0.9964, 3.4837, 2.9267, 4.6183, 0.8713000000000001, 0.9233]))


def test_06_random_valid_case_3():
    _close(solve([4.63, 3.29, -2.3, 4.4, 0.22, 3.3], [4.96, -1.1, -4.02, -2.71, -1.37, -1.03], 0.31), np.array([6.1676, 2.949, -3.5462, 3.5599000000000003, -0.20470000000000002, 2.9806999999999997]))


def test_07_random_valid_case_4():
    _close(solve([2.76, 4.31, -4.36, -2.4, 2.06, 3.86], [-1.38, 1.61, 3.73, 3.74, 1.08, 2.15], 0.73), np.array([1.7526, 5.4853, -1.6371000000000002, 0.33020000000000005, 2.8484, 5.4295]))


def test_08_random_valid_case_5():
    _close(solve([3.36, 3.98, 0.45, 0.5, -4.13, -4.6], [0.56, 0.18, -3.68, -0.95, -1.97, 1.48], 0.45), np.array([3.612, 4.061, -1.2060000000000002, 0.07250000000000001, -5.0165, -3.9339999999999997]))


def test_09_random_valid_case_6():
    _close(solve([-3.53, -3.22, 2.24, -0.4, 3.6, 1.72], [-3.12, -3.19, 4.96, 2.7, 4.92, -0.49], 0.75), np.array([-5.869999999999999, -5.612500000000001, 5.96, 1.6250000000000004, 7.29, 1.3525]))


def test_10_random_valid_case_7():
    _close(solve([-2.14, -0.2, -0.03, 4.1, -2.86, 4.38], [-1.59, 4.86, -3.53, 3.32, 1.67, 4.11], 0.99), np.array([-3.7141, 4.6114, -3.5246999999999997, 7.386799999999999, -1.2066999999999999, 8.4489]))


def test_11_random_valid_case_8():
    _close(solve([4.0, 3.42, 4.05, -4.38, -0.5, 1.38], [-3.02, 0.85, -2.34, -1.55, 1.47, -1.58], 0.76), np.array([1.7048, 4.066, 2.2716, -5.558, 0.6172, 0.1791999999999998]))


def test_12_random_valid_case_9():
    _close(solve([2.68, 1.61, 3.75, -3.31, -3.34, 3.97], [4.41, -3.94, 4.92, -4.15, -3.25, 3.49], 0.58), np.array([5.2378, -0.6751999999999996, 6.6036, -5.7170000000000005, -5.225, 5.9942]))
