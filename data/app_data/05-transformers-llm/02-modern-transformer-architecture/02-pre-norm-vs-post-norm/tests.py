"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/02-pre-norm-vs-post-norm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
post_norm_transformer_block_forward = _module.post_norm_transformer_block_forward
stack_pre_norm_blocks = _module.stack_pre_norm_blocks
stack_post_norm_blocks = _module.stack_post_norm_blocks

pre_norm_transformer_block_forward = load_solution(
    "05-transformers-llm/01-transformer-block/06-assemble-full-block"
).transformer_block_forward
layer_norm_forward = load_solution("05-transformers-llm/01-transformer-block/01-layer-normalization-forward").layer_norm_forward
residual_connection = load_solution("05-transformers-llm/01-transformer-block/03-residual-connection").residual_connection
feedforward_sublayer = load_solution("05-transformers-llm/01-transformer-block/04-feedforward-sublayer").feedforward_sublayer
multi_head_attention = load_solution("04-seq-modeling/04-attention/05-mha-concat-output-projection").multi_head_attention


def _params(rng, d_model, d_ff):
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


def test_post_norm_output_shape_matches_input_shape():
    rng = np.random.RandomState(0)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    params = _params(rng, d_model, d_ff)
    result = post_norm_transformer_block_forward(x, num_heads, **params)
    assert result.shape == x.shape


def test_post_norm_matches_manual_sublayer_residual_norm_order():
    rng = np.random.RandomState(1)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    params = _params(rng, d_model, d_ff)

    attn_out, _ = multi_head_attention(x, x, x, num_heads, params["weight_o"], params["bias_o"])
    x1 = residual_connection(x, attn_out)
    x1 = layer_norm_forward(x1, params["gamma1"], params["beta1"])
    ffn_out = feedforward_sublayer(x1, params["ffn_weight1"], params["ffn_bias1"], params["ffn_weight2"], params["ffn_bias2"])
    x2 = residual_connection(x1, ffn_out)
    expected = layer_norm_forward(x2, params["gamma2"], params["beta2"])

    result = post_norm_transformer_block_forward(x, num_heads, **params)
    assert np.allclose(result, expected, atol=1e-8)


def test_post_norm_output_has_a_bounded_scale_set_by_gamma2():
    # Post-Norm's LAST operation at every block is LayerNorm, so with
    # gamma2=1, beta2=0 the output's per-position root-mean-square must
    # land near 1, regardless of the block's other weights.
    rng = np.random.RandomState(2)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 5, d_model) * 5.0
    params = _params(rng, d_model, d_ff)
    result = post_norm_transformer_block_forward(x, num_heads, **params)
    rms = np.sqrt(np.mean(result**2, axis=-1))
    assert np.allclose(rms, 1.0, atol=1e-2)


def test_stack_pre_norm_and_stack_post_norm_reduce_to_a_single_block_at_depth_one():
    rng = np.random.RandomState(3)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(1, 4, d_model)
    params = _params(rng, d_model, d_ff)

    pre_stacked = stack_pre_norm_blocks(x, num_heads, params, num_blocks=1)
    pre_direct = pre_norm_transformer_block_forward(x, num_heads, **params)
    assert np.allclose(pre_stacked, pre_direct, atol=1e-8)

    post_stacked = stack_post_norm_blocks(x, num_heads, params, num_blocks=1)
    post_direct = post_norm_transformer_block_forward(x, num_heads, **params)
    assert np.allclose(post_stacked, post_direct, atol=1e-8)


def test_pre_norms_residual_stream_norm_grows_with_depth():
    # The defining, empirically observable difference: Pre-Norm never
    # renormalizes the raw residual STREAM itself (only each sublayer's
    # own input), so stacking more identical blocks keeps adding to an
    # unbounded-growing signal.
    rng = np.random.RandomState(4)
    d_model, d_ff, num_heads = 16, 32, 2
    x = rng.randn(1, 6, d_model) * 0.1
    params = _params(rng, d_model, d_ff)

    shallow = stack_pre_norm_blocks(x, num_heads, params, num_blocks=2)
    deep = stack_pre_norm_blocks(x, num_heads, params, num_blocks=16)
    assert np.linalg.norm(deep) > 2.0 * np.linalg.norm(shallow)


def test_post_norms_output_norm_stays_bounded_regardless_of_depth():
    # Contrast directly with the Pre-Norm test above: Post-Norm's final
    # operation at EVERY block is LayerNorm, which re-pins the output
    # scale at every single block, so stacking more blocks does not
    # make the final output grow.
    rng = np.random.RandomState(4)
    d_model, d_ff, num_heads = 16, 32, 2
    x = rng.randn(1, 6, d_model) * 0.1
    params = _params(rng, d_model, d_ff)

    shallow = stack_post_norm_blocks(x, num_heads, params, num_blocks=2)
    deep = stack_post_norm_blocks(x, num_heads, params, num_blocks=16)
    assert np.linalg.norm(deep) < 1.5 * np.linalg.norm(shallow)


def test_pre_norm_and_post_norm_give_different_results_for_the_same_weights():
    # Directly targets a mutant that implements post_norm identically to
    # pre_norm (e.g. by copy-pasting and forgetting to move the norm).
    rng = np.random.RandomState(5)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(1, 4, d_model)
    params = _params(rng, d_model, d_ff)

    pre_out = pre_norm_transformer_block_forward(x, num_heads, **params)
    post_out = post_norm_transformer_block_forward(x, num_heads, **params)
    assert not np.allclose(pre_out, post_out, atol=1e-4)
