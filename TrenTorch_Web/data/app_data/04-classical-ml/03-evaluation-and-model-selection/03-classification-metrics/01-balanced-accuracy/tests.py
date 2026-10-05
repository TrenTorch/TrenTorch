"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

balanced_accuracy = load_solution(__file__).balanced_accuracy


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_perfect_predictions_score_one():
    y = np.array([0, 1, 1, 0, 2])
    assert np.isclose(balanced_accuracy(y, y), 1.0)


def test_always_predicting_the_majority_class_is_penalized():
    y_true = np.array([0, 0, 0, 1])
    y_pred = np.array([0, 0, 0, 0])
    # recall 0 is 1.0, recall 1 is 0.0, so the mean is 0.5 (accuracy would be 0.75)
    assert np.isclose(balanced_accuracy(y_true, y_pred), 0.5)


def test_each_class_counts_equally_regardless_of_size():
    y_true = np.array([0] * 8 + [1] * 2)
    y_pred = np.array([0] * 8 + [0, 1])
    # recall 0 = 1.0, recall 1 = 0.5
    assert np.isclose(balanced_accuracy(y_true, y_pred), 0.75)


def test_predicted_only_labels_are_ignored():
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 0, 1, 2])
    # class 2 never appears in y_true, so only classes 0 and 1 are averaged:
    # recall 0 is 1.0, recall 1 is 0.5 (one of its two rows was predicted 2)
    assert np.isclose(balanced_accuracy(y_true, y_pred), 0.75)


def test_three_classes_mean_of_three_recalls():
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 1, 1, 1, 2, 0])
    # recalls: 0.5, 1.0, 0.5
    assert np.isclose(balanced_accuracy(y_true, y_pred), 2.0 / 3.0)


def test_result_is_between_zero_and_one():
    rng = np.random.default_rng(0)
    y_true = rng.integers(0, 3, size=50)
    y_pred = rng.integers(0, 3, size=50)
    score = balanced_accuracy(y_true, y_pred)
    assert 0.0 <= score <= 1.0


def test_string_labels_work():
    y_true = np.array(["cat", "cat", "dog"])
    y_pred = np.array(["cat", "dog", "dog"])
    # recalls: cat 0.5, dog 1.0
    assert np.isclose(balanced_accuracy(y_true, y_pred), 0.75)


def test_label_renaming_does_not_change_the_score():
    y_true = np.array([0, 0, 1, 1, 1])
    y_pred = np.array([0, 1, 1, 1, 0])
    renamed_true = np.array([5, 5, 9, 9, 9])
    renamed_pred = np.array([5, 9, 9, 9, 5])
    assert np.isclose(balanced_accuracy(y_true, y_pred), balanced_accuracy(renamed_true, renamed_pred))


def test_length_mismatch_raises():
    assert _raises_value_error(balanced_accuracy, np.array([0, 1]), np.array([0]))


def test_empty_input_raises():
    assert _raises_value_error(balanced_accuracy, np.array([]), np.array([]))


def test_returns_a_python_float():
    assert isinstance(balanced_accuracy(np.array([0, 1]), np.array([0, 1])), float)


def test_does_not_modify_inputs():
    y_true = np.array([0, 1, 1])
    y_pred = np.array([0, 0, 1])
    before_true, before_pred = y_true.copy(), y_pred.copy()
    balanced_accuracy(y_true, y_pred)
    assert np.array_equal(y_true, before_true)
    assert np.array_equal(y_pred, before_pred)


def test_all_wrong_scores_zero():
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([1, 1, 0, 0])
    assert np.isclose(balanced_accuracy(y_true, y_pred), 0.0)
