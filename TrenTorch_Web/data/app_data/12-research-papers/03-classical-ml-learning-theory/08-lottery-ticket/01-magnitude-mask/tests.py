"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/08-lottery-ticket/01-magnitude-mask/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lottery-magnitude-mask")
magnitude_mask = _module.magnitude_mask


import numpy as np


def test_1_keep_everything_gives_all_true():
    assert magnitude_mask(np.array([1.0, -2.0]), 1.0).all()


def test_2_keep_nothing_gives_all_false():
    assert not magnitude_mask(np.array([1.0, -2.0]), 0.0).any()


def test_3_keeps_the_largest_magnitudes():
    mask = magnitude_mask(np.array([0.1, -5.0, 2.0, 0.2]), 0.5)
    np.testing.assert_array_equal(mask, [False, True, True, False])


def test_4_mask_has_the_same_shape_as_the_weights():
    assert magnitude_mask(np.ones((2, 3)), 0.5).shape == (2, 3)


def test_5_count_is_the_ceiling_of_the_fraction():
    assert magnitude_mask(np.arange(5.0) + 1, 0.4).sum() == 2


def test_6_does_not_mutate_weights():
    w = np.array([3.0, 1.0])
    magnitude_mask(w, 0.5)
    np.testing.assert_array_equal(w, [3.0, 1.0])

