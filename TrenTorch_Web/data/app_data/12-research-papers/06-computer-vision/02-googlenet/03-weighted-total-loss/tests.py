"""
pytest data/app_data/12-research-papers/06-computer-vision/02-googlenet/03-weighted-total-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-googlenet-aux-loss")
weighted_total_loss = _module.weighted_total_loss


def test_1_default_weight_is_point_three():
    assert abs(weighted_total_loss(1.0, 10.0) - 4.0) < 1e-12


def test_2_zero_weight_ignores_the_auxiliary_loss():
    assert weighted_total_loss(2.0, 99.0, w=0.0) == 2.0


def test_3_weight_one_adds_the_losses():
    assert weighted_total_loss(1.0, 2.0, w=1.0) == 3.0


def test_4_auxiliary_loss_increases_the_total():
    assert weighted_total_loss(1.0, 0.5) > weighted_total_loss(1.0, 0.0)


def test_5_returns_a_float_for_floats():
    assert isinstance(weighted_total_loss(1.0, 1.0), float)


def test_6_is_linear_in_the_auxiliary_loss():
    a = weighted_total_loss(0.0, 1.0, w=0.3)
    b = weighted_total_loss(0.0, 2.0, w=0.3)
    assert abs(b - 2 * a) < 1e-12

