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


def test_01_basic_example():
    _close(solve([[1.0, 2.0], [3.0, 4.0]], 2), np.array([[1.0, 2.0, 1.0, 4.0], [3.0, 4.0, 9.0, 16.0]]))


def test_02_singleton_boundary():
    _close(solve([[1.0, 2.0]], 2), np.array([[1.0, 2.0, 1.0, 4.0]]))


def test_03_parameter_nudge():
    _close(solve([[1.0, 2.0], [3.0, 4.0]], 3), np.array([[1.0, 2.0, 1.0, 4.0, 1.0, 8.0], [3.0, 4.0, 9.0, 16.0, 27.0, 64.0]]))


def test_04_random_valid_case():
    _close(solve([-4.7, 4.5, 1.54, 3.64, 4.58, 2.85], 2), np.array([[-4.7, 22.090000000000003], [4.5, 20.25], [1.54, 2.3716], [3.64, 13.249600000000001], [4.58, 20.9764], [2.85, 8.1225]]))


def test_05_random_valid_case():
    _close(solve([-3.13, 2.45, 2.6, -0.62, 3.8, 0.76], 4), np.array([[-3.13, 9.796899999999999, -30.664296999999998, 95.97924960999998], [2.45, 6.002500000000001, 14.706125000000004, 36.030006250000014], [2.6, 6.760000000000001, 17.576, 45.69760000000001], [-0.62, 0.3844, -0.23832799999999998, 0.14776335999999998], [3.8, 14.44, 54.87199999999999, 208.51359999999997], [0.76, 0.5776, 0.43897600000000003, 0.33362176]]))


def test_06_random_valid_case():
    _close(solve([-1.61, -3.7, 3.55, 4.2, 3.45, 4.65], 1), np.array([[-1.61], [-3.7], [3.55], [4.2], [3.45], [4.65]]))


def test_07_random_valid_case():
    _close(solve([-4.69, 0.43, 3.29, 2.79, 3.23, 3.71], 1), np.array([[-4.69], [0.43], [3.29], [2.79], [3.23], [3.71]]))


def test_08_random_valid_case():
    _close(solve([-1.27, 0.5, -0.58, 4.42, 2.58, 3.16], 2), np.array([[-1.27, 1.6129], [0.5, 0.25], [-0.58, 0.3364], [4.42, 19.5364], [2.58, 6.6564000000000005], [3.16, 9.985600000000002]]))


def test_09_random_valid_case():
    _close(solve([0.12, 2.14, -0.81, -2.99, -2.2, 3.31], 3), np.array([[0.12, 0.0144, 0.0017279999999999997], [2.14, 4.5796, 9.800344], [-0.81, 0.6561000000000001, -0.531441], [-2.99, 8.940100000000001, -26.730899000000004], [-2.2, 4.840000000000001, -10.648000000000003], [3.31, 10.956100000000001, 36.264691]]))


def test_10_random_valid_case():
    _close(solve([-0.37, 2.85, 2.48, -2.53, 2.56, -0.8], 3), np.array([[-0.37, 0.1369, -0.050653], [2.85, 8.1225, 23.149125], [2.48, 6.1504, 15.252991999999999], [-2.53, 6.400899999999999, -16.194276999999996], [2.56, 6.5536, 16.777216000000003], [-0.8, 0.6400000000000001, -0.5120000000000001]]))


def test_11_random_valid_case():
    _close(solve([-1.69, -1.4, 3.09, 4.18, -0.94, 4.66], 1), np.array([[-1.69], [-1.4], [3.09], [4.18], [-0.94], [4.66]]))


def test_12_random_valid_case():
    _close(solve([2.67, -0.14, 2.86, 3.43, -1.97, 2.17], 3), np.array([[2.67, 7.1289, 19.034163], [-0.14, 0.019600000000000003, -0.0027440000000000008], [2.86, 8.179599999999999, 23.393655999999996], [3.43, 11.7649, 40.353607000000004], [-1.97, 3.8809, -7.645372999999999], [2.17, 4.7089, 10.218312999999998]]))
