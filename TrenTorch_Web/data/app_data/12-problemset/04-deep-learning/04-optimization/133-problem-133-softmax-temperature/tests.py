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
    _close(solve([1.0, 2.0, 3.0], 1.0), np.array([0.09003057317038046, 0.24472847105479764, 0.6652409557748218]))


def test_02_readme_example_2():
    _close(solve([1.0, 2.0, 3.0], 0.5), np.array([0.015876239976466765, 0.11731042782619838, 0.8668133321973349]))


def test_03_readme_example_3():
    _close(solve([1.0, 2.0, 3.0], 100.0), np.array([0.33000561097102177, 0.33332222249999355, 0.3366721665289847]))


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], 1.0)


def test_05_random_valid_case_1():
    _close(solve([2.44, 3.26, 0.1, 2.91, 0.99, 2.95], 3.53), np.array([0.1742815165212649, 0.2198546223476008, 0.08981772908943968, 0.19910182529718423, 0.11557353919354887, 0.20137076755096145]))


def test_06_random_valid_case_2():
    _close(solve([3.35, 1.73, 2.91, 2.21, 2.03, 0.03], 1.81), np.array([0.29695954265996327, 0.1213365737344222, 0.2328750367826331, 0.15818443389323503, 0.1432102945943541, 0.0474341183353923]))


def test_07_random_valid_case_3():
    _close(solve([0.2, 0.51, 3.75, 0.82, -2.84, 2.07], 2.18), np.array([0.08941648117822416, 0.10308015126905296, 0.4556593019358202, 0.11883175725146408, 0.02217154268528576, 0.2108407656801529]))


def test_08_random_valid_case_4():
    _close(solve([1.38, 4.65, -0.54, 2.15, 1.7, 2.46], 0.81), np.array([0.015239926641823822, 0.8634670806990937, 0.0014241118643755957, 0.03943035774131366, 0.02262330263497943, 0.05781522041841386]))


def test_09_random_valid_case_5():
    _close(solve([4.21, 2.29, 4.37, 4.64, -3.25, 3.41], 2.82), np.array([0.21962261685117537, 0.11116989665446096, 0.23244375554094243, 0.25579925199496156, 0.01558829987016429, 0.16537617908829533]))


def test_10_random_valid_case_6():
    _close(solve([1.59, 3.99, -1.38, 3.73, -3.07, 0.83], 2.6), np.array([0.1423139939726276, 0.3582076208041709, 0.04540980946833522, 0.3241196587292501, 0.02370599925646679, 0.10624291776914951]))


def test_11_random_valid_case_7():
    _close(solve([-0.37, 2.58, 3.63, 0.49, 0.41, -4.0], 3.17), np.array([0.10023327057489406, 0.25419445482285935, 0.3540116521250611, 0.1314719539070068, 0.12819556602976032, 0.031893102540418335]))


def test_12_random_valid_case_8():
    _close(solve([1.27, 3.81, -3.3, 2.95, -3.98, 3.22], 0.74), np.array([0.017991448203024143, 0.5568684174288301, 3.741142535245108e-05, 0.17419351134859465, 1.4925292089247786e-05, 0.25089428630210936]))
