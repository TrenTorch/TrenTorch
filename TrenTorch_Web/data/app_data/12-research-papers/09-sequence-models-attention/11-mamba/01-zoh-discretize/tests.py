"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/11-mamba/01-zoh-discretize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mamba-zoh-discretize")
zoh_discretize = _module.zoh_discretize


import math


def test_1_hand_value():
    A_bar, B_bar = zoh_discretize(-1.0, 2.0, 1.0)
    assert abs(A_bar - math.exp(-1.0)) < 1e-12
    assert abs(B_bar - (1 - math.exp(-1.0)) * 2.0) < 1e-12


def test_2_zero_step_keeps_the_state():
    A_bar, _ = zoh_discretize(-2.0, 1.0, 0.0)
    assert abs(A_bar - 1.0) < 1e-12


def test_3_stable_state_decays():
    A_bar, _ = zoh_discretize(-3.0, 1.0, 0.5)
    assert 0 < A_bar < 1


def test_4_input_gain_vanishes_as_step_goes_to_zero():
    _, B_bar = zoh_discretize(-1.0, 1.0, 1e-6)
    assert abs(B_bar) < 1e-5


def test_5_returns_two_floats():
    a, b = zoh_discretize(-1.0, 1.0, 0.1)
    assert isinstance(a, float) and isinstance(b, float)


def test_6_matches_definition_of_zoh_integral():
    A, B, d = -0.5, 3.0, 2.0
    _, B_bar = zoh_discretize(A, B, d)
    assert abs(B_bar - (math.exp(d * A) - 1) / A * B) < 1e-12

