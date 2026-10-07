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
    _close(solve(1), np.array(0.7310585786300049))


def test_02_parameter_nudge():
    _close(solve(2), np.array(0.8807970779778823))


def test_03_random_valid_case():
    _close(solve([586.17, 457.39, -29.68, 702.5, 540.8, 740.45]), np.array([1.0, 1.0, 1.2886642398576016e-13, 1.0, 1.0, 1.0]))


def test_04_random_valid_case():
    _close(solve([527.0, 249.04, 698.44, -728.43, 44.18, 638.57]), np.array([1.0, 1.0, 1.0, 4.4347644e-317, 1.0, 1.0]))


def test_05_random_valid_case():
    _close(solve([-397.94, 356.68, 98.1, -591.45, 492.95, 208.09]), np.array([1.5026362837457881e-173, 1.0, 1.0, 1.3693948124006387e-257, 1.0, 1.0]))


def test_06_random_valid_case():
    _close(solve([-58.29, 610.23, -140.39, 278.97, 786.61, 669.9]), np.array([4.841441068534909e-26, 1.0, 1.070034266403068e-61, 1.0, 1.0, 1.0]))


def test_07_random_valid_case():
    _close(solve([-6.0, 592.51, 178.13, -193.49, -315.14, -57.32]), np.array([0.0024726231566347748, 1.0, 1.0, 9.297382458742916e-85, 1.3691056824978965e-137, 1.2771452642031297e-25]))


def test_08_random_valid_case():
    _close(solve([771.54, -555.53, 415.05, 706.62, 770.09, 496.76]), np.array([1.0, 5.449874084022014e-242, 1.0, 1.0, 1.0, 1.0]))


def test_09_random_valid_case():
    _close(solve([-280.8, -470.08, 74.94, -300.71, 374.88, -21.69]), np.array([1.122301340289045e-122, 7.028294433365812e-205, 1.0, 2.5310827667161683e-131, 1.0, 3.8032308514414204e-10]))


def test_10_random_valid_case():
    _close(solve([-32.33, 358.07, 590.55, -549.02, 119.55, 612.55]), np.array([9.104569177354697e-15, 1.0, 1.0, 3.661369382191021e-239, 1.0, 1.0]))


def test_11_random_valid_case():
    _close(solve([758.95, 14.42, 497.58, -714.17, -592.14, -95.76]), np.array([1.0, 0.9999994536469982, 1.0, 6.916873914821e-311, 6.868556670034015e-258, 2.5820248217256547e-42]))


def test_12_random_valid_case():
    _close(solve([351.15, 694.15, 357.21, -512.62, 673.83, -157.68]), np.array([1.0, 1.0, 1.0, 2.3548469540032216e-223, 1.0, 3.314714235951239e-69]))
