"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/01-vae/01-reparameterize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vae-reparameterize")
reparameterize = _module.reparameterize


import numpy as np


def test_1_zero_noise_returns_the_mean():
    np.testing.assert_allclose(reparameterize(np.array([1.0, -2.0]), np.zeros(2), np.zeros(2)), [1.0, -2.0])


def test_2_zero_log_variance_adds_the_noise_directly():
    np.testing.assert_allclose(reparameterize(np.array([0.0]), np.array([0.0]), np.array([1.0])), [1.0])


def test_3_log_variance_two_scales_noise_by_e():
    out = reparameterize(np.array([0.0]), np.array([2.0]), np.array([1.0]))
    np.testing.assert_allclose(out, [np.e])


def test_4_keeps_the_shape():
    assert reparameterize(np.zeros((3, 2)), np.zeros((3, 2)), np.ones((3, 2))).shape == (3, 2)


def test_5_is_linear_in_the_noise():
    a = reparameterize(np.zeros(1), np.zeros(1), np.array([1.0]))
    b = reparameterize(np.zeros(1), np.zeros(1), np.array([2.0]))
    np.testing.assert_allclose(b, 2 * a)


def test_6_does_not_mutate_inputs():
    mu = np.array([1.0])
    reparameterize(mu, np.zeros(1), np.ones(1))
    np.testing.assert_array_equal(mu, [1.0])

