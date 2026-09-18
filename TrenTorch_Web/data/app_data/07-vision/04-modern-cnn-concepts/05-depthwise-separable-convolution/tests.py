"""
pytest data/app_data/07-vision/04-modern-cnn-concepts/05-depthwise-separable-convolution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

depthwise_separable_conv2d = load_solution(
    f"07-vision/04-modern-cnn-concepts/{Path(__file__).resolve().parent.name}"
).depthwise_separable_conv2d
conv2d_single_filter = load_solution("07-vision/01-convolutions/01-single-filter-conv2d").conv2d_single_filter
pointwise_conv = load_solution("07-vision/04-modern-cnn-concepts/03-1x1-convolution").pointwise_conv


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(3, 5, 5))
    dw_kernel = rng.normal(size=(3, 1, 3, 3))
    pw_kernel = rng.normal(size=(2, 3, 1, 1))
    out = depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    assert out.shape == (2, 3, 3)  # 5 - 3 + 1 = 3 spatial, 2 output channels


def test_02_matches_manual_depthwise_then_pointwise():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(3, 6, 6))
    dw_kernel = rng.normal(size=(3, 1, 3, 3))
    pw_kernel = rng.normal(size=(4, 3, 1, 1))
    out = depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    manual_depth = np.stack([conv2d_single_filter(x[c], dw_kernel[c, 0]) for c in range(3)])
    manual = pointwise_conv(manual_depth, pw_kernel)
    assert np.allclose(out, manual)


# --- Shape / general-case coverage -----------------------------------


def test_03_depthwise_stage_never_mixes_channels():
    # Changing channel 1 of x should never affect channel 0's contribution
    # to the depthwise stage -- verify by zeroing out every other channel's
    # depthwise kernel and confirming only that channel's own filter matters.
    rng = np.random.default_rng(2)
    x = rng.normal(size=(2, 5, 5))
    dw_kernel = rng.normal(size=(2, 1, 3, 3))
    pw_kernel = np.array([1.0, 0.0]).reshape(1, 2, 1, 1)  # keep only channel 0 after mixing
    out = depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    expected_channel0_only = conv2d_single_filter(x[0], dw_kernel[0, 0])
    assert np.allclose(out[0], expected_channel0_only)


def test_04_more_channels_and_a_larger_kernel():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(4, 8, 8))
    dw_kernel = rng.normal(size=(4, 1, 3, 3))
    pw_kernel = rng.normal(size=(6, 4, 1, 1))
    out = depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    assert out.shape == (6, 6, 6)


# --- Edge cases ---------------------------------------------------------


def test_05_single_input_channel_single_output_channel():
    x = np.array([[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]])
    dw_kernel = np.ones((1, 1, 2, 2))
    pw_kernel = np.array([[[[1.0]]]])
    out = depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    expected = conv2d_single_filter(x[0], dw_kernel[0, 0])
    assert np.allclose(out[0], expected)


def test_06_zero_pointwise_kernel_zeroes_everything_regardless_of_depthwise():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(3, 5, 5))
    dw_kernel = rng.normal(size=(3, 1, 3, 3))
    pw_kernel = np.zeros((2, 3, 1, 1))
    out = depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    assert np.allclose(out, 0.0)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(5)
    x = rng.normal(size=(3, 5, 5))
    dw_kernel = rng.normal(size=(3, 1, 3, 3))
    pw_kernel = rng.normal(size=(2, 3, 1, 1))
    x_copy, dw_copy, pw_copy = x.copy(), dw_kernel.copy(), pw_kernel.copy()
    depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    assert np.array_equal(x, x_copy)
    assert np.array_equal(dw_kernel, dw_copy)
    assert np.array_equal(pw_kernel, pw_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_grouped_conv_plus_1x1_conv_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.randn(1, 3, 5, 5)
    #   dw_kernel = torch.randn(3, 1, 3, 3)
    #   pw_kernel = torch.randn(2, 3, 1, 1)
    #   depth_out = torch.nn.functional.conv2d(x, dw_kernel, groups=3)
    #   final_out = torch.nn.functional.conv2d(depth_out, pw_kernel)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    x = np.array(
        [
            [-0.8400, 0.1480, -0.7602, -0.7541, -0.8892],
            [-1.0300, 1.1966, -0.4049, -0.0139, 0.7910],
            [-1.6170, 0.6401, 2.0462, -0.0539, -0.4271],
            [1.2244, 0.0005, 0.8331, -1.9352, 0.9091],
            [-1.6828, 0.5918, 1.1327, -0.9156, -1.3644],
        ]
    )
    x = np.stack(
        [
            x,
            np.array(
                [
                    [0.1373, -1.8883, 0.1025, -1.4345, 0.6464],
                    [-0.8127, 0.7841, -1.2800, 0.4713, -2.2912],
                    [-0.4770, -0.1602, -1.3734, 0.1952, -0.4472],
                    [-1.3145, -1.5120, 1.0178, 0.7160, -0.4094],
                    [1.3782, 0.7494, -0.0796, 0.0860, 0.1205],
                ]
            ),
            np.array(
                [
                    [0.9457, -0.9155, -0.1852, -0.0918, -0.1893],
                    [0.9851, 1.1524, -0.3296, -2.1022, -0.6090],
                    [2.2966, 0.0479, 2.4029, 2.7426, -0.9772],
                    [0.6720, 0.8640, -0.9375, 0.7897, -0.7149],
                    [1.6006, -0.2858, 0.2204, -3.1498, -0.9193],
                ]
            ),
        ]
    )
    dw_kernel = np.array(
        [
            [[-1.1588, -2.4849, 0.8468], [-1.7822, 2.6635, 1.5463], [0.5250, 0.4639, 1.0016]],
            [[0.0109, 0.2192, -0.3726], [0.6705, 0.0065, 0.7629], [0.0004, 1.0932, 0.5288]],
            [[-0.8571, -0.3402, 1.2437], [0.3551, -0.3648, 0.1964], [-0.0212, -0.5334, -2.3640]],
        ]
    ).reshape(3, 1, 3, 3)
    pw_kernel = np.array([0.6369, -0.3886, -1.0909, 0.4938, -1.2419, 1.1922]).reshape(2, 3, 1, 1)
    expected = np.array(
        [
            [[12.0662, 6.9515, 2.7243], [3.7535, 6.7041, -3.1954], [0.2379, -15.6067, -4.8107]],
            [[-1.4375, -8.7191, 7.7153], [7.4261, -6.4039, -0.2865], [-0.1887, 10.5135, -6.6976]],
        ]
    )

    out = depthwise_separable_conv2d(x, dw_kernel, pw_kernel)
    assert np.allclose(out, expected, atol=1e-2)
