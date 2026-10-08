"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/06-gelu/03-gelu-derivative/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gelu-derivative")
gelu_derivative = _module.gelu_derivative


import math

import numpy as np


def test_1_derivative_at_zero_is_one_half():
    assert abs(float(gelu_derivative(0.0)) - 0.5) < 1e-12


def test_2_matches_a_finite_difference():
    h = 1e-5
    xs = np.array([-2.0, -0.5, 0.3, 1.7])
    numeric = (gelu_exact_scalar(xs + h) - gelu_exact_scalar(xs - h)) / (2 * h)
    np.testing.assert_allclose(gelu_derivative(xs), numeric, atol=1e-6)


def test_3_derivative_approaches_one_for_large_positive_inputs():
    assert abs(float(gelu_derivative(10.0)) - 1.0) < 1e-6


def test_4_derivative_approaches_zero_for_large_negative_inputs():
    assert abs(float(gelu_derivative(-10.0))) < 1e-6


def test_5_keeps_array_shape():
    assert gelu_derivative(np.zeros((3, 2))).shape == (3, 2)


def test_6_matches_a_known_value_at_one():
    # Phi(1) + 1 * phi(1) = 0.8413447 + 0.2419707 = 1.0833155
    assert abs(float(gelu_derivative(1.0)) - 1.0833154705) < 1e-6


def gelu_exact_scalar(xs):
    return np.array([v * 0.5 * (1.0 + math.erf(v / math.sqrt(2.0))) for v in xs])

