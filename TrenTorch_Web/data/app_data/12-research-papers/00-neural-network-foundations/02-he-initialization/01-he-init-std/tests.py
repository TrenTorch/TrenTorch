"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/02-he-initialization/01-he-init-std/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-he-init-std")
he_init_std = _module.he_init_std


def test_1_standard_deviation_for_fan_in_eight():
    assert abs(he_init_std(8) - 0.5) < 1e-12


def test_2_larger_fan_in_gives_smaller_std():
    assert he_init_std(256) < he_init_std(16)


def test_3_fan_in_two_gives_std_of_one():
    assert abs(he_init_std(2) - 1.0) < 1e-12


def test_4_returns_a_float():
    assert isinstance(he_init_std(10), float)


def test_5_variance_is_twice_the_inverse_fan_in():
    s = he_init_std(50)
    assert abs(s * s - 2.0 / 50) < 1e-12


def test_6_matches_a_hand_computed_value():
    # sqrt(2/32) = sqrt(0.0625) = 0.25
    assert abs(he_init_std(32) - 0.25) < 1e-12

