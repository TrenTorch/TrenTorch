"""
pytest data/app_data/03-dl-training/04-regularization/02-data-augmentation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/04-regularization/{Path(__file__).resolve().parent.name}")
horizontal_flip = _module.horizontal_flip
random_crop = _module.random_crop
add_gaussian_noise = _module.add_gaussian_noise


def test_horizontal_flip_reverses_the_width_axis():
    image = np.array([[[1], [2], [3]]])  # shape (1, 3, 1)
    result = horizontal_flip(image)
    assert np.array_equal(result[0, :, 0], [3, 2, 1])


def test_horizontal_flip_preserves_height_axis_order():
    image = np.array([[[1], [1]], [[2], [2]]])  # shape (2, 2, 1), rows differ
    result = horizontal_flip(image)
    assert result[0, 0, 0] == 1
    assert result[1, 0, 0] == 2


def test_horizontal_flip_twice_returns_the_original():
    image = np.random.randn(4, 5, 3)
    result = horizontal_flip(horizontal_flip(image))
    assert np.allclose(result, image)


def test_random_crop_returns_the_requested_shape():
    image = np.random.randn(20, 30, 3)
    rng = np.random.RandomState(0)
    crop = random_crop(image, crop_h=10, crop_w=15, rng=rng)
    assert crop.shape == (10, 15, 3)


def test_random_crop_stays_within_image_bounds():
    image = np.arange(100).reshape(10, 10)
    rng = np.random.RandomState(1)
    for _ in range(20):
        crop = random_crop(image, crop_h=4, crop_w=4, rng=rng)
        assert crop.shape == (4, 4)
        # every value in the crop must actually come from the original image
        assert np.all(np.isin(crop, image))


def test_random_crop_full_size_returns_the_entire_image():
    image = np.arange(20).reshape(4, 5)
    rng = np.random.RandomState(0)
    crop = random_crop(image, crop_h=4, crop_w=5, rng=rng)
    assert np.array_equal(crop, image)


def test_random_crop_same_seed_gives_the_same_crop():
    image = np.arange(100).reshape(10, 10)
    crop1 = random_crop(image, 5, 5, rng=np.random.RandomState(42))
    crop2 = random_crop(image, 5, 5, rng=np.random.RandomState(42))
    assert np.array_equal(crop1, crop2)


def test_add_gaussian_noise_returns_the_correct_shape():
    image = np.zeros((5, 5, 3))
    rng = np.random.RandomState(0)
    result = add_gaussian_noise(image, std=0.1, rng=rng)
    assert result.shape == image.shape


def test_add_gaussian_noise_with_zero_std_leaves_image_unchanged():
    image = np.random.randn(4, 4)
    rng = np.random.RandomState(0)
    result = add_gaussian_noise(image, std=0.0, rng=rng)
    assert np.allclose(result, image)


def test_add_gaussian_noise_does_not_modify_the_original_image_in_place():
    image = np.zeros((3, 3))
    original = image.copy()
    rng = np.random.RandomState(0)
    add_gaussian_noise(image, std=1.0, rng=rng)
    assert np.array_equal(image, original)


def test_add_gaussian_noise_matches_hand_computation_with_a_seeded_rng():
    image = np.zeros(3)
    rng = np.random.RandomState(0)
    result = add_gaussian_noise(image, std=1.0, rng=rng)
    expected_noise = np.random.RandomState(0).normal(loc=0.0, scale=1.0, size=3)
    assert np.allclose(result, expected_noise)


def test_random_crop_uses_the_passed_in_rng_not_the_global_random_state():
    # Directly targets a mutant that uses np.random.randint (the global,
    # unseeded state) instead of rng.randint: two crops built from
    # SEPARATE RandomState(42) instances would then no longer match.
    image = np.arange(400).reshape(20, 20)
    crop1 = random_crop(image, 5, 5, rng=np.random.RandomState(42))
    crop2 = random_crop(image, 5, 5, rng=np.random.RandomState(42))
    assert np.array_equal(crop1, crop2)
