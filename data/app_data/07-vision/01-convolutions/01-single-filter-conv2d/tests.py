"""
pytest data/app_data/07-vision/01-convolutions/01-single-filter-conv2d/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_single_filter = load_solution(
    f"07-vision/01-convolutions/{Path(__file__).resolve().parent.name}"
).conv2d_single_filter


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matches_hand_computed_3x3_on_4x4():
    image = np.array(
        [
            [1.0, 2.0, 3.0, 0.0],
            [0.0, 1.0, 2.0, 3.0],
            [3.0, 0.0, 1.0, 2.0],
            [2.0, 3.0, 0.0, 1.0],
        ]
    )
    kernel = np.ones((3, 3))
    out = conv2d_single_filter(image, kernel)
    assert out.shape == (2, 2)
    assert np.allclose(out, [[13.0, 14.0], [12.0, 13.0]])


def test_02_identity_kernel_extracts_center_pixel():
    # A kernel that is 1 at its center and 0 elsewhere just copies the
    # pixel under that center -- the simplest possible sanity check that
    # positions line up correctly.
    image = np.arange(16.0).reshape(4, 4)
    kernel = np.zeros((3, 3))
    kernel[1, 1] = 1.0
    out = conv2d_single_filter(image, kernel)
    assert np.allclose(out, image[1:3, 1:3])


# --- Shape / general-case coverage -----------------------------------


def test_03_output_shape_for_non_square_image_and_kernel():
    image = np.random.default_rng(0).normal(size=(6, 8))
    kernel = np.random.default_rng(1).normal(size=(2, 3))
    out = conv2d_single_filter(image, kernel)
    assert out.shape == (5, 6)


def test_04_kernel_same_size_as_image_gives_single_output():
    image = np.random.default_rng(2).normal(size=(4, 4))
    kernel = np.random.default_rng(3).normal(size=(4, 4))
    out = conv2d_single_filter(image, kernel)
    assert out.shape == (1, 1)
    assert np.isclose(out[0, 0], np.sum(image * kernel))


# --- Edge cases ---------------------------------------------------------


def test_05_1x1_kernel_is_a_pure_scale():
    image = np.random.default_rng(4).normal(size=(3, 3))
    kernel = np.array([[2.5]])
    out = conv2d_single_filter(image, kernel)
    assert np.allclose(out, image * 2.5)


def test_06_zero_kernel_gives_all_zero_output():
    image = np.random.default_rng(5).normal(size=(5, 5))
    kernel = np.zeros((2, 2))
    out = conv2d_single_filter(image, kernel)
    assert np.allclose(out, 0.0)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    image = np.random.default_rng(6).normal(size=(5, 5))
    kernel = np.random.default_rng(7).normal(size=(3, 3))
    image_copy, kernel_copy = image.copy(), kernel.copy()
    conv2d_single_filter(image, kernel)
    assert np.array_equal(image, image_copy)
    assert np.array_equal(kernel, kernel_copy)


def test_08_no_flip_this_is_cross_correlation_not_true_convolution():
    # A mutant that flips the kernel (true mathematical convolution)
    # gives a different, wrong answer for any asymmetric kernel -- this
    # is the single most common conv-vs-correlation bug.
    image = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    kernel = np.array([[1.0, 2.0], [3.0, 4.0]])
    out = conv2d_single_filter(image, kernel)
    # image's only nonzero pixel (1.0 at [0,0]) lines up under the
    # kernel's own [0,0] entry with no flip -- output[0,0] must be 1*1=1,
    # not 1*4 (which a flipped-kernel implementation would give).
    assert np.isclose(out[0, 0], 1.0)


# --- Independent correctness oracle -----------------------------------


def test_09_matches_real_pytorch_conv2d_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(0)
    #   image = torch.randn(5, 5)
    #   kernel = torch.randn(3, 3)
    #   out = torch.nn.functional.conv2d(image[None, None], kernel[None, None])[0, 0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [-1.1258, -1.1524, -0.2506, -0.4339, 0.8487],
            [0.692, -0.316, -2.1152, 0.3223, -0.1577],
            [1.4437, 0.266, 0.1665, 0.8744, -0.1435],
            [-0.1116, -0.6136, 1.259, 2.005, 0.0537],
            [0.6181, -0.4128, -0.8411, -2.316, -0.1023],
        ]
    )
    kernel = np.array(
        [
            [0.7455, -0.246, 0.8512],
            [-0.3502, 1.6881, -2.1575],
            [-1.3927, -0.3611, 1.874],
        ]
    )
    expected = np.array(
        [
            [1.223803, -4.114126, 1.450837],
            [1.113753, 3.017806, -2.439815],
            [-4.848448, -4.54551, 4.430755],
        ]
    )
    out = conv2d_single_filter(image, kernel)
    assert np.allclose(out, expected, atol=1e-3)
