"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
equalize_histogram = _module.equalize_histogram


def test_1_two_level_image_is_stretched_to_full_range():
    img = np.array([[100, 100], [110, 110]], dtype=np.uint8)
    assert equalize_histogram(img).tolist() == [[0, 0], [255, 255]]


def test_2_hand_computed_three_levels():
    img = np.array([[10, 10, 20, 30]], dtype=np.uint8)
    # cdf: 10->2, 20->3, 30->4 ; cdf_min=2, N=4 ; lut: 0, 127.5->128 (round half even => 128), 255
    out = equalize_histogram(img)
    assert out.tolist() == [[0, 0, 128, 255]]


def test_3_constant_image_is_unchanged():
    img = np.full((3, 3), 50, dtype=np.uint8)
    assert np.array_equal(equalize_histogram(img), img)


def test_4_order_of_brightness_is_preserved():
    img = np.random.RandomState(0).randint(60, 120, (16, 16)).astype(np.uint8)
    out = equalize_histogram(img)
    order_in = np.argsort(img.ravel(), kind="stable")
    assert np.all(np.diff(out.ravel()[order_in]) >= 0)


def test_5_contrast_range_expands():
    img = np.random.RandomState(1).randint(100, 140, (20, 20)).astype(np.uint8)
    out = equalize_histogram(img)
    assert out.min() == 0 and out.max() == 255


def test_6_output_dtype_and_shape():
    img = np.random.RandomState(2).randint(0, 256, (5, 7)).astype(np.uint8)
    out = equalize_histogram(img)
    assert out.dtype == np.uint8 and out.shape == img.shape


def test_7_input_untouched_and_idempotent_on_flat_histograms():
    img = np.tile(np.arange(256, dtype=np.uint8), (2, 1))
    snap = img.copy()
    out = equalize_histogram(img)
    assert np.array_equal(img, snap) and np.array_equal(out, img)
