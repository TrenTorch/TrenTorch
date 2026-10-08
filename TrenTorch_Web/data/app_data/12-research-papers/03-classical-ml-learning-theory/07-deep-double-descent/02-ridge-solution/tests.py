"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/07-deep-double-descent/02-ridge-solution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-double-descent-ridge")
ridge_solution = _module.ridge_solution


import numpy as np


def test_1_matches_hand_computation_for_one_by_one():
    w = ridge_solution(np.array([[1.0]]), np.array([2.0]), 1.0)
    np.testing.assert_allclose(w, [1.0])


def test_2_zero_penalty_matches_least_squares_when_overdetermined():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(10, 3))
    y = rng.normal(size=10)
    np.testing.assert_allclose(ridge_solution(X, y, 0.0), np.linalg.lstsq(X, y, rcond=None)[0], atol=1e-8)


def test_3_larger_penalty_shrinks_the_weights():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(8, 3))
    y = rng.normal(size=8)
    assert np.linalg.norm(ridge_solution(X, y, 100.0)) < np.linalg.norm(ridge_solution(X, y, 0.01))


def test_4_output_has_feature_count_entries():
    assert ridge_solution(np.ones((4, 2)), np.ones(4), 1.0).shape == (2,)


def test_5_positive_penalty_handles_singular_design():
    X = np.array([[1.0, 1.0], [1.0, 1.0]])
    w = ridge_solution(X, np.array([1.0, 1.0]), 1.0)
    assert np.all(np.isfinite(w))


def test_6_does_not_mutate_inputs():
    X = np.ones((2, 2))
    ridge_solution(X, np.ones(2), 1.0)
    np.testing.assert_array_equal(X, np.ones((2, 2)))

