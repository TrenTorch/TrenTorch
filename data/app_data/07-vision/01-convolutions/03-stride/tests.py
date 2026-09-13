"""
pytest data/app_data/07-vision/01-convolutions/03-stride/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_with_stride = load_solution(
    f"07-vision/01-convolutions/{Path(__file__).resolve().parent.name}"
).conv2d_with_stride


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_stride_1_matches_plain_convolution():
    image = np.random.default_rng(0).normal(size=(5, 5))
    kernel = np.random.default_rng(1).normal(size=(3, 3))
    out_stride1 = conv2d_with_stride(image, kernel, stride=1)
    out_h = image.shape[0] - kernel.shape[0] + 1
    manual = np.array(
        [
            [np.sum(image[i : i + 3, j : j + 3] * kernel) for j in range(out_h)]
            for i in range(out_h)
        ]
    )
    assert np.allclose(out_stride1, manual)


def test_02_stride_2_output_shape():
    image = np.zeros((7, 7))
    kernel = np.zeros((3, 3))
    out = conv2d_with_stride(image, kernel, stride=2)
    assert out.shape == (3, 3)


# --- Shape / general-case coverage -----------------------------------


def test_03_stride_2_skips_every_other_position():
    # An image that's 1 only along even rows/cols, otherwise 0, with a
    # 1x1 kernel: stride=1 sees every value, stride=2 only ever samples
    # positions 0, 2, 4, ... -- always landing on a 1.
    image = np.zeros((5, 5))
    image[::2, ::2] = 1.0
    kernel = np.array([[1.0]])
    out = conv2d_with_stride(image, kernel, stride=2)
    assert np.allclose(out, 1.0)


def test_04_large_stride_gives_single_output():
    image = np.random.default_rng(2).normal(size=(6, 6))
    kernel = np.random.default_rng(3).normal(size=(3, 3))
    out = conv2d_with_stride(image, kernel, stride=4)
    assert out.shape == (1, 1)
    assert np.isclose(out[0, 0], np.sum(image[0:3, 0:3] * kernel))


# --- Edge cases ---------------------------------------------------------


def test_05_stride_equal_to_kernel_size_gives_non_overlapping_patches():
    image = np.arange(16.0).reshape(4, 4)
    kernel = np.ones((2, 2))
    out = conv2d_with_stride(image, kernel, stride=2)
    assert out.shape == (2, 2)
    assert np.isclose(out[0, 0], image[0:2, 0:2].sum())
    assert np.isclose(out[1, 1], image[2:4, 2:4].sum())


# --- Array hygiene ------------------------------------------------------


def test_06_does_not_mutate_its_inputs():
    image = np.random.default_rng(4).normal(size=(6, 6))
    kernel = np.random.default_rng(5).normal(size=(3, 3))
    image_copy, kernel_copy = image.copy(), kernel.copy()
    conv2d_with_stride(image, kernel, stride=2)
    assert np.array_equal(image, image_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_07_matches_real_pytorch_strided_conv2d_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(2)
    #   image = torch.randn(7, 7)
    #   kernel = torch.randn(3, 3)
    #   out = torch.nn.functional.conv2d(image[None, None], kernel[None, None], stride=2)[0, 0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [-1.0408, 0.9166, -1.3042, -1.1097, -1.2188, 1.1676, -1.0574],
            [-0.1188, -0.9078, 0.3452, -0.5713, -0.2351, 1.0076, -0.7529],
            [-0.225, -0.4327, -1.5071, -0.4586, -0.848, 0.5266, 0.0299],
            [-0.0498, 1.0651, 0.886, 0.464, -0.4986, 0.1289, 2.7631],
            [0.1405, 1.1191, 0.3152, 1.7528, -0.765, 0.3157, -1.6036],
            [1.8493, 0.0447, 1.5853, -0.5912, 1.1312, 0.9466, -1.2023],
            [-0.5833, -0.4407, -1.9791, 0.7787, -0.7749, -0.1398, -0.3467],
        ]
    )
    kernel = np.array(
        [
            [0.6965, -0.2904, 1.0966],
            [-0.3521, -0.1459, 1.5554],
            [-0.0757, 1.1269, -2.6291],
        ]
    )
    expected = np.array(
        [
            [1.781923, -0.49979, -3.003881],
            [-0.021822, 0.960732, 8.373314],
            [6.677672, 3.223963, -3.976748],
        ]
    )
    out = conv2d_with_stride(image, kernel, stride=2)
    assert np.allclose(out, expected, atol=1e-3)
