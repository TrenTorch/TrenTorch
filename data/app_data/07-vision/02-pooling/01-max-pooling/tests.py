"""
pytest data/app_data/07-vision/02-pooling/01-max-pooling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

max_pool2d = load_solution(f"07-vision/02-pooling/{Path(__file__).resolve().parent.name}").max_pool2d


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matches_hand_computed_2x2_windows():
    image = np.array([[[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0], [9.0, 10.0, 11.0, 12.0], [13.0, 14.0, 15.0, 16.0]]])
    out = max_pool2d(image, kernel_size=2)
    assert np.allclose(out, [[[6.0, 8.0], [14.0, 16.0]]])


def test_02_output_shape_non_overlapping_default_stride():
    image = np.random.default_rng(0).normal(size=(3, 6, 6))
    out = max_pool2d(image, kernel_size=2)
    assert out.shape == (3, 3, 3)


# --- Shape / general-case coverage -----------------------------------


def test_03_channels_pooled_independently():
    image = np.stack([np.ones((4, 4)), np.full((4, 4), 5.0)])
    out = max_pool2d(image, kernel_size=2)
    assert np.allclose(out[0], 1.0)
    assert np.allclose(out[1], 5.0)


# --- Parameter handling -------------------------------------------------


def test_04_explicit_stride_overrides_default():
    image = np.arange(25.0).reshape(1, 5, 5)
    out_default = max_pool2d(image, kernel_size=2)  # stride=2 default
    out_stride1 = max_pool2d(image, kernel_size=2, stride=1)
    assert out_default.shape == (1, 2, 2)
    assert out_stride1.shape == (1, 4, 4)


# --- Edge cases ---------------------------------------------------------


def test_05_kernel_size_equal_to_image_gives_global_max():
    image = np.random.default_rng(1).normal(size=(2, 5, 5))
    out = max_pool2d(image, kernel_size=5)
    assert out.shape == (2, 1, 1)
    assert np.allclose(out[:, 0, 0], image.max(axis=(1, 2)))


def test_06_all_equal_values_returns_that_value():
    image = np.full((1, 4, 4), 3.0)
    out = max_pool2d(image, kernel_size=2)
    assert np.allclose(out, 3.0)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_input():
    image = np.random.default_rng(2).normal(size=(2, 6, 6))
    image_copy = image.copy()
    max_pool2d(image, kernel_size=2)
    assert np.array_equal(image, image_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_max_pool2d_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(5)
    #   image = torch.randn(2, 4, 4)
    #   out = torch.nn.functional.max_pool2d(image[None], kernel_size=2)[0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [
                [1.8423, 0.5189, -1.7119, -1.7014],
                [2.0194, -0.2686, -0.1307, -1.4374],
                [0.3908, -0.019, -1.3527, -0.7308],
                [0.9879, -0.4194, -0.5849, -0.7823],
            ],
            [
                [2.7799, 1.222, -0.3364, -0.9651],
                [-0.1297, -0.6018, 0.145, -0.1498],
                [-0.4374, 0.7792, -0.0583, -2.0305],
                [1.4829, 0.494, 0.2492, 1.747],
            ],
        ]
    )
    expected = np.array([[[2.0194, -0.1307], [0.9879, -0.5849]], [[2.7799, 0.145], [1.4829, 1.747]]])
    out = max_pool2d(image, kernel_size=2)
    assert np.allclose(out, expected, atol=1e-3)
