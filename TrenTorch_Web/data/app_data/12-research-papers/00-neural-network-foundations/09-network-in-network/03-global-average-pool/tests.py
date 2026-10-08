"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/09-network-in-network/03-global-average-pool/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-nin-global-average-pool")
global_average_pool = _module.global_average_pool


import numpy as np


def test_1_output_has_one_value_per_channel():
    assert global_average_pool(np.ones((4, 5, 3))).shape == (3,)


def test_2_channel_means_are_correct():
    x = np.zeros((2, 2, 2))
    x[:, :, 0] = 1.0
    x[:, :, 1] = 3.0
    np.testing.assert_allclose(global_average_pool(x), [1.0, 3.0])


def test_3_constant_map_returns_the_constant():
    np.testing.assert_allclose(global_average_pool(np.full((3, 3, 2), 7.0)), [7.0, 7.0])


def test_4_single_pixel_map_returns_that_pixel():
    x = np.array([[[4.0, 5.0]]])
    np.testing.assert_allclose(global_average_pool(x), [4.0, 5.0])


def test_5_spatial_size_does_not_change_the_result_for_uniform_maps():
    a = global_average_pool(np.full((2, 2, 1), 2.0))
    b = global_average_pool(np.full((9, 4, 1), 2.0))
    np.testing.assert_allclose(a, b)


def test_6_does_not_mutate_the_input():
    x = np.ones((2, 2, 2))
    global_average_pool(x)
    np.testing.assert_array_equal(x, np.ones((2, 2, 2)))

