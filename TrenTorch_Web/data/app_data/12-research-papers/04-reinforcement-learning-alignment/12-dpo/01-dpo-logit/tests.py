"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/12-dpo/01-dpo-logit/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dpo-logit")
dpo_logit = _module.dpo_logit


def test_1_policy_equal_to_reference_gives_zero_margin():
    assert dpo_logit(-1.0, -2.0, -1.0, -2.0, 0.5) == 0.0


def test_2_matches_a_hand_value():
    # (0 - -1) - (-2 - -1) = 1 + 1 = 2, times beta 0.5 = 1
    assert abs(dpo_logit(0.0, -2.0, -1.0, -1.0, 0.5) - 1.0) < 1e-12


def test_3_raising_the_winner_increases_the_margin():
    assert dpo_logit(0.0, -1.0, -1.0, -1.0, 1.0) > dpo_logit(-2.0, -1.0, -1.0, -1.0, 1.0)


def test_4_raising_the_loser_decreases_the_margin():
    assert dpo_logit(0.0, 0.0, 0.0, -1.0, 1.0) < dpo_logit(0.0, -1.0, 0.0, -1.0, 1.0)


def test_5_returns_a_float_for_scalars():
    assert isinstance(dpo_logit(0.0, 0.0, 0.0, 0.0, 0.1), float)


def test_6_scales_linearly_with_beta():
    a = dpo_logit(1.0, 0.0, 0.0, 0.0, 1.0)
    b = dpo_logit(1.0, 0.0, 0.0, 0.0, 3.0)
    assert abs(b - 3 * a) < 1e-12

