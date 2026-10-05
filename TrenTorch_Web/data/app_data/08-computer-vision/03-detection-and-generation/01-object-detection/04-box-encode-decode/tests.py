"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
encode_boxes = _module.encode_boxes
decode_boxes = _module.decode_boxes


def test_1_identical_box_has_zero_deltas():
    a = np.array([[0.0, 0.0, 4.0, 2.0]])
    assert np.allclose(encode_boxes(a, a), 0.0)


def test_2_hand_computed_encoding():
    anchor = np.array([[0.0, 0.0, 10.0, 10.0]])
    gt = np.array([[5.0, 0.0, 25.0, 10.0]])  # centre (15, 5), size (20, 10)
    assert np.allclose(encode_boxes(gt, anchor), [[1.0, 0.0, np.log(2.0), 0.0]])


def test_3_hand_computed_decoding():
    anchor = np.array([[0.0, 0.0, 10.0, 10.0]])
    out = decode_boxes(np.array([[0.1, -0.2, np.log(2.0), np.log(0.5)]]), anchor)
    # centre (6, 3), size (20, 5)
    assert np.allclose(out, [[-4.0, 0.5, 16.0, 5.5]])


def test_4_round_trip():
    rng = np.random.RandomState(0)
    def boxes(n):
        xy = rng.rand(n, 2) * 50
        return np.hstack([xy, xy + rng.rand(n, 2) * 30 + 1])
    gt, anchors = boxes(20), boxes(20)
    assert np.allclose(decode_boxes(encode_boxes(gt, anchors), anchors), gt)


def test_5_translation_deltas_are_scale_free():
    small = np.array([[0.0, 0.0, 10.0, 10.0]])
    big = small * 10
    shift_small = small + np.array([1.0, 0.0, 1.0, 0.0])
    shift_big = big + np.array([10.0, 0.0, 10.0, 0.0])
    assert np.allclose(encode_boxes(shift_small, small), encode_boxes(shift_big, big))


def test_6_doubling_and_halving_are_symmetric_in_log_space():
    a = np.array([[0.0, 0.0, 8.0, 8.0]])
    up = encode_boxes(np.array([[-4.0, -4.0, 12.0, 12.0]]), a)[0, 2]
    down = encode_boxes(np.array([[2.0, 2.0, 6.0, 6.0]]), a)[0, 2]
    assert np.isclose(up, -down)


def test_7_inputs_untouched():
    gt, anchors = np.array([[1.0, 1.0, 5.0, 4.0]]), np.array([[0.0, 0.0, 6.0, 6.0]])
    sg, sa = gt.copy(), anchors.copy()
    d = encode_boxes(gt, anchors)
    decode_boxes(d, anchors)
    assert np.array_equal(gt, sg) and np.array_equal(anchors, sa)
