"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
box_iou = _module.box_iou


def test_1_identical_boxes_are_one():
    b = np.array([[0.0, 0.0, 2.0, 2.0]])
    assert np.isclose(box_iou(b, b)[0, 0], 1.0)


def test_2_hand_computed_overlap():
    a, b = np.array([[0.0, 0.0, 2.0, 2.0]]), np.array([[1.0, 1.0, 3.0, 3.0]])
    assert np.isclose(box_iou(a, b)[0, 0], 1 / 7)


def test_3_disjoint_and_touching_boxes_are_zero():
    a = np.array([[0.0, 0.0, 1.0, 1.0]])
    assert box_iou(a, np.array([[5.0, 5.0, 6.0, 6.0]]))[0, 0] == 0.0
    assert box_iou(a, np.array([[1.0, 0.0, 2.0, 1.0]]))[0, 0] == 0.0


def test_4_nested_box_is_area_ratio():
    a, b = np.array([[0.0, 0.0, 4.0, 4.0]]), np.array([[1.0, 1.0, 3.0, 3.0]])
    assert np.isclose(box_iou(a, b)[0, 0], 4 / 16)


def test_5_pairwise_shape_and_symmetry():
    rng = np.random.RandomState(0)
    xy = rng.rand(5, 2) * 10
    a = np.hstack([xy, xy + rng.rand(5, 2) * 5 + 0.1])
    xy2 = rng.rand(3, 2) * 10
    b = np.hstack([xy2, xy2 + rng.rand(3, 2) * 5 + 0.1])
    m = box_iou(a, b)
    assert m.shape == (5, 3) and np.allclose(m, box_iou(b, a).T)
    assert (m >= 0).all() and (m <= 1 + 1e-12).all()


def test_6_degenerate_boxes_give_zero_not_nan():
    z = np.array([[1.0, 1.0, 1.0, 1.0]])
    assert box_iou(z, z)[0, 0] == 0.0


def test_7_matches_loop_oracle_and_inputs_untouched():
    rng = np.random.RandomState(1)
    a = np.sort(rng.rand(4, 2, 2), axis=1).reshape(4, 4)[:, [0, 2, 1, 3]]
    a = np.stack([a[:, 0], a[:, 1], a[:, 2], a[:, 3]], axis=1)
    b = a[::-1].copy()
    sa = a.copy()
    m = box_iou(a, b)
    for i in range(4):
        for j in range(4):
            w = max(0, min(a[i, 2], b[j, 2]) - max(a[i, 0], b[j, 0]))
            h = max(0, min(a[i, 3], b[j, 3]) - max(a[i, 1], b[j, 1]))
            ua = (a[i, 2] - a[i, 0]) * (a[i, 3] - a[i, 1]) + (b[j, 2] - b[j, 0]) * (b[j, 3] - b[j, 1]) - w * h
            assert np.isclose(m[i, j], (w * h / ua) if ua > 0 else 0.0)
    assert np.array_equal(a, sa)
