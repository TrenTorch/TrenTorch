"""
pytest data/app_data/12-research-papers/06-computer-vision/02-googlenet/02-inception-channels/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-googlenet-inception-channels")
inception_out_channels = _module.inception_out_channels


def test_1_inception_3a_channel_count():
    assert inception_out_channels(64, 128, 32, 32) == 256


def test_2_branches_are_summed():
    assert inception_out_channels(1, 2, 3, 4) == 10


def test_3_zero_branches_give_zero():
    assert inception_out_channels(0, 0, 0, 0) == 0


def test_4_returns_an_integer():
    assert isinstance(inception_out_channels(1, 1, 1, 1), int)


def test_5_order_does_not_matter():
    assert inception_out_channels(4, 3, 2, 1) == inception_out_channels(1, 2, 3, 4)


def test_6_single_branch_passes_its_channels():
    assert inception_out_channels(7, 0, 0, 0) == 7

