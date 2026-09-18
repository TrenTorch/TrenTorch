"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/01-output-projection/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
output_projection = _module.output_projection


def test_output_shape_is_vocab_size():
    rng = np.random.RandomState(0)
    batch, seq_len, d_model, vocab_size = 2, 4, 8, 30
    hidden_states = rng.randn(batch, seq_len, d_model)
    output_weight = rng.randn(vocab_size, d_model)
    logits = output_projection(hidden_states, output_weight)
    assert logits.shape == (batch, seq_len, vocab_size)


def test_matches_manual_matmul_with_transpose():
    rng = np.random.RandomState(1)
    seq_len, d_model, vocab_size = 3, 5, 7
    hidden_states = rng.randn(seq_len, d_model)
    output_weight = rng.randn(vocab_size, d_model)
    logits = output_projection(hidden_states, output_weight)
    assert np.allclose(logits, hidden_states @ output_weight.T, atol=1e-10)


def test_zero_output_weight_gives_zero_logits():
    rng = np.random.RandomState(2)
    seq_len, d_model, vocab_size = 3, 5, 7
    hidden_states = rng.randn(seq_len, d_model)
    output_weight = np.zeros((vocab_size, d_model))
    logits = output_projection(hidden_states, output_weight)
    assert np.allclose(logits, 0.0, atol=1e-10)


def test_each_vocab_row_produces_an_independent_logit():
    # Directly targets a mutant that mixes up rows/columns of output_weight
    # (e.g. using output_weight directly instead of its transpose).
    d_model, vocab_size = 4, 3
    hidden_states = np.array([[1.0, 0.0, 0.0, 0.0]])  # picks out row 0 of output_weight.T's contribution
    output_weight = np.array([[10.0, 0.0, 0.0, 0.0], [0.0, 20.0, 0.0, 0.0], [0.0, 0.0, 30.0, 0.0]])
    logits = output_projection(hidden_states, output_weight)
    assert np.allclose(logits, [[10.0, 0.0, 0.0]], atol=1e-10)
