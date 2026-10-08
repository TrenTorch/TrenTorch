"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/07-swish/01-swish-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-swish-forward")
swish = _module.swish


import numpy as np


def test_1_swish_of_zero_is_zero():
    assert abs(float(swish(0.0))) < 1e-12


def test_2_matches_a_known_value_at_one():
    # 1 * sigmoid(1) = 0.7310585786
    assert abs(float(swish(1.0)) - 0.7310585786300049) < 1e-9


def test_3_large_positive_inputs_pass_through():
    assert abs(float(swish(20.0)) - 20.0) < 1e-6


def test_4_large_negative_inputs_go_to_zero():
    assert abs(float(swish(-20.0))) < 1e-6


def test_5_beta_controls_the_gate_sharpness():
    assert abs(float(swish(1.0, beta=100.0)) - 1.0) < 1e-6


def test_6_keeps_array_shape():
    assert swish(np.ones((2, 2))).shape == (2, 2)

