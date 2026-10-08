"""
pytest data/app_data/12-research-papers/01-optimization-and-training/09-large-minibatch/01-scaled-lr/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-goyal-scaled-lr")
scaled_lr = _module.scaled_lr


def test_1_hand_case():
    assert abs(scaled_lr(0.1, 1024, 256) - 0.4) < 1e-12


def test_2_same_batch_keeps_learning_rate():
    assert scaled_lr(0.1, 256, 256) == 0.1


def test_3_halving_batch_halves_learning_rate():
    assert abs(scaled_lr(0.2, 128, 256) - 0.1) < 1e-12


def test_4_linear_in_base_lr():
    assert abs(scaled_lr(0.3, 512, 256) - 2 * scaled_lr(0.15, 512, 256)) < 1e-12


def test_5_returns_a_float():
    assert isinstance(scaled_lr(0.1, 512, 256), float)


def test_6_scales_with_batch_ratio():
    assert abs(scaled_lr(0.05, 4096, 256) - 0.8) < 1e-12

