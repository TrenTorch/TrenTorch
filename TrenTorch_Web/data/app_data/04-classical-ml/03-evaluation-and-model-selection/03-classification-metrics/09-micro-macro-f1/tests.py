"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
f1_micro = _module.f1_micro
f1_macro = _module.f1_macro


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


Y_TRUE = np.array([0, 0, 1, 1, 2, 2])
Y_PRED = np.array([0, 1, 1, 1, 2, 0])


def test_micro_equals_accuracy_for_single_label_data():
    # 4 of 6 correct
    assert np.isclose(f1_micro(Y_TRUE, Y_PRED), 4.0 / 6.0)


def test_macro_worked_example():
    # per-class F1: class 0 = 0.5, class 1 = 0.8, class 2 = 2/3
    assert np.isclose(f1_macro(Y_TRUE, Y_PRED), (0.5 + 0.8 + 2.0 / 3.0) / 3.0)


def test_perfect_predictions_score_one_for_both():
    assert np.isclose(f1_micro(Y_TRUE, Y_TRUE), 1.0)
    assert np.isclose(f1_macro(Y_TRUE, Y_TRUE), 1.0)


def test_macro_punishes_ignoring_a_rare_class_more_than_micro():
    y_true = np.array([0] * 9 + [1])
    y_pred = np.zeros(10, dtype=int)
    # micro: 9 of 10 correct; macro: class 1 has F1 0, class 0 has F1 about 0.947
    assert f1_micro(y_true, y_pred) > f1_macro(y_true, y_pred)


def test_class_never_predicted_contributes_zero_to_macro():
    y_true = np.array([0, 1])
    y_pred = np.array([0, 0])
    # class 0: tp 1, fp 1, fn 0 -> 2/3; class 1: all zero -> 0
    assert np.isclose(f1_macro(y_true, y_pred), (2.0 / 3.0) / 2.0)


def test_micro_is_within_zero_and_one():
    rng = np.random.default_rng(11)
    y_true = rng.integers(0, 4, size=60)
    y_pred = rng.integers(0, 4, size=60)
    assert 0.0 <= f1_micro(y_true, y_pred) <= 1.0


def test_macro_is_within_zero_and_one():
    rng = np.random.default_rng(12)
    y_true = rng.integers(0, 4, size=60)
    y_pred = rng.integers(0, 4, size=60)
    assert 0.0 <= f1_macro(y_true, y_pred) <= 1.0


def test_micro_matches_accuracy_on_random_labels():
    rng = np.random.default_rng(13)
    y_true = rng.integers(0, 5, size=80)
    y_pred = rng.integers(0, 5, size=80)
    assert np.isclose(f1_micro(y_true, y_pred), np.mean(y_true == y_pred))


def test_string_labels_work():
    y_true = np.array(["a", "b", "b"])
    y_pred = np.array(["a", "b", "a"])
    assert np.isclose(f1_micro(y_true, y_pred), 2.0 / 3.0)


def test_label_renaming_does_not_change_either_score():
    mapping = np.array([7, 8, 9])  # 0 -> 7, 1 -> 8, 2 -> 9
    renamed_true = mapping[Y_TRUE]
    renamed_pred = mapping[Y_PRED]
    assert np.isclose(f1_micro(Y_TRUE, Y_PRED), f1_micro(renamed_true, renamed_pred))
    assert np.isclose(f1_macro(Y_TRUE, Y_PRED), f1_macro(renamed_true, renamed_pred))


def test_length_mismatch_raises():
    assert _raises_value_error(f1_micro, np.array([0, 1]), np.array([0]))
    assert _raises_value_error(f1_macro, np.array([0, 1]), np.array([0]))


def test_empty_input_raises():
    assert _raises_value_error(f1_micro, np.array([]), np.array([]))
    assert _raises_value_error(f1_macro, np.array([]), np.array([]))


def test_does_not_modify_inputs():
    y_true = Y_TRUE.copy()
    y_pred = Y_PRED.copy()
    f1_micro(y_true, y_pred)
    f1_macro(y_true, y_pred)
    assert np.array_equal(y_true, Y_TRUE)
    assert np.array_equal(y_pred, Y_PRED)
