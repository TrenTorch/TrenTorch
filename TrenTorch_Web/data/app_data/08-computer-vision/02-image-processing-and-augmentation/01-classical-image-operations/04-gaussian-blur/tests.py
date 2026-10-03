"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
gaussian_kernel = _module.gaussian_kernel
gaussian_blur = _module.gaussian_blur


def test_1_kernel_sums_to_one_and_is_symmetric():
    w = gaussian_kernel(7, 1.5)
    assert np.isclose(w.sum(), 1.0) and np.allclose(w, w[::-1]) and w.argmax() == 3


def test_2_kernel_hand_computed():
    w = gaussian_kernel(3, 1.0)
    raw = np.array([np.exp(-0.5), 1.0, np.exp(-0.5)])
    assert np.allclose(w, raw / raw.sum())


def test_3_constant_image_is_unchanged():
    assert np.allclose(gaussian_blur(np.full((6, 6), 4.0), 5, 1.2), 4.0)


def test_4_impulse_response_is_the_outer_product_kernel():
    img = np.zeros((9, 9))
    img[4, 4] = 1.0
    out = gaussian_blur(img, 5, 1.0)
    w = gaussian_kernel(5, 1.0)
    assert np.allclose(out[2:7, 2:7], np.outer(w, w))


def test_5_brightness_is_preserved_away_from_borders():
    img = np.zeros((15, 15))
    img[7, 7] = 10.0
    assert np.isclose(gaussian_blur(img, 5, 1.0).sum(), 10.0)


def test_6_blur_reduces_variance_and_keeps_shape():
    img = np.random.RandomState(0).rand(20, 16)
    out = gaussian_blur(img, 5, 1.5)
    assert out.shape == img.shape and out.var() < img.var()


def test_7_matches_full_2d_convolution_oracle_and_input_untouched():
    rng = np.random.RandomState(1)
    img = rng.rand(8, 9)
    snap = img.copy()
    w = gaussian_kernel(5, 1.1)
    K = np.outer(w, w)
    pad = np.pad(img, 2, mode="edge")
    ref = np.zeros_like(img)
    for i in range(8):
        for j in range(9):
            ref[i, j] = (pad[i:i + 5, j:j + 5] * K).sum()
    assert np.allclose(gaussian_blur(img, 5, 1.1), ref) and np.array_equal(img, snap)
