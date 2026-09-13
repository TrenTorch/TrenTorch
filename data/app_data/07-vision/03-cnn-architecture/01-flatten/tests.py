"""
pytest data/app_data/07-vision/03-cnn-architecture/01-flatten/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

flatten = load_solution(f"07-vision/03-cnn-architecture/{Path(__file__).resolve().parent.name}").flatten


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matches_hand_computed_order():
    image = np.array([[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    out = flatten(image)
    assert np.array_equal(out, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])


def test_02_output_length_is_product_of_all_dims():
    image = np.random.default_rng(0).normal(size=(3, 4, 5))
    out = flatten(image)
    assert out.shape == (60,)


# --- Shape / general-case coverage -----------------------------------


def test_03_single_channel():
    image = np.random.default_rng(1).normal(size=(1, 5, 5))
    out = flatten(image)
    assert out.shape == (25,)
    assert np.array_equal(out, image[0].reshape(-1))


def test_04_non_square_spatial_dims():
    image = np.random.default_rng(2).normal(size=(2, 3, 7))
    out = flatten(image)
    assert out.shape == (42,)


# --- Edge cases ---------------------------------------------------------


def test_05_single_pixel_image():
    image = np.array([[[5.0]], [[7.0]]])
    out = flatten(image)
    assert np.array_equal(out, [5.0, 7.0])


def test_06_values_are_preserved_exactly_not_just_shape():
    image = np.arange(24.0).reshape(2, 3, 4)
    out = flatten(image)
    assert np.array_equal(out, np.arange(24.0))


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_input():
    image = np.random.default_rng(3).normal(size=(2, 4, 4))
    image_copy = image.copy()
    flatten(image)
    assert np.array_equal(image, image_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_flatten_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(7)
    #   x = torch.randn(2, 3, 3)
    #   flat = torch.flatten(x)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [[-0.8201, 0.3956, 1.9264], [-0.33, 0.1984, 0.7821], [1.0391, -0.7245, -0.8489]],
            [[-1.2169, -1.8157, -0.3452], [-2.0615, 0.6741, -1.3233], [-1.3598, -0.8667, -0.564]],
        ]
    )
    expected = np.array(
        [
            -0.8201, 0.3956, 1.9264, -0.33, 0.1984, 0.7821, 1.0391, -0.7245, -0.8489,
            -1.2169, -1.8157, -0.3452, -2.0615, 0.6741, -1.3233, -1.3598, -0.8667, -0.564,
        ]
    )
    out = flatten(image)
    assert np.allclose(out, expected, atol=1e-4)
