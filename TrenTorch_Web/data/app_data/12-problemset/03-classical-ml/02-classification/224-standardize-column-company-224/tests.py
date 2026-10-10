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
    _close(solve([1, 2, 3]), np.array([-1.224744871391589, 0.0, 1.224744871391589]))


def test_02_readme_example_2():
    _close(solve([4.0, 4.0, 4.0]), np.array([0.0, 0.0, 0.0]))


def test_03_random_valid_case_1():
    _close(solve([2.0, 2.0, 2.0]), np.array([0.0, 0.0, 0.0]))


def test_04_random_valid_case_2():
    _close(solve([2.08, 0.8, 1.05, 2.04, 3.12, 3.99, 1.74, -3.09]), np.array([0.31047810892220845, -0.3370363178320511, -0.2105686563566098, 0.2902432830861378, 0.8365835806600443, 1.27669104259458, 0.1384820893156082, -2.304873130389918]))


def test_05_random_valid_case_3():
    _close(solve([-4.37, -0.94, 2.07, 3.1, 0.34, 0.39, 0.3, -3.92]), np.array([-1.6218047757625418, -0.22805836026225523, 0.9950252288502409, 1.413555493563155, 0.2920569201576767, 0.31237392329908026, 0.2758033176445538, -1.4389517474899094]))


def test_06_random_valid_case_4():
    _close(solve([3.31, 0.48, -2.17, 4.07, 4.92, -2.07, 2.96, 1.4]), np.array([0.6731557872937938, -0.44910098916655156, -1.499977475958041, 0.9745392325622966, 1.311612822665227, -1.4603217594753433, 0.5343607796043518, -0.0842683975257326]))


def test_07_random_valid_case_5():
    _close(solve([-4.38, 1.54, 0.41, 3.9, -3.15, -0.64, 0.01, 4.4]), np.array([-1.6148938990825825, 0.4449330618802807, 0.051756631831626, 1.266080296318179, -1.1869230946933391, -0.3135842987445575, -0.08742086553072963, 1.4400521680211233]))


def test_08_random_valid_case_6():
    _close(solve([-3.91, 1.51, 1.62, -1.91, 3.17, -4.74, 3.66, 3.2]), np.array([-1.34641513327338, 0.376741896795503, 0.4117137184389675, -0.710563830664936, 0.9044984779605113, -1.6102934238558841, 1.0602820470995802, 0.9140362474996381]))


def test_09_random_valid_case_7():
    _close(solve([-1.39, -1.0, 4.02, 2.29, 2.44, 3.51, -1.14, 1.02]), np.array([-1.2831483107519157, -1.0913216346835892, 1.3778319906061538, 0.5269085300979357, 0.600688020893446, 1.126981721901419, -1.1601824927593987, -0.09775782530405108]))


def test_10_random_valid_case_8():
    _close(solve([0.87, 2.4, 4.6, -0.23, -1.81, -1.31, -3.88, 1.13]), np.array([0.2630442311300444, 0.8834028802691083, 1.7754218528873704, -0.18296525517908663, -0.8235970627867476, -0.620865478100779, -1.6629058233866576, 0.36846465516674803]))


def test_11_random_valid_case_9():
    _close(solve([2.68, 2.75, 4.09, 1.11, 4.56, 0.41, -3.43, -4.71]), np.array([0.5503447386960575, 0.5723900215050555, 0.9943997209915886, 0.0559005385513879, 1.1424180484234323, -0.16455228953859216, -1.3738935179179113, -1.7770072607110177]))


def test_12_random_valid_case_10():
    _close(solve([3.87, -1.06, 4.52, 2.5, 3.98, 3.51, -1.74, -0.61]), np.array([0.8305760603435869, -1.2180743349003824, 1.10068209622768, 0.26127564624942096, 0.8762863125701256, 0.6809788712385505, -1.5006468032098952, -1.031077848519087]))
