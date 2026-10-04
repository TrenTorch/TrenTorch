"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
import pytest

choice_scores = _module.choice_scores
pick_choice = _module.pick_choice
multiple_choice_accuracy = _module.multiple_choice_accuracy


def test_1_sum_mode_returns_the_log_probabilities():
    assert np.allclose(choice_scores([-3.0, -5.0], [1, 4], "sum"), [-3.0, -5.0])


def test_2_mean_mode_divides_by_length():
    assert np.allclose(choice_scores([-3.0, -6.0], [1, 4], "mean"), [-3.0, -1.5])


def test_3_modes_can_disagree_on_the_same_candidates():
    lp, ln = [-3.0, -6.0], [1, 4]
    assert pick_choice(lp, ln, "sum") == 0
    assert pick_choice(lp, ln, "mean") == 1


def test_4_ties_go_to_the_lowest_index():
    assert pick_choice([-2.0, -2.0, -5.0], [1, 1, 1], "sum") == 0


def test_5_unknown_mode_raises():
    with pytest.raises(ValueError):
        choice_scores([-1.0], [1], "max")


def test_6_accuracy_hand_computed():
    lps = [[-1.0, -4.0], [-5.0, -2.0], [-3.0, -3.5]]
    lens = [[1, 1], [1, 1], [1, 1]]
    assert np.isclose(multiple_choice_accuracy(lps, lens, [0, 1, 1], "sum"), 2 / 3)


def test_7_accuracy_depends_on_normalization_and_inputs_untouched():
    lp = np.array([-3.0, -6.0])
    ln = np.array([1, 4])
    s1, s2 = lp.copy(), ln.copy()
    a_sum = multiple_choice_accuracy([lp], [ln], [1], "sum")
    a_mean = multiple_choice_accuracy([lp], [ln], [1], "mean")
    assert a_sum == 0.0 and a_mean == 1.0
    assert np.array_equal(lp, s1) and np.array_equal(ln, s2)
