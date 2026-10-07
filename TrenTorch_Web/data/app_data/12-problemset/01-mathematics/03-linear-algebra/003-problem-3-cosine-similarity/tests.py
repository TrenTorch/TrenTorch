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
    _close(solve([1.0, 0.0], [1.0, 1.0]), 0.7071067811865475)


def test_02_readme_example_2():
    _close(solve([1.0, 2.0], [-1.0, -2.0]), -0.9999999999999998)


def test_03_random_valid_case_1():
    _close(solve([-0.5, 2.93, 0.06, 0.73, 1.5], [0.94, -0.08, 1.78, -3.37, 4.9]), 0.20052722331100273)


def test_04_random_valid_case_2():
    _close(solve([-4.38, 3.86, 0.75, 1.9, -3.45], [2.19, 0.87, 0.5, -0.96, 4.93]), -0.6258721840559637)


def test_05_random_valid_case_3():
    _close(solve([2.19, -4.35, 2.43, 0.31, 0.28], [-3.52, 0.7, -4.97, 1.3, 4.83]), -0.48797375921350294)


def test_06_random_valid_case_4():
    _close(solve([-4.04, 4.6, -1.06, 2.15, 3.22], [3.37, 3.26, -0.73, 4.18, 3.28]), 0.416154754715801)


def test_07_random_valid_case_5():
    _close(solve([0.95, -3.28, -3.62, 4.8, -3.51], [-0.1, 2.2, 4.58, 0.38, -3.96]), -0.16319751859910833)


def test_08_random_valid_case_6():
    _close(solve([-3.4, -3.8, 3.2, -3.58, -1.59], [-4.55, 1.22, 4.98, -3.64, 0.67]), 0.692302954622797)


def test_09_random_valid_case_7():
    _close(solve([-4.66, -2.02, 1.64, -1.56, -4.0], [-0.79, 0.7, 2.69, -4.58, 4.83]), -0.11057714126534554)


def test_10_random_valid_case_8():
    _close(solve([3.33, 4.52, -1.61, 2.65, -4.35], [2.47, 0.23, -1.17, 3.46, -3.92]), 0.8167110384869543)


def test_11_random_valid_case_9():
    _close(solve([0.94, -4.77, -1.24, 4.99, -3.07], [3.29, 4.21, 3.02, 1.88, -4.03]), 0.017436827543546977)


def test_12_random_valid_case_10():
    _close(solve([1.65, -3.98, -3.59, 1.61, -2.56], [4.2, 0.62, -0.87, -0.9, -4.92]), 0.44423299498815605)
