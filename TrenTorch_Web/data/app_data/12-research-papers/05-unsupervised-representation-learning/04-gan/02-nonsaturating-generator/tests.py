"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/04-gan/02-nonsaturating-generator/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gan-generator-loss")
gan_generator_loss = _module.gan_generator_loss


import math

import numpy as np


def test_1_chance_discriminator_gives_log_two():
    assert abs(gan_generator_loss(np.full(2, 0.5)) - math.log(2.0)) < 1e-12


def test_2_fully_fooled_discriminator_gives_zero():
    assert abs(gan_generator_loss(np.array([1.0]))) < 1e-12


def test_3_loss_falls_as_the_discriminator_is_fooled():
    assert gan_generator_loss(np.array([0.9])) < gan_generator_loss(np.array([0.1]))


def test_4_returns_a_python_float():
    assert isinstance(gan_generator_loss(np.array([0.3])), float)


def test_5_averages_over_samples():
    out = gan_generator_loss(np.array([0.5, 0.25]))
    assert abs(out - (-(math.log(0.5) + math.log(0.25)) / 2)) < 1e-12


def test_6_does_not_mutate_inputs():
    d = np.array([0.4])
    gan_generator_loss(d)
    np.testing.assert_array_equal(d, [0.4])

