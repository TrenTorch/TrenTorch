"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/06-simclr/01-cosine-similarity/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-simclr-cosine")
cosine_similarity = _module.cosine_similarity


import numpy as np


def test_1_parallel_vectors_have_similarity_one():
    assert abs(cosine_similarity(np.array([1.0, 2.0]), np.array([2.0, 4.0])) - 1.0) < 1e-12


def test_2_orthogonal_vectors_have_similarity_zero():
    assert abs(cosine_similarity(np.array([1.0, 0.0]), np.array([0.0, 3.0]))) < 1e-12


def test_3_opposite_vectors_have_similarity_minus_one():
    assert abs(cosine_similarity(np.array([1.0, 1.0]), np.array([-1.0, -1.0])) + 1.0) < 1e-12


def test_4_scale_invariant():
    a = np.array([1.0, 3.0])
    assert abs(cosine_similarity(a, np.array([2.0, 1.0])) - cosine_similarity(5 * a, np.array([2.0, 1.0]))) < 1e-12


def test_5_zero_vector_gives_zero():
    assert cosine_similarity(np.zeros(2), np.array([1.0, 1.0])) == 0.0


def test_6_does_not_mutate_inputs():
    a = np.array([1.0, 2.0])
    cosine_similarity(a, np.array([3.0, 4.0]))
    np.testing.assert_array_equal(a, [1.0, 2.0])

