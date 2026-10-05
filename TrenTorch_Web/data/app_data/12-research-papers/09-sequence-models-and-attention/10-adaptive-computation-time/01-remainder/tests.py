"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/10-adaptive-computation-time/01-remainder/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-act-remainder")
act_remainder = _module.act_remainder


def test_1_remainder_for_two_steps():
    assert abs(act_remainder([0.3, 0.5]) - 0.7) < 1e-12


def test_2_single_step_has_full_remainder():
    assert act_remainder([0.4]) == 1.0


def test_3_remainder_is_nonnegative_when_halts_sum_below_one():
    assert act_remainder([0.2, 0.3, 0.4]) >= 0


def test_4_returns_a_float():
    assert isinstance(act_remainder([0.5, 0.5]), float)


def test_5_more_early_halting_shrinks_the_remainder():
    assert act_remainder([0.6, 0.1]) < act_remainder([0.1, 0.1])


def test_6_does_not_mutate_halts():
    h = [0.2, 0.3]
    act_remainder(h)
    assert h == [0.2, 0.3]

