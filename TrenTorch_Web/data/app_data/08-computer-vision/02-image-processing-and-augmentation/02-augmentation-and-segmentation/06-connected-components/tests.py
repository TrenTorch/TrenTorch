"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
label_components = _module.label_components


def test_1_two_separate_blobs_hand_computed():
    img = np.array([[1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1]])
    labels, n = label_components(img)
    assert n == 2 and labels.tolist() == [[1, 1, 0, 0], [0, 0, 0, 2], [0, 0, 0, 2]]


def test_2_diagonal_contact_does_not_connect_under_4_connectivity():
    img = np.array([[1, 0], [0, 1]])
    _, n = label_components(img)
    assert n == 2


def test_3_u_shape_is_one_component():
    img = np.array([[1, 0, 1], [1, 0, 1], [1, 1, 1]])
    labels, n = label_components(img)
    assert n == 1 and (labels[img == 1] == 1).all()


def test_4_empty_and_full_images():
    assert label_components(np.zeros((3, 3), int))[1] == 0
    labels, n = label_components(np.ones((3, 3), int))
    assert n == 1 and (labels == 1).all()


def test_5_labels_follow_raster_order_of_first_pixel():
    img = np.array([[0, 1, 0, 1], [1, 0, 0, 0], [0, 0, 1, 0]])
    labels, _ = label_components(img)
    assert labels[0, 1] == 1 and labels[0, 3] == 2 and labels[1, 0] == 3 and labels[2, 2] == 4


def test_6_large_component_does_not_overflow_the_stack():
    img = np.ones((120, 120), dtype=int)
    _, n = label_components(img)
    assert n == 1


def test_7_matches_union_of_pixels_and_input_untouched():
    rng = np.random.RandomState(0)
    img = (rng.rand(12, 12) > 0.6).astype(int)
    snap = img.copy()
    labels, n = label_components(img)
    assert np.array_equal(labels > 0, img == 1) and np.array_equal(img, snap)
    for k in range(1, n + 1):
        ys, xs = np.where(labels == k)
        # every pixel in a component has a 4-neighbour in the same component unless it is alone
        if len(ys) > 1:
            for y, x in zip(ys, xs):
                nb = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
                assert any(0 <= a < 12 and 0 <= b < 12 and labels[a, b] == k for a, b in nb)
