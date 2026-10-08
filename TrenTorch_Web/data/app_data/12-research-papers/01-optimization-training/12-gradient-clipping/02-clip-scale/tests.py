"""
pytest data/app_data/12-research-papers/01-optimization-and-training/12-gradient-clipping/02-clip-scale/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clip-scale")
clip_scale = _module.clip_scale


def test_1_hand_case():
    assert abs(clip_scale(10.0, 2.0) - 0.2) < 1e-12


def test_2_under_threshold_is_one():
    assert clip_scale(0.5, 2.0) == 1.0


def test_3_at_threshold_is_one():
    assert clip_scale(2.0, 2.0) == 1.0


def test_4_scale_brings_norm_to_threshold():
    assert abs(clip_scale(8.0, 2.0) * 8.0 - 2.0) < 1e-12


def test_5_returns_a_float():
    assert isinstance(clip_scale(5.0, 1.0), float)


def test_6_never_exceeds_one():
    assert clip_scale(0.001, 100.0) <= 1.0

