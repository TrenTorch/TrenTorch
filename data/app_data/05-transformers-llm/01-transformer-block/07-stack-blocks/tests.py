"""
pytest data/app_data/05-transformers-llm/01-transformer-block/07-stack-blocks/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/01-transformer-block/{Path(__file__).resolve().parent.name}")
stack_transformer_blocks = _module.stack_transformer_blocks

transformer_block_forward = load_solution(
    "05-transformers-llm/01-transformer-block/06-assemble-full-block"
).transformer_block_forward


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


def test_output_shape_matches_input_shape():
    rng = np.random.RandomState(0)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    blocks_params = [_random_block_params(rng, d_model, d_ff) for _ in range(3)]
    result = stack_transformer_blocks(x, num_heads, blocks_params)
    assert result.shape == x.shape


def test_zero_blocks_is_the_identity():
    rng = np.random.RandomState(1)
    d_model, num_heads = 8, 2
    x = rng.randn(2, 4, d_model)
    result = stack_transformer_blocks(x, num_heads, blocks_params=[])
    assert np.allclose(result, x)


def test_one_block_matches_calling_transformer_block_forward_directly():
    rng = np.random.RandomState(2)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    params = _random_block_params(rng, d_model, d_ff)

    stacked_result = stack_transformer_blocks(x, num_heads, [params])
    direct_result = transformer_block_forward(x, num_heads, **params)
    assert np.allclose(stacked_result, direct_result, atol=1e-8)


def test_two_blocks_feed_the_first_blocks_output_into_the_second():
    rng = np.random.RandomState(3)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    params1 = _random_block_params(rng, d_model, d_ff)
    params2 = _random_block_params(rng, d_model, d_ff)

    stacked_result = stack_transformer_blocks(x, num_heads, [params1, params2])

    after_block1 = transformer_block_forward(x, num_heads, **params1)
    manual_result = transformer_block_forward(after_block1, num_heads, **params2)
    assert np.allclose(stacked_result, manual_result, atol=1e-8)


def test_block_order_matters_swapping_two_different_blocks_changes_the_result():
    # Directly targets a mutant that processes blocks_params in the
    # wrong order (e.g. reversed), or independently on the original x
    # instead of chaining each block's output into the next.
    rng = np.random.RandomState(4)
    d_model, d_ff, num_heads = 8, 16, 2
    x = rng.randn(2, 4, d_model)
    params1 = _random_block_params(rng, d_model, d_ff)
    params2 = _random_block_params(rng, d_model, d_ff)

    forward_order = stack_transformer_blocks(x, num_heads, [params1, params2])
    reversed_order = stack_transformer_blocks(x, num_heads, [params2, params1])
    assert not np.allclose(forward_order, reversed_order, atol=1e-4)


def test_mask_is_shared_across_every_block_in_the_stack():
    rng = np.random.RandomState(5)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    x = rng.randn(1, seq_len, d_model)
    blocks_params = [_random_block_params(rng, d_model, d_ff) for _ in range(2)]
    causal_mask = np.triu(np.full((seq_len, seq_len), -np.inf), k=1)

    result = stack_transformer_blocks(x, num_heads, blocks_params, mask=causal_mask)
    assert result.shape == x.shape
    assert np.all(np.isfinite(result))
