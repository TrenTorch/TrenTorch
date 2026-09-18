"""
pytest data/app_data/01-classical-ml/04-support-vector-machines/01-hinge-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-support-vector-machines/{Path(__file__).resolve().parent.name}")
hinge_loss = _module.hinge_loss


def test_hinge_loss_is_zero_for_confidently_correct_predictions():
    scores = np.array([5.0])
    target = np.array([1.0])
    assert np.isclose(hinge_loss(scores, target, "none")[0], 0.0)


def test_hinge_loss_matches_known_oracle_values():
    # generated once, offline, via sklearn.metrics.hinge_loss on
    # individual examples
    scores = np.array([2.0, 0.5, -1.0, -3.0])
    target = np.array([1.0, 1.0, -1.0, 1.0])
    expected = np.array([0.0, 0.5, 0.0, 4.0])
    assert np.allclose(hinge_loss(scores, target, "none"), expected)


def test_hinge_loss_mean_matches_sklearn_reference():
    scores = np.array([2.0, 0.5, -1.0, -3.0])
    target = np.array([1.0, 1.0, -1.0, 1.0])
    result = hinge_loss(scores, target, "mean")

    from sklearn.metrics import hinge_loss as sklearn_hinge_loss

    assert np.isclose(result, sklearn_hinge_loss(target, scores))


def test_hinge_loss_is_exactly_zero_right_at_the_margin_boundary():
    # margin == 1 exactly is the boundary: max(0, 1-1) = 0
    scores = np.array([1.0])
    target = np.array([1.0])
    assert np.isclose(hinge_loss(scores, target, "none")[0], 0.0)


def test_hinge_loss_grows_linearly_past_the_margin():
    target = np.array([1.0])
    loss_at_0 = hinge_loss(np.array([0.0]), target, "none")[0]
    loss_at_neg1 = hinge_loss(np.array([-1.0]), target, "none")[0]
    assert np.isclose(loss_at_0, 1.0)
    assert np.isclose(loss_at_neg1, 2.0)
    assert np.isclose(loss_at_neg1 - loss_at_0, 1.0)  # linear growth


def test_hinge_loss_handles_negative_class_symmetrically():
    # For target=-1, the loss is max(0, 1 + scores), the mirror image.
    scores = np.array([-5.0, 0.0, 5.0])
    target = np.array([-1.0, -1.0, -1.0])
    result = hinge_loss(scores, target, "none")
    assert np.allclose(result, [0.0, 1.0, 6.0])


def test_hinge_loss_raises_on_invalid_reduction():
    x = np.array([1.0])
    with pytest.raises(ValueError):
        hinge_loss(x, x, reduction="bogus")


def test_hinge_loss_does_not_forget_to_multiply_by_target():
    # Directly targets a mutant that computes max(0, 1 - scores)
    # regardless of target's sign (ignoring the label entirely). For a
    # negative-class example with a very negative score (correctly and
    # confidently classified), the correct loss is 0, an ignoring-target
    # mutant would incorrectly report a large loss.
    scores = np.array([-10.0])
    target = np.array([-1.0])
    result = hinge_loss(scores, target, "none")[0]
    assert np.isclose(result, 0.0)
    assert not np.isclose(result, 11.0)
