"""
pytest data/app_data/12-research-papers/06-computer-vision/03-vgg/01-stack-receptive-field/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vgg-receptive-field")
receptive_field_stack = _module.receptive_field_stack


def test_1_single_three_by_three_sees_three_pixels():
    assert receptive_field_stack(1, 3) == 3


def test_2_three_stacked_three_by_threes_see_seven_pixels():
    assert receptive_field_stack(3, 3) == 7


def test_3_one_by_one_stacks_never_grow():
    assert receptive_field_stack(10, 1) == 1


def test_4_default_kernel_is_three():
    assert receptive_field_stack(2) == 5


def test_5_returns_an_integer():
    assert isinstance(receptive_field_stack(4), int)


def test_6_grows_linearly_with_depth():
    assert receptive_field_stack(5, 3) - receptive_field_stack(4, 3) == 2

