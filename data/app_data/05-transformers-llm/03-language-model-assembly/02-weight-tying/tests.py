"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/02-weight-tying/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
compute_output_logits = _module.compute_output_logits
count_output_head_parameters = _module.count_output_head_parameters


def test_tied_uses_the_embedding_table():
    rng = np.random.RandomState(0)
    vocab_size, d_model, seq_len = 10, 6, 3
    hidden_states = rng.randn(seq_len, d_model)
    embedding_table = rng.randn(vocab_size, d_model)
    logits = compute_output_logits(hidden_states, embedding_table, tied=True)
    assert np.allclose(logits, hidden_states @ embedding_table.T, atol=1e-10)


def test_untied_uses_output_weight_not_embedding_table():
    rng = np.random.RandomState(1)
    vocab_size, d_model, seq_len = 10, 6, 3
    hidden_states = rng.randn(seq_len, d_model)
    embedding_table = rng.randn(vocab_size, d_model)
    output_weight = rng.randn(vocab_size, d_model)
    logits = compute_output_logits(hidden_states, embedding_table, tied=False, output_weight=output_weight)
    assert np.allclose(logits, hidden_states @ output_weight.T, atol=1e-10)
    assert not np.allclose(logits, hidden_states @ embedding_table.T, atol=1e-4)


def test_tied_and_untied_agree_when_the_matrices_happen_to_be_equal():
    rng = np.random.RandomState(2)
    vocab_size, d_model, seq_len = 8, 5, 2
    hidden_states = rng.randn(seq_len, d_model)
    shared = rng.randn(vocab_size, d_model)
    tied_logits = compute_output_logits(hidden_states, shared, tied=True)
    untied_logits = compute_output_logits(hidden_states, shared, tied=False, output_weight=shared)
    assert np.allclose(tied_logits, untied_logits, atol=1e-10)


def test_tied_output_head_adds_zero_parameters():
    assert count_output_head_parameters(vocab_size=50000, d_model=768, tied=True) == 0


def test_untied_output_head_adds_vocab_size_times_d_model_parameters():
    assert count_output_head_parameters(vocab_size=50000, d_model=768, tied=False) == 50000 * 768


def test_untied_always_has_strictly_more_parameters_than_tied():
    vocab_size, d_model = 30000, 512
    tied_count = count_output_head_parameters(vocab_size, d_model, tied=True)
    untied_count = count_output_head_parameters(vocab_size, d_model, tied=False)
    assert untied_count > tied_count
