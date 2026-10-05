"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
cutmix_box = _module.cutmix_box
cutmix = _module.cutmix
adjusted_lambda = _module.adjusted_lambda


def test_1_box_hand_computed():
    # lam=0.75 -> sqrt(0.25)=0.5 -> 4x4 of a 8x8 image
    assert cutmix_box(8, 8, 0.75, 4, 4) == (2, 6, 2, 6)


def test_2_box_is_clipped_at_the_border():
    y1, y2, x1, x2 = cutmix_box(8, 8, 0.75, 0, 0)
    assert (y1, x1) == (0, 0) and (y2, x2) == (2, 2)


def test_3_lambda_one_gives_an_empty_box_and_no_change():
    box = cutmix_box(8, 8, 1.0, 4, 4)
    a, b = np.zeros((8, 8)), np.ones((8, 8))
    assert box[1] - box[0] == 0 and np.array_equal(cutmix(a, b, box), a)


def test_4_paste_hand_computed():
    a, b = np.zeros((4, 4)), np.ones((4, 4))
    out = cutmix(a, b, (1, 3, 1, 3))
    assert out.sum() == 4 and out[1:3, 1:3].all()


def test_5_adjusted_lambda_uses_the_clipped_area():
    box = cutmix_box(8, 8, 0.75, 0, 0)
    assert np.isclose(adjusted_lambda(box, 8, 8), 1 - 4 / 64)
    assert np.isclose(adjusted_lambda(cutmix_box(8, 8, 0.75, 4, 4), 8, 8), 1 - 16 / 64)


def test_6_pasted_fraction_of_pixels_matches_adjusted_lambda():
    a, b = np.zeros((10, 10)), np.ones((10, 10))
    box = cutmix_box(10, 10, 0.5, 3, 6)
    out = cutmix(a, b, box)
    assert np.isclose(1 - out.mean(), adjusted_lambda(box, 10, 10))


def test_7_works_for_colour_images_and_inputs_untouched():
    a, b = np.random.RandomState(0).rand(6, 6, 3), np.random.RandomState(1).rand(6, 6, 3)
    sa, sb = a.copy(), b.copy()
    out = cutmix(a, b, (1, 4, 2, 5))
    assert np.array_equal(out[1:4, 2:5], b[1:4, 2:5]) and np.array_equal(out[0], a[0])
    assert np.array_equal(a, sa) and np.array_equal(b, sb)
