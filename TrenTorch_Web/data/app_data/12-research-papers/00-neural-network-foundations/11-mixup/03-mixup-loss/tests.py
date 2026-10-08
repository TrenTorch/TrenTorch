"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/11-mixup/03-mixup-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mixup-loss")
mixup_loss = _module.mixup_loss


import numpy as np


def test_1_lam_one_returns_the_first_loss():
    assert abs(mixup_loss(2.0, 5.0, 1.0) - 2.0) < 1e-12


def test_2_lam_zero_returns_the_second_loss():
    assert abs(mixup_loss(2.0, 5.0, 0.0) - 5.0) < 1e-12


def test_3_equal_losses_are_unchanged_by_lam():
    assert abs(mixup_loss(3.0, 3.0, 0.37) - 3.0) < 1e-12


def test_4_lam_half_averages_the_losses():
    assert abs(mixup_loss(2.0, 4.0, 0.5) - 3.0) < 1e-12


def test_5_works_on_numpy_arrays():
    out = mixup_loss(np.array([1.0, 2.0]), np.array([3.0, 4.0]), 0.25)
    np.testing.assert_allclose(out, [2.5, 3.5])


def test_6_is_a_convex_combination():
    val = mixup_loss(1.0, 9.0, 0.75)
    assert 1.0 <= val <= 9.0

