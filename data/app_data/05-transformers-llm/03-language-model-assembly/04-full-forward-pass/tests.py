"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/04-full-forward-pass/tests.py
"""

import sys
from math import log
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
full_lm_forward = _module.full_lm_forward

build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def _random_block_params(rng, d_model, d_ff):
    return dict(
        weight_o=rng.randn(d_model, d_model) * 0.3,
        bias_o=rng.randn(d_model) * 0.1,
        ffn_weight1=rng.randn(d_ff, d_model) * 0.3,
        ffn_bias1=rng.randn(d_ff) * 0.1,
        ffn_weight2=rng.randn(d_model, d_ff) * 0.3,
        ffn_bias2=rng.randn(d_model) * 0.1,
        gamma1=np.ones(d_model),
        beta1=np.zeros(d_model),
        gamma2=np.ones(d_model),
        beta2=np.zeros(d_model),
    )


def test_output_shape_is_batch_seq_len_vocab_size_tied():
    rng = np.random.RandomState(0)
    vocab_size, d_model, d_ff, num_heads, seq_len = 20, 8, 16, 2, 6
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)
    blocks_params = [_random_block_params(rng, d_model, d_ff) for _ in range(2)]

    logits = full_lm_forward(token_ids, embedding_table, blocks_params, num_heads, tied=True)
    assert logits.shape == (1, seq_len, vocab_size)


def test_output_shape_untied():
    rng = np.random.RandomState(1)
    vocab_size, d_model, d_ff, num_heads, seq_len = 20, 8, 16, 2, 6
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)
    output_weight = rng.randn(vocab_size, d_model)
    blocks_params = [_random_block_params(rng, d_model, d_ff) for _ in range(2)]

    logits = full_lm_forward(
        token_ids, embedding_table, blocks_params, num_heads, tied=False, output_weight=output_weight
    )
    assert logits.shape == (1, seq_len, vocab_size)


def test_supports_a_causal_mask():
    rng = np.random.RandomState(2)
    vocab_size, d_model, d_ff, num_heads, seq_len = 20, 8, 16, 2, 6
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)
    blocks_params = [_random_block_params(rng, d_model, d_ff)]
    mask = build_causal_mask(seq_len)

    logits = full_lm_forward(token_ids, embedding_table, blocks_params, num_heads, tied=True, mask=mask)
    assert logits.shape == (1, seq_len, vocab_size)
    assert np.all(np.isfinite(logits))


def test_zero_blocks_still_produces_logits_from_embeddings_alone():
    rng = np.random.RandomState(3)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    logits = full_lm_forward(token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True)
    token_embeddings = embedding_table[token_ids]

    pos = np.arange(seq_len)[:, None]
    div_term = np.exp(np.arange(0, d_model, 2) * -(log(10000.0) / d_model))
    pe = np.zeros((seq_len, d_model))
    pe[:, 0::2] = np.sin(pos * div_term)
    pe[:, 1::2] = np.cos(pos * div_term)
    expected_hidden = token_embeddings + pe
    expected_logits = expected_hidden @ embedding_table.T
    assert np.allclose(logits, expected_logits, atol=1e-8)


def test_different_token_ids_produce_different_logits():
    rng = np.random.RandomState(4)
    vocab_size, d_model, d_ff, num_heads, seq_len = 15, 8, 16, 2, 5
    embedding_table = rng.randn(vocab_size, d_model)
    blocks_params = [_random_block_params(rng, d_model, d_ff)]

    token_ids_a = rng.randint(0, vocab_size, size=(1, seq_len))
    token_ids_b = rng.randint(0, vocab_size, size=(1, seq_len))
    logits_a = full_lm_forward(token_ids_a, embedding_table, blocks_params, num_heads, tied=True)
    logits_b = full_lm_forward(token_ids_b, embedding_table, blocks_params, num_heads, tied=True)
    assert not np.allclose(logits_a, logits_b, atol=1e-4)


def test_tied_and_untied_give_different_logits_for_independent_matrices():
    # Directly targets a mutant that ignores the `tied` flag entirely.
    rng = np.random.RandomState(5)
    vocab_size, d_model, d_ff, num_heads, seq_len = 15, 8, 16, 2, 5
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)
    output_weight = rng.randn(vocab_size, d_model)
    blocks_params = [_random_block_params(rng, d_model, d_ff)]

    tied_logits = full_lm_forward(token_ids, embedding_table, blocks_params, num_heads, tied=True)
    untied_logits = full_lm_forward(
        token_ids, embedding_table, blocks_params, num_heads, tied=False, output_weight=output_weight
    )
    assert not np.allclose(tied_logits, untied_logits, atol=1e-4)
