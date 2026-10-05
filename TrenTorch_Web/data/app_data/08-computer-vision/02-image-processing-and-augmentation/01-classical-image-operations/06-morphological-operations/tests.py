"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
erode = _module.erode
dilate = _module.dilate
opening = _module.opening


def _blob():
    img = np.zeros((9, 9), dtype=int)
    img[2:7, 2:7] = 1
    return img


def test_1_erosion_shrinks_a_square_by_one_ring():
    out = erode(_blob(), 3)
    expected = np.zeros((9, 9), int)
    expected[3:6, 3:6] = 1
    assert np.array_equal(out, expected)


def test_2_dilation_grows_a_square_by_one_ring():
    out = dilate(_blob(), 3)
    expected = np.zeros((9, 9), int)
    expected[1:8, 1:8] = 1
    assert np.array_equal(out, expected)


def test_3_border_counts_as_background_for_erosion():
    img = np.ones((3, 3), dtype=int)
    assert erode(img, 3).tolist() == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]


def test_4_opening_removes_isolated_noise_and_keeps_the_large_shape():
    img = _blob()
    img[0, 0] = 1  # speck
    out = opening(img, 3)
    assert out[0, 0] == 0 and np.array_equal(out, _blob())


def test_5_dilation_fills_a_one_pixel_hole():
    img = _blob()
    img[4, 4] = 0
    assert dilate(img, 3)[4, 4] == 1


def test_6_erosion_is_anti_extensive_and_dilation_extensive():
    img = (np.random.RandomState(0).rand(12, 12) > 0.4).astype(int)
    assert (erode(img, 3) <= img).all() and (dilate(img, 3) >= img).all()


def test_7_shape_dtype_and_input_untouched():
    img = _blob()
    snap = img.copy()
    out = opening(img, 5)
    assert out.shape == img.shape and np.issubdtype(out.dtype, np.integer) and np.array_equal(img, snap)
