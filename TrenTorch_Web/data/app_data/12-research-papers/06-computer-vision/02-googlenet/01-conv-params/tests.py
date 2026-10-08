"""
pytest data/app_data/12-research-papers/06-computer-vision/02-googlenet/01-conv-params/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-googlenet-conv-params")
conv_params = _module.conv_params


def test_1_first_googlenet_conv_has_9472_parameters():
    assert conv_params(3, 64, 7) == 9472


def test_2_one_by_one_conv_counts_channels_only():
    assert conv_params(10, 4, 1) == 10 * 4 + 4


def test_3_parameters_scale_with_kernel_area():
    assert conv_params(2, 2, 3) == 2 * 2 * 9 + 2


def test_4_returns_an_integer():
    assert isinstance(conv_params(1, 1, 1), int)


def test_5_doubling_output_channels_roughly_doubles_weights():
    a = conv_params(16, 16, 3) - 16
    b = conv_params(16, 32, 3) - 32
    assert b == 2 * a


def test_6_zero_channels_has_no_parameters():
    assert conv_params(0, 0, 3) == 0

