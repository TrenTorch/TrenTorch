"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

weighted_majority_vote = load_solution(__file__).weighted_majority_vote


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _preds():
    return np.array([
        [0, 1, 2],
        [0, 1, 1],
        [1, 1, 2],
    ])


def test_equal_weights_give_plain_majority():
    out = weighted_majority_vote(_preds(), np.ones(3))
    assert out.tolist() == [0, 1, 2]


def test_one_heavy_classifier_overrides_the_others():
    out = weighted_majority_vote(_preds(), np.array([0.1, 0.1, 5.0]))
    assert out.tolist() == [1, 1, 2]


def test_zero_weight_removes_a_classifier_and_ties_break_low():
    out = weighted_majority_vote(_preds(), np.array([0.0, 1.0, 1.0]))
    assert out.tolist() == [0, 1, 1]


def test_ties_go_to_the_smaller_label():
    P = np.array([[0], [1]])
    assert weighted_majority_vote(P, np.array([1.0, 1.0])).tolist() == [0]


def test_output_length_is_number_of_samples():
    out = weighted_majority_vote(_preds(), np.ones(3))
    assert out.shape == (3,)


def test_output_is_integer():
    out = weighted_majority_vote(_preds(), np.ones(3))
    assert np.issubdtype(out.dtype, np.integer)


def test_scaling_all_weights_does_not_change_the_vote():
    a = weighted_majority_vote(_preds(), np.array([0.2, 0.5, 0.3]))
    b = weighted_majority_vote(_preds(), np.array([2.0, 5.0, 3.0]))
    assert np.array_equal(a, b)


def test_negative_weight_raises():
    assert _raises_value_error(weighted_majority_vote, _preds(), np.array([1.0, -1.0, 1.0]))


def test_all_zero_weights_raise():
    assert _raises_value_error(weighted_majority_vote, _preds(), np.zeros(3))


def test_weight_count_mismatch_raises():
    assert _raises_value_error(weighted_majority_vote, _preds(), np.ones(2))


def test_does_not_modify_inputs():
    P = _preds()
    w = np.array([0.2, 0.5, 0.3])
    P0, w0 = P.copy(), w.copy()
    weighted_majority_vote(P, w)
    assert np.array_equal(P, P0) and np.array_equal(w, w0)
