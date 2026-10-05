"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
match_anchors = _module.match_anchors
GT = np.array([[0.0, 0.0, 10.0, 10.0]])


def test_1_threshold_rules_hand_computed():
    anchors = np.array([[0, 0, 10, 10], [0, 0, 10, 6], [0, 0, 10, 4], [20, 20, 30, 30]], dtype=float)
    # IoUs with GT: 1.0, 0.6, 0.4, 0.0
    m = match_anchors(anchors, GT, pos_thresh=0.5, neg_thresh=0.3)
    assert m.tolist() == [0, 0, -2, -1]


def test_2_each_ground_truth_claims_its_best_anchor():
    anchors = np.array([[0, 0, 10, 2], [30, 30, 40, 40]], dtype=float)  # best IoU 0.2 < both thresholds
    m = match_anchors(anchors, GT, pos_thresh=0.5, neg_thresh=0.3)
    assert m.tolist() == [0, -1]


def test_3_no_ground_truth_means_all_background():
    anchors = np.array([[0, 0, 1, 1], [2, 2, 3, 3]], dtype=float)
    assert match_anchors(anchors, np.zeros((0, 4)), 0.5, 0.4).tolist() == [-1, -1]


def test_4_anchor_goes_to_the_overlapping_ground_truth_with_highest_iou():
    gt = np.array([[0, 0, 10, 10], [5, 0, 15, 10]], dtype=float)
    anchors = np.array([[4, 0, 14, 10]], dtype=float)  # IoU with gt1 = 1/ (..)
    assert match_anchors(anchors, gt, 0.3, 0.2).tolist() == [1]


def test_5_zero_overlap_best_anchor_is_not_forced():
    gt = np.array([[100.0, 100.0, 110.0, 110.0]])
    anchors = np.array([[0, 0, 5, 5]], dtype=float)
    assert match_anchors(anchors, gt, 0.5, 0.4).tolist() == [-1]


def test_6_ties_prefer_lower_indices():
    anchors = np.array([[0, 0, 10, 10], [0, 0, 10, 10]], dtype=float)
    m = match_anchors(anchors, GT, 0.5, 0.4)
    assert m.tolist() == [0, 0]


def test_7_output_dtype_shape_and_inputs_untouched():
    rng = np.random.RandomState(0)
    xy = rng.rand(10, 2) * 20
    anchors = np.hstack([xy, xy + 8])
    sa = anchors.copy()
    m = match_anchors(anchors, np.array([[5.0, 5.0, 15.0, 15.0]]), 0.5, 0.3)
    assert m.shape == (10,) and np.issubdtype(m.dtype, np.integer) and set(m.tolist()) <= {-2, -1, 0}
    assert (m == 0).any() and np.array_equal(anchors, sa)
