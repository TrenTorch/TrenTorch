"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/07-greedy-decoding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
greedy_decode = _module.greedy_decode


def test_output_length_grows_by_num_new_tokens():
    rng = np.random.RandomState(0)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result = greedy_decode(token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None, num_new_tokens=5)
    assert result.shape == (1, seq_len + 5)


def test_original_tokens_are_preserved_as_a_prefix():
    rng = np.random.RandomState(1)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result = greedy_decode(token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None, num_new_tokens=4)
    assert np.array_equal(result[:, :seq_len], token_ids)


def test_decoding_is_deterministic():
    rng = np.random.RandomState(2)
    vocab_size, d_model, num_heads, seq_len = 8, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result_a = greedy_decode(token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None, num_new_tokens=3)
    result_b = greedy_decode(token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None, num_new_tokens=3)
    assert np.array_equal(result_a, result_b)


def test_always_picks_the_single_highest_scoring_token():
    # d_model=1, and every token's embedding is the SAME large positive
    # constant (dominating the bounded [-1, 1] positional encoding), so
    # every hidden state is guaranteed positive. output_weight[2] is a
    # large POSITIVE multiplier (huge positive logit), every other row a
    # large NEGATIVE multiplier (huge negative logit) -- token 2 must
    # always win, regardless of which tokens came before it.
    vocab_size, d_model, num_heads, seq_len = 5, 1, 1, 3
    token_ids = np.array([[0, 1, 3]])
    embedding_table = np.full((vocab_size, d_model), 100.0)
    output_weight = np.full((vocab_size, d_model), -1.0)
    output_weight[2] = 1.0

    result = greedy_decode(
        token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=False, output_weight=output_weight, num_new_tokens=3
    )
    generated = result[:, seq_len:]
    assert np.all(generated == 2)


def test_num_new_tokens_zero_returns_the_input_unchanged():
    rng = np.random.RandomState(4)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result = greedy_decode(token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None, num_new_tokens=0)
    assert np.array_equal(result, token_ids)
