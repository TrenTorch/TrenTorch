"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/04-gan/01-discriminator-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gan-discriminator-loss")
gan_discriminator_loss = _module.gan_discriminator_loss


import math

import numpy as np


def test_1_chance_discriminator_gives_two_log_two():
    assert abs(gan_discriminator_loss(np.full(3, 0.5), np.full(3, 0.5)) - 2 * math.log(2.0)) < 1e-12


def test_2_perfect_discriminator_has_near_zero_loss():
    assert gan_discriminator_loss(np.array([1 - 1e-9]), np.array([1e-9])) < 1e-6


def test_3_fooled_discriminator_has_large_loss():
    assert gan_discriminator_loss(np.array([1e-6]), np.array([1 - 1e-6])) > 10.0


def test_4_returns_a_python_float():
    assert isinstance(gan_discriminator_loss(np.array([0.5]), np.array([0.5])), float)


def test_5_worse_discriminator_has_higher_loss():
    a = gan_discriminator_loss(np.array([0.2]), np.array([0.8]))
    b = gan_discriminator_loss(np.array([0.8]), np.array([0.2]))
    assert a > b


def test_6_does_not_mutate_inputs():
    d = np.array([0.5])
    gan_discriminator_loss(d, np.array([0.5]))
    np.testing.assert_array_equal(d, [0.5])

