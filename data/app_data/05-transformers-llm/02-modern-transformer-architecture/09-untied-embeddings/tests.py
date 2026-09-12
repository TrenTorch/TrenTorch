"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/09-untied-embeddings/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
output_projection_tied = _module.output_projection_tied
output_projection_untied = _module.output_projection_untied


def test_tied_output_shape_is_vocab_size():
    rng = np.random.RandomState(0)
    vocab_size, d_model, seq_len = 20, 8, 5
    hidden_states = rng.randn(seq_len, d_model)
    embedding_table = rng.randn(vocab_size, d_model)
    logits = output_projection_tied(hidden_states, embedding_table)
    assert logits.shape == (seq_len, vocab_size)


def test_untied_output_shape_is_vocab_size():
    rng = np.random.RandomState(1)
    vocab_size, d_model, seq_len = 20, 8, 5
    hidden_states = rng.randn(seq_len, d_model)
    output_weight = rng.randn(vocab_size, d_model)
    logits = output_projection_untied(hidden_states, output_weight)
    assert logits.shape == (seq_len, vocab_size)


def test_tied_and_untied_agree_when_given_the_same_matrix():
    rng = np.random.RandomState(2)
    vocab_size, d_model, seq_len = 10, 6, 3
    hidden_states = rng.randn(seq_len, d_model)
    shared_matrix = rng.randn(vocab_size, d_model)

    tied_logits = output_projection_tied(hidden_states, shared_matrix)
    untied_logits = output_projection_untied(hidden_states, shared_matrix)
    assert np.allclose(tied_logits, untied_logits, atol=1e-10)


def test_tied_projection_changes_if_the_embedding_table_changes():
    # Weight tying's whole point: updating the (shared) embedding table
    # during training automatically changes the output projection too,
    # since it's literally the SAME matrix, not a copy.
    rng = np.random.RandomState(3)
    vocab_size, d_model, seq_len = 10, 6, 3
    hidden_states = rng.randn(seq_len, d_model)
    embedding_table = rng.randn(vocab_size, d_model)

    logits_before = output_projection_tied(hidden_states, embedding_table)
    embedding_table += rng.randn(vocab_size, d_model) * 5.0
    logits_after = output_projection_tied(hidden_states, embedding_table)
    assert not np.allclose(logits_before, logits_after, atol=1e-4)


def test_untied_projection_is_unaffected_by_changes_to_an_unrelated_embedding_table():
    # Directly demonstrates the CONTRAST: an untied model's embedding
    # table and output projection are independent parameters, so
    # changing one has no effect on the other.
    rng = np.random.RandomState(4)
    vocab_size, d_model, seq_len = 10, 6, 3
    hidden_states = rng.randn(seq_len, d_model)
    embedding_table = rng.randn(vocab_size, d_model)
    output_weight = rng.randn(vocab_size, d_model)

    logits_before = output_projection_untied(hidden_states, output_weight)
    embedding_table += rng.randn(vocab_size, d_model) * 5.0  # unrelated matrix, changed
    logits_after = output_projection_untied(hidden_states, output_weight)
    assert np.allclose(logits_before, logits_after, atol=1e-10)


def test_projects_via_the_matrixs_transpose_not_the_matrix_itself():
    # Directly targets a mutant that forgets to transpose (or transposes
    # the wrong operand), which would either error on shape mismatch or
    # silently produce the wrong result for non-square matrices.
    rng = np.random.RandomState(5)
    vocab_size, d_model, seq_len = 7, 4, 2  # non-square, catches a missing .T immediately
    hidden_states = rng.randn(seq_len, d_model)
    embedding_table = rng.randn(vocab_size, d_model)
    logits = output_projection_tied(hidden_states, embedding_table)
    expected = hidden_states @ embedding_table.T
    assert np.allclose(logits, expected, atol=1e-10)
