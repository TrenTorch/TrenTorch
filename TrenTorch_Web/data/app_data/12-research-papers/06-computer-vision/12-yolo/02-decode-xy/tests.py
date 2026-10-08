"""
pytest data/app_data/12-research-papers/06-computer-vision/12-yolo/02-decode-xy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-yolo-decode-xy")
decode_xy = _module.decode_xy


import math


def test_1_zero_raw_offset_gives_cell_centre():
    x, y = decode_xy(0.0, 0.0, 0, 0, 7, 448)
    assert abs(x - 32.0) < 1e-9 and abs(y - 32.0) < 1e-9


def test_2_centre_stays_inside_its_cell():
    x, _ = decode_xy(100.0, 0.0, 2, 0, 7, 448)
    cell = 448 / 7
    assert 2 * cell <= x <= 3 * cell


def test_3_hand_value_for_column_one():
    x, _ = decode_xy(0.0, 0.0, 1, 0, 2, 100)
    assert abs(x - 75.0) < 1e-9


def test_4_returns_a_tuple_of_floats():
    out = decode_xy(0.5, -0.5, 1, 1, 4, 64)
    assert isinstance(out, tuple) and all(isinstance(v, float) for v in out)


def test_5_row_offset_uses_the_y_output():
    _, y = decode_xy(0.0, 1.0, 0, 3, 4, 40)
    expected = (3 + 1 / (1 + math.exp(-1.0))) * 10
    assert abs(y - expected) < 1e-9


def test_6_coordinates_are_nonnegative_for_nonnegative_cells():
    x, y = decode_xy(-3.0, -3.0, 0, 0, 7, 448)
    assert x >= 0 and y >= 0

