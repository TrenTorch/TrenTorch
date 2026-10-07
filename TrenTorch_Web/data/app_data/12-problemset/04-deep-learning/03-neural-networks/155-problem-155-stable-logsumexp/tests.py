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
    _close(solve([1000.0, 1001.0]), 1001.3132616875182)


def test_02_readme_example_2():
    _close(solve([0.0, 0.0]), 0.6931471805599453)


def test_03_readme_example_3():
    _close(solve([-1000.0, -1000.0]), -999.3068528194401)


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([])


def test_05_random_valid_case_1():
    _close(solve([1.48, 2.66, -1.0, 2.45, 4.53, 3.98, 1.98]), 5.215825574836552)


def test_06_random_valid_case_2():
    _close(solve([2.09, 4.97, -4.73, 4.47, 0.7, -3.76, 4.7]), 5.862100348001003)


def test_07_random_valid_case_3():
    _close(solve([-3.86, 4.1, -1.4, 0.58, -1.13, 3.79, -3.2]), 4.67296141191575)


def test_08_random_valid_case_4():
    _close(solve([0.51, 3.13, -2.51, 2.34, 0.92, 1.48, -1.45]), 3.740963755657644)


def test_09_random_valid_case_5():
    _close(solve([-4.87, -4.9, -1.88, -0.85, -2.27, 1.57, 4.3]), 4.372037901209763)


def test_10_random_valid_case_6():
    _close(solve([-4.68, 3.75, -3.01, 4.12, 4.84, -4.33, 1.42]), 5.4585574738704965)


def test_11_random_valid_case_7():
    _close(solve([3.81, 1.83, -2.99, -0.85, 3.03, -2.92, 3.02]), 4.5337223663059065)


def test_12_random_valid_case_8():
    _close(solve([2.56, 0.11, 2.62, -1.37, -4.82, -0.49, -2.85]), 3.3576098802904704)
