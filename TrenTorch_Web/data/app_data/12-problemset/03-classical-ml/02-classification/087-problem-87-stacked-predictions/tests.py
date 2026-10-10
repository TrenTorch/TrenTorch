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
    _close(solve([[1.0, 2.0], [3.0, 4.0]]), np.array([[1.0, 3.0], [2.0, 4.0]]))


def test_02_singleton_boundary():
    _close(solve([[1.0, 2.0]]), np.array([[1.0], [2.0]]))


def test_03_random_valid_case():
    _close(solve([[-4.52, 4.54, 2.38, 4.5, 3.86], [-1.48, -4.3, 0.37, 1.79, 2.7], [-4.26, 4.93, -2.75, 2.81, 0.1]]), np.array([[-4.52, -1.48, -4.26], [4.54, -4.3, 4.93], [2.38, 0.37, -2.75], [4.5, 1.79, 2.81], [3.86, 2.7, 0.1]]))


def test_04_random_valid_case():
    _close(solve([[2.54, 3.71, 1.07, 4.12, 2.72], [4.05, -0.65, 4.01, 2.58, 2.09], [0.78, 1.63, 4.82, 2.31, -1.21]]), np.array([[2.54, 4.05, 0.78], [3.71, -0.65, 1.63], [1.07, 4.01, 4.82], [4.12, 2.58, 2.31], [2.72, 2.09, -1.21]]))


def test_05_random_valid_case():
    _close(solve([[1.8, -2.83, -0.14, 0.2, 1.33], [-3.84, 0.79, 4.12, 0.18, -4.61], [-0.46, -3.7, -4.57, 1.6, 4.21]]), np.array([[1.8, -3.84, -0.46], [-2.83, 0.79, -3.7], [-0.14, 4.12, -4.57], [0.2, 0.18, 1.6], [1.33, -4.61, 4.21]]))


def test_06_random_valid_case():
    _close(solve([[-0.78, -1.14, 1.19, 1.4, -1.32], [0.83, 4.42, 0.34, -3.84, 2.3], [4.94, -2.99, -3.78, 1.08, 4.66]]), np.array([[-0.78, 0.83, 4.94], [-1.14, 4.42, -2.99], [1.19, 0.34, -3.78], [1.4, -3.84, 1.08], [-1.32, 2.3, 4.66]]))


def test_07_random_valid_case():
    _close(solve([[4.53, 3.89, -0.16, 1.26, 4.84], [4.37, 0.73, 1.01, 2.79, -4.03], [-0.79, 3.18, 1.68, -4.03, 1.86]]), np.array([[4.53, 4.37, -0.79], [3.89, 0.73, 3.18], [-0.16, 1.01, 1.68], [1.26, 2.79, -4.03], [4.84, -4.03, 1.86]]))


def test_08_random_valid_case():
    _close(solve([[0.11, -4.04, 3.11, 4.77, -0.34], [2.4, -2.22, -4.06, -0.35, -1.5], [-4.0, -1.48, 1.88, 3.4, -2.0]]), np.array([[0.11, 2.4, -4.0], [-4.04, -2.22, -1.48], [3.11, -4.06, 1.88], [4.77, -0.35, 3.4], [-0.34, -1.5, -2.0]]))


def test_09_random_valid_case():
    _close(solve([[0.5, -2.46, -0.75, -2.48, 2.57], [4.81, -1.3, -3.78, -1.43, 0.98], [2.12, 1.44, -3.06, 1.16, 1.93]]), np.array([[0.5, 4.81, 2.12], [-2.46, -1.3, 1.44], [-0.75, -3.78, -3.06], [-2.48, -1.43, 1.16], [2.57, 0.98, 1.93]]))


def test_10_random_valid_case():
    _close(solve([[-3.12, -3.86, -4.47, 2.26, -1.7], [-2.82, 0.24, -4.7, -2.66, 1.33], [4.38, 4.98, 1.59, 3.07, 4.64]]), np.array([[-3.12, -2.82, 4.38], [-3.86, 0.24, 4.98], [-4.47, -4.7, 1.59], [2.26, -2.66, 3.07], [-1.7, 1.33, 4.64]]))


def test_11_random_valid_case():
    _close(solve([[4.95, 4.92, -3.84, 4.33, 2.78], [0.94, 0.46, -3.15, -4.99, 4.33], [-1.44, -3.04, 4.4, -2.01, 0.25]]), np.array([[4.95, 0.94, -1.44], [4.92, 0.46, -3.04], [-3.84, -3.15, 4.4], [4.33, -4.99, -2.01], [2.78, 4.33, 0.25]]))


def test_12_random_valid_case():
    _close(solve([[4.12, -3.27, -4.81, -4.86, -1.71], [-3.52, 1.3, 0.13, -1.37, -2.03], [2.2, 0.25, -4.98, 4.7, 0.12]]), np.array([[4.12, -3.52, 2.2], [-3.27, 1.3, 0.25], [-4.81, 0.13, -4.98], [-4.86, -1.37, 4.7], [-1.71, -2.03, 0.12]]))
