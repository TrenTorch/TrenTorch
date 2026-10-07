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
    _close(solve([1.0, 2.0, 3.0, 4.0], 0.5, 0), np.array([0.0, 4.0, 6.0, 8.0]))


def test_02_readme_example_2():
    _close(solve([1.0, 2.0, 3.0], 1.0, 0), np.array([1.0, 2.0, 3.0]))


def test_03_readme_example_3():
    with pytest.raises(ValueError):
        solve([1.0, 2.0], 0.0, 0)


def test_04_random_valid_case_1():
    _close(solve([3.0, 1.36, 4.92, 3.2, 3.09, 4.0, 1.79, 3.9, 4.88, 3.83, 3.13, 4.4], 0.54, 3), np.array([5.555555555555555, 2.5185185185185186, 0.0, 0.0, 5.722222222222221, 7.4074074074074066, 3.314814814814815, 7.222222222222221, 0.0, 7.092592592592593, 5.796296296296296, 8.148148148148149]))


def test_05_random_valid_case_2():
    _close(solve([4.93, 4.28, 4.79, 3.3, 3.28, 2.29, 4.35, 4.4, 4.43, 4.88, 3.2, 2.53], 0.5, 353), np.array([0.0, 8.56, 0.0, 0.0, 0.0, 4.58, 8.7, 0.0, 8.86, 9.76, 6.4, 5.06]))


def test_06_random_valid_case_3():
    _close(solve([4.1, 3.68, 1.72, 3.4, 4.01, 1.39, 2.9, 2.41, 1.66, 1.91, 3.62, 2.89], 0.54, 646), np.array([7.592592592592592, 6.814814814814815, 3.185185185185185, 6.296296296296296, 0.0, 2.5740740740740735, 5.37037037037037, 4.462962962962963, 0.0, 0.0, 6.703703703703703, 0.0]))


def test_07_random_valid_case_4():
    _close(solve([2.86, 4.63, 4.93, 3.95, 4.52, 1.0, 2.58, 3.0, 4.13, 4.72, 3.63, 1.67], 0.56, 399), np.array([0.0, 0.0, 0.0, 7.053571428571428, 0.0, 0.0, 4.607142857142857, 5.357142857142857, 7.374999999999999, 8.428571428571427, 6.482142857142857, 2.9821428571428568]))


def test_08_random_valid_case_5():
    _close(solve([2.3, 3.91, 3.04, 1.62, 1.73, 4.3, 1.27, 4.69, 3.34, 3.91, 3.19, 4.05], 0.49, 942), np.array([4.693877551020408, 0.0, 0.0, 3.306122448979592, 0.0, 0.0, 2.5918367346938775, 0.0, 0.0, 0.0, 6.510204081632653, 0.0]))


def test_09_random_valid_case_6():
    _close(solve([3.11, 2.4, 1.3, 1.83, 4.93, 3.89, 1.42, 4.06, 3.71, 2.56, 3.73, 1.65], 0.56, 675), np.array([5.553571428571428, 0.0, 2.321428571428571, 3.267857142857143, 8.803571428571427, 0.0, 0.0, 7.249999999999998, 0.0, 4.571428571428571, 6.660714285714285, 0.0]))


def test_10_random_valid_case_7():
    _close(solve([4.94, 4.18, 1.03, 4.99, 1.55, 3.63, 2.51, 1.4, 4.41, 2.26, 2.25, 1.68], 0.35, 178), np.array([0.0, 11.942857142857143, 2.942857142857143, 0.0, 4.428571428571429, 0.0, 0.0, 0.0, 12.600000000000001, 6.457142857142857, 0.0, 0.0]))


def test_11_random_valid_case_8():
    _close(solve([2.91, 4.54, 2.06, 3.84, 2.0, 2.68, 3.33, 4.7, 2.84, 3.87, 1.19, 3.23], 0.53, 1211), np.array([5.490566037735849, 0.0, 3.8867924528301887, 7.245283018867924, 0.0, 0.0, 0.0, 8.867924528301886, 0.0, 7.30188679245283, 2.2452830188679243, 6.094339622641509]))


def test_12_random_valid_case_9():
    _close(solve([4.16, 4.94, 2.12, 1.47, 1.35, 3.02, 2.73, 2.19, 2.09, 1.82, 1.29, 3.2], 0.61, 654), np.array([6.8196721311475414, 0.0, 0.0, 0.0, 2.2131147540983607, 4.950819672131147, 4.475409836065574, 3.5901639344262297, 0.0, 0.0, 0.0, 5.245901639344263]))
