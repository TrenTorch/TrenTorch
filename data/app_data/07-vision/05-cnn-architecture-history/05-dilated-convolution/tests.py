"""
pytest data/app_data/07-vision/05-cnn-architecture-history/05-dilated-convolution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

dilated_conv2d = load_solution(
    f"07-vision/05-cnn-architecture-history/{Path(__file__).resolve().parent.name}"
).dilated_conv2d


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_dilation_1_matches_a_plain_convolution():
    rng = np.random.default_rng(0)
    image = rng.normal(size=(5, 5))
    kernel = rng.normal(size=(3, 3))
    out = dilated_conv2d(image, kernel, dilation=1)
    manual = np.array(
        [
            [np.sum(image[i : i + 3, j : j + 3] * kernel) for j in range(3)]
            for i in range(3)
        ]
    )
    assert out.shape == (3, 3)
    assert np.allclose(out, manual)


def test_02_dilation_2_shrinks_output_more_than_dilation_1():
    rng = np.random.default_rng(1)
    image = rng.normal(size=(7, 7))
    kernel = rng.normal(size=(3, 3))
    out_d1 = dilated_conv2d(image, kernel, dilation=1)
    out_d2 = dilated_conv2d(image, kernel, dilation=2)
    assert out_d1.shape == (5, 5)
    assert out_d2.shape == (3, 3)


# --- Shape / general-case coverage -----------------------------------


def test_03_effective_kernel_size_formula():
    # A (kH, kW) kernel with dilation d spans (kH-1)*d + 1 pixels -- a 3x3
    # kernel at dilation 3 spans 7 pixels, same as a 7x7 plain kernel would.
    image = np.arange(9 * 9, dtype=float).reshape(9, 9)
    kernel = np.zeros((3, 3))
    kernel[0, 0] = 1.0  # picks out exactly the top-left tap of each window
    out = dilated_conv2d(image, kernel, dilation=3)
    assert out.shape == (3, 3)  # 9 - 7 + 1 = 3
    assert np.isclose(out[0, 0], image[0, 0])  # window starts at (0, 0); top-left tap = image[0, 0]
    assert np.isclose(out[1, 1], image[1, 1])  # window starts at (1, 1); top-left tap = image[1, 1]


def test_04_only_the_dilated_taps_contribute_not_the_skipped_pixels():
    image = np.zeros((5, 5))
    image[0, 0] = 10.0  # sits exactly on a dilated tap
    image[0, 1] = 999.0  # sits BETWEEN taps at dilation=2, must be skipped
    kernel = np.ones((3, 3))
    out = dilated_conv2d(image, kernel, dilation=2)
    assert out.shape == (1, 1)
    assert np.isclose(out[0, 0], 10.0)  # the skipped 999 never enters the sum


# --- Parameter handling -------------------------------------------------


def test_05_zero_kernel_gives_all_zero_output_regardless_of_dilation():
    rng = np.random.default_rng(2)
    image = rng.normal(size=(6, 6))
    kernel = np.zeros((3, 3))
    assert np.allclose(dilated_conv2d(image, kernel, dilation=2), 0.0)


# --- Edge cases ---------------------------------------------------------


def test_06_smallest_valid_input_for_a_given_dilation():
    # A 3x3 kernel at dilation 2 needs at least a 5x5 image (eff size 5).
    image = np.arange(25, dtype=float).reshape(5, 5)
    kernel = np.zeros((3, 3))
    kernel[1, 1] = 1.0  # picks out the exact center tap
    out = dilated_conv2d(image, kernel, dilation=2)
    assert out.shape == (1, 1)
    assert np.isclose(out[0, 0], image[2, 2])


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(3)
    image = rng.normal(size=(7, 7))
    kernel = rng.normal(size=(3, 3))
    image_copy, kernel_copy = image.copy(), kernel.copy()
    dilated_conv2d(image, kernel, dilation=2)
    assert np.array_equal(image, image_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_dilated_conv2d_at_dilation_1_and_2_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.randn(1, 1, 7, 7)
    #   kernel = torch.randn(1, 1, 3, 3)
    #   out1 = torch.nn.functional.conv2d(x, kernel, dilation=1)
    #   out2 = torch.nn.functional.conv2d(x, kernel, dilation=2)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [-0.2386, -1.0934, 0.1558, 0.1750, -0.9526, -0.5442, 1.1985],
            [0.9604, -1.1074, -0.8403, -0.0020, 0.2240, 0.8766, -0.5379],
            [-0.2994, 0.9785, 1.5818, -0.2637, -0.8172, 1.4276, 1.7598],
            [1.1749, 0.2644, -0.6843, 1.3014, -0.0108, -0.5931, 0.7040],
            [-0.4759, -0.0982, 0.2107, -0.2471, -0.5589, 0.4677, -0.6218],
            [-0.6322, 0.0812, -0.3079, 0.7399, -0.6557, -0.7039, 2.3700],
            [-1.5539, -1.0817, -0.7842, 0.8656, -2.4925, -1.6823, 0.8697],
        ]
    )
    kernel = np.array([[-0.0263, 0.9403, 0.2149], [-0.9623, 0.1157, -1.0072], [1.1443, -0.5288, -1.3037]])
    expected_d1 = np.array(
        [
            [-4.1166, 1.8104, 3.5534, -3.6031, -3.7858],
            [-0.3421, -2.2867, -2.1183, 1.3886, -0.7346],
            [0.0898, -0.1410, 1.4552, -1.7080, 0.8986],
            [-0.0601, -0.7119, 1.6823, 1.6413, -2.6558],
            [0.7097, -2.6630, 2.5787, 4.0044, -4.6129],
        ]
    )
    expected_d2 = np.array([[1.3150, -2.9250, -2.6839], [-1.6720, 1.3285, -3.0299], [4.2510, 0.1254, -0.7863]])

    out_d1 = dilated_conv2d(image, kernel, dilation=1)
    out_d2 = dilated_conv2d(image, kernel, dilation=2)
    assert np.allclose(out_d1, expected_d1, atol=1e-2)
    assert np.allclose(out_d2, expected_d2, atol=1e-2)
