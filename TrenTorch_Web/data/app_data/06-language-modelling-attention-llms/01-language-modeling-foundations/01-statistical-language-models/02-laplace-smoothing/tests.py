"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
smoothed_probabilities = _module.smoothed_probabilities


def test_1_hand_computed():
    counts = np.array([[1, 3], [0, 0]])
    p = smoothed_probabilities(counts, 1.0)
    assert np.allclose(p, [[2 / 6, 4 / 6], [0.5, 0.5]])


def test_2_rows_sum_to_one():
    rng = np.random.RandomState(0)
    counts = rng.randint(0, 9, size=(6, 6))
    p = smoothed_probabilities(counts, 0.5)
    assert np.allclose(p.sum(axis=1), 1.0)


def test_3_unseen_pairs_get_positive_probability():
    counts = np.array([[5, 0, 0], [0, 4, 1], [0, 0, 0]])
    assert (smoothed_probabilities(counts, 0.1) > 0).all()


def test_4_small_alpha_approaches_maximum_likelihood():
    counts = np.array([[6, 2, 2], [1, 8, 1]])
    p = smoothed_probabilities(counts, 1e-9)
    assert np.allclose(p, counts / counts.sum(axis=1, keepdims=True), atol=1e-6)


def test_5_large_alpha_approaches_uniform():
    counts = np.array([[100, 0, 0], [0, 7, 3]])
    assert np.allclose(smoothed_probabilities(counts, 1e9), 1 / 3, atol=1e-6)


def test_6_matches_explicit_formula():
    counts = np.array([[3, 0, 1], [2, 2, 2]])
    alpha, V = 0.7, 3
    p = smoothed_probabilities(counts, alpha)
    for i in range(2):
        for j in range(3):
            assert np.isclose(p[i, j], (counts[i, j] + alpha) / (counts[i].sum() + alpha * V))


def test_7_input_not_modified():
    counts = np.array([[1, 2], [3, 4]])
    snapshot = counts.copy()
    smoothed_probabilities(counts, 1.0)
    assert np.array_equal(counts, snapshot)
