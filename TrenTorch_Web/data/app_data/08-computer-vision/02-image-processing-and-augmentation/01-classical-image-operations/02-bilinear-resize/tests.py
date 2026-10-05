"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
bilinear_resize = _module.bilinear_resize


def test_1_hand_computed_upsample():
    out = bilinear_resize(np.array([[0.0, 1.0]]), 1, 4)
    assert np.allclose(out, [[0.0, 0.25, 0.75, 1.0]])


def test_2_identity_resize_is_exact():
    img = np.random.RandomState(0).rand(5, 7)
    assert np.allclose(bilinear_resize(img, 5, 7), img)


def test_3_constant_image_stays_constant():
    assert np.allclose(bilinear_resize(np.full((4, 4), 3.0), 9, 6), 3.0)


def test_4_linear_ramp_stays_linear_in_the_interior():
    ramp = np.tile(np.arange(8.0), (3, 1))
    out = bilinear_resize(ramp, 3, 16)
    inner = out[0, 2:-2]
    assert np.allclose(np.diff(inner), np.diff(inner)[0])


def test_5_two_dimensional_hand_computed():
    img = np.array([[0.0, 2.0], [4.0, 6.0]])
    out = bilinear_resize(img, 4, 4)
    assert np.isclose(out[1, 1], 0.75 * 0.75 * 0 + 0.75 * 0.25 * 2 + 0.25 * 0.75 * 4 + 0.25 * 0.25 * 6)
    # corners replicate the original corners because of clipping
    assert np.isclose(out[0, 0], 0.0) and np.isclose(out[-1, -1], 6.0)


def test_6_downscale_values_stay_within_input_range():
    img = np.random.RandomState(1).rand(16, 16)
    out = bilinear_resize(img, 5, 5)
    assert out.min() >= img.min() - 1e-12 and out.max() <= img.max() + 1e-12


def test_7_input_untouched_and_shape():
    img = np.random.RandomState(2).rand(4, 6)
    snap = img.copy()
    assert bilinear_resize(img, 8, 3).shape == (8, 3) and np.array_equal(img, snap)
