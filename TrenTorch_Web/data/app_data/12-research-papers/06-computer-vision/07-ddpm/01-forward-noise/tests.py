"""
pytest data/app_data/12-research-papers/06-computer-vision/07-ddpm/01-forward-noise/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ddpm-forward-noise")
forward_noise = _module.forward_noise


import numpy as np


def test_1_no_noise_budget_returns_the_clean_sample():
    x = np.array([1.0, 2.0])
    np.testing.assert_allclose(forward_noise(x, 1.0, np.array([9.0, 9.0])), x)


def test_2_full_noise_returns_the_noise():
    e = np.array([0.5, -0.5])
    np.testing.assert_allclose(forward_noise(np.array([7.0, 7.0]), 0.0, e), e)


def test_3_hand_value():
    out = forward_noise(np.array([2.0]), 0.25, np.array([4.0]))
    np.testing.assert_allclose(out, [0.5 * 2.0 + np.sqrt(0.75) * 4.0])


def test_4_keeps_the_shape():
    assert forward_noise(np.zeros((2, 3)), 0.5, np.zeros((2, 3))).shape == (2, 3)


def test_5_variance_of_output_is_one_for_unit_data():
    rng = np.random.default_rng(0)
    x0 = rng.normal(size=100000)
    eps = rng.normal(size=100000)
    out = forward_noise(x0, 0.6, eps)
    assert abs(out.var() - 1.0) < 0.02


def test_6_does_not_mutate_inputs():
    x = np.array([1.0])
    forward_noise(x, 0.5, np.array([1.0]))
    np.testing.assert_array_equal(x, [1.0])

