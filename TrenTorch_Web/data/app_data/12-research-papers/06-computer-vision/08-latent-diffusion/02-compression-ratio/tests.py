"""
pytest data/app_data/12-research-papers/06-computer-vision/08-latent-diffusion/02-compression-ratio/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ldm-compression-ratio")
compression_ratio = _module.compression_ratio


def test_1_factor_eight_with_four_latent_channels_gives_48():
    assert abs(compression_ratio(512, 512, 3, 8, 4) - 48.0) < 1e-12


def test_2_no_compression_gives_ratio_one():
    assert abs(compression_ratio(16, 16, 3, 1, 3) - 1.0) < 1e-12


def test_3_more_latent_channels_lower_the_ratio():
    assert compression_ratio(64, 64, 3, 8, 8) < compression_ratio(64, 64, 3, 8, 4)


def test_4_returns_a_python_float():
    assert isinstance(compression_ratio(32, 32, 3, 4, 4), float)


def test_5_larger_factor_raises_the_ratio():
    assert compression_ratio(64, 64, 3, 8, 4) > compression_ratio(64, 64, 3, 4, 4)


def test_6_matches_a_hand_computed_value():
    # 64 * 64 * 3 = 12288; latent 8 * 8 * 4 = 256; ratio 48
    assert abs(compression_ratio(64, 64, 3, 8, 4) - 48.0) < 1e-12

