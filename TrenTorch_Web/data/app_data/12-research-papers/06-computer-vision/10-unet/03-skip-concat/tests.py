"""
pytest data/app_data/12-research-papers/06-computer-vision/10-unet/03-skip-concat/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-unet-skip-concat")
skip_concat = _module.skip_concat


import numpy as np


def test_1_channels_add_up():
    assert skip_concat(np.zeros((2, 2, 3)), np.zeros((2, 2, 5))).shape == (2, 2, 8)


def test_2_encoder_channels_come_first():
    out = skip_concat(np.ones((1, 1, 1)), np.zeros((1, 1, 1)))
    np.testing.assert_allclose(out[0, 0], [1.0, 0.0])


def test_3_spatial_size_is_unchanged():
    assert skip_concat(np.zeros((4, 4, 1)), np.zeros((4, 4, 2))).shape[:2] == (4, 4)


def test_4_values_are_preserved():
    e = np.array([[[1.0]]])
    d = np.array([[[2.0]]])
    np.testing.assert_allclose(skip_concat(e, d), [[[1.0, 2.0]]])


def test_5_works_with_one_channel_each():
    assert skip_concat(np.zeros((3, 3, 1)), np.zeros((3, 3, 1))).shape == (3, 3, 2)


def test_6_does_not_mutate_inputs():
    e = np.ones((1, 1, 1))
    skip_concat(e, np.ones((1, 1, 1)))
    np.testing.assert_array_equal(e, np.ones((1, 1, 1)))

