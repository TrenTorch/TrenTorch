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
    _close(solve([3, 4], 2), np.array([1.2000000000000002, 1.6]))


def test_02_readme_example_2():
    _close(solve([0.3, 0.4], 1.0), np.array([0.3, 0.4]))


def test_03_random_valid_case_1():
    _close(solve([0.34, 1.13, 2.6, -0.83, 3.18], 3.09), np.array([0.24131774014104676, 0.8020266069393611, 1.8453709540197691, -0.5890991891678493, 2.2570306283780255]))


def test_04_random_valid_case_2():
    _close(solve([3.18, 2.43, 0.17, 2.12, 1.54], 1.57), np.array([1.0430217783160796, 0.797026075883042, 0.055759025884821865, 0.6953478522107197, 0.505111175662504]))


def test_05_random_valid_case_3():
    _close(solve([0.86, -2.37, 3.44, 1.7, 1.39], 4.87), np.array([0.86, -2.37, 3.44, 1.7, 1.39]))


def test_06_random_valid_case_4():
    _close(solve([4.42, 3.82, 2.85, 3.92, -0.96], 4.34), np.array([2.507195712200456, 2.1668524028519776, 1.6166307194052711, 2.2235762877433904, -0.544549294957565]))


def test_07_random_valid_case_5():
    _close(solve([4.48, -1.7, -0.32, -3.6, 3.08], 2.66), np.array([1.7664853906523004, -0.670318116988596, -0.12617752790373574, -1.419497188917027, 1.2144587060734564]))


def test_08_random_valid_case_6():
    _close(solve([-3.54, 3.19, -3.87, 1.9, 3.06], 3.01), np.array([-1.4970795586719716, 1.3490632181253077, -1.636637822615969, 0.8035172772533181, 1.2940857202079756]))


def test_09_random_valid_case_7():
    _close(solve([1.43, -2.55, 3.93, 3.66, 2.63], 1.39), np.array([0.2986245081911999, -0.5325122348864054, 0.8206953267072837, 0.7643116783075466, 0.5492185010789201]))


def test_10_random_valid_case_8():
    _close(solve([3.17, 3.8, -3.82, 3.13, -0.18], 4.95), np.array([2.243690586875248, 2.6895975489356285, -2.703753325508974, 2.2153790337285573, -0.12740198916010873]))


def test_11_random_valid_case_9():
    _close(solve([-1.51, 0.46, 2.18, 1.12, -0.44], 1.14), np.array([-0.5838744101774133, 0.17786902561696036, 0.8429445127064643, 0.4330724101978165, -0.17013558972057077]))


def test_12_random_valid_case_10():
    _close(solve([2.18, -1.82, 2.61, 0.16, -3.77], 4.49), np.array([1.814017423469342, -1.5144549131716525, 2.1718281996582487, 0.13313889346563978, -3.137085177284137]))
