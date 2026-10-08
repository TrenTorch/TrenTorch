"""
pytest data/app_data/12-research-papers/06-computer-vision/07-ddpm/03-noise-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ddpm-noise-loss")
noise_prediction_loss = _module.noise_prediction_loss


import numpy as np


def test_1_perfect_prediction_gives_zero():
    e = np.array([1.0, -1.0])
    assert noise_prediction_loss(e, e) == 0.0


def test_2_hand_value():
    assert abs(noise_prediction_loss(np.array([0.0, 0.0]), np.array([1.0, 3.0])) - 5.0) < 1e-12


def test_3_predicting_zero_costs_the_noise_power():
    e = np.array([2.0, 2.0])
    assert abs(noise_prediction_loss(e, np.zeros(2)) - 4.0) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(noise_prediction_loss(np.ones(2), np.zeros(2)), float)


def test_5_symmetric_in_its_arguments():
    a = np.array([1.0, 2.0])
    b = np.array([3.0, 0.0])
    assert noise_prediction_loss(a, b) == noise_prediction_loss(b, a)


def test_6_does_not_mutate_inputs():
    e = np.array([1.0])
    noise_prediction_loss(e, np.zeros(1))
    np.testing.assert_array_equal(e, [1.0])

