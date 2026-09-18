"""
pytest data/app_data/04-seq-modeling/02-embeddings/04-learned-positional-embedding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/02-embeddings/{Path(__file__).resolve().parent.name}")
learned_positional_embedding = _module.learned_positional_embedding


def test_output_shape_matches_seq_len_and_embed_dim():
    table = np.random.randn(20, 8)
    result = learned_positional_embedding(seq_len=5, position_table=table)
    assert result.shape == (5, 8)


def test_returns_rows_in_original_position_order():
    table = np.array([[1.0], [2.0], [3.0], [4.0]])
    result = learned_positional_embedding(seq_len=3, position_table=table)
    assert np.allclose(result, [[1.0], [2.0], [3.0]])


def test_row_zero_matches_the_tables_own_row_zero():
    table = np.array([[9.0, 9.0], [1.0, 1.0]])
    result = learned_positional_embedding(seq_len=2, position_table=table)
    assert np.allclose(result[0], table[0])


def test_seq_len_shorter_than_table_only_returns_the_needed_rows():
    table = np.random.randn(100, 4)
    result = learned_positional_embedding(seq_len=3, position_table=table)
    assert result.shape[0] == 3
    assert np.allclose(result, table[:3])


def test_seq_len_equal_to_full_table_length_returns_the_whole_table():
    table = np.random.randn(10, 4)
    result = learned_positional_embedding(seq_len=10, position_table=table)
    assert np.allclose(result, table)


def test_does_not_reorder_rows():
    # Directly targets a mutant that reverses or shuffles the rows
    # (position order matters: row i must be position i's embedding, not
    # some other position's).
    table = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    result = learned_positional_embedding(seq_len=5, position_table=table)
    assert np.array_equal(result.flatten(), [1.0, 2.0, 3.0, 4.0, 5.0])
