"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
nms = _module.nms


def test_1_duplicate_boxes_collapse_to_the_best():
    boxes = np.array([[0, 0, 10, 10], [1, 1, 11, 11], [0, 0, 10, 9]], dtype=float)
    scores = np.array([0.8, 0.9, 0.7])
    assert nms(boxes, scores, 0.5) == [1]


def test_2_distant_boxes_are_all_kept_in_score_order():
    boxes = np.array([[0, 0, 1, 1], [10, 10, 11, 11], [20, 20, 21, 21]], dtype=float)
    scores = np.array([0.5, 0.9, 0.7])
    assert nms(boxes, scores, 0.5) == [1, 2, 0]


def test_3_threshold_is_strict():
    boxes = np.array([[0, 0, 2, 2], [1, 0, 3, 2]], dtype=float)  # IoU = 1/3
    scores = np.array([0.9, 0.8])
    assert nms(boxes, scores, 1 / 3) == [0, 1]
    assert nms(boxes, scores, 0.3) == [0]


def test_4_suppression_chains_use_only_kept_boxes():
    # A overlaps B, B overlaps C, but A and C are far apart: B is suppressed by A, so C survives
    boxes = np.array([[0, 0, 4, 4], [3, 0, 7, 4], [6, 0, 10, 4]], dtype=float)
    scores = np.array([0.9, 0.8, 0.7])
    assert nms(boxes, scores, 0.1) == [0, 2]


def test_5_tie_scores_prefer_the_lower_index():
    boxes = np.array([[0, 0, 5, 5], [0, 0, 5, 5]], dtype=float)
    assert nms(boxes, np.array([0.5, 0.5]), 0.5) == [0]


def test_6_empty_input():
    assert nms(np.zeros((0, 4)), np.zeros(0), 0.5) == []


def test_7_every_removed_box_overlaps_a_kept_one_and_inputs_untouched():
    rng = np.random.RandomState(0)
    xy = rng.rand(30, 2) * 20
    boxes = np.hstack([xy, xy + rng.rand(30, 2) * 8 + 1])
    scores = rng.rand(30)
    sb, ss = boxes.copy(), scores.copy()
    keep = nms(boxes, scores, 0.4)
    def iou(p, q):
        w = max(0, min(p[2], q[2]) - max(p[0], q[0]))
        h = max(0, min(p[3], q[3]) - max(p[1], q[1]))
        return w * h / ((p[2] - p[0]) * (p[3] - p[1]) + (q[2] - q[0]) * (q[3] - q[1]) - w * h)
    for i in range(30):
        if i not in keep:
            assert any(iou(boxes[i], boxes[k]) > 0.4 and scores[k] >= scores[i] for k in keep)
    for a in keep:
        for b in keep:
            if a != b:
                assert iou(boxes[a], boxes[b]) <= 0.4
    assert np.array_equal(boxes, sb) and np.array_equal(scores, ss)
