"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/07-swish/03-swish-vs-relu-gap/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-swish-vs-relu-gap")
swish_relu_gap = _module.swish_relu_gap


import numpy as np


def test_1_gap_is_zero_at_x_equal_zero():
    assert abs(swish_relu_gap(np.array([0.0]))) < 1e-12


def test_2_gap_is_small_for_large_beta_on_positive_inputs():
    assert swish_relu_gap(np.array([1.0, 2.0, 5.0]), beta=100.0) < 1e-6


def test_3_gap_is_nonzero_when_beta_is_one():
    assert swish_relu_gap(np.array([1.0])) > 0.1


def test_4_returns_a_python_float():
    assert isinstance(swish_relu_gap(np.array([1.0])), float)


def test_5_is_symmetric_difference_magnitude():
    # At x=1 with beta=1: swish = 0.731, relu = 1 -> gap 0.2689...
    assert abs(swish_relu_gap(np.array([1.0])) - 0.2689414213699951) < 1e-9


def test_6_does_not_mutate_input():
    x = np.array([-1.0, 1.0])
    swish_relu_gap(x)
    np.testing.assert_array_equal(x, [-1.0, 1.0])

