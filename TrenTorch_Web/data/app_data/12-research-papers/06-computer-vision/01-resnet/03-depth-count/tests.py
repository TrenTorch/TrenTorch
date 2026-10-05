"""
pytest data/app_data/12-research-papers/06-computer-vision/01-resnet/03-depth-count/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-resnet-depth-count")
resnet_depth = _module.resnet_depth


def test_1_resnet_18_has_depth_18():
    assert resnet_depth([2, 2, 2, 2]) == 18


def test_2_resnet_34_has_depth_34():
    assert resnet_depth([3, 4, 6, 3]) == 34


def test_3_no_blocks_is_just_stem_and_classifier():
    assert resnet_depth([]) == 2


def test_4_adding_a_block_adds_two_layers():
    assert resnet_depth([2, 2, 2, 3]) - resnet_depth([2, 2, 2, 2]) == 2


def test_5_returns_an_integer():
    assert isinstance(resnet_depth([1]), int)


def test_6_order_of_stages_does_not_matter():
    assert resnet_depth([3, 4, 6, 3]) == resnet_depth([3, 6, 4, 3])

