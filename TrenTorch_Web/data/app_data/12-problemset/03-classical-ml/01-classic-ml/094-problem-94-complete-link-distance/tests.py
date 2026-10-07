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
    _close(solve([[0.0, 0.0], [1.0, 0.0]], [[0.0, 1.0], [2.0, 1.0]]), 2.23606797749979)


def test_02_singleton_boundary():
    _close(solve([[0.0, 0.0]], [[0.0, 1.0]]), 1.0)


def test_03_random_valid_case():
    _close(solve([[2.12, -0.59, 4.67], [-1.96, -3.71, 1.1], [-0.47, 2.33, -0.18], [4.8, 0.56, -2.79]], [[0.7, -3.75, 2.79], [0.83, 1.37, 0.29], [0.0, 2.97, 1.25], [3.3, 0.11, -2.12], [1.98, 4.37, -0.8]]), 9.188035698668132)


def test_04_random_valid_case():
    _close(solve([[4.36, -4.83, -0.01], [3.63, 0.14, 0.41], [2.45, -2.97, -1.22], [4.08, 1.35, -1.08]], [[-3.02, 4.97, -2.65], [0.1, -0.48, 0.95], [3.0, 2.39, 3.25], [3.24, 4.22, 4.96], [2.19, 4.31, 0.85]]), 12.548864490462874)


def test_05_random_valid_case():
    _close(solve([[4.56, -1.0, -0.61], [2.38, 4.3, 1.12], [-0.8, 0.06, 0.01], [3.23, -0.4, 4.87]], [[2.25, -4.64, -4.88], [-4.66, -1.59, 3.6], [-0.74, 4.87, 4.01], [-4.47, -3.04, 1.95], [0.17, -0.13, 1.8]]), 10.7675670418159)


def test_06_random_valid_case():
    _close(solve([[-3.15, 3.76, 3.33], [-3.6, -2.96, 0.09], [0.0, -1.25, -4.46], [2.93, -0.69, 0.27]], [[-4.53, 1.49, -1.2], [4.51, -3.8, 1.5], [-3.88, -4.53, 3.21], [1.3, 4.8, -4.39], [-1.94, -2.44, 0.05]]), 10.916872262695025)


def test_07_random_valid_case():
    _close(solve([[-4.11, 4.82, -0.88], [-3.34, -1.41, 3.12], [0.67, 1.53, 3.68], [-1.41, 4.16, 0.8]], [[-1.82, -3.6, -2.19], [-1.89, 1.18, 2.5], [3.21, -3.47, -0.77], [4.85, -4.3, -0.33], [2.8, 3.64, 1.89]]), 12.79681601024255)


def test_08_random_valid_case():
    _close(solve([[-0.85, 2.37, -3.72], [0.93, -3.87, 1.94], [-0.62, -2.87, 0.19], [1.39, -0.61, 4.52]], [[-3.12, -2.8, 0.8], [4.22, 3.09, -4.87], [4.08, -3.82, 2.53], [-4.75, 2.63, 0.3], [4.34, -0.75, -4.8]]), 10.481936843923455)


def test_09_random_valid_case():
    _close(solve([[-1.2, 4.56, -1.0], [0.76, 3.26, -3.04], [-4.02, -2.56, -4.66], [0.11, -2.05, 0.75]], [[2.64, 3.12, -2.04], [-2.27, -1.81, 0.93], [-0.77, 0.77, -1.1], [1.52, 4.1, 4.17], [2.33, -3.43, 0.94]]), 12.36996766366024)


def test_10_random_valid_case():
    _close(solve([[0.55, 0.27, -0.48], [0.96, -2.56, -2.97], [-4.65, 4.29, 3.23], [1.57, 3.94, 3.64]], [[-2.58, 3.82, 3.0], [-2.24, -0.9, 4.13], [-4.89, 2.77, 4.63], [-1.39, 2.82, -0.25], [-4.93, 4.84, -3.79]]), 10.972301490571612)


def test_11_random_valid_case():
    _close(solve([[-1.75, 2.94, 2.33], [-1.36, 1.13, 2.05], [3.72, -1.95, -0.11], [2.21, -3.18, -0.58]], [[-2.68, 2.6, 2.36], [1.67, -3.71, -1.35], [4.19, 4.79, 3.65], [3.66, 1.23, 2.98], [-0.82, -4.88, 2.57]]), 9.237651216624279)


def test_12_random_valid_case():
    _close(solve([[1.67, -2.51, 3.88], [-3.3, 3.78, 3.7], [4.04, 4.29, -2.05], [1.86, -1.17, 2.05]], [[-0.07, 4.73, -2.18], [-0.47, 3.35, -1.58], [4.72, 0.75, -1.63], [-2.44, 0.14, -2.68], [-1.19, 1.34, -0.99]]), 10.09505819695954)
