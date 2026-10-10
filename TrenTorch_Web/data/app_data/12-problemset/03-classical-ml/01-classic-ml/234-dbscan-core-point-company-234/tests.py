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
    _close(solve([[0, 0], [0, 1], [5, 5]], 1.1, 2), np.array([True, True, False]))


def test_02_readme_example_2():
    _close(solve([[0.0], [1.0], [2.0], [3.0]], 1.0, 3), np.array([False, True, True, False]))


def test_03_random_valid_case_1():
    _close(solve([[1.15, 3.53], [2.0, 3.7], [0.5, 0.72], [1.26, 0.41], [1.82, 0.8], [3.02, 2.23], [0.49, 3.32], [2.82, 0.95], [3.3, 0.38], [0.18, 1.76], [1.91, 1.65], [3.03, 0.52], [3.16, 3.37], [1.03, 0.1], [1.81, 1.37], [2.41, 1.66], [2.41, 0.48], [1.08, 0.3], [3.73, 0.43], [2.44, 0.66], [1.39, 3.69], [0.28, 3.32], [3.63, 1.6], [0.76, 2.0], [0.05, 0.61]], 0.9, 4), np.array([True, False, True, True, True, False, False, True, True, False, True, True, False, True, True, True, True, True, False, True, False, False, False, False, False]))


def test_04_random_valid_case_2():
    _close(solve([[2.63, 3.01], [1.54, 3.08], [1.93, 2.43], [2.17, 3.38], [3.38, 0.25], [0.95, 1.13], [1.89, 1.88], [0.28, 3.28], [0.35, 1.83], [1.4, 1.43], [2.59, 3.87], [1.9, 2.07], [0.57, 3.85], [3.94, 1.2], [3.05, 0.71], [3.33, 2.38], [0.59, 2.3], [3.03, 0.68], [2.52, 2.74], [0.9, 0.15], [0.24, 0.34], [0.53, 0.24], [1.22, 0.7], [1.67, 0.63], [1.2, 2.62]], 0.9, 2), np.array([True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True]))


def test_05_random_valid_case_3():
    _close(solve([[0.73, 1.66], [2.33, 2.15], [3.44, 1.18], [2.2, 2.0], [3.2, 1.08], [3.67, 0.03], [0.49, 3.42], [3.66, 0.66], [2.19, 3.61], [3.4, 1.6], [2.86, 0.36], [3.1, 3.09], [1.61, 3.87], [0.49, 3.96], [3.8, 0.64], [0.12, 0.41], [3.86, 1.34], [0.49, 3.32], [1.59, 3.98], [1.35, 3.71], [2.06, 0.94], [0.31, 0.49], [0.89, 3.69], [0.15, 0.29], [2.69, 0.84]], 0.9, 2), np.array([False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True]))


def test_06_random_valid_case_4():
    _close(solve([[2.9, 0.93], [3.79, 2.56], [0.32, 3.97], [2.95, 1.21], [3.0, 1.4], [2.99, 2.11], [3.51, 3.91], [3.54, 2.03], [0.91, 2.07], [0.4, 0.08], [1.93, 3.47], [1.2, 0.75], [3.87, 3.69], [2.44, 1.59], [0.57, 3.12], [1.39, 1.98], [1.17, 3.38], [0.11, 0.95], [1.33, 3.01], [2.35, 2.71], [0.01, 1.28], [1.18, 2.8], [0.12, 2.52], [2.89, 3.75], [3.66, 3.05]], 0.9, 2), np.array([True, True, True, True, True, True, True, True, True, False, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True]))


def test_07_random_valid_case_5():
    _close(solve([[3.7, 1.69], [1.17, 1.36], [3.0, 1.01], [3.27, 1.21], [3.46, 0.8], [1.2, 0.98], [2.43, 3.67], [0.48, 0.72], [3.53, 3.22], [3.27, 2.97], [1.88, 2.15], [3.49, 0.76], [3.64, 0.82], [3.09, 0.86], [0.03, 1.29], [2.44, 0.97], [0.66, 2.77], [1.43, 3.44], [1.84, 0.53], [3.25, 3.68], [3.48, 1.06], [3.12, 1.17], [1.31, 1.42], [1.16, 2.89], [1.5, 0.9]], 0.9, 3), np.array([True, True, True, True, True, True, False, True, True, True, False, True, True, True, False, True, False, False, True, True, True, True, True, True, True]))


def test_08_random_valid_case_6():
    _close(solve([[2.29, 3.9], [0.39, 1.02], [2.04, 3.03], [3.29, 3.3], [3.14, 0.53], [0.48, 2.62], [2.25, 1.87], [0.93, 2.74], [0.84, 2.7], [2.28, 3.62], [3.32, 3.01], [1.13, 3.29], [3.32, 3.33], [2.73, 2.28], [1.0, 0.81], [3.88, 0.1], [2.42, 1.18], [0.69, 1.51], [0.19, 0.73], [2.39, 1.43], [2.07, 0.36], [3.89, 1.86], [3.87, 3.57], [1.15, 1.9], [3.66, 2.87]], 0.9, 2), np.array([True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True]))


def test_09_random_valid_case_7():
    _close(solve([[2.56, 0.41], [2.07, 3.4], [3.78, 1.57], [3.52, 2.56], [3.99, 0.37], [1.05, 1.1], [2.38, 1.96], [0.83, 3.27], [2.65, 1.92], [3.0, 3.96], [0.49, 0.43], [1.64, 1.0], [3.17, 3.61], [3.82, 2.36], [2.24, 3.13], [1.03, 3.37], [3.48, 1.06], [2.32, 2.99], [0.55, 3.76], [1.39, 3.26], [0.0, 0.0], [0.05, 3.78], [1.66, 0.66], [3.94, 3.72], [0.95, 1.12]], 0.9, 3), np.array([False, True, True, False, False, True, False, True, False, False, True, True, True, True, True, True, True, True, True, True, False, False, True, False, True]))


def test_10_random_valid_case_8():
    _close(solve([[1.28, 1.61], [0.72, 0.34], [3.42, 3.75], [3.45, 3.82], [0.84, 0.53], [3.12, 0.84], [0.67, 0.86], [0.71, 1.99], [2.33, 3.71], [2.87, 1.66], [3.57, 3.12], [3.74, 2.12], [0.73, 1.42], [3.6, 0.84], [0.8, 2.98], [1.31, 2.52], [2.47, 3.56], [1.25, 2.98], [3.95, 0.23], [3.02, 3.19], [2.93, 3.8], [2.3, 1.83], [2.96, 1.8], [1.04, 1.06], [0.04, 2.89]], 0.9, 3), np.array([True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, False, True, True, True, True, True, False]))


def test_11_random_valid_case_9():
    _close(solve([[2.15, 3.97], [2.88, 2.54], [3.99, 3.29], [3.49, 2.99], [2.54, 1.49], [2.87, 0.76], [0.0, 2.51], [3.23, 3.76], [2.32, 0.47], [3.9, 2.84], [0.25, 2.21], [2.8, 2.42], [3.21, 2.15], [3.15, 1.65], [0.7, 3.91], [2.98, 0.61], [2.32, 2.62], [2.06, 0.81], [3.17, 2.6], [3.49, 1.47], [0.26, 3.84], [1.51, 1.93], [2.13, 1.37], [2.83, 3.73], [3.69, 0.77]], 0.9, 4), np.array([False, True, True, True, True, True, False, True, True, True, False, True, True, True, False, True, True, True, True, True, False, False, True, False, True]))


def test_12_random_valid_case_10():
    _close(solve([[3.09, 3.59], [0.7, 3.83], [0.37, 0.56], [1.03, 2.25], [2.69, 3.89], [2.15, 2.64], [0.62, 3.07], [1.77, 2.21], [3.44, 1.56], [0.53, 1.96], [2.02, 2.58], [1.52, 3.7], [0.72, 3.83], [0.79, 2.66], [0.05, 1.32], [1.99, 2.15], [0.68, 0.03], [3.08, 1.11], [0.39, 3.56], [3.2, 3.43], [1.49, 1.09], [3.52, 2.07], [0.84, 1.67], [0.2, 3.98], [1.66, 2.27]], 0.9, 2), np.array([True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]))
