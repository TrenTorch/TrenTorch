"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
average_precision = _module.average_precision


def test_1_perfect_ranking_is_one():
    assert np.isclose(average_precision([0.9, 0.8, 0.7], [True, True, True], 3), 1.0)


def test_2_all_false_positives_is_zero():
    assert average_precision([0.9, 0.8], [False, False], 2) == 0.0


def test_3_hand_computed_with_a_false_positive_in_the_middle():
    # ranked: TP, FP, TP ; n_gt=2 -> precision [1, .5, 2/3], recall [.5, .5, 1]
    # envelope: p at recall .5 -> 1, at recall 1 -> 2/3 ; AP = .5*1 + .5*(2/3)
    assert np.isclose(average_precision([0.9, 0.8, 0.7], [True, False, True], 2), 0.5 + 0.5 * 2 / 3)


def test_4_missed_ground_truth_caps_recall():
    # one TP found out of 2 ground truths: AP = 0.5 * 1.0
    assert np.isclose(average_precision([0.9], [True], 2), 0.5)


def test_5_scores_not_order_of_input_determine_ranking():
    a = average_precision([0.1, 0.9, 0.5], [True, False, True], 2)
    b = average_precision([0.9, 0.5, 0.1], [False, True, True], 2)
    assert np.isclose(a, b)


def test_6_good_ranking_beats_bad_ranking():
    good = average_precision([0.9, 0.8, 0.2, 0.1], [True, True, False, False], 2)
    bad = average_precision([0.9, 0.8, 0.2, 0.1], [False, False, True, True], 2)
    assert good > bad and np.isclose(good, 1.0)


def test_7_empty_detections_and_inputs_untouched():
    assert average_precision([], [], 3) == 0.0
    s, t = np.array([0.3, 0.9]), np.array([True, False])
    ss, ts = s.copy(), t.copy()
    average_precision(s, t, 1)
    assert np.array_equal(s, ss) and np.array_equal(t, ts)
