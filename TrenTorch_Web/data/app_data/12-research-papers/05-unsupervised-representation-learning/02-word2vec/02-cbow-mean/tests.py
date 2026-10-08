"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/02-word2vec/02-cbow-mean/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-w2v-cbow-mean")
cbow_context_mean = _module.cbow_context_mean


import numpy as np


def test_1_averages_the_rows():
    np.testing.assert_allclose(cbow_context_mean(np.array([[1.0, 2.0], [3.0, 4.0]])), [2.0, 3.0])


def test_2_single_context_word_is_returned():
    np.testing.assert_allclose(cbow_context_mean(np.array([[5.0, -1.0]])), [5.0, -1.0])


def test_3_output_has_embedding_dimension():
    assert cbow_context_mean(np.ones((4, 7))).shape == (7,)


def test_4_identical_contexts_give_that_vector():
    np.testing.assert_allclose(cbow_context_mean(np.array([[2.0], [2.0], [2.0]])), [2.0])


def test_5_order_of_context_words_does_not_matter():
    a = cbow_context_mean(np.array([[1.0], [3.0]]))
    b = cbow_context_mean(np.array([[3.0], [1.0]]))
    np.testing.assert_allclose(a, b)


def test_6_does_not_mutate_input():
    x = np.array([[1.0], [2.0]])
    cbow_context_mean(x)
    np.testing.assert_array_equal(x, [[1.0], [2.0]])

