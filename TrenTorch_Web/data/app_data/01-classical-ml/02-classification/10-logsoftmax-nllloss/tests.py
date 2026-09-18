"""
pytest data/app_data/01-classical-ml/02-classification/10-logsoftmax-nllloss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}")
log_softmax = _module.log_softmax
nll_loss = _module.nll_loss

_softmax_cce = load_solution("01-classical-ml/02-classification/06-softmax-cce")
softmax = _softmax_cce.softmax
cce_loss = _softmax_cce.cce_loss


def test_log_softmax_exponentiates_back_to_softmax():
    Z = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0]])
    assert np.allclose(np.exp(log_softmax(Z)), softmax(Z), atol=1e-8)


def test_log_softmax_rows_sum_to_one_after_exponentiating():
    Z = np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0]])
    probs = np.exp(log_softmax(Z))
    assert np.allclose(probs.sum(axis=1), 1.0)


def test_log_softmax_stays_finite_on_extreme_logits():
    # The exact scenario the naive log(softmax(Z)) breaks on: one
    # dominant logit collapses the other classes' probabilities to
    # (numerically) zero.
    Z = np.array([[1000.0, 1.0, 0.0]])
    result = log_softmax(Z)
    assert np.all(np.isfinite(result))


def test_log_softmax_matches_naive_computation_on_well_scaled_logits():
    # On ordinary, non-extreme logits, the fused version must agree
    # with the naive two-step version (both are mathematically the
    # same formula, only their numerical behavior differs).
    Z = np.array([[1.0, 2.0, 0.5]])
    naive = np.log(softmax(Z))
    stable = log_softmax(Z)
    assert np.allclose(naive, stable, atol=1e-8)


def test_nll_loss_matches_hand_computation():
    log_probs = np.log(np.array([[0.25, 0.75], [0.6, 0.4]]))
    y_indices = np.array([0, 1])
    # -mean(log(0.25), log(0.4))
    expected = -np.mean([np.log(0.25), np.log(0.4)])
    assert np.isclose(nll_loss(log_probs, y_indices), expected)


def test_nll_loss_is_zero_for_perfectly_confident_correct_predictions():
    log_probs = np.log(np.array([[1.0, 0.0], [0.0, 1.0]]) + 1e-300)  # avoid log(0)
    y_indices = np.array([0, 1])
    assert nll_loss(log_probs, y_indices) < 1e-6


def test_composed_log_softmax_and_nll_loss_matches_softmax_and_cce_loss():
    # The core equivalence this question exists to demonstrate: the
    # fused (log_softmax + nll_loss) pipeline and the naive (softmax +
    # cce_loss) pipeline compute the exact same loss value.
    Z = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0], [1.0, 1.0, 1.0]])
    y_indices = np.array([0, 1, 2])
    fused_loss = nll_loss(log_softmax(Z), y_indices)
    naive_loss = cce_loss(softmax(Z), y_indices)
    assert np.isclose(fused_loss, naive_loss, atol=1e-6)


def test_log_softmax_does_not_call_log_of_softmax_directly():
    # Directly targets a mutant that reintroduces the naive two-step
    # computation (np.log(softmax(Z))): on extreme logits, the naive
    # version produces -inf/nan, the correct fused version stays finite.
    Z = np.array([[2000.0, 1.0, 0.0]])
    result = log_softmax(Z)
    assert np.all(np.isfinite(result))
    naive_would_be = np.log(softmax(Z))
    assert not np.all(np.isfinite(naive_would_be))  # confirms the naive path really does break here
