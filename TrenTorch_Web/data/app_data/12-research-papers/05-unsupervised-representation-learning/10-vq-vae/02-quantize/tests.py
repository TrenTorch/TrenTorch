"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/10-vq-vae/02-quantize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vq-quantize")
quantize = _module.quantize


import numpy as np


def test_1_single_index_returns_that_row():
    np.testing.assert_allclose(quantize(np.array([[1.0, 2.0], [3.0, 4.0]]), 1), [3.0, 4.0])


def test_2_array_of_indices_returns_matrix():
    out = quantize(np.eye(3), np.array([2, 0]))
    np.testing.assert_allclose(out, [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])


def test_3_output_dimension_is_code_dimension():
    assert quantize(np.zeros((5, 7)), 0).shape == (7,)


def test_4_repeated_index_repeats_the_code():
    out = quantize(np.array([[9.0]]), np.array([0, 0]))
    np.testing.assert_allclose(out, [[9.0], [9.0]])


def test_5_nearest_then_quantize_returns_the_code():
    codebook = np.array([[0.0], [5.0]])
    np.testing.assert_allclose(quantize(codebook, 1), [5.0])


def test_6_does_not_mutate_codebook():
    cb = np.array([[1.0], [2.0]])
    quantize(cb, 0)
    np.testing.assert_array_equal(cb, [[1.0], [2.0]])

