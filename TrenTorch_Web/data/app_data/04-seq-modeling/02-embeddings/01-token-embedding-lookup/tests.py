"""
pytest data/app_data/04-seq-modeling/02-embeddings/01-token-embedding-lookup/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/02-embeddings/{Path(__file__).resolve().parent.name}")
embedding_forward = _module.embedding_forward


def test_single_id_returns_that_rows_embedding():
    table = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    result = embedding_forward(np.array([1]), table)
    assert np.allclose(result, [[3.0, 4.0]])


def test_sequence_of_ids_returns_corresponding_rows_in_order():
    table = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    ids = np.array([2, 0, 1])
    result = embedding_forward(ids, table)
    assert np.allclose(result, [[1.0, 1.0], [1.0, 0.0], [0.0, 1.0]])


def test_batch_of_sequences_has_correct_output_shape():
    table = np.random.randn(20, 8)
    ids = np.random.randint(0, 20, size=(4, 6))
    result = embedding_forward(ids, table)
    assert result.shape == (4, 6, 8)


def test_repeated_id_returns_the_same_row_every_time():
    table = np.array([[1.0, 2.0], [9.0, 9.0]])
    ids = np.array([1, 1, 1])
    result = embedding_forward(ids, table)
    assert np.allclose(result[0], result[1])
    assert np.allclose(result[1], result[2])


def test_does_not_modify_the_embedding_table():
    table = np.array([[1.0, 2.0], [3.0, 4.0]])
    original = table.copy()
    result = embedding_forward(np.array([0, 1]), table)
    result[0, 0] = 999.0
    assert np.allclose(table, original)


def test_matches_known_oracle_from_pytorch_nn_embedding():
    # verified directly against torch.nn.Embedding with a fixed seed
    table = np.array(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9],
        ]
    )
    ids = np.array([[0, 1], [2, 0]])
    result = embedding_forward(ids, table)
    expected = np.array([[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], [[0.7, 0.8, 0.9], [0.1, 0.2, 0.3]]])
    assert np.allclose(result, expected)


def test_uses_the_actual_table_rows_not_the_ids_themselves():
    # Directly targets a mutant that accidentally returns token_ids cast
    # to float, or some transformation of the ids directly, instead of
    # actually indexing into embedding_table: a table with values
    # unrelated to the ids' own numeric value would expose this clearly.
    table = np.array([[100.0, 200.0], [300.0, 400.0], [500.0, 600.0]])
    ids = np.array([0, 1, 2])
    result = embedding_forward(ids, table)
    assert np.allclose(result, table)
