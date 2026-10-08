"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/01-vae/02-kl-standard-normal/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vae-kl")
kl_std_normal = _module.kl_std_normal


import numpy as np


def test_1_matches_the_prior_gives_zero():
    assert abs(kl_std_normal(np.zeros(3), np.zeros(3))) < 1e-12


def test_2_hand_value_for_unit_mean_shift():
    # -0.5 * (1 + 0 - 1 - 1) = 0.5
    assert abs(kl_std_normal(np.array([1.0]), np.array([0.0])) - 0.5) < 1e-12


def test_3_kl_is_nonnegative():
    rng = np.random.default_rng(0)
    assert kl_std_normal(rng.normal(size=5), rng.normal(size=5)) >= -1e-12


def test_4_sums_over_latent_dimensions():
    one = kl_std_normal(np.array([1.0]), np.array([0.0]))
    two = kl_std_normal(np.array([1.0, 1.0]), np.array([0.0, 0.0]))
    assert abs(two - 2 * one) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(kl_std_normal(np.zeros(1), np.zeros(1)), float)


def test_6_does_not_mutate_inputs():
    mu = np.array([0.5])
    kl_std_normal(mu, np.zeros(1))
    np.testing.assert_array_equal(mu, [0.5])

