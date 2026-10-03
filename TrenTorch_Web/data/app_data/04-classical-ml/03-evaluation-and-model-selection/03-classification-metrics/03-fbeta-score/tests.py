"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

fbeta_score = load_solution(__file__).fbeta_score


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


# tp = 2, fp = 0, fn = 2 -> precision 1.0, recall 0.5
Y_TRUE = np.array([1, 1, 1, 1, 0])
Y_PRED = np.array([1, 1, 0, 0, 0])


def test_beta_one_matches_the_harmonic_mean():
    # F1 = 2 * 1.0 * 0.5 / 1.5 = 2/3
    assert np.isclose(fbeta_score(Y_TRUE, Y_PRED, beta=1.0), 2.0 / 3.0)


def test_default_beta_is_one():
    assert np.isclose(fbeta_score(Y_TRUE, Y_PRED), 2.0 / 3.0)


def test_beta_two_leans_toward_recall():
    # 5 * 1.0 * 0.5 / (4 * 1.0 + 0.5) = 2.5 / 4.5
    assert np.isclose(fbeta_score(Y_TRUE, Y_PRED, beta=2.0), 2.5 / 4.5)


def test_beta_half_leans_toward_precision():
    # 1.25 * 0.5 / (0.25 * 1.0 + 0.5) = 0.625 / 0.75
    assert np.isclose(fbeta_score(Y_TRUE, Y_PRED, beta=0.5), 0.625 / 0.75)


def test_larger_beta_scores_a_recall_heavy_model_higher():
    # precision 1.0, recall 0.5: raising beta moves the score toward recall (0.5)
    f1 = fbeta_score(Y_TRUE, Y_PRED, beta=1.0)
    f2 = fbeta_score(Y_TRUE, Y_PRED, beta=2.0)
    assert f2 < f1


def test_perfect_predictions_score_one_for_any_beta():
    y = np.array([1, 0, 1, 0])
    for beta in (0.5, 1.0, 3.0):
        assert np.isclose(fbeta_score(y, y, beta=beta), 1.0)


def test_no_predicted_positives_returns_zero():
    y_true = np.array([1, 1, 0])
    y_pred = np.array([0, 0, 0])
    assert fbeta_score(y_true, y_pred) == 0.0


def test_no_actual_positives_and_no_predicted_positives_returns_zero():
    y_true = np.array([0, 0])
    y_pred = np.array([0, 0])
    assert fbeta_score(y_true, y_pred) == 0.0


def test_beta_must_be_positive():
    assert _raises_value_error(fbeta_score, Y_TRUE, Y_PRED, beta=0.0)
    assert _raises_value_error(fbeta_score, Y_TRUE, Y_PRED, beta=-1.0)


def test_length_mismatch_raises():
    assert _raises_value_error(fbeta_score, np.array([1, 0]), np.array([1]))


def test_positive_argument_selects_the_class():
    y_true = np.array([0, 0, 0, 1])
    y_pred = np.array([0, 0, 1, 1])
    # treating 0 as positive: tp 2, fp 0, fn 1 -> P 1.0, R 2/3, F1 = 0.8
    assert np.isclose(fbeta_score(y_true, y_pred, positive=0), 0.8)


def test_score_is_between_zero_and_one():
    rng = np.random.default_rng(3)
    y_true = rng.integers(0, 2, size=40)
    y_pred = rng.integers(0, 2, size=40)
    for beta in (0.3, 1.0, 4.0):
        assert 0.0 <= fbeta_score(y_true, y_pred, beta=beta) <= 1.0


def test_does_not_modify_inputs():
    y_true = Y_TRUE.copy()
    y_pred = Y_PRED.copy()
    fbeta_score(y_true, y_pred, beta=2.0)
    assert np.array_equal(y_true, Y_TRUE)
    assert np.array_equal(y_pred, Y_PRED)


def test_returns_a_python_float():
    assert isinstance(fbeta_score(Y_TRUE, Y_PRED), float)
