"""
pytest data/app_data/12-research-papers/06-computer-vision/04-zeiler-visualization/01-receptive-field/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zeiler-receptive-field")
receptive_field = _module.receptive_field


def test_1_two_stride_one_three_by_threes_give_five():
    assert receptive_field([3, 3], [1, 1]) == 5


def test_2_single_layer_is_its_kernel():
    assert receptive_field([3], [2]) == 3


def test_3_stride_two_makes_later_layers_jump_further():
    assert receptive_field([2, 2], [2, 2]) == 4


def test_4_no_layers_see_one_pixel():
    assert receptive_field([], []) == 1


def test_5_returns_an_integer():
    assert isinstance(receptive_field([3], [1]), int)


def test_6_bigger_kernels_see_more():
    assert receptive_field([5], [1]) > receptive_field([3], [1])

