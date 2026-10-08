"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/08-ddpg/03-ou-noise-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ddpg-ou-step")
ou_step = _module.ou_step


def test_1_no_noise_and_no_reversion_keeps_the_value():
    assert ou_step(2.0, 0.0, 0.0, 0.1, 5.0) == 2.0


def test_2_drift_pulls_toward_zero_without_noise():
    assert abs(ou_step(1.0, 1.0, 0.0, 0.25, 0.0) - 0.75) < 1e-12


def test_3_noise_term_scales_with_sqrt_dt():
    # x = 1, theta = 1, dt = 0.25: drift = -0.25, noise = 1 * 0.5 * 2 = 1.0
    assert abs(ou_step(1.0, 1.0, 1.0, 0.25, 2.0) - 1.75) < 1e-12


def test_4_negative_value_is_pulled_up():
    assert ou_step(-1.0, 1.0, 0.0, 0.5, 0.0) > -1.0


def test_5_returns_a_float_for_scalars():
    assert isinstance(ou_step(0.0, 0.1, 0.1, 0.1, 0.0), float)


def test_6_zero_value_with_zero_noise_stays_zero():
    assert ou_step(0.0, 0.5, 0.0, 0.1, 0.0) == 0.0

