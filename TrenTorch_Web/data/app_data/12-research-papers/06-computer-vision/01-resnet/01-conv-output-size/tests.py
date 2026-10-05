"""
pytest data/app_data/12-research-papers/06-computer-vision/01-resnet/01-conv-output-size/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-resnet-conv-output-size")
conv_output_size = _module.conv_output_size


def test_1_resnet_stem_halves_224_to_112():
    assert conv_output_size(224, 7, 2, 3) == 112


def test_2_same_padding_keeps_the_size():
    assert conv_output_size(5, 3, 1, 1) == 5


def test_3_stride_two_with_no_padding():
    assert conv_output_size(4, 2, 2, 0) == 2


def test_4_kernel_equal_to_input_gives_one():
    assert conv_output_size(7, 7, 1, 0) == 1


def test_5_returns_an_integer():
    assert isinstance(conv_output_size(10, 3, 1, 0), int)


def test_6_padding_adds_to_the_output():
    assert conv_output_size(8, 3, 1, 2) == 10

