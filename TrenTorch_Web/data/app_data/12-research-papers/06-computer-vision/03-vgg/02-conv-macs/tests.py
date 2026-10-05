"""
pytest data/app_data/12-research-papers/06-computer-vision/03-vgg/02-conv-macs/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vgg-conv-macs")
conv_macs = _module.conv_macs


def test_1_one_pixel_one_channel_one_by_one():
    assert conv_macs(1, 1, 1, 1, 1) == 1


def test_2_three_by_three_default_kernel():
    assert conv_macs(2, 2, 3, 4) == 2 * 2 * 3 * 4 * 9


def test_3_doubling_height_doubles_the_cost():
    assert conv_macs(8, 4, 2, 2) == 2 * conv_macs(4, 4, 2, 2)


def test_4_returns_an_integer():
    assert isinstance(conv_macs(3, 3, 3, 3), int)


def test_5_zero_channels_cost_nothing():
    assert conv_macs(5, 5, 0, 8) == 0


def test_6_larger_kernel_costs_more():
    assert conv_macs(4, 4, 2, 2, k=5) > conv_macs(4, 4, 2, 2, k=3)

