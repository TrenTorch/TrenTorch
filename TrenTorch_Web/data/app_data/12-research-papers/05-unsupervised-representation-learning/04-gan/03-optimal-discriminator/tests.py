"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/04-gan/03-optimal-discriminator/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gan-optimal-discriminator")
optimal_discriminator = _module.optimal_discriminator


import numpy as np


def test_1_equal_densities_give_one_half():
    np.testing.assert_allclose(optimal_discriminator(np.array([2.0]), np.array([2.0])), [0.5])


def test_2_model_mass_zero_gives_one():
    np.testing.assert_allclose(optimal_discriminator(np.array([0.3]), np.array([0.0])), [1.0])


def test_3_data_mass_zero_gives_zero():
    np.testing.assert_allclose(optimal_discriminator(np.array([0.0]), np.array([0.7])), [0.0])


def test_4_values_lie_in_unit_interval():
    out = optimal_discriminator(np.array([0.1, 0.5, 0.9]), np.array([0.4, 0.4, 0.4]))
    assert np.all(out >= 0) and np.all(out <= 1)


def test_5_hand_value():
    np.testing.assert_allclose(optimal_discriminator(np.array([1.0]), np.array([3.0])), [0.25])


def test_6_does_not_mutate_inputs():
    p = np.array([1.0])
    optimal_discriminator(p, np.array([1.0]))
    np.testing.assert_array_equal(p, [1.0])

