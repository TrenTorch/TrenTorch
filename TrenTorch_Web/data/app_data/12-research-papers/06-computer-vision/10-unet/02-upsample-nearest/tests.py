"""
pytest data/app_data/12-research-papers/06-computer-vision/10-unet/02-upsample-nearest/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-unet-upsample")
upsample_nearest = _module.upsample_nearest


import numpy as np


def test_1_doubles_height_and_width():
    assert upsample_nearest(np.zeros((2, 3)), 2).shape == (4, 6)


def test_2_repeats_each_value_into_a_block():
    out = upsample_nearest(np.array([[1.0, 2.0]]), 2)
    np.testing.assert_allclose(out, [[1.0, 1.0, 2.0, 2.0], [1.0, 1.0, 2.0, 2.0]])


def test_3_factor_one_is_the_identity():
    x = np.arange(4.0).reshape(2, 2)
    np.testing.assert_allclose(upsample_nearest(x, 1), x)


def test_4_keeps_channels():
    assert upsample_nearest(np.ones((2, 2, 3)), 2).shape == (4, 4, 3)


def test_5_mean_is_preserved():
    x = np.array([[1.0, 3.0]])
    assert abs(upsample_nearest(x, 4).mean() - x.mean()) < 1e-12


def test_6_does_not_mutate_input():
    x = np.ones((1, 1))
    upsample_nearest(x, 2)
    np.testing.assert_array_equal(x, [[1.0]])

