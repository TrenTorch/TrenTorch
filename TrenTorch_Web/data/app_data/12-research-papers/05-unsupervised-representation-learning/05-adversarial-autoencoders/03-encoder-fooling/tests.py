"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/05-adversarial-autoencoders/03-encoder-fooling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-aae-encoder-loss")
encoder_fooling_loss = _module.encoder_fooling_loss


import math

import numpy as np


def test_1_discriminator_convinced_gives_zero():
    assert abs(encoder_fooling_loss(np.array([1.0]))) < 1e-12


def test_2_chance_gives_log_two():
    assert abs(encoder_fooling_loss(np.array([0.5])) - math.log(2.0)) < 1e-12


def test_3_lower_discriminator_score_gives_higher_loss():
    assert encoder_fooling_loss(np.array([0.1])) > encoder_fooling_loss(np.array([0.9]))


def test_4_returns_a_python_float():
    assert isinstance(encoder_fooling_loss(np.array([0.3])), float)


def test_5_averages_over_codes():
    out = encoder_fooling_loss(np.array([0.5, 0.25]))
    assert abs(out - (-(math.log(0.5) + math.log(0.25)) / 2)) < 1e-12


def test_6_does_not_mutate_inputs():
    d = np.array([0.6])
    encoder_fooling_loss(d)
    np.testing.assert_array_equal(d, [0.6])

