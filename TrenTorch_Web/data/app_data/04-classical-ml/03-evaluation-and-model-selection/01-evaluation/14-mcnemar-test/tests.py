"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

mcnemar_statistic = load_solution(__file__).mcnemar_statistic


def _build(b, c, both=5, neither=3):
    # b samples only A gets right, c samples only B gets right.
    y = np.zeros(b + c + both + neither, dtype=int)
    pa = y.copy()
    pb = y.copy()
    i = 0
    for _ in range(b):
        pb[i] = 1
        i += 1
    for _ in range(c):
        pa[i] = 1
        i += 1
    for _ in range(neither):
        pa[i] = 1
        pb[i] = 1
        i += 1
    return y, pa, pb


def test_hand_computed_value():
    y, pa, pb = _build(10, 3)
    assert np.isclose(mcnemar_statistic(y, pa, pb), (7 - 1) ** 2 / 13)


def test_symmetric_in_the_two_models():
    y, pa, pb = _build(10, 3)
    assert np.isclose(mcnemar_statistic(y, pa, pb), mcnemar_statistic(y, pb, pa))


def test_even_split_is_zero():
    y, pa, pb = _build(6, 6)
    assert mcnemar_statistic(y, pa, pb) == 0.0


def test_no_disagreement_is_zero():
    y = np.array([0, 1, 1, 0])
    assert mcnemar_statistic(y, y, y) == 0.0


def test_identical_wrong_answers_are_ignored():
    y = np.array([0, 0, 0, 0])
    pa = np.array([1, 1, 0, 0])
    pb = np.array([1, 1, 0, 0])
    assert mcnemar_statistic(y, pa, pb) == 0.0


def test_more_lopsided_is_larger():
    y1, a1, b1 = _build(12, 4)
    y2, a2, b2 = _build(16, 0)
    assert mcnemar_statistic(y2, a2, b2) > mcnemar_statistic(y1, a1, b1)


def test_returns_python_float():
    y, pa, pb = _build(4, 1)
    assert isinstance(mcnemar_statistic(y, pa, pb), float)
