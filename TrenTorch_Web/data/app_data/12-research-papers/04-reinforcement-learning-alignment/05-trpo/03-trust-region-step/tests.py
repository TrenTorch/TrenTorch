"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/05-trpo/03-trust-region-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-trpo-step-size")
trust_region_step_size = _module.trust_region_step_size


import math


def test_1_matches_a_hand_value():
    assert abs(trust_region_step_size(1.0, 2.0) - 1.0) < 1e-12


def test_2_doubling_the_limit_scales_by_sqrt_two():
    assert abs(trust_region_step_size(2.0, 1.0) / trust_region_step_size(1.0, 1.0) - math.sqrt(2)) < 1e-12


def test_3_steeper_curvature_gives_smaller_steps():
    assert trust_region_step_size(1.0, 10.0) < trust_region_step_size(1.0, 1.0)


def test_4_result_satisfies_the_quadratic_constraint():
    beta = trust_region_step_size(0.5, 4.0)
    assert abs(0.5 * beta**2 * 4.0 - 0.5) < 1e-12


def test_5_returns_a_float():
    assert isinstance(trust_region_step_size(1.0, 1.0), float)


def test_6_step_is_positive():
    assert trust_region_step_size(0.1, 3.0) > 0

