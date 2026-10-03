"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
rotate_nearest = _module.rotate_nearest
M = np.arange(9).reshape(3, 3)


def test_1_zero_rotation_is_identity():
    assert np.array_equal(rotate_nearest(M, 0), M)


def test_2_ninety_degrees_matches_numpy_rot90():
    assert np.array_equal(rotate_nearest(M, 90), np.rot90(M))
    big = np.random.RandomState(0).randint(0, 9, (6, 6))
    assert np.array_equal(rotate_nearest(big, 90), np.rot90(big))


def test_3_180_and_270_degrees():
    assert np.array_equal(rotate_nearest(M, 180), np.rot90(M, 2))
    assert np.array_equal(rotate_nearest(M, 270), np.rot90(M, 3))


def test_4_four_quarter_turns_return_the_image():
    out = M
    for _ in range(4):
        out = rotate_nearest(out, 90)
    assert np.array_equal(out, M)


def test_5_corners_fall_outside_after_45_degrees():
    img = np.ones((5, 5), dtype=int)
    out = rotate_nearest(img, 45)
    assert out[0, 0] == 0 and out[2, 2] == 1


def test_6_centre_pixel_is_fixed():
    img = np.random.RandomState(1).randint(1, 9, (7, 7))
    for ang in (10, 37, 90, 123):
        assert rotate_nearest(img, ang)[3, 3] == img[3, 3]


def test_7_dtype_shape_and_input_untouched():
    img = np.random.RandomState(2).randint(0, 255, (4, 6)).astype(np.uint8)
    snap = img.copy()
    out = rotate_nearest(img, 30)
    assert out.dtype == np.uint8 and out.shape == img.shape and np.array_equal(img, snap)
