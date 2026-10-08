"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/07-swish/02-swish-derivative/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-swish-derivative")
swish_derivative = _module.swish_derivative


import numpy as np


def swish_numeric(x, beta):
    return x / (1.0 + np.exp(-beta * x))


def test_1_derivative_at_zero_is_one_half():
    assert abs(float(swish_derivative(0.0)) - 0.5) < 1e-12


def test_2_matches_a_finite_difference():
    h = 1e-6
    xs = np.array([-2.0, -0.4, 0.7, 2.5])
    numeric = (swish_numeric(xs + h, 1.5) - swish_numeric(xs - h, 1.5)) / (2 * h)
    np.testing.assert_allclose(swish_derivative(xs, beta=1.5), numeric, atol=1e-6)


def test_3_derivative_approaches_one_for_large_positive_inputs():
    assert abs(float(swish_derivative(30.0)) - 1.0) < 1e-6


def test_4_derivative_approaches_zero_for_large_negative_inputs():
    assert abs(float(swish_derivative(-30.0))) < 1e-6


def test_5_beta_changes_the_derivative():
    assert not np.isclose(swish_derivative(1.0, beta=1.0), swish_derivative(1.0, beta=3.0))


def test_6_keeps_array_shape():
    assert swish_derivative(np.zeros((2, 3))).shape == (2, 3)

