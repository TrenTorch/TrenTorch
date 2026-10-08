"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/12-dpo/02-dpo-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dpo-loss")
dpo_loss = _module.dpo_loss


import math

import numpy as np


def test_1_zero_margin_gives_log_two():
    assert abs(float(dpo_loss(0.0)) - math.log(2.0)) < 1e-12


def test_2_large_positive_margin_gives_near_zero_loss():
    assert float(dpo_loss(40.0)) < 1e-10


def test_3_large_negative_margin_gives_large_loss():
    assert float(dpo_loss(-40.0)) > 39.0


def test_4_loss_decreases_as_margin_grows():
    assert float(dpo_loss(2.0)) < float(dpo_loss(1.0))


def test_5_works_on_arrays():
    out = dpo_loss(np.array([0.0, 0.0]))
    np.testing.assert_allclose(out, [math.log(2.0), math.log(2.0)])


def test_6_matches_negative_log_sigmoid():
    m = 0.7
    expected = -math.log(1 / (1 + math.exp(-m)))
    assert abs(float(dpo_loss(m)) - expected) < 1e-12

