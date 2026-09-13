"""
pytest data/app_data/07-vision/04-modern-cnn-concepts/03-1x1-convolution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

pointwise_conv = load_solution(
    f"07-vision/04-modern-cnn-concepts/{Path(__file__).resolve().parent.name}"
).pointwise_conv


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_is_num_filters_by_same_spatial_size():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(4, 5, 5))
    kernel = rng.normal(size=(2, 4, 1, 1))
    out = pointwise_conv(x, kernel)
    assert out.shape == (2, 5, 5)


def test_02_identity_kernel_reproduces_a_single_channel():
    x = np.arange(2 * 3 * 3, dtype=float).reshape(2, 3, 3)
    kernel = np.array([1.0, 0.0]).reshape(1, 2, 1, 1)  # picks out channel 0
    out = pointwise_conv(x, kernel)
    assert np.allclose(out[0], x[0])


# --- Shape / general-case coverage -----------------------------------


def test_03_each_output_pixel_is_independent_linear_combo_of_input_channels():
    x = np.zeros((3, 2, 2))
    x[:, 0, 0] = [1.0, 2.0, 3.0]
    kernel = np.array([2.0, 0.0, -1.0]).reshape(1, 3, 1, 1)
    out = pointwise_conv(x, kernel)
    assert np.isclose(out[0, 0, 0], 2.0 * 1.0 + 0.0 * 2.0 + (-1.0) * 3.0)
    assert np.allclose(out[0, 0, 1], 0.0)
    assert np.allclose(out[0, 1, :], 0.0)


def test_04_multiple_output_filters_stack_independently():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(3, 4, 4))
    kernel = rng.normal(size=(5, 3, 1, 1))
    out = pointwise_conv(x, kernel)
    for f in range(5):
        single_filter_out = pointwise_conv(x, kernel[f : f + 1])
        assert np.allclose(out[f], single_filter_out[0])


# --- Edge cases ---------------------------------------------------------


def test_05_single_input_and_output_channel_is_plain_scalar_multiply():
    x = np.array([[[1.0, 2.0], [3.0, 4.0]]])
    kernel = np.array([[[[3.0]]]])
    out = pointwise_conv(x, kernel)
    assert np.allclose(out, x * 3.0)


def test_06_zero_kernel_gives_all_zero_output():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(4, 3, 3))
    kernel = np.zeros((2, 4, 1, 1))
    out = pointwise_conv(x, kernel)
    assert np.allclose(out, 0.0)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(3, 4, 4))
    kernel = rng.normal(size=(2, 3, 1, 1))
    x_copy, kernel_copy = x.copy(), kernel.copy()
    pointwise_conv(x, kernel)
    assert np.array_equal(x, x_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_1x1_conv2d_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.randn(3, 4, 4)
    #   kernel = torch.randn(2, 3, 1, 1)
    #   out = torch.nn.functional.conv2d(x[None], kernel)[0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    x = np.array(
        [
            [
                [0.4372, 0.3701, 1.5816, -0.1556],
                [0.1511, -1.3495, -0.7089, -0.2434],
                [-0.0389, 1.0810, 0.9088, 0.0789],
                [-0.0895, 0.1714, -0.1575, 1.9800],
            ],
            [
                [0.7573, -0.4274, -1.5918, -0.0736],
                [-2.5141, 0.1140, 0.9822, 0.0681],
                [-0.0996, 0.8033, 1.0441, -0.5201],
                [0.8059, 1.0867, 0.2593, 1.8514],
            ],
            [
                [1.3406, 1.7659, 0.5640, -0.6749],
                [0.0914, 0.3948, 1.5457, -0.3610],
                [-0.2723, 0.6279, -2.7544, 0.4208],
                [-1.0226, -0.7471, -0.5051, 0.4636],
            ],
        ]
    )
    kernel = np.array([-0.4406, 0.7069, 0.9999, -0.8294, 1.7844, -2.4621]).reshape(2, 3, 1, 1)
    expected = np.array(
        [
            [
                [1.6832, 1.3006, -1.2581, -0.6583],
                [-1.7524, 1.0699, 2.5522, -0.2055],
                [-0.3255, 0.7194, -2.4165, 0.0183],
                [-0.4134, -0.0544, -0.2524, 0.8999],
            ],
            [
                [-2.3118, -5.4173, -5.5408, 1.6594],
                [-4.8366, 0.3507, -1.4651, 1.2122],
                [0.5249, -1.0089, 7.8910, -2.0295],
                [4.0301, 3.6365, 1.8369, 0.5200],
            ],
        ]
    )

    out = pointwise_conv(x, kernel)
    assert np.allclose(out, expected, atol=1e-2)
