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
    _close(solve([1.0, 2.0], [0.1, 0.2], 0.01), np.array([0.999, 1.998]))


def test_02_readme_example_2():
    _close(solve([5.0], [-2.0], 0.5), np.array([6.0]))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], [0.1, 0.2], 0.01)


def test_04_random_valid_case_1():
    _close(solve([4.37, 4.12, 4.86, 3.61, 1.07], [-0.1, 0.6, 3.28, 3.68, 4.32], 0.92), np.array([4.462, 3.568, 1.8424000000000005, 0.2243999999999997, -2.9044000000000008]))


def test_05_random_valid_case_2():
    _close(solve([4.99, 2.5, 1.34, 4.23, -0.41], [4.65, 2.2, -1.13, -1.54, -3.78], 0.7), np.array([1.7350000000000003, 0.96, 2.1310000000000002, 5.308, 2.2359999999999998]))


def test_06_random_valid_case_3():
    _close(solve([-0.65, 3.13, 0.49, -3.04, 4.2], [2.29, 1.9, -2.38, 4.82, 1.03], 0.66), np.array([-2.1614, 1.876, 2.0608, -6.2212000000000005, 3.5202]))


def test_07_random_valid_case_4():
    _close(solve([1.91, 2.88, -4.0, -4.26, 1.11], [1.08, 0.77, -4.15, 3.24, 4.52], 0.41), np.array([1.4671999999999998, 2.5643, -2.2984999999999998, -5.5884, -0.7431999999999996]))


def test_08_random_valid_case_5():
    _close(solve([0.86, -2.19, 2.6, -1.71, 4.64], [0.09, 3.8, 0.98, -3.72, -0.42], 0.34), np.array([0.8294, -3.482, 2.2668, -0.4451999999999998, 4.7828]))


def test_09_random_valid_case_6():
    _close(solve([-1.41, 2.21, -0.6, 0.72, -4.41], [-1.54, 0.01, -3.8, 1.58, 3.85], 0.75), np.array([-0.2549999999999999, 2.2025, 2.2499999999999996, -0.4650000000000001, -7.2975]))


def test_10_random_valid_case_7():
    _close(solve([0.11, 3.5, 1.72, 0.16, -2.25], [-0.5, -0.11, 3.44, -3.54, -3.49], 0.42), np.array([0.32, 3.5462, 0.2752000000000001, 1.6467999999999998, -0.7842]))


def test_11_random_valid_case_8():
    _close(solve([3.17, 1.5, -3.47, -1.79, -3.16], [-1.12, 0.51, 4.76, 1.51, 2.37], 0.06), np.array([3.2372, 1.4694, -3.7556000000000003, -1.8806, -3.3022]))


def test_12_random_valid_case_9():
    _close(solve([1.76, 1.05, 3.97, -4.45, 4.39], [-4.43, 0.9, -3.76, 0.28, -0.53], 0.11), np.array([2.2473, 0.9510000000000001, 4.3836, -4.4808, 4.4483]))
