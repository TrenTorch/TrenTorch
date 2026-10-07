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
    _close(solve([1.0, -1.0, 2.0], [1.0, -1.0, -1.0]), 1.0)


def test_02_readme_example_2():
    _close(solve([1, -1], [3.0, -0.5]), 0.25)


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], [1.0, -1.0, -1.0])


def test_04_random_valid_case_1():
    _close(solve([1, 1, -1, 1, 1, 1, 1, -1, 1], [3.34, 2.5, -3.87, 0.79, 3.83, -2.76, 1.5, -2.89, 0.15]), 0.5355555555555555)


def test_05_random_valid_case_2():
    _close(solve([1, 1, 1, -1, 1, 1, -1, -1, -1], [3.5, 4.4, 1.21, 0.33, 4.02, -2.77, 4.15, -3.22, 3.86]), 1.6788888888888889)


def test_06_random_valid_case_3():
    _close(solve([-1, 1, 1, 1, 1, 1, -1, -1, -1], [0.92, 0.61, -2.4, 3.33, 4.02, 4.82, -3.0, -4.66, 4.29]), 1.2222222222222223)


def test_07_random_valid_case_4():
    _close(solve([-1, 1, 1, 1, -1, 1, -1, 1, 1], [3.57, 2.96, 0.22, -4.2, -0.05, 3.71, 1.34, 2.96, -3.96]), 2.088888888888889)


def test_08_random_valid_case_5():
    _close(solve([1, -1, 1, 1, 1, 1, -1, 1, 1], [-3.37, -3.08, 1.92, -4.5, 2.13, 3.29, -1.77, -3.13, 4.27]), 1.5555555555555556)


def test_09_random_valid_case_6():
    _close(solve([-1, 1, 1, 1, 1, 1, -1, 1, -1], [0.81, -2.73, -0.97, 4.19, -1.0, 0.15, -0.55, 4.36, 4.57]), 1.8199999999999998)


def test_10_random_valid_case_7():
    _close(solve([1, -1, 1, 1, 1, -1, 1, -1, 1], [3.91, 2.94, 4.33, 4.55, -1.63, -0.5, -0.85, -1.48, -2.36]), 1.3644444444444443)


def test_11_random_valid_case_8():
    _close(solve([-1, 1, -1, -1, -1, -1, -1, 1, 1], [-3.62, 3.33, -3.29, 4.85, 0.13, 4.2, 3.8, 1.43, -1.28]), 2.1399999999999997)


def test_12_random_valid_case_9():
    _close(solve([-1, 1, -1, -1, -1, -1, 1, -1, 1], [-4.1, 3.35, 2.19, 2.35, 0.19, -1.08, -2.8, 1.21, 0.28]), 1.6066666666666665)
