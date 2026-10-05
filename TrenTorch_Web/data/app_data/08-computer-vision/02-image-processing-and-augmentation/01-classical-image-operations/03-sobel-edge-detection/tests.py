"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sobel_gradients = _module.sobel_gradients
sobel_magnitude = _module.sobel_magnitude


def test_1_vertical_edge_has_only_horizontal_gradient():
    img = np.zeros((5, 5))
    img[:, 2:] = 1.0
    gx, gy = sobel_gradients(img)
    assert np.allclose(gy, 0.0) and np.isclose(gx[1, 0], 4.0) and np.isclose(gx[1, 2], 0.0)


def test_2_horizontal_edge_has_only_vertical_gradient():
    img = np.zeros((5, 5))
    img[2:, :] = 1.0
    gx, gy = sobel_gradients(img)
    assert np.allclose(gx, 0.0) and np.isclose(gy[0, 1], 4.0)


def test_3_flat_image_has_no_edges():
    assert np.allclose(sobel_magnitude(np.full((6, 6), 7.0)), 0.0)


def test_4_output_shape_is_valid_region():
    assert sobel_magnitude(np.zeros((7, 9))).shape == (5, 7)


def test_5_linear_ramp_gives_constant_gradient():
    img = np.tile(np.arange(6.0), (6, 1))
    gx, _ = sobel_gradients(img)
    assert np.allclose(gx, 8.0)  # (1+2+1) rows * (2 pixels step) = 8


def test_6_matches_independent_loop_oracle():
    img = np.random.RandomState(0).rand(6, 7)
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float)
    gx, gy = sobel_gradients(img)
    for i in range(4):
        for j in range(5):
            patch = img[i:i + 3, j:j + 3]
            assert np.isclose(gx[i, j], (patch * kx).sum()) and np.isclose(gy[i, j], (patch * kx.T).sum())


def test_7_input_untouched_and_magnitude_nonnegative():
    img = np.random.RandomState(1).rand(5, 5)
    snap = img.copy()
    assert (sobel_magnitude(img) >= 0).all() and np.array_equal(img, snap)
