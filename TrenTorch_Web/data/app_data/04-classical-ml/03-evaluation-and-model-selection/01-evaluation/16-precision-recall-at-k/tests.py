"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

precision_at_k = load_solution(__file__).precision_at_k
recall_at_k = load_solution(__file__).recall_at_k

RANKED = ["a", "b", "c", "d", "e"]
RELEVANT = {"a", "c", "z"}


def test_precision_hand_values():
    assert np.isclose(precision_at_k(RANKED, RELEVANT, 1), 1.0)
    assert np.isclose(precision_at_k(RANKED, RELEVANT, 3), 2 / 3)
    assert np.isclose(precision_at_k(RANKED, RELEVANT, 5), 2 / 5)


def test_recall_hand_values():
    assert np.isclose(recall_at_k(RANKED, RELEVANT, 1), 1 / 3)
    assert np.isclose(recall_at_k(RANKED, RELEVANT, 3), 2 / 3)
    assert np.isclose(recall_at_k(RANKED, RELEVANT, 5), 2 / 3)


def test_short_list_is_penalised_in_precision():
    assert np.isclose(precision_at_k(["a"], {"a"}, 4), 0.25)


def test_k_larger_than_list_is_safe():
    assert np.isclose(recall_at_k(RANKED, RELEVANT, 100), 2 / 3)


def test_no_relevant_items():
    assert recall_at_k(RANKED, set(), 3) == 0.0
    assert precision_at_k(RANKED, set(), 3) == 0.0


def test_non_positive_k():
    assert precision_at_k(RANKED, RELEVANT, 0) == 0.0
    assert recall_at_k(RANKED, RELEVANT, -1) == 0.0


def test_recall_never_decreases_with_k():
    values = [recall_at_k(RANKED, RELEVANT, k) for k in range(1, 6)]
    assert values == sorted(values)


def test_accepts_list_or_set_for_relevant():
    assert precision_at_k(RANKED, ["a", "c"], 3) == precision_at_k(RANKED, {"a", "c"}, 3)


def test_returns_python_floats():
    assert isinstance(precision_at_k(RANKED, RELEVANT, 2), float)
    assert isinstance(recall_at_k(RANKED, RELEVANT, 2), float)
