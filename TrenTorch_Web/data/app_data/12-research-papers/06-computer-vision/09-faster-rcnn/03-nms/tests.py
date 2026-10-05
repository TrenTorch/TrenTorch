"""
pytest data/app_data/12-research-papers/06-computer-vision/09-faster-rcnn/03-nms/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-frcnn-nms")
nms = _module.nms


def test_1_keeps_the_highest_scoring_of_two_overlapping_boxes():
    assert nms([[0, 0, 2, 2], [0, 0, 2, 2.1]], [0.5, 0.9], 0.5) == [1]


def test_2_keeps_both_when_they_do_not_overlap():
    assert sorted(nms([[0, 0, 1, 1], [5, 5, 6, 6]], [0.5, 0.9], 0.5)) == [0, 1]


def test_3_output_is_ordered_by_score():
    keep = nms([[0, 0, 1, 1], [5, 5, 6, 6], [10, 10, 11, 11]], [0.2, 0.9, 0.5], 0.5)
    assert keep == [1, 2, 0]


def test_4_empty_input_gives_empty_output():
    assert nms([], [], 0.5) == []


def test_5_threshold_one_keeps_everything():
    assert len(nms([[0, 0, 2, 2], [0, 0, 2, 2]], [0.9, 0.8], 1.0)) == 2


def test_6_does_not_mutate_scores():
    s = [0.1, 0.9]
    nms([[0, 0, 1, 1], [0, 0, 1, 1]], s, 0.5)
    assert s == [0.1, 0.9]

