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
    _close(solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 1.0]), np.array([3.0, 7.0]))


def test_02_readme_example_2():
    _close(solve([[0.0, 1.0, 0.0]], [5.0, 6.0, 7.0]), np.array([6.0]))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([[1.0, 2.0]], [1.0])


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([[1.0, 2.0], [3.0, 4.0]], [])


def test_05_random_valid_case_1():
    _close(solve([[-1.74, 1.25, 1.48], [1.25, 2.39, -4.0], [3.97, 4.0, 1.88], [2.86, 0.31, -0.75]], [2.58, -2.23, 4.65]), np.array([-0.3946999999999994, -20.704700000000003, 10.064600000000002, 3.1999999999999997]))


def test_06_random_valid_case_2():
    _close(solve([[4.12, -1.13, -3.39], [3.33, -3.69, -2.89], [-3.6, 0.35, -0.79], [4.5, 2.98, 4.43]], [0.73, 0.4, 4.55]), np.array([-12.8689, -12.1946, -6.0825, 24.633499999999998]))


def test_07_random_valid_case_3():
    _close(solve([[1.37, -0.58, 4.18], [2.38, 0.85, 2.88], [2.83, 2.43, -3.28], [2.43, -2.23, -2.38]], [1.9, 4.33, -0.44]), np.array([-1.7475999999999998, 6.935299999999999, 17.342100000000002, -3.9917000000000007]))


def test_08_random_valid_case_4():
    _close(solve([[-3.92, -0.73, 3.99], [-4.51, 4.5, 3.28], [-4.64, 1.91, 1.8], [0.17, 3.42, -4.46]], [2.89, -3.45, -1.7]), np.array([-15.593300000000003, -34.1349, -23.059099999999997, -3.725699999999999]))


def test_09_random_valid_case_5():
    _close(solve([[-0.62, 3.2, 4.18], [-3.84, -3.1, -2.42], [0.43, -0.85, 2.84], [-4.5, -3.39, -4.78]], [3.04, 0.18, 2.43]), np.array([8.8486, -18.1122, 8.0554, -25.9056]))


def test_10_random_valid_case_6():
    _close(solve([[-1.07, 2.41, -3.88], [1.54, -0.6, 3.0], [-4.57, 0.88, -4.94], [-4.87, 4.85, -3.35]], [0.23, -1.47, 3.9]), np.array([-18.9208, 12.9362, -21.6107, -21.3146]))


def test_11_random_valid_case_7():
    _close(solve([[-0.46, 1.79, -0.77], [-2.44, 4.41, -1.88], [-2.01, -4.6, 2.75], [-1.97, -2.03, 3.9]], [-1.6, 0.63, 0.66]), np.array([1.3555000000000001, 5.4415, 2.133, 4.4471]))


def test_12_random_valid_case_8():
    _close(solve([[3.38, -1.35, 3.57], [-3.95, 2.52, 2.84], [1.94, 2.96, -4.09], [-0.04, -0.95, -2.24]], [3.54, -0.23, 3.1]), np.array([23.3427, -5.7585999999999995, -6.4922, -6.867100000000001]))
