"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/02-word2vec/03-skipgram-probability/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-w2v-skipgram-prob")
skipgram_probability = _module.skipgram_probability


import numpy as np


def test_1_zero_output_vectors_give_uniform_probability():
    assert abs(skipgram_probability(np.ones(2), np.zeros((5, 2)), 0) - 0.2) < 1e-12


def test_2_hand_value_for_two_words():
    p = skipgram_probability(np.array([1.0]), np.array([[1.0], [0.0]]), 0)
    assert abs(p - np.e / (np.e + 1.0)) < 1e-12


def test_3_probabilities_over_vocabulary_sum_to_one():
    U = np.array([[1.0, 0.0], [0.0, 2.0], [-1.0, 1.0]])
    v = np.array([0.3, 0.7])
    total = sum(skipgram_probability(v, U, o) for o in range(3))
    assert abs(total - 1.0) < 1e-12


def test_4_higher_score_gives_higher_probability():
    U = np.array([[1.0], [3.0]])
    assert skipgram_probability(np.array([1.0]), U, 1) > skipgram_probability(np.array([1.0]), U, 0)


def test_5_returns_a_python_float():
    assert isinstance(skipgram_probability(np.ones(2), np.ones((3, 2)), 1), float)


def test_6_does_not_mutate_inputs():
    v = np.array([1.0, 2.0])
    skipgram_probability(v, np.ones((2, 2)), 0)
    np.testing.assert_array_equal(v, [1.0, 2.0])

