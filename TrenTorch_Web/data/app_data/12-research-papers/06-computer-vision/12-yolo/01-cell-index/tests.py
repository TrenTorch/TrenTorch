"""
pytest data/app_data/12-research-papers/06-computer-vision/12-yolo/01-cell-index/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-yolo-cell-index")
cell_index = _module.cell_index


def test_1_centre_in_the_top_left_cell():
    assert cell_index(1, 1, 448, 7) == (0, 0)


def test_2_centre_in_the_bottom_right_cell():
    assert cell_index(447, 447, 448, 7) == (6, 6)


def test_3_middle_of_image_maps_to_middle_cell():
    assert cell_index(224, 224, 448, 7) == (3, 3)


def test_4_returns_a_tuple_of_ints():
    out = cell_index(10, 10, 100, 4)
    assert isinstance(out, tuple) and all(isinstance(v, int) for v in out)


def test_5_row_and_column_are_not_swapped():
    assert cell_index(400, 10, 448, 7) == (0, 6)


def test_6_coordinate_on_the_edge_is_clamped():
    assert cell_index(448, 448, 448, 7) == (6, 6)

