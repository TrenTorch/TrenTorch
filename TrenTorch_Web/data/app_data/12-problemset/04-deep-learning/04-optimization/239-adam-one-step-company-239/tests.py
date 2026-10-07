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
    _close(solve([1.0, 2.0], [0.5, -1.0], 0.1, 0.9, 0.999, 1e-8), np.array([0.900000002, 2.099999999]))


def test_02_readme_example_2():
    _close(solve([1.0], [0.0], 0.1, 0.9, 0.999, 1e-8), np.array([1.0]))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve(np.array([]), np.array([1.0, -1.0, 2.0]), 1, 1, 1, 1)


def test_04_random_valid_case_1():
    _close(solve([4.5, 3.87, -2.78, 1.39], [1.82, 0.6, 2.94, 1.13], 0.04, 0.9, 0.999, 1e-08), np.array([4.460000000219781, 3.830000000666667, -2.8199999998639456, 1.3500000003539823]))


def test_05_random_valid_case_2():
    _close(solve([4.57, 2.35, 2.34, 4.43], [1.54, 1.13, -1.1, 0.07], 0.09, 0.9, 0.999, 1e-08), np.array([4.480000000584416, 2.2600000007964605, 2.429999999181818, 4.340000012857141]))


def test_06_random_valid_case_3():
    _close(solve([4.39, 0.32, 3.26, -2.41], [0.77, 0.91, 1.88, 2.99], 0.01, 0.9, 0.999, 1e-08), np.array([4.38000000012987, 0.3100000001098901, 3.2500000000531912, -2.419999999966555]))


def test_07_random_valid_case_4():
    _close(solve([-0.15, -3.57, 4.76, 2.74], [-0.06, 1.57, -0.6, 2.76], 0.1, 0.9, 0.999, 1e-08), np.array([-0.050000016666663885, -3.669999999363057, 4.8599999983333335, 2.640000000362319]))


def test_08_random_valid_case_5():
    _close(solve([2.91, 2.07, -0.21, -0.16], [-1.64, -2.7, 3.28, 2.59], 0.0, 0.9, 0.999, 1e-08), np.array([2.91, 2.07, -0.21, -0.16]))


def test_09_random_valid_case_6():
    _close(solve([1.01, 0.0, -4.46, 1.81], [4.59, -4.13, -3.78, -2.28], 0.1, 0.9, 0.999, 1e-08), np.array([0.910000000217865, 0.09999999975786926, -4.3600000002645505, 1.9099999995614036]))


def test_10_random_valid_case_7():
    _close(solve([3.16, 3.33, -2.51, 0.53], [1.83, -0.68, 4.71, 1.22], 0.05, 0.9, 0.999, 1e-08), np.array([3.110000000273224, 3.379999999264706, -2.5599999998938427, 0.4800000004098361]))


def test_11_random_valid_case_8():
    _close(solve([2.95, 2.51, -0.85, -2.92], [3.15, 0.59, -0.25, 0.05], 0.03, 0.9, 0.999, 1e-08), np.array([2.9200000000952384, 2.4800000005084746, -0.8200000011999999, -2.949999994000001]))


def test_12_random_valid_case_9():
    _close(solve([1.23, -3.65, 1.59, 4.7], [-4.66, -3.39, 0.56, -0.75], 0.06, 0.9, 0.999, 1e-08), np.array([1.2899999998712446, -3.590000000176991, 1.5300000010714285, 4.759999999200001]))
