"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/12-bayesian-optimization/02-lower-confidence-bound/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bo-lower-confidence-bound")
lower_confidence_bound = _module.lower_confidence_bound


import numpy as np


def test_1_matches_a_hand_value():
    assert abs(float(lower_confidence_bound(2.0, 1.0, 0.5)) - 1.5) < 1e-12


def test_2_zero_kappa_is_the_mean():
    np.testing.assert_allclose(lower_confidence_bound(np.array([1.0, 3.0]), np.array([9.0, 9.0]), 0.0), [1.0, 3.0])


def test_3_uncertainty_lowers_the_bound():
    assert float(lower_confidence_bound(0.0, 2.0, 1.0)) < 0.0


def test_4_larger_kappa_favors_uncertain_points():
    a = float(lower_confidence_bound(1.0, 1.0, 1.0))
    b = float(lower_confidence_bound(1.0, 1.0, 3.0))
    assert b < a


def test_5_keeps_the_shape():
    assert lower_confidence_bound(np.ones(4), np.ones(4), 1.0).shape == (4,)


def test_6_does_not_mutate_inputs():
    mu = np.array([1.0])
    lower_confidence_bound(mu, np.array([1.0]), 1.0)
    np.testing.assert_array_equal(mu, [1.0])

