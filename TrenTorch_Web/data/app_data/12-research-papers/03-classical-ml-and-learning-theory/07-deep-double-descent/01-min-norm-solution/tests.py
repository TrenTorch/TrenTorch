"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/07-deep-double-descent/01-min-norm-solution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-double-descent-min-norm")
min_norm_solution = _module.min_norm_solution


import numpy as np


def test_1_overparameterized_system_is_interpolated():
    X = np.array([[1.0, 2.0, 3.0]])
    y = np.array([6.0])
    np.testing.assert_allclose(X @ min_norm_solution(X, y), y, atol=1e-9)


def test_2_chooses_the_smallest_norm_solution():
    X = np.array([[1.0, 1.0]])
    w = min_norm_solution(X, np.array([2.0]))
    np.testing.assert_allclose(w, [1.0, 1.0], atol=1e-9)


def test_3_output_shape_is_feature_count():
    assert min_norm_solution(np.ones((2, 5)), np.ones(2)).shape == (5,)


def test_4_matches_least_squares_when_overdetermined():
    X = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    y = np.array([1.0, 2.0, 3.0])
    w = min_norm_solution(X, y)
    np.testing.assert_allclose(w, np.linalg.lstsq(X, y, rcond=None)[0], atol=1e-9)


def test_5_solution_lies_in_the_row_space():
    X = np.array([[1.0, 2.0, 0.0]])
    w = min_norm_solution(X, np.array([1.0]))
    null_direction = np.array([2.0, -1.0, 0.0])
    assert abs(w @ null_direction) < 1e-9


def test_6_does_not_mutate_inputs():
    X = np.ones((1, 2))
    min_norm_solution(X, np.array([1.0]))
    np.testing.assert_array_equal(X, np.ones((1, 2)))

