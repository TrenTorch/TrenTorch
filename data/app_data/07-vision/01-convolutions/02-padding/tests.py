"""
pytest data/app_data/07-vision/01-convolutions/02-padding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_with_padding = load_solution(
    f"07-vision/01-convolutions/{Path(__file__).resolve().parent.name}"
).conv2d_with_padding


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_valid_matches_unpadded_conv():
    image = np.random.default_rng(0).normal(size=(5, 5))
    kernel = np.random.default_rng(1).normal(size=(3, 3))
    out = conv2d_with_padding(image, kernel, padding="valid")
    assert out.shape == (3, 3)


def test_02_same_output_shape_equals_input_shape():
    image = np.random.default_rng(2).normal(size=(6, 6))
    kernel = np.random.default_rng(3).normal(size=(3, 3))
    out = conv2d_with_padding(image, kernel, padding="same")
    assert out.shape == image.shape


# --- Shape / general-case coverage -----------------------------------


def test_03_same_with_1x1_kernel_is_a_no_op_shape():
    image = np.random.default_rng(4).normal(size=(4, 4))
    kernel = np.array([[1.0]])
    out = conv2d_with_padding(image, kernel, padding="same")
    assert out.shape == (4, 4)
    assert np.allclose(out, image)


def test_04_same_with_5x5_kernel_pads_more():
    image = np.random.default_rng(5).normal(size=(7, 7))
    kernel = np.random.default_rng(6).normal(size=(5, 5))
    out = conv2d_with_padding(image, kernel, padding="same")
    assert out.shape == (7, 7)


# --- Edge cases ---------------------------------------------------------


def test_05_same_padding_border_uses_zeros():
    # The corner output, under "same", sees mostly zero-padding -- an
    # all-ones kernel there should sum only the real pixels that
    # actually overlap, treating everything outside the image as 0.
    image = np.ones((3, 3))
    kernel = np.ones((3, 3))
    out = conv2d_with_padding(image, kernel, padding="same")
    assert np.isclose(out[0, 0], 4.0)  # only the 2x2 real overlap contributes
    assert np.isclose(out[1, 1], 9.0)  # full kernel overlap in the center


def test_06_invalid_padding_mode_raises():
    import pytest

    image = np.zeros((4, 4))
    kernel = np.zeros((3, 3))
    with pytest.raises(ValueError):
        conv2d_with_padding(image, kernel, padding="banana")


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    image = np.random.default_rng(7).normal(size=(5, 5))
    kernel = np.random.default_rng(8).normal(size=(3, 3))
    image_copy, kernel_copy = image.copy(), kernel.copy()
    conv2d_with_padding(image, kernel, padding="same")
    assert np.array_equal(image, image_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_same_padding_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(1)
    #   image = torch.randn(5, 5)
    #   kernel = torch.randn(3, 3)
    #   out = torch.nn.functional.conv2d(image[None, None], kernel[None, None], padding='same')[0, 0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [-1.5256, -0.7502, -0.654, -1.6095, -0.1002],
            [-0.6092, -0.9798, -1.6091, -0.7121, 1.1712],
            [1.7674, -0.0954, 0.1394, -1.5785, -0.3206],
            [-0.2993, 1.8793, 0.3357, 0.2753, 1.7163],
            [-0.0561, 0.9107, -1.3924, 2.6891, -0.111],
        ]
    )
    kernel = np.array(
        [
            [-0.1103, 0.2913, 0.5848],
            [0.2149, -0.409, -0.1663],
            [0.6696, 0.1177, -0.3584],
        ]
    )
    expected = np.array(
        [
            [1.028186, 0.141192, -0.216321, -1.046621, -0.643872],
            [-0.228806, 1.226957, 0.035248, -0.68217, -1.57841],
            [-2.166217, -0.863105, 0.607117, 1.025912, 0.59797],
            [-0.064058, -0.461332, -1.169053, -1.564618, 1.22547],
            [0.883324, 0.623794, 0.369502, -0.33375, 1.092879],
        ]
    )
    out = conv2d_with_padding(image, kernel, padding="same")
    assert np.allclose(out, expected, atol=1e-3)
