"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/08-lottery-ticket/02-apply-mask/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lottery-apply-mask")
apply_mask = _module.apply_mask


import numpy as np


def test_1_masked_entries_become_zero():
    np.testing.assert_allclose(apply_mask(np.array([1.0, 2.0]), np.array([True, False])), [1.0, 0.0])


def test_2_full_mask_keeps_all_weights():
    w = np.array([[1.0, -2.0], [3.0, 4.0]])
    np.testing.assert_allclose(apply_mask(w, np.ones((2, 2), dtype=bool)), w)


def test_3_empty_mask_zeros_everything():
    np.testing.assert_allclose(apply_mask(np.ones(3), np.zeros(3, dtype=bool)), 0.0)


def test_4_keeps_the_shape():
    assert apply_mask(np.ones((2, 3)), np.ones((2, 3), dtype=bool)).shape == (2, 3)


def test_5_sign_is_preserved_for_kept_weights():
    out = apply_mask(np.array([-4.0, 4.0]), np.array([True, True]))
    np.testing.assert_allclose(out, [-4.0, 4.0])


def test_6_does_not_mutate_weights():
    w = np.array([5.0])
    apply_mask(w, np.array([False]))
    np.testing.assert_array_equal(w, [5.0])

