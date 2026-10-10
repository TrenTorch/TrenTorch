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
    _close(solve([('a', 1.0), ('b', 2.0), ('a', 1.0)]), {'a': 0.5, 'b': 0.5})


def test_02_singleton_boundary():
    _close(solve([('a', 1.0)]), {'a': 1.0})


def test_03_empty_or_degenerate_input():
    _close(solve([]), {})


def test_04_random_valid_case():
    _close(solve([('a', 0.02), ('b', 0.29), ('c', 0.28), ('c', 0.53), ('c', 0.2), ('a', 0.7), ('a', 0.56), ('b', 0.27)]), {'a': 0.44912280701754387, 'b': 0.19649122807017544, 'c': 0.3543859649122807})


def test_05_random_valid_case():
    _close(solve([('a', 0.35), ('a', 0.31), ('c', 0.71), ('c', 0.78), ('c', 0.03), ('c', 0.26), ('a', 0.2), ('b', 0.4)]), {'a': 0.28289473684210525, 'c': 0.5855263157894738, 'b': 0.13157894736842107})


def test_06_random_valid_case():
    _close(solve([('c', 0.92), ('c', 0.69), ('a', 0.19), ('a', 0.9), ('b', 0.05), ('b', 0.8), ('c', 0.39), ('b', 0.18)]), {'c': 0.4854368932038835, 'a': 0.2645631067961165, 'b': 0.25})


def test_07_random_valid_case():
    _close(solve([('b', 0.13), ('b', 0.2), ('a', 0.78), ('a', 0.18), ('b', 0.12), ('a', 0.84), ('c', 0.62), ('c', 0.6)]), {'b': 0.12968299711815562, 'a': 0.5187319884726225, 'c': 0.3515850144092219})


def test_08_random_valid_case():
    _close(solve([('b', 0.54), ('b', 0.99), ('b', 0.41), ('a', 0.19), ('b', 0.45), ('a', 0.88), ('a', 0.6), ('c', 0.22)]), {'b': 0.5584112149532711, 'a': 0.3901869158878504, 'c': 0.0514018691588785})


def test_09_random_valid_case():
    _close(solve([('c', 0.71), ('a', 0.09), ('a', 0.09), ('c', 0.65), ('a', 0.97), ('a', 0.17), ('a', 0.85), ('a', 0.3)]), {'c': 0.35509138381201044, 'a': 0.6449086161879896})


def test_10_random_valid_case():
    _close(solve([('c', 0.22), ('c', 0.5), ('c', 0.98), ('a', 0.34), ('a', 0.92), ('c', 0.64), ('a', 0.32), ('b', 0.77)]), {'c': 0.4989339019189766, 'a': 0.33688699360341157, 'b': 0.16417910447761197})


def test_11_random_valid_case():
    _close(solve([('b', 0.62), ('c', 0.23), ('b', 0.02), ('c', 0.4), ('c', 0.15), ('c', 0.04), ('a', 0.39), ('a', 0.47)]), {'b': 0.2758620689655173, 'c': 0.353448275862069, 'a': 0.3706896551724138})


def test_12_random_valid_case():
    _close(solve([('b', 0.87), ('b', 0.91), ('c', 0.84), ('a', 0.42), ('c', 0.05), ('b', 0.46), ('c', 0.63), ('c', 0.4)]), {'b': 0.48908296943231444, 'c': 0.4192139737991266, 'a': 0.09170305676855894})
