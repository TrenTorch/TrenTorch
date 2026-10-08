"""
pytest data/app_data/12-research-papers/01-optimization-and-training/09-large-minibatch/02-warmup/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-goyal-warmup")
gradual_warmup_lr = _module.gradual_warmup_lr


def test_1_mid_warmup():
    assert abs(gradual_warmup_lr(0.4, 2, 4) - 0.2) < 1e-12


def test_2_after_warmup_holds_target():
    assert abs(gradual_warmup_lr(0.4, 10, 4) - 0.4) < 1e-12


def test_3_at_end_of_warmup_is_target():
    assert abs(gradual_warmup_lr(0.4, 4, 4) - 0.4) < 1e-12


def test_4_is_nondecreasing():
    vals = [gradual_warmup_lr(1.0, t, 5) for t in range(1, 10)]
    assert all(b >= a for a, b in zip(vals, vals[1:]))


def test_5_first_step_is_fraction_of_target():
    assert abs(gradual_warmup_lr(1.0, 1, 4) - 0.25) < 1e-12


def test_6_zero_target_stays_zero():
    assert gradual_warmup_lr(0.0, 3, 5) == 0.0

