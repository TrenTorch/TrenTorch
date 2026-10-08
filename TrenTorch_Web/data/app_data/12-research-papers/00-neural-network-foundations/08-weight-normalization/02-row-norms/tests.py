"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/08-weight-normalization/02-row-norms/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-weight-norm-row-norms")
row_norms = _module.row_norms


import numpy as np


def test_1_norm_of_a_three_four_five_row():
    np.testing.assert_allclose(row_norms(np.array([[3.0, 4.0]])), [5.0])


def test_2_output_has_one_entry_per_row():
    assert row_norms(np.ones((5, 2))).shape == (5,)


def test_3_zero_row_has_zero_norm():
    np.testing.assert_allclose(row_norms(np.zeros((1, 3))), [0.0])


def test_4_norms_are_nonnegative():
    rng = np.random.default_rng(0)
    assert np.all(row_norms(rng.normal(size=(6, 4))) >= 0)


def test_5_matches_numpy_linalg_norm():
    rng = np.random.default_rng(1)
    v = rng.normal(size=(4, 5))
    np.testing.assert_allclose(row_norms(v), np.linalg.norm(v, axis=1))


def test_6_does_not_mutate_the_input():
    v = np.array([[3.0, 4.0]])
    row_norms(v)
    np.testing.assert_array_equal(v, [[3.0, 4.0]])

