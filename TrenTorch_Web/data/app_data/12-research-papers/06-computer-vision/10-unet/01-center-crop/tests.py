"""
pytest data/app_data/12-research-papers/06-computer-vision/10-unet/01-center-crop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-unet-crop")
center_crop = _module.center_crop


import numpy as np


def test_1_crops_the_center():
    x = np.arange(16.0).reshape(4, 4)
    np.testing.assert_allclose(center_crop(x, 2, 2), [[5.0, 6.0], [9.0, 10.0]])


def test_2_full_size_crop_is_the_input():
    x = np.arange(9.0).reshape(3, 3)
    np.testing.assert_allclose(center_crop(x, 3, 3), x)


def test_3_keeps_channel_axis():
    assert center_crop(np.ones((6, 6, 3)), 2, 2).shape == (2, 2, 3)


def test_4_output_shape_is_requested_size():
    assert center_crop(np.zeros((10, 8)), 4, 6).shape == (4, 6)


def test_5_crop_is_a_view_of_the_center_values():
    x = np.arange(25.0).reshape(5, 5)
    assert center_crop(x, 1, 1)[0, 0] == x[2, 2]


def test_6_does_not_mutate_input():
    x = np.ones((4, 4))
    center_crop(x, 2, 2)
    np.testing.assert_array_equal(x, np.ones((4, 4)))

