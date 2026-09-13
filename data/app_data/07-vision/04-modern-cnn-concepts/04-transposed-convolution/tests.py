"""
pytest data/app_data/07-vision/04-modern-cnn-concepts/04-transposed-convolution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv_transpose2d = load_solution(
    f"07-vision/04-modern-cnn-concepts/{Path(__file__).resolve().parent.name}"
).conv_transpose2d


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_stride_1():
    x = np.zeros((1, 3, 3))
    kernel = np.zeros((1, 1, 2, 2))
    out = conv_transpose2d(x, kernel, stride=1)
    assert out.shape == (1, 4, 4)  # (3-1)*1 + 2 = 4


def test_02_output_shape_stride_2_is_much_larger():
    x = np.zeros((1, 3, 3))
    kernel = np.zeros((1, 1, 2, 2))
    out = conv_transpose2d(x, kernel, stride=2)
    assert out.shape == (1, 6, 6)  # (3-1)*2 + 2 = 6


# --- Shape / general-case coverage -----------------------------------


def test_03_single_nonzero_pixel_places_a_scaled_copy_of_the_kernel():
    x = np.zeros((1, 3, 3))
    x[0, 1, 1] = 2.0
    kernel = np.array([[[[1.0, 2.0], [3.0, 4.0]]]])
    out = conv_transpose2d(x, kernel, stride=1)
    expected = np.zeros((4, 4))
    expected[1:3, 1:3] = 2.0 * np.array([[1.0, 2.0], [3.0, 4.0]])
    assert np.allclose(out[0], expected)


def test_04_stride_greater_than_kernel_size_gives_no_overlap():
    x = np.array([[[1.0, 1.0], [1.0, 1.0]]])
    kernel = np.ones((1, 1, 2, 2))
    out = conv_transpose2d(x, kernel, stride=3)
    # (2-1)*3 + 2 = 5 -> each 2x2 block sits in its own non-overlapping tile
    assert out.shape == (1, 5, 5)
    assert np.allclose(out[0, 0:2, 0:2], 1.0)
    assert np.allclose(out[0, 3:5, 3:5], 1.0)
    assert np.allclose(out[0, 2, :], 0.0)  # gap row between tiles


# --- Parameter handling -------------------------------------------------


def test_05_overlapping_windows_sum_rather_than_overwrite():
    x = np.ones((1, 2, 2))
    kernel = np.ones((1, 1, 2, 2))
    out = conv_transpose2d(x, kernel, stride=1)
    # the single interior output pixel receives contributions from all 4 input pixels
    assert out.shape == (1, 3, 3)
    assert np.isclose(out[0, 1, 1], 4.0)


# --- Edge cases ---------------------------------------------------------


def test_06_zero_kernel_gives_all_zero_output():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(1, 3, 3))
    kernel = np.zeros((1, 1, 2, 2))
    out = conv_transpose2d(x, kernel, stride=1)
    assert np.allclose(out, 0.0)


def test_07_single_pixel_input_just_reproduces_a_scaled_kernel():
    x = np.array([[[3.0]]])
    kernel = np.array([[[[1.0, -1.0], [2.0, 0.5]]]])
    out = conv_transpose2d(x, kernel, stride=1)
    assert out.shape == (1, 2, 2)
    assert np.allclose(out[0], 3.0 * kernel[0, 0])


# --- Array hygiene ------------------------------------------------------


def test_08_does_not_mutate_its_inputs():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(1, 3, 3))
    kernel = rng.normal(size=(1, 1, 2, 2))
    x_copy, kernel_copy = x.copy(), kernel.copy()
    conv_transpose2d(x, kernel, stride=2)
    assert np.array_equal(x, x_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_09_matches_real_pytorch_conv_transpose2d_stride1_and_stride2_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.randn(1, 3, 3)
    #   kernel = torch.randn(1, 1, 2, 2)
    #   out1 = torch.nn.functional.conv_transpose2d(x[None], kernel, stride=1)[0]
    #   out2 = torch.nn.functional.conv_transpose2d(x[None], kernel, stride=2)[0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    x = np.array([[-1.0141, -0.3720, -0.7516], [-0.8623, -0.3270, 0.5212], [1.2622, -1.4680, -0.1037]]).reshape(
        1, 3, 3
    )
    kernel = np.array([0.5177, -1.0845, -2.0901, -0.1508]).reshape(1, 1, 2, 2)
    expected_stride1 = np.array(
        [
            [-0.5250, 0.9072, 0.0143, 0.8151],
            [1.6732, 1.6963, 2.2515, -0.4519],
            [2.4557, -1.3153, 0.4983, 0.0339],
            [-2.6381, 2.8778, 0.4382, 0.0156],
        ]
    )
    expected_stride2 = np.array(
        [
            [-0.5250, 1.0998, -0.1926, 0.4035, -0.3891, 0.8151],
            [2.1196, 0.1530, 0.7776, 0.0561, 1.5709, 0.1134],
            [-0.4464, 0.9351, -0.1693, 0.3547, 0.2698, -0.5652],
            [1.8022, 0.1301, 0.6835, 0.0493, -1.0893, -0.0786],
            [0.6535, -1.3688, -0.7600, 1.5920, -0.0537, 0.1125],
            [-2.6381, -0.1904, 3.0682, 0.2214, 0.2168, 0.0156],
        ]
    )

    out1 = conv_transpose2d(x, kernel, stride=1)
    out2 = conv_transpose2d(x, kernel, stride=2)
    assert np.allclose(out1[0], expected_stride1, atol=1e-2)
    assert np.allclose(out2[0], expected_stride2, atol=1e-2)
