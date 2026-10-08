"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/07-scaling-laws/03-ratio-for-size-increase/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-scaling-ratio")
loss_ratio_for_size_increase = _module.loss_ratio_for_size_increase


import numpy as np


def test_1_no_growth_leaves_loss_unchanged():
    assert abs(float(loss_ratio_for_size_increase(1.0, 0.3)) - 1.0) < 1e-12


def test_2_ten_times_growth_matches_the_formula():
    assert abs(float(loss_ratio_for_size_increase(10.0, 0.5)) - 10 ** -0.5) < 1e-12


def test_3_growth_always_reduces_loss():
    assert float(loss_ratio_for_size_increase(2.0, 0.1)) < 1.0


def test_4_array_of_factors_keeps_shape():
    assert loss_ratio_for_size_increase(np.array([1.0, 2.0, 4.0]), 0.2).shape == (3,)


def test_5_two_doublings_compound():
    once = float(loss_ratio_for_size_increase(2.0, 0.07))
    twice = float(loss_ratio_for_size_increase(4.0, 0.07))
    assert abs(twice - once * once) < 1e-12


def test_6_zero_alpha_means_no_gain():
    assert abs(float(loss_ratio_for_size_increase(100.0, 0.0)) - 1.0) < 1e-12

