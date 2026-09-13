"""
pytest data/app_data/07-vision/01-convolutions/05-multiple-output-filters/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_filter = load_solution(
    f"07-vision/01-convolutions/{Path(__file__).resolve().parent.name}"
).conv2d_multi_filter
conv2d_multi_channel = load_solution(
    "07-vision/01-convolutions/04-multi-channel-input"
).conv2d_multi_channel


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_single_output_filter_matches_conv2d_multi_channel():
    image = np.random.default_rng(0).normal(size=(3, 5, 5))
    kernel = np.random.default_rng(1).normal(size=(1, 3, 3, 3))
    out = conv2d_multi_filter(image, kernel)
    expected = conv2d_multi_channel(image, kernel[0])
    assert out.shape == (1, 3, 3)
    assert np.allclose(out[0], expected)


def test_02_each_output_channel_matches_its_own_filter_independently():
    image = np.random.default_rng(2).normal(size=(2, 4, 4))
    kernel = np.random.default_rng(3).normal(size=(3, 2, 3, 3))
    out = conv2d_multi_filter(image, kernel)
    for f in range(3):
        assert np.allclose(out[f], conv2d_multi_channel(image, kernel[f]))


# --- Shape / general-case coverage -----------------------------------


def test_03_output_shape_is_c_out_first():
    image = np.random.default_rng(4).normal(size=(4, 6, 6))
    kernel = np.random.default_rng(5).normal(size=(5, 4, 3, 3))
    out = conv2d_multi_filter(image, kernel)
    assert out.shape == (5, 4, 4)


# --- Edge cases ---------------------------------------------------------


def test_04_identical_filters_give_identical_output_channels():
    image = np.random.default_rng(6).normal(size=(2, 5, 5))
    one_filter = np.random.default_rng(7).normal(size=(2, 3, 3))
    kernel = np.stack([one_filter, one_filter, one_filter])
    out = conv2d_multi_filter(image, kernel)
    assert np.allclose(out[0], out[1])
    assert np.allclose(out[1], out[2])


def test_05_single_output_filter_and_single_input_channel():
    image = np.random.default_rng(8).normal(size=(1, 4, 4))
    kernel = np.random.default_rng(9).normal(size=(1, 1, 2, 2))
    out = conv2d_multi_filter(image, kernel)
    assert out.shape == (1, 3, 3)


# --- Array hygiene ------------------------------------------------------


def test_06_does_not_mutate_its_inputs():
    image = np.random.default_rng(10).normal(size=(2, 5, 5))
    kernel = np.random.default_rng(11).normal(size=(3, 2, 3, 3))
    image_copy, kernel_copy = image.copy(), kernel.copy()
    conv2d_multi_filter(image, kernel)
    assert np.array_equal(image, image_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_07_matches_real_pytorch_conv2d_with_multiple_filters_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(4)
    #   image = torch.randn(2, 4, 4)
    #   kernel = torch.randn(3, 2, 3, 3)
    #   out = torch.nn.functional.conv2d(image[None], kernel)[0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [
                [-0.9414, 1.2632, -0.1838, 0.1505],
                [0.1075, -0.278, -2.6021, 0.6245],
                [-0.8684, -0.2051, 0.3976, 0.6699],
                [-0.0537, 0.0467, -1.7671, -2.1205],
            ],
            [
                [1.5191, -0.6682, 0.0031, -0.1535],
                [1.1396, -0.2302, 1.1877, 0.7677],
                [-0.7588, -0.1853, -0.8558, -0.2346],
                [-0.4215, 0.8488, -0.6776, -0.9445],
            ],
        ]
    )
    kernel = np.array(
        [
            [
                [[-0.4815, 1.2434, 2.3693], [0.2829, -0.2345, 1.6892], [0.2716, -0.1365, -0.6948]],
                [[-1.3186, -0.9694, 0.6403], [0.8201, -0.9151, -2.1437], [1.4072, -0.0263, 2.7204]],
            ],
            [
                [[-0.5955, 0.9871, 1.0861], [0.061, 0.0417, 0.6783], [-0.8952, -1.0143, -0.2429]],
                [[-1.5727, 1.394, -0.1941], [0.0048, -1.3165, 0.0204], [-0.1652, 0.2109, 0.5167]],
            ],
            [
                [[0.243, -0.3522, 1.7228], [-0.4043, 0.5627, -0.0078], [1.4371, 1.0855, 0.0188]],
                [[1.7349, -0.6573, 1.5234], [0.0484, -0.2402, -0.1605], [1.244, 1.758, -0.8418]],
            ],
        ]
    )
    expected = np.array(
        [
            [[-9.340715, -2.487185], [-6.477692, 0.506253]],
            [[-2.61763, -1.589624], [-4.748776, 3.217894]],
            [[-0.183096, -3.92857], [1.43515, 1.21876]],
        ]
    )
    out = conv2d_multi_filter(image, kernel)
    assert np.allclose(out, expected, atol=1e-3)
