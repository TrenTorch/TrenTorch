"""
pytest data/app_data/12-research-papers/01-optimization-and-training/06-adafactor/01-factored-moment/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adafactor-factored-moment")
factored_second_moment = _module.factored_second_moment


import numpy as np


def test_1_hand_value():
    out = factored_second_moment(np.array([1.0, 2.0]), np.array([3.0, 4.0]))
    assert abs(out[0, 0] - 1.0) < 1e-12 and abs(out[1, 1] - 8.0 / 3.0) < 1e-12


def test_2_output_shape_is_rows_by_cols():
    assert factored_second_moment(np.ones(3), np.ones(5)).shape == (3, 5)


def test_3_rank_one_matrix_is_recovered_exactly():
    V = np.array([[2.0, 4.0], [1.0, 2.0]])
    out = factored_second_moment(V.sum(axis=1), V.sum(axis=0))
    np.testing.assert_allclose(out, V / V.sum() * V.sum(), atol=1e-9)


def test_4_entries_are_nonnegative_for_nonnegative_inputs():
    assert np.all(factored_second_moment(np.array([1.0, 3.0]), np.array([2.0])) >= 0)


def test_5_row_sums_match_the_inputs():
    row, col = np.array([1.0, 2.0]), np.array([3.0, 4.0])
    out = factored_second_moment(row, col)
    np.testing.assert_allclose(out.sum(axis=1), row * col.sum() / row.sum())


def test_6_does_not_mutate_inputs():
    r = np.array([1.0, 2.0])
    factored_second_moment(r, np.array([3.0]))
    np.testing.assert_array_equal(r, [1.0, 2.0])

