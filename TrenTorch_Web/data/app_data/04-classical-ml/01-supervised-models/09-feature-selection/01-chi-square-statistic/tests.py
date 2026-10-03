"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
chi2_statistic = _module.chi2_statistic


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_independent_table_gives_zero():
    x = np.array([0, 0, 1, 1])
    y = np.array([0, 1, 0, 1])
    assert np.isclose(chi2_statistic(x, y), 0.0)


def test_perfectly_separating_table_hand_computed():
    # O = [[3, 0], [0, 3]], E = 1.5 everywhere, so sum((O-E)^2 / E) = 4 * 1.5 = 6
    x = np.array([0, 0, 0, 1, 1, 1])
    y = np.array([0, 0, 0, 1, 1, 1])
    assert np.isclose(chi2_statistic(x, y), 6.0)


def test_label_renaming_does_not_change_the_statistic():
    x = np.array([0, 0, 0, 1, 1, 1])
    y = np.array([0, 0, 0, 1, 1, 1])
    assert np.isclose(chi2_statistic(x, y), chi2_statistic(x, 7 - y))


def test_category_renaming_does_not_change_the_statistic():
    x = np.array([0, 0, 0, 1, 1, 1])
    y = np.array([0, 0, 1, 1, 1, 0])
    assert np.isclose(chi2_statistic(x, y), chi2_statistic(10 * x + 3, y))


def test_statistic_is_nonnegative():
    rng = np.random.default_rng(0)
    x = rng.integers(0, 4, size=50)
    y = rng.integers(0, 3, size=50)
    assert chi2_statistic(x, y) >= 0.0


def test_stronger_association_gives_larger_statistic():
    y = np.array([0] * 10 + [1] * 10)
    weak = np.array([0] * 8 + [1] * 2 + [0] * 2 + [1] * 8)
    strong = np.array([0] * 10 + [1] * 10)
    assert chi2_statistic(strong, y) > chi2_statistic(weak, y)


def test_returns_a_python_float():
    value = chi2_statistic(np.array([0, 1, 1]), np.array([0, 0, 1]))
    assert isinstance(value, float)


def test_matches_an_explicit_loop_on_a_2x3_table():
    x = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
    y = np.array([0, 1, 2, 0, 1, 1, 2, 2, 0, 1])
    O = np.array([[2, 1, 1], [1, 3, 2]], dtype=float)
    N = O.sum()
    rows, cols = O.sum(1), O.sum(0)
    expected = 0.0
    for i in range(2):
        for j in range(3):
            E = rows[i] * cols[j] / N
            expected += (O[i, j] - E) ** 2 / E
    assert np.isclose(chi2_statistic(x, y), expected)


def test_length_mismatch_raises():
    assert _raises_value_error(chi2_statistic, np.array([0, 1]), np.array([0]))


def test_empty_input_raises():
    assert _raises_value_error(chi2_statistic, np.array([], dtype=int), np.array([], dtype=int))


def test_two_dimensional_input_raises():
    assert _raises_value_error(chi2_statistic, np.zeros((2, 2)), np.zeros((2, 2)))


def test_does_not_modify_inputs():
    x = np.array([0, 0, 1, 1, 2])
    y = np.array([0, 1, 0, 1, 1])
    x0, y0 = x.copy(), y.copy()
    chi2_statistic(x, y)
    assert np.array_equal(x, x0) and np.array_equal(y, y0)
