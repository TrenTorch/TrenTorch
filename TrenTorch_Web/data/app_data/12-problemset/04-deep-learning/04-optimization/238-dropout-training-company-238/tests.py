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
    _close(solve([1, 2, 3, 4], 0.5), np.array([2.0, 0.0, 0.0, 0.0]))


def test_02_readme_example_2():
    _close(solve([1.0, 2.0], 0.0), np.array([1.0, 2.0]))


def test_03_readme_example_3():
    with pytest.raises(ValueError):
        solve([1.0], 1.0)


def test_04_random_valid_case_1():
    _close(solve([4.13, 2.55, 2.86, 3.37, 1.04, 2.3, 1.7, 4.15, 4.6, 2.6, 1.2, 1.57], 0.53, 3), np.array([0.0, 0.0, 6.085106382978723, 7.170212765957447, 0.0, 0.0, 0.0, 0.0, 9.787234042553191, 0.0, 0.0, 0.0]))


def test_05_random_valid_case_2():
    _close(solve([3.51, 4.95, 1.21, 4.24, 1.09, 2.97, 4.94, 2.97, 3.2, 1.61, 3.44, 1.7], 0.25, 13), np.array([4.68, 6.6000000000000005, 1.6133333333333333, 5.653333333333333, 0.0, 3.9600000000000004, 6.586666666666667, 0.0, 4.266666666666667, 2.146666666666667, 4.586666666666667, 2.2666666666666666]))


def test_06_random_valid_case_3():
    _close(solve([3.01, 1.72, 2.91, 2.22, 1.05, 4.9, 3.08, 3.9, 3.85, 1.78, 4.9, 2.05], 0.36, 526), np.array([0.0, 0.0, 0.0, 3.4687500000000004, 1.640625, 7.65625, 0.0, 6.09375, 6.015625, 2.78125, 0.0, 3.2031249999999996]))


def test_07_random_valid_case_4():
    _close(solve([2.8, 4.45, 3.73, 3.97, 1.1, 2.48, 4.47, 1.21, 3.34, 3.78, 2.21, 4.29], 0.66, 689), np.array([0.0, 13.088235294117649, 0.0, 0.0, 3.2352941176470593, 7.294117647058824, 0.0, 0.0, 0.0, 0.0, 6.500000000000001, 12.61764705882353]))


def test_08_random_valid_case_5():
    _close(solve([3.26, 2.08, 3.58, 2.16, 4.18, 1.2, 2.64, 4.71, 4.77, 4.43, 1.09, 3.1], 0.32, 522), np.array([0.0, 3.058823529411765, 5.264705882352942, 0.0, 6.147058823529412, 1.7647058823529413, 3.882352941176471, 0.0, 7.014705882352941, 0.0, 1.6029411764705885, 4.558823529411765]))


def test_09_random_valid_case_6():
    _close(solve([4.45, 3.73, 4.28, 2.7, 4.41, 3.56, 4.57, 1.62, 2.3, 3.95, 1.84, 2.88], 0.61, 665), np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 11.717948717948719, 0.0, 0.0, 10.128205128205128, 0.0, 0.0]))


def test_10_random_valid_case_7():
    _close(solve([3.81, 1.65, 4.02, 4.06, 2.54, 1.95, 4.45, 1.15, 3.77, 2.93, 3.8, 1.33], 0.59, 588), np.array([9.292682926829269, 4.024390243902438, 9.804878048780486, 0.0, 6.1951219512195115, 0.0, 0.0, 2.804878048780487, 0.0, 7.146341463414634, 0.0, 0.0]))


def test_11_random_valid_case_8():
    _close(solve([3.33, 1.19, 3.77, 1.5, 4.75, 2.54, 1.67, 3.27, 2.94, 1.67, 4.0, 1.67], 0.58, 1131), np.array([7.928571428571428, 0.0, 0.0, 0.0, 0.0, 0.0, 3.976190476190476, 7.785714285714285, 0.0, 3.976190476190476, 0.0, 3.976190476190476]))


def test_12_random_valid_case_9():
    _close(solve([1.15, 1.89, 1.25, 1.38, 3.54, 1.15, 2.87, 3.55, 3.56, 4.84, 3.23, 1.09], 0.4, 584), np.array([1.9166666666666665, 3.15, 2.0833333333333335, 0.0, 5.9, 1.9166666666666665, 4.783333333333334, 5.916666666666667, 0.0, 0.0, 0.0, 1.8166666666666669]))
