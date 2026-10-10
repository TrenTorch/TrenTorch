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
    _close(solve([[0.0, 0.0], [1.0, 0.0]], [[0.0, 1.0], [2.0, 1.0]]), 1.0)


def test_02_singleton_boundary():
    _close(solve([[0.0, 0.0]], [[0.0, 1.0]]), 1.0)


def test_03_random_valid_case():
    _close(solve([[-4.56, 0.68, 4.4], [-1.45, 4.7, -1.2], [3.31, -3.01, -4.95], [2.11, 1.65, 0.34]], [[2.35, -3.89, 0.33], [0.06, 3.6, -2.78], [2.79, -0.85, 0.0], [3.5, -1.56, -0.67], [4.04, 3.91, 2.34]]), 2.4467325150085366)


def test_04_random_valid_case():
    _close(solve([[-2.43, 1.86, 3.33], [-2.27, 3.09, 4.43], [4.35, 2.28, 1.32], [-3.95, -1.34, -0.48]], [[0.16, 4.57, 4.01], [1.03, -0.13, 2.82], [4.23, -0.34, 2.1], [-2.12, 2.45, 4.79], [2.67, -3.72, 3.3]]), 0.7494664769020691)


def test_05_random_valid_case():
    _close(solve([[-0.98, 3.19, 0.8], [3.85, -0.86, 1.42], [-3.44, 4.63, 1.62], [4.45, 3.05, 4.7]], [[-4.8, -3.52, 2.31], [4.02, 1.27, -4.0], [3.36, 2.29, -3.28], [-1.29, -4.13, -1.57], [1.09, 2.92, -2.22]]), 3.671266811333658)


def test_06_random_valid_case():
    _close(solve([[3.99, 2.6, -4.77], [-3.86, 0.86, 2.47], [0.56, 0.51, -1.66], [0.74, 3.86, 4.79]], [[-4.51, 2.19, -1.74], [-4.75, -1.2, -4.62], [1.03, -4.57, 4.02], [-2.89, 4.0, -2.14], [-0.83, 0.27, 1.27]]), 3.2518610056396935)


def test_07_random_valid_case():
    _close(solve([[2.7, -2.93, 1.81], [-4.28, 2.07, -4.94], [-2.59, -0.97, 1.75], [-4.76, 1.03, 1.48]], [[2.09, -0.16, 0.15], [1.07, 0.47, 1.36], [-2.93, -1.68, 1.82], [-3.11, 2.58, -3.0], [2.81, 4.77, -0.3]]), 0.7903163923391695)


def test_08_random_valid_case():
    _close(solve([[0.3, 2.95, 2.42], [-3.69, -3.06, 0.47], [-1.55, -0.48, -3.44], [-2.04, 3.93, 4.65]], [[-4.84, 3.24, -2.9], [3.68, -1.31, -2.32], [4.74, 4.99, -2.22], [2.02, 3.85, 2.51], [-2.51, 0.9, 1.27]]), 1.9433218981939147)


def test_09_random_valid_case():
    _close(solve([[1.86, 4.1, 1.29], [2.28, 1.68, -1.62], [-1.24, 1.35, 2.82], [-3.56, -4.59, -0.89]], [[-3.55, 1.79, -3.33], [-2.85, -1.7, 1.52], [0.48, -4.83, -2.89], [3.45, 0.66, -0.33], [4.33, -3.22, 4.28]]), 2.0182665829864996)


def test_10_random_valid_case():
    _close(solve([[1.55, 4.77, 2.78], [1.34, -0.22, 0.34], [-4.11, 4.84, -1.77], [-2.14, 1.72, -3.78]], [[2.05, -2.0, -1.08], [3.67, -0.58, -2.2], [2.17, -1.59, 1.39], [2.6, -1.08, -0.36], [-3.77, -4.98, 2.72]]), 1.6784516674602221)


def test_11_random_valid_case():
    _close(solve([[-0.26, -2.4, 0.45], [0.38, 2.74, -1.5], [-1.45, 2.77, 2.04], [0.22, -2.03, 2.22]], [[-2.44, 1.11, 2.15], [-2.07, -4.07, -2.81], [-3.89, 3.49, 3.26], [4.8, -3.88, -1.75], [-3.75, 4.99, -4.69]]), 1.9359235522096423)


def test_12_random_valid_case():
    _close(solve([[2.63, 0.8, -4.45], [3.29, 0.16, -3.41], [2.62, -1.52, -4.21], [-2.04, 1.85, -1.22]], [[3.45, -1.4, 1.86], [-4.4, 4.32, -3.85], [-0.67, -0.25, 0.43], [-4.6, -3.64, -2.87], [-4.26, 3.97, -1.57]]), 3.001566257806081)
