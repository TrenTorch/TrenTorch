"""
pytest data/app_data/12-research-papers/06-computer-vision/03-vgg/03-stacked-params/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vgg-stacked-params")
stacked_params = _module.stacked_params


def test_1_three_three_by_three_layers_with_two_channels():
    assert stacked_params(3, 2, 3) == 108


def test_2_three_three_by_threes_use_fewer_weights_than_one_seven_by_seven():
    assert stacked_params(3, 16, 3) < stacked_params(1, 16, 7)


def test_3_one_layer_is_kernel_area_times_channels_squared():
    assert stacked_params(1, 4, 3) == 9 * 16


def test_4_returns_an_integer():
    assert isinstance(stacked_params(2, 2), int)


def test_5_zero_layers_have_no_weights():
    assert stacked_params(0, 8) == 0


def test_6_scales_linearly_with_depth():
    assert stacked_params(4, 3) == 2 * stacked_params(2, 3)

