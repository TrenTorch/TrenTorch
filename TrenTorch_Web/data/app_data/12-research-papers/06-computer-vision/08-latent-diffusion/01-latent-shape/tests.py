"""
pytest data/app_data/12-research-papers/06-computer-vision/08-latent-diffusion/01-latent-shape/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ldm-latent-shape")
latent_shape = _module.latent_shape


def test_1_paper_512_image_with_factor_eight_gives_64():
    assert latent_shape(512, 512, 8) == (64, 64)


def test_2_factor_one_keeps_the_size():
    assert latent_shape(100, 60, 1) == (100, 60)


def test_3_height_and_width_are_handled_separately():
    assert latent_shape(256, 128, 4) == (64, 32)


def test_4_returns_a_tuple_of_ints():
    out = latent_shape(64, 64, 8)
    assert isinstance(out, tuple) and all(isinstance(v, int) for v in out)


def test_5_non_divisible_size_floors():
    assert latent_shape(10, 10, 4) == (2, 2)


def test_6_larger_factor_gives_smaller_latents():
    assert latent_shape(512, 512, 16)[0] < latent_shape(512, 512, 8)[0]

