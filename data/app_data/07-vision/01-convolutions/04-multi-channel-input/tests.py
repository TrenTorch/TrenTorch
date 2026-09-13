"""
pytest data/app_data/07-vision/01-convolutions/04-multi-channel-input/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_channel = load_solution(
    f"07-vision/01-convolutions/{Path(__file__).resolve().parent.name}"
).conv2d_multi_channel
conv2d_single_filter = load_solution(
    "07-vision/01-convolutions/01-single-filter-conv2d"
).conv2d_single_filter


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_single_channel_matches_conv2d_single_filter():
    # C_in=1 must reduce exactly to 01-single-filter-conv2d.
    image = np.random.default_rng(0).normal(size=(1, 5, 5))
    kernel = np.random.default_rng(1).normal(size=(1, 3, 3))
    out = conv2d_multi_channel(image, kernel)
    expected = conv2d_single_filter(image[0], kernel[0])
    assert np.allclose(out, expected)


def test_02_two_channels_sums_both_channel_convolutions():
    image = np.random.default_rng(2).normal(size=(2, 5, 5))
    kernel = np.random.default_rng(3).normal(size=(2, 3, 3))
    out = conv2d_multi_channel(image, kernel)
    expected = conv2d_single_filter(image[0], kernel[0]) + conv2d_single_filter(image[1], kernel[1])
    assert np.allclose(out, expected)


# --- Shape / general-case coverage -----------------------------------


def test_03_output_shape_ignores_channel_count():
    image = np.random.default_rng(4).normal(size=(5, 6, 6))
    kernel = np.random.default_rng(5).normal(size=(5, 3, 3))
    out = conv2d_multi_channel(image, kernel)
    assert out.shape == (4, 4)


# --- Edge cases ---------------------------------------------------------


def test_04_zero_kernel_on_one_channel_ignores_that_channel():
    image = np.random.default_rng(6).normal(size=(2, 4, 4))
    kernel = np.zeros((2, 3, 3))
    kernel[0] = np.random.default_rng(7).normal(size=(3, 3))
    out = conv2d_multi_channel(image, kernel)
    expected = conv2d_single_filter(image[0], kernel[0])
    assert np.allclose(out, expected)


def test_05_many_channels_accumulate_correctly():
    # 10 channels, each contributing a known constant sum -- output
    # must be exactly 10x a single channel's contribution.
    image = np.ones((10, 3, 3))
    kernel = np.ones((10, 3, 3))
    out = conv2d_multi_channel(image, kernel)
    assert out.shape == (1, 1)
    assert np.isclose(out[0, 0], 10 * 9)


# --- Array hygiene ------------------------------------------------------


def test_06_does_not_mutate_its_inputs():
    image = np.random.default_rng(8).normal(size=(3, 5, 5))
    kernel = np.random.default_rng(9).normal(size=(3, 3, 3))
    image_copy, kernel_copy = image.copy(), kernel.copy()
    conv2d_multi_channel(image, kernel)
    assert np.array_equal(image, image_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_07_matches_real_pytorch_multi_channel_conv2d_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(3)
    #   image = torch.randn(2, 4, 4)
    #   kernel = torch.randn(2, 3, 3)
    #   out = torch.nn.functional.conv2d(image[None], kernel[None])[0, 0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [
                [-0.0766, 0.3599, -0.782, 0.0715],
                [0.6648, -0.2868, 1.6206, -1.5967],
                [-0.0517, -0.306, 0.2485, -0.2226],
                [0.9132, 0.2043, 0.574, 0.4163],
            ],
            [
                [0.2615, 0.9311, -0.5145, -1.6517],
                [1.046, 0.5222, -0.1668, 0.053],
                [0.5638, 2.2566, 1.8693, -1.1952],
                [0.9979, 0.4592, 2.4364, -0.1468],
            ],
        ]
    )
    kernel = np.array(
        [
            [[-0.476, -0.2929, -0.377], [-0.1437, 0.648, -2.3256], [1.2683, -0.2483, 0.6197]],
            [[1.9097, -1.6483, 0.829], [-0.8373, -0.5296, 1.3544], [1.3778, 0.6238, 1.1436]],
        ]
    )
    expected = np.array([[-2.177931, 8.135857], [6.161778, 0.163587]])
    out = conv2d_multi_channel(image, kernel)
    assert np.allclose(out, expected, atol=1e-3)
