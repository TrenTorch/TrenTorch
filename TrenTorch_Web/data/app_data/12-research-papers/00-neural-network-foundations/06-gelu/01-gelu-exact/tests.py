"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/06-gelu/01-gelu-exact/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gelu-exact")
gelu_exact = _module.gelu_exact


import math

import numpy as np


def test_1_gelu_of_zero_is_zero():
    assert abs(float(gelu_exact(0.0))) < 1e-12


def test_2_large_positive_inputs_pass_through():
    assert abs(float(gelu_exact(10.0)) - 10.0) < 1e-6


def test_3_large_negative_inputs_go_to_zero():
    assert abs(float(gelu_exact(-10.0))) < 1e-6


def test_4_matches_a_known_value():
    # Phi(1) = 0.8413447..., so GELU(1) = 0.8413447...
    assert abs(float(gelu_exact(1.0)) - 0.8413447460685429) < 1e-9


def test_5_keeps_array_shape():
    assert gelu_exact(np.ones((2, 3))).shape == (2, 3)


def test_6_is_monotone_on_the_positive_side():
    values = gelu_exact(np.array([0.5, 1.0, 2.0]))
    assert np.all(np.diff(values) > 0)

