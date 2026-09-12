"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/01-encoder-decoder-arrangements/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
encoder_block_forward = _module.encoder_block_forward
decoder_block_forward = _module.decoder_block_forward
encoder_decoder_cross_attention = _module.encoder_decoder_cross_attention


def _random_block_params(rng, d_model, d_ff):
    return dict(
        weight_o=rng.randn(d_model, d_model),
        bias_o=rng.randn(d_model),
        ffn_weight1=rng.randn(d_ff, d_model),
        ffn_bias1=rng.randn(d_ff),
        ffn_weight2=rng.randn(d_model, d_ff),
        ffn_bias2=rng.randn(d_model),
        gamma1=rng.randn(d_model),
        beta1=rng.randn(d_model),
        gamma2=rng.randn(d_model),
        beta2=rng.randn(d_model),
    )


def test_encoder_output_at_an_early_position_changes_when_a_later_token_changes():
    # Bidirectional: every position can see every other position,
    # including ones that come after it.
    rng = np.random.RandomState(0)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    x = rng.randn(1, seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)

    out_original = encoder_block_forward(x, num_heads, **params)

    x_perturbed = x.copy()
    x_perturbed[0, -1] += rng.randn(d_model) * 10.0  # non-uniform perturbation of the LAST (latest) position
    out_perturbed = encoder_block_forward(x_perturbed, num_heads, **params)

    assert not np.allclose(out_original[0, 0], out_perturbed[0, 0], atol=1e-4)


def test_decoder_output_at_an_early_position_is_unaffected_by_a_later_token():
    # Causal: an early position must never be influenced by a token that
    # comes after it.
    rng = np.random.RandomState(1)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    x = rng.randn(1, seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)

    out_original = decoder_block_forward(x, num_heads, **params)

    x_perturbed = x.copy()
    x_perturbed[0, -1] += rng.randn(d_model) * 10.0  # non-uniform perturbation of the LAST (latest) position
    out_perturbed = decoder_block_forward(x_perturbed, num_heads, **params)

    assert np.allclose(out_original[0, 0], out_perturbed[0, 0], atol=1e-6)
    # Sanity: the perturbed position's OWN output must change.
    assert not np.allclose(out_original[0, -1], out_perturbed[0, -1], atol=1e-4)


def test_decoder_output_at_an_early_position_changes_when_an_earlier_token_changes():
    # Causal masking still permits attending to earlier (and the same)
    # position -- only strictly-future positions are blocked.
    rng = np.random.RandomState(2)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    x = rng.randn(1, seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)

    out_original = decoder_block_forward(x, num_heads, **params)

    x_perturbed = x.copy()
    x_perturbed[0, 0] += rng.randn(d_model) * 10.0  # non-uniform perturbation of the FIRST (earliest) position
    out_perturbed = decoder_block_forward(x_perturbed, num_heads, **params)

    assert not np.allclose(out_original[0, -1], out_perturbed[0, -1], atol=1e-4)


def test_cross_attention_query_and_key_value_sequence_lengths_can_differ():
    rng = np.random.RandomState(3)
    d_model, num_heads = 8, 2
    decoder_seq_len, encoder_seq_len = 4, 7
    decoder_hidden = rng.randn(1, decoder_seq_len, d_model)
    encoder_output = rng.randn(1, encoder_seq_len, d_model)
    weight_o = rng.randn(d_model, d_model)
    bias_o = rng.randn(d_model)

    result = encoder_decoder_cross_attention(decoder_hidden, encoder_output, num_heads, weight_o, bias_o)
    assert result.shape == (1, decoder_seq_len, d_model)


def test_cross_attention_output_depends_on_encoder_output_not_only_decoder_hidden():
    # Directly targets a mutant that accidentally runs self-attention on
    # decoder_hidden (ignoring encoder_output as key/value).
    rng = np.random.RandomState(4)
    d_model, num_heads, seq_len = 8, 2, 4
    decoder_hidden = rng.randn(1, seq_len, d_model)
    encoder_output_a = rng.randn(1, seq_len, d_model)
    encoder_output_b = rng.randn(1, seq_len, d_model)
    weight_o = rng.randn(d_model, d_model)
    bias_o = rng.randn(d_model)

    result_a = encoder_decoder_cross_attention(decoder_hidden, encoder_output_a, num_heads, weight_o, bias_o)
    result_b = encoder_decoder_cross_attention(decoder_hidden, encoder_output_b, num_heads, weight_o, bias_o)
    assert not np.allclose(result_a, result_b, atol=1e-4)


def test_encoder_and_decoder_blocks_give_different_results_on_the_same_input():
    # Directly targets a mutant that makes decoder_block_forward
    # forget the causal mask (silently reducing it to the encoder case).
    rng = np.random.RandomState(5)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    x = rng.randn(1, seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)

    encoder_out = encoder_block_forward(x, num_heads, **params)
    decoder_out = decoder_block_forward(x, num_heads, **params)
    assert not np.allclose(encoder_out, decoder_out, atol=1e-4)
