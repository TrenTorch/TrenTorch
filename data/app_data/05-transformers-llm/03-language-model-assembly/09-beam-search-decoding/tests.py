"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/09-beam-search-decoding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
sequence_log_prob = _module.sequence_log_prob
beam_search_decode = _module.beam_search_decode

greedy_decode = load_solution("05-transformers-llm/03-language-model-assembly/07-greedy-decoding").greedy_decode


def test_output_length_grows_by_num_new_tokens():
    rng = np.random.RandomState(0)
    vocab_size, d_model, num_heads, seq_len = 8, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result = beam_search_decode(
        token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None,
        num_new_tokens=4, beam_width=3,
    )
    assert result.shape == (1, seq_len + 4)


def test_original_tokens_are_preserved_as_a_prefix():
    rng = np.random.RandomState(1)
    vocab_size, d_model, num_heads, seq_len = 8, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result = beam_search_decode(
        token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None,
        num_new_tokens=3, beam_width=2,
    )
    assert np.array_equal(result[:, :seq_len], token_ids)


def test_beam_width_one_matches_greedy_decode_exactly():
    rng = np.random.RandomState(2)
    vocab_size, d_model, num_heads, seq_len = 8, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    beam_result = beam_search_decode(
        token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None,
        num_new_tokens=5, beam_width=1,
    )
    greedy_result = greedy_decode(
        token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None,
        num_new_tokens=5,
    )
    assert np.array_equal(beam_result, greedy_result)


def test_beam_search_is_deterministic():
    rng = np.random.RandomState(3)
    vocab_size, d_model, num_heads, seq_len = 8, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result_a = beam_search_decode(
        token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None,
        num_new_tokens=4, beam_width=3,
    )
    result_b = beam_search_decode(
        token_ids, embedding_table, blocks_params=[], num_heads=num_heads, tied=True, output_weight=None,
        num_new_tokens=4, beam_width=3,
    )
    assert np.array_equal(result_a, result_b)


def test_wider_beam_finds_a_sequence_with_at_least_as_high_log_probability():
    # The defining property of beam search: widening the beam can only
    # ever find an equal-or-BETTER (higher cumulative log-probability)
    # completed sequence than a narrower beam, never a worse one, since
    # the narrower beam's entire search tree is a subset of the wider
    # beam's.
    rng = np.random.RandomState(4)
    vocab_size, d_model, d_ff, num_heads, seq_len = 12, 8, 16, 2, 4
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)
    blocks_params = [
        dict(
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
    ]

    scores = []
    for beam_width in [1, 2, 4]:
        result = beam_search_decode(
            token_ids, embedding_table, blocks_params, num_heads, tied=True, output_weight=None,
            num_new_tokens=4, beam_width=beam_width,
        )
        score = sequence_log_prob(result, embedding_table, blocks_params, num_heads, tied=True, output_weight=None)
        scores.append(score)

    assert scores[0] <= scores[1] + 1e-8
    assert scores[1] <= scores[2] + 1e-8


def test_sequence_log_prob_is_negative_of_what_next_token_loss_would_sum_to():
    rng = np.random.RandomState(5)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 5
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    next_token_cross_entropy_loss = load_solution(
        "05-transformers-llm/03-language-model-assembly/03-next-token-cross-entropy"
    ).next_token_cross_entropy_loss
    build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask
    full_lm_forward = load_solution("05-transformers-llm/03-language-model-assembly/04-full-forward-pass").full_lm_forward

    mask = build_causal_mask(seq_len)
    logits = full_lm_forward(token_ids, embedding_table, [], num_heads, tied=True, output_weight=None, mask=mask)
    mean_loss = next_token_cross_entropy_loss(logits, token_ids)

    log_prob = sequence_log_prob(token_ids, embedding_table, [], num_heads, tied=True, output_weight=None)
    # mean_loss * (seq_len - 1) is the SUM of negative log-probs; log_prob
    # should be its exact negation.
    assert np.isclose(log_prob, -mean_loss * (seq_len - 1), atol=1e-6)
