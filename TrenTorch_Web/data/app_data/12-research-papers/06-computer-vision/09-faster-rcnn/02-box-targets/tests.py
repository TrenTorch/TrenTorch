"""
pytest data/app_data/12-research-papers/06-computer-vision/09-faster-rcnn/02-box-targets/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-frcnn-box-targets")
box_targets = _module.box_targets


import math


def test_1_identical_boxes_give_zero_targets():
    out = box_targets([0, 0, 4, 4], [0, 0, 4, 4])
    assert all(abs(v) < 1e-12 for v in out)


def test_2_pure_shift_gives_scaled_center_offset():
    # anchor 2x2 centered at (1,1); gt centered at (2,1) -> tx = 1 / 2
    out = box_targets([0, 0, 2, 2], [1, 0, 3, 2])
    assert abs(out[0] - 0.5) < 1e-12 and abs(out[1]) < 1e-12


def test_3_doubling_width_gives_log_two():
    out = box_targets([0, 0, 2, 2], [0, 0, 4, 2])
    assert abs(out[2] - math.log(2.0)) < 1e-12


def test_4_returns_four_values():
    assert len(box_targets([0, 0, 1, 1], [0, 0, 2, 2])) == 4


def test_5_height_scale_gives_log_for_th():
    out = box_targets([0, 0, 2, 2], [0, 0, 2, 8])
    assert abs(out[3] - math.log(4.0)) < 1e-12


def test_6_does_not_mutate_boxes():
    a = [0, 0, 2, 2]
    box_targets(a, [0, 0, 4, 4])
    assert a == [0, 0, 2, 2]

