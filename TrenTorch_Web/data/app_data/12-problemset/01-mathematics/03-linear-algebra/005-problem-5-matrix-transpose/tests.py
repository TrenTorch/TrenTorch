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
    _close(solve([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]), np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]))


def test_02_singleton_boundary():
    _close(solve([[1.0, 2.0, 3.0]]), np.array([[1.0], [2.0], [3.0]]))


def test_03_random_valid_case():
    _close(solve([[1.24, 2.7, 1.52, 0.41, 2.02], [3.76, 0.76, -3.18, 3.38, 3.97], [3.96, 4.7, 3.44, -0.6, 1.18]]), np.array([[1.24, 3.76, 3.96], [2.7, 0.76, 4.7], [1.52, -3.18, 3.44], [0.41, 3.38, -0.6], [2.02, 3.97, 1.18]]))


def test_04_random_valid_case():
    _close(solve([[-2.73, 0.31, -2.42, 0.73, 4.09], [0.3, 0.85, -3.8, -3.81, 4.19], [-4.57, 1.78, 4.23, 1.63, -3.2]]), np.array([[-2.73, 0.3, -4.57], [0.31, 0.85, 1.78], [-2.42, -3.8, 4.23], [0.73, -3.81, 1.63], [4.09, 4.19, -3.2]]))


def test_05_random_valid_case():
    _close(solve([[-1.17, -4.87, 2.42, -4.4, 3.97], [0.39, 2.42, -1.91, 3.64, -3.39], [0.34, 2.1, 1.99, -3.29, 0.21]]), np.array([[-1.17, 0.39, 0.34], [-4.87, 2.42, 2.1], [2.42, -1.91, 1.99], [-4.4, 3.64, -3.29], [3.97, -3.39, 0.21]]))


def test_06_random_valid_case():
    _close(solve([[-1.06, -3.71, 0.04, -2.1, -0.79], [1.41, 2.15, 1.44, 2.68, 1.07], [1.82, 0.03, -3.81, -1.44, 1.21]]), np.array([[-1.06, 1.41, 1.82], [-3.71, 2.15, 0.03], [0.04, 1.44, -3.81], [-2.1, 2.68, -1.44], [-0.79, 1.07, 1.21]]))


def test_07_random_valid_case():
    _close(solve([[0.41, -1.68, 0.05, -3.04, 4.95], [-2.73, -2.86, 1.11, -3.27, 4.97], [0.6, 3.47, -0.58, 3.02, 4.87]]), np.array([[0.41, -2.73, 0.6], [-1.68, -2.86, 3.47], [0.05, 1.11, -0.58], [-3.04, -3.27, 3.02], [4.95, 4.97, 4.87]]))


def test_08_random_valid_case():
    _close(solve([[3.46, -3.13, -2.35, 1.1, -3.84], [-0.42, -0.82, 4.0, 2.49, 1.45], [-2.49, 3.47, 0.96, -3.5, -4.59]]), np.array([[3.46, -0.42, -2.49], [-3.13, -0.82, 3.47], [-2.35, 4.0, 0.96], [1.1, 2.49, -3.5], [-3.84, 1.45, -4.59]]))


def test_09_random_valid_case():
    _close(solve([[0.82, -1.26, -1.68, -1.25, 1.9], [2.29, -2.1, -3.78, 0.62, 3.17], [3.56, 3.31, -0.86, -1.94, 2.27]]), np.array([[0.82, 2.29, 3.56], [-1.26, -2.1, 3.31], [-1.68, -3.78, -0.86], [-1.25, 0.62, -1.94], [1.9, 3.17, 2.27]]))


def test_10_random_valid_case():
    _close(solve([[0.78, 0.5, -4.79, -3.6, -2.24], [-3.27, 0.69, -1.17, 4.67, -0.07], [3.74, 3.3, -2.88, -0.77, 2.22]]), np.array([[0.78, -3.27, 3.74], [0.5, 0.69, 3.3], [-4.79, -1.17, -2.88], [-3.6, 4.67, -0.77], [-2.24, -0.07, 2.22]]))


def test_11_random_valid_case():
    _close(solve([[4.27, -4.77, 0.28, -1.57, 2.8], [3.08, 1.25, -0.91, 4.77, 2.19], [-4.39, 1.44, -3.8, -0.96, -2.37]]), np.array([[4.27, 3.08, -4.39], [-4.77, 1.25, 1.44], [0.28, -0.91, -3.8], [-1.57, 4.77, -0.96], [2.8, 2.19, -2.37]]))


def test_12_random_valid_case():
    _close(solve([[3.73, 4.83, -2.44, -0.51, -0.67], [-0.47, 0.46, -3.24, 4.53, -3.8], [1.65, -3.24, 3.1, -4.45, -1.8]]), np.array([[3.73, -0.47, 1.65], [4.83, 0.46, -3.24], [-2.44, -3.24, 3.1], [-0.51, 4.53, -4.45], [-0.67, -3.8, -1.8]]))
