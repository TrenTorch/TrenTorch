"""
pytest data/01-classical-ml/02-classification/02-bce-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

bce_loss = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").bce_loss


def test_zero_loss_on_exact_match():
    # Not exactly 0.0: the required clip to [1e-12, 1-1e-12] means a
    # perfect p=1.0 prediction is actually scored against 1-1e-12, so
    # the loss floors at a tiny ~1e-12 residual rather than true zero --
    # that's the clip doing its job, not a bug. Near-zero is the
    # correct bar here, not bit-exact zero.
    y = np.array([1.0, 0.0, 1.0])
    assert np.isclose(bce_loss(y, y), 0.0, atol=1e-9)


def test_hand_computed_value():
    # p=0.5, y=1 -> -log(0.5) = ln(2) ~= 0.6931
    assert np.isclose(bce_loss(np.array([0.5]), np.array([1.0])), np.log(2))


def test_confidently_wrong_costs_more_than_unsure():
    y = np.array([1.0])
    unsure = bce_loss(np.array([0.5]), y)
    confidently_wrong = bce_loss(np.array([0.01]), y)
    assert confidently_wrong > unsure


def test_saturated_prediction_does_not_produce_nan():
    # p exactly 0.0 or 1.0 before clipping -- the actual edge case the
    # clip inside the function exists to survive.
    result = bce_loss(np.array([0.0, 1.0]), np.array([0.0, 1.0]))
    assert np.isfinite(result)


def test_returns_plain_float():
    assert isinstance(bce_loss(np.array([0.5]), np.array([1.0])), float)


def test_batch_averages_correctly():
    p = np.array([0.9, 0.1])
    y = np.array([1.0, 0.0])
    per_sample = -np.log(0.9)
    assert np.isclose(bce_loss(p, y), per_sample)
