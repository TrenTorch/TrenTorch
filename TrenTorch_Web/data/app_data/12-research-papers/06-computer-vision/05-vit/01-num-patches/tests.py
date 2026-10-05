"""
pytest data/app_data/12-research-papers/06-computer-vision/05-vit/01-num-patches/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vit-num-patches")
num_patches = _module.num_patches


def test_1_standard_vit_has_196_patches():
    assert num_patches(224, 16) == 196


def test_2_patch_equal_to_image_gives_one():
    assert num_patches(32, 32) == 1


def test_3_smaller_patches_mean_more_tokens():
    assert num_patches(64, 8) > num_patches(64, 16)


def test_4_returns_an_integer():
    assert isinstance(num_patches(10, 2), int)


def test_5_non_divisible_size_drops_the_remainder():
    assert num_patches(10, 4) == 4


def test_6_grows_quadratically_with_resolution():
    assert num_patches(128, 16) == 4 * num_patches(64, 16)

