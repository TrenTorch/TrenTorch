"""
pytest data/app_data/12-research-papers/06-computer-vision/09-faster-rcnn/01-iou/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-frcnn-iou")
iou = _module.iou


def test_1_identical_boxes_have_iou_one():
    assert abs(iou([0, 0, 2, 2], [0, 0, 2, 2]) - 1.0) < 1e-12


def test_2_disjoint_boxes_have_iou_zero():
    assert iou([0, 0, 1, 1], [5, 5, 6, 6]) == 0.0


def test_3_hand_value_for_overlapping_squares():
    # intersection 1, union 4 + 4 - 1 = 7
    assert abs(iou([0, 0, 2, 2], [1, 1, 3, 3]) - 1 / 7) < 1e-12


def test_4_is_symmetric():
    assert iou([0, 0, 3, 1], [1, 0, 4, 2]) == iou([1, 0, 4, 2], [0, 0, 3, 1])


def test_5_contained_box_gives_area_ratio():
    assert abs(iou([0, 0, 4, 4], [0, 0, 2, 2]) - 0.25) < 1e-12


def test_6_touching_edges_give_zero():
    assert iou([0, 0, 1, 1], [1, 0, 2, 1]) == 0.0

