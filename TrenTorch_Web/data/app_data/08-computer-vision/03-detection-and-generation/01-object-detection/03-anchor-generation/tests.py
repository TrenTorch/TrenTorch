"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
generate_anchors = _module.generate_anchors


def test_1_count_and_shape():
    a = generate_anchors(3, 4, 16, [32, 64], [0.5, 1.0, 2.0])
    assert a.shape == (3 * 4 * 2 * 3, 4)


def test_2_hand_computed_single_cell():
    a = generate_anchors(1, 1, 16, [4.0], [1.0])
    assert np.allclose(a, [[6.0, 6.0, 10.0, 10.0]])


def test_3_area_is_scale_squared_for_every_ratio():
    a = generate_anchors(1, 1, 8, [10.0], [0.5, 1.0, 2.0])
    area = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    assert np.allclose(area, 100.0)


def test_4_aspect_ratio_is_height_over_width():
    a = generate_anchors(1, 1, 8, [10.0], [0.5, 2.0])
    h, w = a[:, 3] - a[:, 1], a[:, 2] - a[:, 0]
    assert np.allclose(h / w, [0.5, 2.0])


def test_5_centres_follow_the_stride_grid():
    a = generate_anchors(2, 3, 10, [4.0], [1.0])
    centres = np.stack([(a[:, 0] + a[:, 2]) / 2, (a[:, 1] + a[:, 3]) / 2], axis=1)
    assert np.allclose(centres, [[5, 5], [15, 5], [25, 5], [5, 15], [15, 15], [25, 15]])


def test_6_ordering_is_cells_then_scales_then_ratios():
    a = generate_anchors(1, 2, 10, [2.0, 4.0], [1.0, 4.0])
    w = a[:, 2] - a[:, 0]
    assert np.allclose(w[:4], [2.0, 1.0, 4.0, 2.0]) and np.allclose(a[4:, 0] + w[4:] / 2, 15.0)


def test_7_deterministic_and_float():
    a = generate_anchors(2, 2, 8, [16], [1.0])
    assert np.issubdtype(a.dtype, np.floating) and np.array_equal(a, generate_anchors(2, 2, 8, [16], [1.0]))
