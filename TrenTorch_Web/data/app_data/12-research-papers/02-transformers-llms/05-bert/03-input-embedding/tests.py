"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/05-bert/03-input-embedding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bert-input-embedding")
bert_input_embedding = _module.bert_input_embedding


import numpy as np


def test_1_output_shape_is_sequence_by_dimension():
    out = bert_input_embedding(np.array([0, 1, 2]), np.array([0, 0, 1]), np.ones((5, 4)), np.ones((2, 4)), np.ones((8, 4)))
    assert out.shape == (3, 4)


def test_2_sums_the_three_embeddings_by_hand():
    tok = np.array([[1.0], [10.0]])
    seg = np.array([[100.0], [1000.0]])
    pos = np.array([[0.1], [0.2]])
    out = bert_input_embedding(np.array([1, 0]), np.array([0, 1]), tok, seg, pos)
    np.testing.assert_allclose(out, [[10.0 + 100.0 + 0.1], [1.0 + 1000.0 + 0.2]])


def test_3_zero_tables_give_zero():
    out = bert_input_embedding(np.array([0]), np.array([0]), np.zeros((3, 2)), np.zeros((2, 2)), np.zeros((4, 2)))
    np.testing.assert_allclose(out, 0.0)


def test_4_positions_follow_the_sequence_order():
    pos = np.arange(6.0).reshape(6, 1)
    out = bert_input_embedding(np.array([0, 0, 0]), np.array([0, 0, 0]), np.zeros((1, 1)), np.zeros((2, 1)), pos)
    np.testing.assert_allclose(out[:, 0], [0.0, 1.0, 2.0])


def test_5_segment_changes_the_representation():
    tok = np.zeros((2, 2))
    seg = np.array([[1.0, 0.0], [0.0, 1.0]])
    pos = np.zeros((3, 2))
    out = bert_input_embedding(np.array([0, 0]), np.array([0, 1]), tok, seg, pos)
    assert not np.array_equal(out[0], out[1])


def test_6_does_not_mutate_the_tables():
    tok = np.ones((2, 2))
    bert_input_embedding(np.array([0]), np.array([0]), tok, np.ones((2, 2)), np.ones((2, 2)))
    np.testing.assert_array_equal(tok, np.ones((2, 2)))

