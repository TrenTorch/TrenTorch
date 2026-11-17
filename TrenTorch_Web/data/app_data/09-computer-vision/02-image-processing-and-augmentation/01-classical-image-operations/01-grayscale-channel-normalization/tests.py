"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
to_grayscale = _module.to_grayscale
normalize_channels = _module.normalize_channels


def test_1_pure_channels_hand_computed():
    img = np.array([[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]])
    assert np.allclose(to_grayscale(img), [[0.299, 0.587, 0.114]])


def test_2_gray_pixels_are_unchanged():
    img = np.full((2, 2, 3), 0.5)
    assert np.allclose(to_grayscale(img), 0.5)


def test_3_shape():
    assert to_grayscale(np.zeros((4, 6, 3))).shape == (4, 6)


def test_4_normalize_hand_computed():
    img = np.array([[[10.0, 20.0]]])
    assert np.allclose(normalize_channels(img, [5.0, 10.0], [5.0, 2.0]), [[[1.0, 5.0]]])


def test_5_normalized_dataset_has_zero_mean_and_unit_std():
    rng = np.random.RandomState(0)
    data = rng.rand(50, 8, 8, 3) * np.array([1.0, 5.0, 20.0]) + np.array([0.0, 3.0, -7.0])
    mean, std = data.mean(axis=(0, 1, 2)), data.std(axis=(0, 1, 2))
    out = normalize_channels(data, mean, std)
    assert np.allclose(out.mean(axis=(0, 1, 2)), 0.0, atol=1e-9) and np.allclose(out.std(axis=(0, 1, 2)), 1.0)


def test_6_normalization_is_invertible():
    img = np.random.RandomState(1).rand(3, 3, 3)
    mean, std = np.array([0.1, 0.2, 0.3]), np.array([0.5, 0.6, 0.7])
    assert np.allclose(normalize_channels(img, mean, std) * std + mean, img)


def test_7_inputs_untouched():
    img = np.random.RandomState(2).rand(3, 3, 3)
    snap = img.copy()
    to_grayscale(img)
    normalize_channels(img, [0.1] * 3, [0.2] * 3)
    assert np.array_equal(img, snap)
