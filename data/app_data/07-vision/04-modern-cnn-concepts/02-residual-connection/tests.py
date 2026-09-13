"""
pytest data/app_data/07-vision/04-modern-cnn-concepts/02-residual-connection/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

residual_block = load_solution(
    f"07-vision/04-modern-cnn-concepts/{Path(__file__).resolve().parent.name}"
).residual_block
conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_matches_input_shape():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(3, 5, 5))
    kernel = rng.normal(size=(3, 3, 3, 3))
    out = residual_block(x, kernel)
    assert out.shape == x.shape


def test_02_zero_kernel_reduces_to_relu_of_x():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(2, 4, 4))
    kernel = np.zeros((2, 2, 3, 3))
    out = residual_block(x, kernel)
    assert np.allclose(out, np.maximum(0.0, x))


# --- Shape / general-case coverage -----------------------------------


def test_03_matches_manual_pad_conv_add_relu():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(2, 6, 6))
    kernel = rng.normal(size=(2, 2, 3, 3))
    out = residual_block(x, kernel)
    manual_conv = conv2d_multi_filter(np.pad(x, ((0, 0), (1, 1), (1, 1))), kernel)
    manual = np.maximum(0.0, x + manual_conv)
    assert np.allclose(out, manual)


def test_04_more_channels():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(5, 7, 7))
    kernel = rng.normal(size=(5, 5, 3, 3))
    out = residual_block(x, kernel)
    assert out.shape == (5, 7, 7)


# --- Parameter handling -------------------------------------------------


def test_05_output_never_negative_after_relu():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(3, 5, 5))
    kernel = rng.normal(size=(3, 3, 3, 3))
    out = residual_block(x, kernel)
    assert np.all(out >= 0.0)


# --- Edge cases ---------------------------------------------------------


def test_06_single_channel_smallest_valid_input():
    x = np.array([[[1.0, -2.0, 3.0], [-1.0, 0.5, -0.5], [2.0, -3.0, 1.0]]])
    kernel = np.zeros((1, 1, 3, 3))
    out = residual_block(x, kernel)
    assert out.shape == (1, 3, 3)
    assert np.allclose(out, np.maximum(0.0, x))


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(5)
    x = rng.normal(size=(2, 5, 5))
    kernel = rng.normal(size=(2, 2, 3, 3))
    x_copy, kernel_copy = x.copy(), kernel.copy()
    residual_block(x, kernel)
    assert np.array_equal(x, x_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_conv_padding1_plus_skip_plus_relu_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.tensor(...)      # shape (2, 4, 4)
    #   kernel = torch.tensor(...) # shape (2, 2, 3, 3)
    #   c = torch.nn.functional.conv2d(x[None], kernel, padding=1)[0]
    #   out = torch.relu(x + c)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    x = np.array(
        [
            [
                [-0.1320, -0.1254, 0.3443, -0.4519],
                [-0.8888, -0.3526, -1.3373, 0.5223],
                [-1.1118, -0.7171, 1.0426, -1.2510],
                [-0.5107, -0.3843, -0.4899, 0.5306],
            ],
            [
                [-0.4929, -0.2625, -0.1610, -0.8372],
                [-1.2945, -0.2623, -0.5353, 1.3466],
                [-2.7361, 1.9106, 0.4924, -0.6921],
                [-0.6944, -0.2125, 0.2362, -1.2438],
            ],
        ]
    )
    kernel = np.array(
        [
            [
                [[-0.1243, 0.3991, -0.3595], [0.4583, -1.0828, -0.6006], [0.0555, 0.7082, -0.8722]],
                [[0.6665, 0.6810, 0.4522], [-0.9402, 0.1808, -0.5538], [1.5044, 0.5993, 2.2986]],
            ],
            [
                [[-0.8951, -2.7441, 1.7111], [1.2434, -0.7915, -0.1689], [-1.0491, 0.4409, 0.0227]],
                [[0.0385, 1.2419, -0.3072], [-0.1767, -0.7352, -0.4283], [0.2923, -0.6721, 1.4264]],
            ],
        ]
    )
    expected = np.array(
        [
            [
                [0.0000, 0.0000, 1.8245, 0.4928],
                [2.3245, 0.0000, 2.0601, 0.0000],
                [0.0000, 0.2335, 0.0000, 0.8867],
                [0.0000, 0.0000, 2.7277, 0.0000],
            ],
            [
                [0.2036, 0.0000, 2.0062, 1.1642],
                [4.2064, 0.0367, 0.0000, 0.0000],
                [0.0000, 0.0000, 0.5785, 5.0845],
                [0.0000, 6.5802, 0.0000, 0.2589],
            ],
        ]
    )

    out = residual_block(x, kernel)
    assert np.allclose(out, expected, atol=1e-2)
