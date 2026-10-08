"""
pytest data/app_data/12-research-papers/06-computer-vision/07-ddpm/02-linear-schedule/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ddpm-linear-schedule")
alpha_bars = _module.alpha_bars


import numpy as np


def test_1_length_is_the_step_count():
    assert len(alpha_bars(50, 1e-4, 0.02)) == 50


def test_2_first_value_is_one_minus_first_beta():
    assert abs(alpha_bars(10, 0.1, 0.2)[0] - 0.9) < 1e-12


def test_3_values_decrease_over_time():
    ab = alpha_bars(100, 1e-4, 0.02)
    assert np.all(np.diff(ab) < 0)


def test_4_values_stay_in_unit_interval():
    ab = alpha_bars(100, 1e-4, 0.02)
    assert np.all(ab > 0) and np.all(ab <= 1)


def test_5_two_step_hand_value():
    # betas = [0.1, 0.2]: cumprod(1 - beta) = [0.9, 0.72]
    np.testing.assert_allclose(alpha_bars(2, 0.1, 0.2), [0.9, 0.72])


def test_6_returns_an_array():
    assert isinstance(alpha_bars(3, 0.1, 0.2), np.ndarray)

