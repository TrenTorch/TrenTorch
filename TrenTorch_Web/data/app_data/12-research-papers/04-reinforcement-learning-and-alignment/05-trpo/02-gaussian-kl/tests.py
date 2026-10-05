"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/05-trpo/02-gaussian-kl/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-trpo-gaussian-kl")
gaussian_kl = _module.gaussian_kl


import math


def test_1_identical_gaussians_have_zero_kl():
    assert abs(gaussian_kl(1.0, 2.0, 1.0, 2.0)) < 1e-12


def test_2_hand_value_for_shifted_mean():
    # (1 + 1) / 2 - 0.5 = 0.5
    assert abs(gaussian_kl(0.0, 1.0, 1.0, 1.0) - 0.5) < 1e-12


def test_3_kl_is_nonnegative():
    assert gaussian_kl(0.0, 1.0, 3.0, 0.5) >= 0


def test_4_kl_is_not_symmetric():
    assert abs(gaussian_kl(0.0, 1.0, 0.0, 2.0) - gaussian_kl(0.0, 2.0, 0.0, 1.0)) > 1e-6


def test_5_returns_a_float():
    assert isinstance(gaussian_kl(0.0, 1.0, 0.0, 1.0), float)


def test_6_matches_the_scale_formula():
    # KL(N(0,1) || N(0,2)) = log 2 + 1/8 - 1/2
    assert abs(gaussian_kl(0.0, 1.0, 0.0, 2.0) - (math.log(2.0) + 0.125 - 0.5)) < 1e-12

