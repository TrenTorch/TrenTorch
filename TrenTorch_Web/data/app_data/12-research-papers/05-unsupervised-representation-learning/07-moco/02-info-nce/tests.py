"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/07-moco/02-info-nce/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-moco-info-nce")
info_nce = _module.info_nce


import math

import numpy as np


def test_1_equal_similarities_give_log_of_candidates():
    q = np.array([1.0, 0.0])
    keys = np.array([1.0, 0.0])
    negs = np.array([[1.0, 0.0], [1.0, 0.0]])
    assert abs(info_nce(q, keys, negs, 1.0) - math.log(3.0)) < 1e-9


def test_2_positive_much_closer_gives_small_loss():
    q = np.array([1.0, 0.0])
    assert info_nce(q, np.array([1.0, 0.0]), np.array([[-1.0, 0.0]]), 0.1) < 1e-6


def test_3_scaling_the_query_changes_nothing():
    q = np.array([1.0, 2.0])
    k = np.array([2.0, 1.0])
    negs = np.array([[0.0, 1.0]])
    assert abs(info_nce(q, k, negs, 0.5) - info_nce(10 * q, k, negs, 0.5)) < 1e-9


def test_4_returns_a_python_float():
    assert isinstance(info_nce(np.ones(2), np.ones(2), np.ones((2, 2)), 1.0), float)


def test_5_more_queue_entries_raise_the_loss():
    q = np.array([1.0, 0.0])
    k = np.array([0.0, 1.0])
    a = info_nce(q, k, np.array([[1.0, 0.0]]), 1.0)
    b = info_nce(q, k, np.array([[1.0, 0.0], [1.0, 0.0], [1.0, 0.0]]), 1.0)
    assert b > a


def test_6_does_not_mutate_inputs():
    q = np.array([3.0, 4.0])
    info_nce(q, np.array([1.0, 0.0]), np.array([[0.0, 1.0]]), 1.0)
    np.testing.assert_array_equal(q, [3.0, 4.0])

