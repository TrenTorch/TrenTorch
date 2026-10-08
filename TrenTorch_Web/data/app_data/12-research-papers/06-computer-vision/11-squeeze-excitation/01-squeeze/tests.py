"""
pytest data/app_data/12-research-papers/06-computer-vision/11-squeeze-excitation/01-squeeze/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-se-squeeze")
squeeze = _module.squeeze


import numpy as np


def test_1_output_has_one_value_per_channel():
    assert squeeze(np.ones((3, 4, 5))).shape == (5,)


def test_2_channel_averages_are_correct():
    x = np.zeros((2, 2, 2))
    x[:, :, 1] = 4.0
    np.testing.assert_allclose(squeeze(x), [0.0, 4.0])


def test_3_constant_map_returns_the_constant():
    np.testing.assert_allclose(squeeze(np.full((2, 2, 3), 7.0)), [7.0, 7.0, 7.0])


def test_4_single_pixel_returns_that_pixel():
    np.testing.assert_allclose(squeeze(np.array([[[1.0, 2.0]]])), [1.0, 2.0])


def test_5_spatial_size_does_not_change_uniform_result():
    assert np.allclose(squeeze(np.full((2, 2, 1), 3.0)), squeeze(np.full((8, 8, 1), 3.0)))


def test_6_does_not_mutate_input():
    x = np.ones((2, 2, 1))
    squeeze(x)
    np.testing.assert_array_equal(x, np.ones((2, 2, 1)))

