"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/11-deep-infomax/01-jsd-estimate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dim-jsd-estimate")
jsd_estimate = _module.jsd_estimate


import math

import numpy as np


def test_1_equal_scores_give_minus_two_log_two():
    assert abs(jsd_estimate(np.zeros(3), np.zeros(3)) - (-2 * math.log(2.0))) < 1e-12


def test_2_well_separated_scores_give_larger_estimate():
    well = jsd_estimate(np.full(4, 10.0), np.full(4, -10.0))
    poor = jsd_estimate(np.zeros(4), np.zeros(4))
    assert well > poor


def test_3_returns_a_python_float():
    assert isinstance(jsd_estimate(np.ones(2), np.zeros(2)), float)


def test_4_positive_scores_help_negative_scores_hurt():
    assert jsd_estimate(np.array([2.0]), np.array([0.0])) > jsd_estimate(np.array([0.0]), np.array([2.0]))


def test_5_is_bounded_above_by_zero_for_equal_inputs():
    assert jsd_estimate(np.array([1.0]), np.array([1.0])) <= 0.0


def test_6_does_not_mutate_inputs():
    p = np.array([1.0])
    jsd_estimate(p, np.array([0.0]))
    np.testing.assert_array_equal(p, [1.0])

