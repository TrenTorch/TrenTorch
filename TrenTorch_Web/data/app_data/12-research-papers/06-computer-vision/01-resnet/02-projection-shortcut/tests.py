"""
pytest data/app_data/12-research-papers/06-computer-vision/01-resnet/02-projection-shortcut/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-resnet-projection-shortcut")
needs_projection = _module.needs_projection


def test_1_same_channels_and_stride_need_no_projection():
    assert needs_projection(64, 64, 1) is False


def test_2_channel_change_needs_projection():
    assert needs_projection(64, 128, 1) is True


def test_3_stride_two_needs_projection():
    assert needs_projection(64, 64, 2) is True


def test_4_both_changes_need_projection():
    assert needs_projection(32, 64, 2) is True


def test_5_returns_a_bool():
    assert isinstance(needs_projection(1, 2, 1), bool)


def test_6_identical_dimensions_at_any_size_do_not_project():
    assert needs_projection(256, 256, 1) is False

