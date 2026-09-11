"""
pytest data/01-classical-ml/02-classification/08-weighted-bce/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

weighted_bce_loss = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").weighted_bce_loss
bce_loss = load_solution("01-classical-ml/02-classification/02-bce-loss").bce_loss


def test_equal_weights_matches_plain_bce():
    p = np.array([0.9, 0.2, 0.6])
    y = np.array([1.0, 0.0, 1.0])
    assert np.isclose(weighted_bce_loss(p, y, {0: 1.0, 1: 1.0}), bce_loss(p, y))


def test_higher_weight_on_minority_class_increases_its_contribution():
    p = np.array([0.1])  # confidently wrong
    y = np.array([1.0])  # minority class
    low_weight = weighted_bce_loss(p, y, {0: 1.0, 1: 1.0})
    high_weight = weighted_bce_loss(p, y, {0: 1.0, 1: 10.0})
    assert high_weight > low_weight
    assert np.isclose(high_weight, 10 * low_weight)


def test_majority_class_weight_scales_its_own_errors_only():
    p = np.array([0.9, 0.1])
    y = np.array([0.0, 1.0])
    scaled = weighted_bce_loss(p, y, {0: 5.0, 1: 1.0})
    # only the y=0 sample's error term should be scaled by 5
    expected = (5 * -np.log(1 - 0.9) + 1 * -np.log(0.1)) / 2
    assert np.isclose(scaled, expected)
