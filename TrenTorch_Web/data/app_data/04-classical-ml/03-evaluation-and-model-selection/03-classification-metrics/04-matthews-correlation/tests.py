"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

matthews_corrcoef = load_solution(__file__).matthews_corrcoef


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


# tp 2, fn 1, fp 1, tn 2 -> (4 - 1) / sqrt(3 * 3 * 3 * 3) = 3 / 9
Y_TRUE = np.array([1, 1, 1, 0, 0, 0])
Y_PRED = np.array([1, 1, 0, 1, 0, 0])


def test_worked_example():
    assert np.isclose(matthews_corrcoef(Y_TRUE, Y_PRED), 1.0 / 3.0)


def test_perfect_predictions_give_one():
    assert np.isclose(matthews_corrcoef(Y_TRUE, Y_TRUE), 1.0)


def test_fully_inverted_predictions_give_minus_one():
    assert np.isclose(matthews_corrcoef(Y_TRUE, 1 - Y_TRUE), -1.0)


def test_constant_predictions_give_zero():
    assert matthews_corrcoef(Y_TRUE, np.ones(6, dtype=int)) == 0.0
    assert matthews_corrcoef(Y_TRUE, np.zeros(6, dtype=int)) == 0.0


def test_constant_truth_gives_zero():
    assert matthews_corrcoef(np.zeros(4, dtype=int), np.array([0, 1, 0, 1])) == 0.0


def test_ignores_label_scale_beyond_the_positive_class():
    y_true = np.array([2, 2, 2, 7, 7, 7])
    y_pred = np.array([2, 2, 7, 2, 7, 7])
    assert np.isclose(matthews_corrcoef(y_true, y_pred, positive=2), 1.0 / 3.0)


def test_is_symmetric_in_the_two_arguments():
    rng = np.random.default_rng(4)
    a = rng.integers(0, 2, size=50)
    b = rng.integers(0, 2, size=50)
    assert np.isclose(matthews_corrcoef(a, b), matthews_corrcoef(b, a))


def test_result_stays_in_minus_one_to_one():
    rng = np.random.default_rng(5)
    for _ in range(5):
        a = rng.integers(0, 2, size=30)
        b = rng.integers(0, 2, size=30)
        assert -1.0 <= matthews_corrcoef(a, b) <= 1.0


def test_scores_a_majority_guesser_zero_even_when_accuracy_is_high():
    y_true = np.array([0] * 9 + [1])
    y_pred = np.zeros(10, dtype=int)
    assert matthews_corrcoef(y_true, y_pred) == 0.0


def test_flipping_the_positive_class_keeps_the_same_value():
    # relabeling 1 <-> 0 on both sides leaves the correlation unchanged
    value = matthews_corrcoef(Y_TRUE, Y_PRED, positive=1)
    flipped = matthews_corrcoef(1 - Y_TRUE, 1 - Y_PRED, positive=0)
    assert np.isclose(value, flipped)


def test_length_mismatch_raises():
    assert _raises_value_error(matthews_corrcoef, np.array([0, 1]), np.array([0]))


def test_does_not_modify_inputs():
    y_true = Y_TRUE.copy()
    y_pred = Y_PRED.copy()
    matthews_corrcoef(y_true, y_pred)
    assert np.array_equal(y_true, Y_TRUE)
    assert np.array_equal(y_pred, Y_PRED)


def test_returns_a_python_float():
    assert isinstance(matthews_corrcoef(Y_TRUE, Y_PRED), float)
