"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/09-cpc/01-cpc-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-cpc-loss")
cpc_loss = _module.cpc_loss


import math

import numpy as np


def test_1_uniform_scores_give_log_n():
    assert abs(cpc_loss(np.zeros(5), 2) - math.log(5.0)) < 1e-12


def test_2_dominant_true_score_gives_small_loss():
    assert cpc_loss(np.array([0.0, 0.0, 30.0]), 2) < 1e-6


def test_3_wrong_candidate_scored_highest_gives_large_loss():
    assert cpc_loss(np.array([10.0, 0.0]), 1) > 9.0


def test_4_returns_a_python_float():
    assert isinstance(cpc_loss(np.array([1.0, 2.0]), 0), float)


def test_5_is_invariant_to_adding_a_constant():
    s = np.array([0.5, 1.5, -0.2])
    assert abs(cpc_loss(s, 1) - cpc_loss(s + 7.0, 1)) < 1e-12


def test_6_does_not_mutate_scores():
    s = np.array([1.0, 2.0])
    cpc_loss(s, 0)
    np.testing.assert_array_equal(s, [1.0, 2.0])

