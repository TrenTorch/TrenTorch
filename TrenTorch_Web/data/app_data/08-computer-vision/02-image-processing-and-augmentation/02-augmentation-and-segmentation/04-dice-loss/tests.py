"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
dice_coefficient = _module.dice_coefficient
dice_loss = _module.dice_loss


def test_1_perfect_overlap_is_one():
    t = np.array([[[1, 1], [0, 0]]], dtype=float)
    assert np.isclose(dice_coefficient(t, t)[0], 1.0) and np.isclose(dice_loss(t, t), 0.0, atol=1e-9)


def test_2_disjoint_masks_score_zero():
    p = np.array([[[1, 0], [0, 0]]], dtype=float)
    t = np.array([[[0, 0], [0, 1]]], dtype=float)
    assert np.isclose(dice_coefficient(p, t, eps=0.0)[0], 0.0)


def test_3_hand_computed_partial_overlap():
    p = np.array([[[1, 1, 0, 0]]], dtype=float)
    t = np.array([[[1, 0, 1, 0]]], dtype=float)
    # intersection 1, sums 2+2 -> 2/4
    assert np.isclose(dice_coefficient(p, t, eps=0.0)[0], 0.5)


def test_4_both_empty_is_one_thanks_to_eps():
    z = np.zeros((1, 3, 3))
    assert np.isclose(dice_coefficient(z, z)[0], 1.0)


def test_5_all_background_prediction_is_penalized_despite_tiny_object():
    t = np.zeros((1, 10, 10))
    t[0, 4, 4] = 1.0
    p = np.zeros((1, 10, 10))
    assert dice_loss(p, t, eps=1e-6) > 0.99


def test_6_matches_iou_relation_for_binary_masks():
    rng = np.random.RandomState(0)
    p = (rng.rand(1, 8, 8) > 0.5).astype(float)
    t = (rng.rand(1, 8, 8) > 0.5).astype(float)
    inter = (p * t).sum()
    iou = inter / (p.sum() + t.sum() - inter)
    assert np.isclose(dice_coefficient(p, t, eps=0.0)[0], 2 * iou / (1 + iou))


def test_7_per_sample_mean_and_inputs_untouched():
    p = np.array([[[1.0, 0.0]], [[0.0, 0.0]]])
    t = np.array([[[1.0, 0.0]], [[1.0, 0.0]]])
    sp = p.copy()
    d = dice_coefficient(p, t, eps=0.0)
    assert np.allclose(d, [1.0, 0.0]) and np.isclose(dice_loss(p, t, eps=0.0), 0.5) and np.array_equal(p, sp)
