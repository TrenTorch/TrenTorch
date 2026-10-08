"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/09-scikit-learn/02-cv-mean/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sklearn-cv-mean")
mean_cv_score = _module.mean_cv_score


import numpy as np


def test_1_matches_a_hand_value():
    assert abs(mean_cv_score([0.8, 0.9, 1.0]) - 0.9) < 1e-12


def test_2_single_fold_is_its_own_score():
    assert mean_cv_score([0.42]) == 0.42


def test_3_identical_scores_give_that_score():
    assert abs(mean_cv_score([0.5, 0.5, 0.5]) - 0.5) < 1e-12


def test_4_accepts_numpy_arrays():
    assert abs(mean_cv_score(np.array([1.0, 3.0])) - 2.0) < 1e-12


def test_5_returns_a_float():
    assert isinstance(mean_cv_score([1, 2]), float)


def test_6_lies_between_the_min_and_max_scores():
    s = [0.1, 0.5, 0.9]
    assert min(s) <= mean_cv_score(s) <= max(s)

