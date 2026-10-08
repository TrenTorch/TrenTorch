"""
pytest data/app_data/12-research-papers/01-optimization-and-training/08-sophia/02-hutchinson/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sophia-hutchinson")
hutchinson_estimate = _module.hutchinson_estimate


import numpy as np


def test_1_hand_case():
    np.testing.assert_allclose(hutchinson_estimate(np.array([2.0, 3.0]), np.array([1.0, -1.0])), [2.0, -3.0])


def test_2_probe_of_ones_gives_hessian_vector_product():
    np.testing.assert_allclose(hutchinson_estimate(np.array([5.0, 7.0]), np.ones(2)), [5.0, 7.0])


def test_3_keeps_the_shape():
    assert hutchinson_estimate(np.ones(4), np.ones(4)).shape == (4,)


def test_4_sign_flips_with_probe():
    a = hutchinson_estimate(np.array([3.0]), np.array([1.0]))
    b = hutchinson_estimate(np.array([3.0]), np.array([-1.0]))
    np.testing.assert_allclose(a, -b)


def test_5_averages_to_diagonal_over_probes():
    H = np.array([[2.0, 1.0], [1.0, 3.0]])
    rng = np.random.default_rng(0)
    est = np.zeros(2)
    n = 4000
    for _ in range(n):
        u = rng.choice([-1.0, 1.0], size=2)
        est += hutchinson_estimate(H @ u, u)
    np.testing.assert_allclose(est / n, np.diag(H), atol=0.15)


def test_6_does_not_mutate_inputs():
    u = np.array([1.0, -1.0])
    hutchinson_estimate(np.array([1.0, 1.0]), u)
    np.testing.assert_array_equal(u, [1.0, -1.0])

