"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/01-vae/03-elbo/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vae-elbo")
elbo = _module.elbo


def test_1_zero_kl_returns_the_reconstruction():
    assert elbo(-3.0, 0.0) == -3.0


def test_2_matches_a_hand_value():
    assert abs(elbo(-2.0, 0.5) - (-2.5)) < 1e-12


def test_3_larger_kl_lowers_the_bound():
    assert elbo(-1.0, 2.0) < elbo(-1.0, 1.0)


def test_4_better_reconstruction_raises_the_bound():
    assert elbo(-0.5, 1.0) > elbo(-2.0, 1.0)


def test_5_returns_a_float_for_scalars():
    assert isinstance(elbo(-1.0, 1.0), float)


def test_6_negative_loss_is_the_bound_to_minimize():
    assert -elbo(-2.0, 0.5) == 2.5

