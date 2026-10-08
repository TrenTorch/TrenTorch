"""
pytest data/app_data/12-research-papers/06-computer-vision/08-latent-diffusion/03-cfg-combine/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ldm-cfg-combine")
cfg_combine = _module.cfg_combine


import numpy as np


def test_1_zero_guidance_returns_the_unconditional_prediction():
    np.testing.assert_allclose(cfg_combine(np.array([1.0]), np.array([5.0]), 0.0), [1.0])


def test_2_unit_guidance_returns_the_conditional_prediction():
    np.testing.assert_allclose(cfg_combine(np.array([1.0]), np.array([5.0]), 1.0), [5.0])


def test_3_hand_value_with_guidance_two():
    np.testing.assert_allclose(cfg_combine(np.array([1.0]), np.array([2.0]), 2.0), [3.0])


def test_4_identical_predictions_are_unchanged():
    e = np.array([0.3, -0.7])
    np.testing.assert_allclose(cfg_combine(e, e, 7.5), e)


def test_5_keeps_the_shape():
    assert cfg_combine(np.zeros((2, 3)), np.ones((2, 3)), 3.0).shape == (2, 3)


def test_6_does_not_mutate_inputs():
    u = np.array([1.0])
    cfg_combine(u, np.array([2.0]), 2.0)
    np.testing.assert_array_equal(u, [1.0])

