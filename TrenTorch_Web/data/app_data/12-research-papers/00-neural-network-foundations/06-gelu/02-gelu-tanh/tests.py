"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/06-gelu/02-gelu-tanh/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gelu-tanh")
gelu_tanh = _module.gelu_tanh


import math

import numpy as np


def exact(v):
    return v * 0.5 * (1.0 + math.erf(v / math.sqrt(2.0)))


def test_1_zero_maps_to_zero():
    assert abs(float(gelu_tanh(0.0))) < 1e-12


def test_2_close_to_exact_gelu_on_a_grid():
    xs = np.linspace(-3, 3, 61)
    approx = gelu_tanh(xs)
    truth = np.array([exact(v) for v in xs])
    assert np.max(np.abs(approx - truth)) < 1e-3


def test_3_large_positive_inputs_pass_through():
    assert abs(float(gelu_tanh(10.0)) - 10.0) < 1e-6


def test_4_large_negative_inputs_go_to_zero():
    assert abs(float(gelu_tanh(-10.0))) < 1e-6


def test_5_keeps_array_shape():
    assert gelu_tanh(np.ones((4, 2))).shape == (4, 2)


def test_6_does_not_mutate_input():
    x = np.array([1.0, -1.0])
    gelu_tanh(x)
    np.testing.assert_array_equal(x, [1.0, -1.0])

