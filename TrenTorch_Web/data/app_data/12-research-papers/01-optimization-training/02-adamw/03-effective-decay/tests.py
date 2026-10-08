"""
pytest data/app_data/12-research-papers/01-optimization-and-training/02-adamw/03-effective-decay/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adamw-effective-decay")
effective_decay = _module.effective_decay


def test_1_one_step_shrink():
    assert abs(effective_decay(0.1, 0.5, 1) - 0.95) < 1e-12


def test_2_two_steps_compound():
    assert abs(effective_decay(0.1, 0.5, 2) - 0.9025) < 1e-12


def test_3_zero_steps_keep_everything():
    assert effective_decay(0.1, 0.5, 0) == 1.0


def test_4_zero_decay_keeps_everything():
    assert effective_decay(0.1, 0.0, 50) == 1.0


def test_5_more_steps_decay_more():
    assert effective_decay(0.1, 0.5, 10) < effective_decay(0.1, 0.5, 5)


def test_6_returns_a_float():
    assert isinstance(effective_decay(0.1, 0.5, 3), float)

