"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

log_loss = load_solution(__file__).log_loss


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_coin_flip_predictions_cost_ln_two():
    assert np.isclose(log_loss(np.array([1, 0]), np.array([0.5, 0.5])), math.log(2))


def test_confident_correct_predictions_are_near_zero():
    assert log_loss(np.array([1, 0]), np.array([1.0, 0.0])) < 1e-10


def test_confident_wrong_prediction_is_large_but_finite():
    loss = log_loss(np.array([1]), np.array([0.0]))
    assert np.isfinite(loss)
    assert np.isclose(loss, -math.log(1e-15))


def test_better_probabilities_lower_the_loss():
    y = np.array([1, 0, 1, 1])
    weak = log_loss(y, np.array([0.6, 0.4, 0.6, 0.6]))
    strong = log_loss(y, np.array([0.9, 0.1, 0.9, 0.9]))
    assert strong < weak


def test_worked_example_matches_the_formula():
    y = np.array([1, 0])
    p = np.array([0.8, 0.3])
    expected = -(math.log(0.8) + math.log(0.7)) / 2
    assert np.isclose(log_loss(y, p), expected)


def test_loss_is_non_negative():
    rng = np.random.default_rng(8)
    y = rng.integers(0, 2, size=30)
    p = rng.random(30)
    assert log_loss(y, p) >= 0.0


def test_eps_argument_controls_the_clip():
    assert log_loss(np.array([1]), np.array([0.0]), eps=1e-3) < log_loss(np.array([1]), np.array([0.0]))


def test_labels_must_be_zero_or_one():
    assert _raises_value_error(log_loss, np.array([2, 0]), np.array([0.5, 0.5]))


def test_probabilities_must_be_in_unit_interval():
    assert _raises_value_error(log_loss, np.array([1, 0]), np.array([1.2, 0.5]))
    assert _raises_value_error(log_loss, np.array([1, 0]), np.array([-0.1, 0.5]))


def test_length_mismatch_raises():
    assert _raises_value_error(log_loss, np.array([1, 0]), np.array([0.5]))


def test_empty_input_raises():
    assert _raises_value_error(log_loss, np.array([]), np.array([]))


def test_flipping_labels_and_probabilities_keeps_the_loss():
    y = np.array([1, 0, 1])
    p = np.array([0.7, 0.2, 0.4])
    assert np.isclose(log_loss(y, p), log_loss(1 - y, 1 - p))


def test_does_not_modify_inputs():
    y = np.array([1, 0])
    p = np.array([0.0, 0.5])
    before_y, before_p = y.copy(), p.copy()
    log_loss(y, p)
    assert np.array_equal(y, before_y)
    assert np.array_equal(p, before_p)
