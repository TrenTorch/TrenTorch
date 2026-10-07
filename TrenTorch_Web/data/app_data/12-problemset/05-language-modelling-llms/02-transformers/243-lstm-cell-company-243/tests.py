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
    _close(solve([0.5, 0.5], [0.9, 0.9], [1.0, 1.0], [0.2, -0.2], [0.0, 0.0]), (np.array([0.09966799462495582, -0.09966799462495582]), np.array([0.1, -0.1])))


def test_02_readme_example_2():
    _close(solve([0.0], [1.0], [1.0], [5.0], [2.0]), (np.array([0.9640275800758169]), np.array([2.0])))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve(np.array([]), np.array([1.0, -1.0, 2.0]), np.array([1.0, -1.0, 2.0]), np.array([1.0, -1.0, 2.0]), np.array([1.0, -1.0, 2.0]))


def test_04_random_valid_case_1():
    _close(solve([0.7, 0.36, 0.39, 0.05], [0.89, 0.04, 0.75, 0.46], [0.4, 0.1, 0.8, 0.02], [-0.6, 0.45, 0.04, 0.11], [0.57, 0.43, 0.07, 0.21]), (np.array([0.034831557792104235, 0.017730612814598628, 0.05439593693963271, 0.0020349339140422686]), np.array([0.08729999999999999, 0.1792, 0.06810000000000001, 0.10210000000000001])))


def test_05_random_valid_case_2():
    _close(solve([0.63, 0.07, 0.81, 0.14], [0.89, 0.04, 0.85, 0.28], [0.06, 0.0, 0.3, 0.91], [0.0, 0.05, 0.87, 0.33], [0.49, 0.15, 0.83, 0.09]), (np.array([0.02462439191334247, 0.0, 0.2662609788446232, 0.06486381306829478]), np.array([0.4361, 0.009500000000000001, 1.4102, 0.0714])))


def test_06_random_valid_case_3():
    _close(solve([0.24, 0.2, 0.3, 0.33], [0.48, 0.43, 0.94, 0.25], [0.12, 0.08, 0.9, 0.84], [-0.12, 0.37, 0.68, -0.17], [0.03, 0.88, 0.65, 0.7]), (np.array([-0.0017278805705459466, 0.03390958470914796, 0.6051053497979539, 0.09940799036681319]), np.array([-0.0144, 0.4524, 0.815, 0.11889999999999998])))


def test_07_random_valid_case_4():
    _close(solve([0.1, 0.39, 0.31, 0.88], [0.59, 0.6, 0.9, 0.52], [0.36, 0.48, 1.0, 0.07], [-0.79, -0.55, -0.43, 0.17], [0.0, 0.34, 0.05, 0.82]), (np.array([-0.02838098264654385, -0.005039814788167843, -0.08807122500457484, 0.036382644968722955]), np.array([-0.07900000000000001, -0.01050000000000001, -0.08829999999999999, 0.5760000000000001])))


def test_08_random_valid_case_5():
    _close(solve([0.51, 0.53, 0.55, 0.44], [0.69, 0.85, 0.29, 0.71], [0.62, 0.27, 1.0, 0.45], [-0.6, -0.54, -0.56, 0.98], [0.6, 0.9, 0.15, 0.61]), (np.array([0.0667008684570102, 0.12022615507597287, -0.2584996953186597, 0.3143099315665354]), np.array([0.10799999999999998, 0.4788, -0.26450000000000007, 0.8643])))


def test_09_random_valid_case_6():
    _close(solve([0.78, 0.96, 0.02, 0.17], [0.45, 0.83, 0.52, 0.71], [0.0, 0.7, 0.02, 0.69], [0.5, 0.89, -0.55, -0.53], [0.57, 0.55, 0.93, 0.37]), (np.array([0.0, 0.6051520726974823, 0.008805953418927462, 0.1179252911267029]), np.array([0.6465000000000001, 1.3109, 0.4726, 0.17259999999999998])))


def test_10_random_valid_case_7():
    _close(solve([0.43, 0.41, 0.93, 0.76], [0.61, 0.16, 0.63, 0.44], [0.63, 0.27, 0.65, 0.84], [0.8, 0.75, -0.3, 0.09], [0.94, 0.55, 0.45, 0.62]), (np.array([0.4565390143791315, 0.1015448452016852, 0.0029249802564099256, 0.27598055833441665]), np.array([0.9174, 0.3955, 0.004500000000000004, 0.3412])))


def test_11_random_valid_case_8():
    _close(solve([0.73, 0.78, 0.82, 0.92], [0.91, 0.32, 0.5, 0.93], [0.51, 0.96, 0.1, 0.58], [0.26, -0.49, -0.44, 0.06], [0.74, 0.05, 0.28, 0.67]), (np.array([0.3559303885617753, -0.33663689270377584, -0.021728042522121578, 0.3424396014007616]), np.array([0.8632, -0.36619999999999997, -0.22079999999999994, 0.6783000000000001])))


def test_12_random_valid_case_9():
    _close(solve([0.86, 0.49, 0.31, 0.9], [0.78, 0.26, 0.6, 0.89], [0.83, 0.74, 0.3, 0.75], [-0.05, -0.47, -0.13, -0.07], [0.94, 0.59, 0.3, 0.84]), (np.array([0.49643168896980316, -0.05679409140916566, 0.041639471887007215, 0.4458763061751694]), np.array([0.6901999999999999, -0.07689999999999997, 0.1397, 0.6845999999999999])))
