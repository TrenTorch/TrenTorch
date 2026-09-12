"""
pytest data/app_data/05-transformers-llm/01-transformer-block/06-assemble-full-block/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/01-transformer-block/{Path(__file__).resolve().parent.name}")
transformer_block_forward = _module.transformer_block_forward

layer_norm_forward = load_solution("05-transformers-llm/01-transformer-block/01-layer-normalization-forward").layer_norm_forward
feedforward_sublayer = load_solution("05-transformers-llm/01-transformer-block/04-feedforward-sublayer").feedforward_sublayer
multi_head_attention = load_solution("04-seq-modeling/04-attention/05-mha-concat-output-projection").multi_head_attention


def _random_block_params(rng, d_model, d_ff, num_heads):
    return dict(
        num_heads=num_heads,
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


def test_output_shape_matches_input_shape():
    rng = np.random.RandomState(0)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 5, d_model)
    params = _random_block_params(rng, d_model, d_ff, num_heads)
    result = transformer_block_forward(x, **params)
    assert result.shape == x.shape


def test_zeroing_both_sublayers_output_reduces_the_block_to_the_identity():
    # If the attention output projection AND the FFN's second layer are
    # both zeroed, both sublayers contribute exactly 0 to their residual
    # connections, regardless of what LayerNorm or the earlier layers
    # computed -- so the block's output must equal its raw input `x`
    # exactly. This single check catches several distinct wiring bugs at
    # once: a residual connection wired to the wrong tensor (e.g. adding
    # back the NORMALIZED input instead of the raw one), a missing
    # residual connection, or a sublayer applied in the wrong place.
    rng = np.random.RandomState(1)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(3, 4, d_model)
    params = _random_block_params(rng, d_model, d_ff, num_heads)
    params["weight_o"] = np.zeros((d_model, d_model))
    params["bias_o"] = np.zeros(d_model)
    params["ffn_weight2"] = np.zeros((d_model, d_ff))
    params["ffn_bias2"] = np.zeros(d_model)

    result = transformer_block_forward(x, **params)
    assert np.allclose(result, x, atol=1e-8)


def test_attention_operates_on_the_normalized_input_not_the_raw_input():
    # Pre-norm: LayerNorm is applied BEFORE the attention sublayer, not
    # after. If gamma1/beta1 genuinely change the input attention sees,
    # the block's output must differ from a version where attention is
    # run on the raw (un-normalized) x instead.
    rng = np.random.RandomState(2)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    params = _random_block_params(rng, d_model, d_ff, num_heads)
    # Make gamma1/beta1 a very different transform from the identity.
    params["gamma1"] = np.full(d_model, 5.0)
    params["beta1"] = np.full(d_model, 3.0)

    result = transformer_block_forward(x, **params)

    # Manually replicate the block but feed RAW x into attention instead
    # of LayerNorm(x, gamma1, beta1).
    attn_out_raw, _ = multi_head_attention(x, x, x, num_heads, params["weight_o"], params["bias_o"])
    x1 = x + attn_out_raw
    normed2 = layer_norm_forward(x1, params["gamma2"], params["beta2"])
    ffn_out = feedforward_sublayer(normed2, params["ffn_weight1"], params["ffn_bias1"], params["ffn_weight2"], params["ffn_bias2"])
    post_norm_variant = x1 + ffn_out

    assert not np.allclose(result, post_norm_variant, atol=1e-4)


def test_matches_manual_step_by_step_composition():
    rng = np.random.RandomState(3)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    params = _random_block_params(rng, d_model, d_ff, num_heads)

    normed1 = layer_norm_forward(x, params["gamma1"], params["beta1"])
    attn_out, _ = multi_head_attention(normed1, normed1, normed1, num_heads, params["weight_o"], params["bias_o"])
    x1 = x + attn_out
    normed2 = layer_norm_forward(x1, params["gamma2"], params["beta2"])
    ffn_out = feedforward_sublayer(normed2, params["ffn_weight1"], params["ffn_bias1"], params["ffn_weight2"], params["ffn_bias2"])
    expected = x1 + ffn_out

    result = transformer_block_forward(x, **params)
    assert np.allclose(result, expected, atol=1e-8)


def test_supports_a_causal_mask_passed_through_to_attention():
    rng = np.random.RandomState(4)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    x = rng.randn(1, seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff, num_heads)
    causal_mask = np.triu(np.full((seq_len, seq_len), -np.inf), k=1)

    result = transformer_block_forward(x, mask=causal_mask, **params)
    assert result.shape == x.shape
    assert np.all(np.isfinite(result))
