"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

specificity = load_solution(__file__).specificity


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_worked_example():
    y_true = np.array([1, 0, 0, 0, 1, 0])
    y_pred = np.array([1, 1, 0, 0, 0, 0])
    # negatives at 1, 2, 3, 5: predictions 1, 0, 0, 0 -> TN 3, FP 1
    assert np.isclose(specificity(y_true, y_pred), 0.75)


def test_all_negatives_correct_is_one():
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 0, 1, 0])
    assert np.isclose(specificity(y_true, y_pred), 1.0)


def test_all_negatives_flagged_is_zero():
    y_true = np.array([0, 0, 1])
    y_pred = np.array([1, 1, 1])
    assert np.isclose(specificity(y_true, y_pred), 0.0)


def test_positive_argument_swaps_the_negative_class():
    y_true = np.array([1, 0, 0, 0, 1, 0])
    y_pred = np.array([1, 1, 0, 0, 0, 0])
    # with positive=0 the negatives are the rows labeled 1: indices 0 and 4
    # predictions there are 1 and 0 -> TN 1, FP 1
    assert np.isclose(specificity(y_true, y_pred, positive=0), 0.5)


def test_no_negatives_returns_zero():
    y_true = np.array([1, 1, 1])
    y_pred = np.array([1, 0, 1])
    assert specificity(y_true, y_pred) == 0.0


def test_result_stays_in_zero_one():
    rng = np.random.default_rng(2)
    y_true = rng.integers(0, 2, size=60)
    y_pred = rng.integers(0, 2, size=60)
    assert 0.0 <= specificity(y_true, y_pred) <= 1.0


def test_predicting_all_negative_gives_specificity_one():
    y_true = np.array([0, 1, 0, 1, 0])
    y_pred = np.zeros(5, dtype=int)
    assert np.isclose(specificity(y_true, y_pred), 1.0)


def test_only_negative_rows_matter():
    y_true = np.array([1, 1, 0, 0])
    # the positive rows predict 1 and 0 here, which must not affect the score
    assert np.isclose(specificity(y_true, np.array([1, 1, 1, 1])), 0.0)
    assert np.isclose(specificity(y_true, np.array([0, 0, 0, 1])), 0.5)


def test_string_labels_with_explicit_positive():
    y_true = np.array(["spam", "ham", "ham", "spam"])
    y_pred = np.array(["spam", "ham", "spam", "spam"])
    # negatives are the "ham" rows: predictions "ham", "spam" -> TN 1, FP 1
    assert np.isclose(specificity(y_true, y_pred, positive="spam"), 0.5)


def test_length_mismatch_raises():
    assert _raises_value_error(specificity, np.array([0, 1]), np.array([0]))


def test_does_not_modify_inputs():
    y_true = np.array([0, 1, 0])
    y_pred = np.array([0, 1, 1])
    before_true, before_pred = y_true.copy(), y_pred.copy()
    specificity(y_true, y_pred)
    assert np.array_equal(y_true, before_true)
    assert np.array_equal(y_pred, before_pred)


def test_returns_a_python_float():
    assert isinstance(specificity(np.array([0, 1]), np.array([0, 1])), float)


def test_adding_true_negatives_moves_score_toward_one():
    base_true = np.array([0, 0, 1])
    base_pred = np.array([1, 0, 1])
    more_true = np.array([0, 0, 1, 0, 0])
    more_pred = np.array([1, 0, 1, 0, 0])
    assert specificity(more_true, more_pred) > specificity(base_true, base_pred)
