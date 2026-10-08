"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/06-simclr/03-l2-normalize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-simclr-l2-normalize")
l2_normalize = _module.l2_normalize


import numpy as np


def test_1_result_has_unit_norm():
    assert abs(np.linalg.norm(l2_normalize(np.array([3.0, 4.0]))) - 1.0) < 1e-12


def test_2_matches_a_hand_value():
    np.testing.assert_allclose(l2_normalize(np.array([3.0, 4.0])), [0.6, 0.8])


def test_3_direction_is_preserved():
    z = np.array([1.0, -2.0, 2.0])
    out = l2_normalize(z)
    assert np.allclose(out / np.linalg.norm(out), z / np.linalg.norm(z))


def test_4_zero_vector_stays_zero():
    np.testing.assert_allclose(l2_normalize(np.zeros(3)), np.zeros(3))


def test_5_keeps_the_shape():
    assert l2_normalize(np.ones(6)).shape == (6,)


def test_6_does_not_mutate_input():
    z = np.array([3.0, 4.0])
    l2_normalize(z)
    np.testing.assert_array_equal(z, [3.0, 4.0])

