"""
pytest data/app_data/12-research-papers/06-computer-vision/05-vit/02-patchify/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vit-patchify")
patchify = _module.patchify


import numpy as np


def test_1_output_shape():
    assert patchify(np.zeros((4, 4)), 2).shape == (4, 4)


def test_2_first_patch_is_the_top_left_block():
    img = np.arange(16.0).reshape(4, 4)
    np.testing.assert_allclose(patchify(img, 2)[0], [0.0, 1.0, 4.0, 5.0])


def test_3_patches_are_in_row_major_order():
    img = np.arange(16.0).reshape(4, 4)
    np.testing.assert_allclose(patchify(img, 2)[1], [2.0, 3.0, 6.0, 7.0])


def test_4_patches_cover_every_pixel_exactly_once():
    img = np.arange(16.0).reshape(4, 4)
    assert sorted(patchify(img, 2).ravel().tolist()) == list(range(16))


def test_5_single_patch_is_the_flattened_image():
    img = np.arange(4.0).reshape(2, 2)
    np.testing.assert_allclose(patchify(img, 2), [[0.0, 1.0, 2.0, 3.0]])


def test_6_does_not_mutate_input():
    img = np.ones((2, 2))
    patchify(img, 1)
    np.testing.assert_array_equal(img, np.ones((2, 2)))

