"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/04-distillation/03-combined-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-distill-combined-loss")
combined_loss = _module.combined_loss


def test_1_alpha_zero_returns_the_hard_loss():
    assert abs(combined_loss(2.0, 5.0, 0.0) - 2.0) < 1e-12


def test_2_alpha_one_returns_the_soft_loss():
    assert abs(combined_loss(2.0, 5.0, 1.0) - 5.0) < 1e-12


def test_3_alpha_half_averages_the_two():
    assert abs(combined_loss(2.0, 4.0, 0.5) - 3.0) < 1e-12


def test_4_result_lies_between_the_two_losses():
    v = combined_loss(1.0, 9.0, 0.3)
    assert 1.0 <= v <= 9.0


def test_5_equal_losses_are_unchanged_by_alpha():
    assert abs(combined_loss(3.0, 3.0, 0.9) - 3.0) < 1e-12


def test_6_returns_a_float():
    assert isinstance(combined_loss(1.0, 2.0, 0.5), float)

