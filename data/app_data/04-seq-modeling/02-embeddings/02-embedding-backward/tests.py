"""
pytest data/app_data/04-seq-modeling/02-embeddings/02-embedding-backward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/02-embeddings/{Path(__file__).resolve().parent.name}")
embedding_backward = _module.embedding_backward


def test_output_shape_matches_vocab_size_and_embed_dim():
    grad_output = np.ones((3, 4))
    token_ids = np.array([0, 1, 2])
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=5)
    assert grad_table.shape == (5, 4)


def test_unreferenced_rows_stay_exactly_zero():
    grad_output = np.ones((2, 3))
    token_ids = np.array([0, 1])
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=5)
    assert np.allclose(grad_table[2], 0.0)
    assert np.allclose(grad_table[3], 0.0)
    assert np.allclose(grad_table[4], 0.0)


def test_single_occurrence_copies_the_gradient_directly():
    grad_output = np.array([[1.0, 2.0, 3.0]])
    token_ids = np.array([2])
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=4)
    assert np.allclose(grad_table[2], [1.0, 2.0, 3.0])


def test_repeated_id_sums_all_of_its_gradient_contributions():
    grad_output = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])
    token_ids = np.array([0, 0, 0])  # same id, three times
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=2)
    assert np.allclose(grad_table[0], [6.0, 6.0])


def test_matches_known_oracle_from_pytorch_embedding_backward():
    # verified directly against torch.nn.Embedding + loss.backward(), with
    # repeated ids present (id 1 appears three times)
    grad_output = np.ones((2, 3, 3))
    token_ids = np.array([[1, 2, 1], [0, 1, 4]])
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=5)
    expected = np.array(
        [
            [1.0, 1.0, 1.0],
            [3.0, 3.0, 3.0],
            [1.0, 1.0, 1.0],
            [0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0],
        ]
    )
    assert np.allclose(grad_table, expected)


def test_works_on_a_batch_of_sequences():
    grad_output = np.random.randn(2, 4, 6)
    token_ids = np.random.randint(0, 10, size=(2, 4))
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=10)
    assert grad_table.shape == (10, 6)


def test_total_gradient_sum_matches_sum_of_grad_output():
    # Sanity invariant: since every position's gradient ends up SOMEWHERE
    # in grad_table (accumulated, never dropped), the total sum across
    # the whole grad_table must equal the total sum across grad_output.
    grad_output = np.random.randn(3, 5, 4)
    token_ids = np.random.randint(0, 6, size=(3, 5))
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=6)
    assert np.isclose(grad_table.sum(), grad_output.sum())


def test_uses_accumulation_not_overwrite_for_repeated_ids():
    # Directly targets a mutant that uses plain fancy-indexed assignment
    # (grad_table[flat_ids] += flat_grad, or worse, grad_table[flat_ids]
    # = flat_grad) instead of a genuine scatter-add: for NumPy, `+=` on
    # fancy-indexed duplicate indices does NOT accumulate correctly (it
    # reads the same original value for every duplicate before writing,
    # so only the LAST write survives), silently dropping earlier
    # contributions for any repeated id.
    grad_output = np.array([[1.0], [10.0], [100.0]])
    token_ids = np.array([0, 0, 0])
    grad_table = embedding_backward(grad_output, token_ids, vocab_size=1)
    # correct: 1 + 10 + 100 = 111 (accumulated)
    # broken (last-write-wins): would be 100 only
    assert np.isclose(grad_table[0, 0], 111.0)
