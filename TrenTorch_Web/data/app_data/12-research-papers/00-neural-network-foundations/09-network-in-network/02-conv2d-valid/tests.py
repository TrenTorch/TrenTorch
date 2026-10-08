"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/09-network-in-network/02-conv2d-valid/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-nin-conv2d-valid")
conv2d_valid = _module.conv2d_valid


import numpy as np


def test_1_output_shape_is_valid_size():
    out = conv2d_valid(np.ones((5, 6)), np.ones((3, 2)))
    assert out.shape == (3, 5)


def test_2_all_ones_kernel_sums_each_window():
    img = np.arange(9.0).reshape(3, 3)
    out = conv2d_valid(img, np.ones((2, 2)))
    np.testing.assert_allclose(out, [[8.0, 12.0], [20.0, 24.0]])


def test_3_identity_kernel_crops_the_image():
    img = np.arange(16.0).reshape(4, 4)
    out = conv2d_valid(img, np.array([[1.0]]))
    np.testing.assert_allclose(out, img)


def test_4_kernel_of_full_size_gives_one_value():
    img = np.array([[1.0, 2.0], [3.0, 4.0]])
    out = conv2d_valid(img, img)
    np.testing.assert_allclose(out, [[30.0]])


def test_5_is_cross_correlation_not_flipped():
    img = np.array([[1.0, 2.0, 3.0]])
    out = conv2d_valid(img, np.array([[1.0, 0.0]]))
    np.testing.assert_allclose(out, [[1.0, 2.0]])


def test_6_does_not_mutate_inputs():
    img = np.ones((3, 3))
    conv2d_valid(img, np.ones((2, 2)))
    np.testing.assert_array_equal(img, np.ones((3, 3)))

