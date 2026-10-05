"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
pick_pseudo_labels = _module.pick_pseudo_labels


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_only_view_a_confident_uses_its_label():
    idx, lab = pick_pseudo_labels(np.array([0.9]), np.array([1]), np.array([0.2]), np.array([0]), 0.8)
    assert idx.tolist() == [0] and lab.tolist() == [1]


def test_only_view_b_confident_uses_its_label():
    idx, lab = pick_pseudo_labels(np.array([0.2]), np.array([1]), np.array([0.95]), np.array([0]), 0.8)
    assert idx.tolist() == [0] and lab.tolist() == [0]


def test_both_confident_and_agreeing_is_selected():
    idx, lab = pick_pseudo_labels(np.array([0.9]), np.array([2]), np.array([0.9]), np.array([2]), 0.8)
    assert idx.tolist() == [0] and lab.tolist() == [2]


def test_both_confident_but_disagreeing_is_skipped():
    idx, lab = pick_pseudo_labels(np.array([0.9]), np.array([1]), np.array([0.99]), np.array([0]), 0.8)
    assert idx.size == 0 and lab.size == 0


def test_neither_confident_is_skipped():
    idx, _ = pick_pseudo_labels(np.array([0.5]), np.array([1]), np.array([0.4]), np.array([1]), 0.8)
    assert idx.size == 0


def test_threshold_is_inclusive():
    idx, _ = pick_pseudo_labels(np.array([0.8]), np.array([1]), np.array([0.0]), np.array([1]), 0.8)
    assert idx.tolist() == [0]


def test_indices_are_increasing_and_match_labels():
    conf_a = np.array([0.9, 0.1, 0.9, 0.5, 0.2])
    pred_a = np.array([0, 1, 1, 0, 2])
    conf_b = np.array([0.1, 0.95, 0.9, 0.5, 0.3])
    pred_b = np.array([0, 2, 0, 1, 2])
    idx, lab = pick_pseudo_labels(conf_a, pred_a, conf_b, pred_b, 0.8)
    assert idx.tolist() == [0, 1]
    assert lab.tolist() == [0, 2]


def test_mixed_batch_hand_example():
    conf_a = np.array([0.95, 0.85, 0.3])
    pred_a = np.array([3, 1, 0])
    conf_b = np.array([0.9, 0.2, 0.9])
    pred_b = np.array([3, 0, 0])
    idx, lab = pick_pseudo_labels(conf_a, pred_a, conf_b, pred_b, 0.8)
    # Point 0 agrees, point 1 comes from view a, point 2 comes from view b.
    assert idx.tolist() == [0, 1, 2]
    assert lab.tolist() == [3, 1, 0]


def test_empty_input_returns_empty_arrays():
    idx, lab = pick_pseudo_labels(np.array([]), np.array([]), np.array([]), np.array([]), 0.5)
    assert idx.size == 0 and lab.size == 0


def test_inputs_are_not_modified():
    conf_a = np.array([0.9, 0.1])
    before = conf_a.copy()
    pick_pseudo_labels(conf_a, np.array([0, 1]), np.array([0.2, 0.9]), np.array([0, 1]), 0.8)
    assert np.array_equal(conf_a, before)


def test_threshold_zero_raises():
    assert _raises_value_error(pick_pseudo_labels, np.array([0.9]), np.array([0]), np.array([0.9]), np.array([0]), 0.0)


def test_threshold_above_one_raises():
    assert _raises_value_error(pick_pseudo_labels, np.array([0.9]), np.array([0]), np.array([0.9]), np.array([0]), 1.5)


def test_confidence_out_of_range_raises():
    assert _raises_value_error(pick_pseudo_labels, np.array([1.2]), np.array([0]), np.array([0.9]), np.array([0]), 0.5)


def test_length_mismatch_raises():
    assert _raises_value_error(pick_pseudo_labels, np.array([0.9, 0.1]), np.array([0]), np.array([0.9]), np.array([0]), 0.5)
