"""
pytest data/app_data/07-vision/06-vision-transformer/04-vit-encoder-block/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

vit_encoder_block = load_solution(
    f"07-vision/06-vision-transformer/{Path(__file__).resolve().parent.name}"
).vit_encoder_block
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


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_matches_input_shape():
    rng = np.random.RandomState(0)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    sequence = rng.randn(seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)
    out = vit_encoder_block(sequence, num_heads, **params)
    assert out.shape == (seq_len, d_model)


def test_02_matches_transformer_block_forward_with_a_manually_added_batch_dim():
    rng = np.random.RandomState(1)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 6
    sequence = rng.randn(seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)
    out = vit_encoder_block(sequence, num_heads, **params)
    manual = transformer_block_forward(sequence[None, :, :], num_heads, **params)[0]
    assert np.allclose(out, manual)


# --- Shape / general-case coverage -----------------------------------


def test_03_different_num_heads_and_sequence_length():
    rng = np.random.RandomState(2)
    d_model, d_ff, num_heads, seq_len = 12, 24, 3, 10  # e.g. a CLS token + 9 patches
    sequence = rng.randn(seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)
    out = vit_encoder_block(sequence, num_heads, **params)
    assert out.shape == (seq_len, d_model)


def test_04_single_token_sequence():
    rng = np.random.RandomState(3)
    d_model, d_ff, num_heads = 8, 16, 2
    sequence = rng.randn(1, d_model)
    params = _random_block_params(rng, d_model, d_ff)
    out = vit_encoder_block(sequence, num_heads, **params)
    assert out.shape == (1, d_model)


# --- Parameter handling -------------------------------------------------


def test_05_output_is_not_identical_to_input_for_nontrivial_parameters():
    rng = np.random.RandomState(4)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    sequence = rng.randn(seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)
    out = vit_encoder_block(sequence, num_heads, **params)
    assert not np.allclose(out, sequence)


# --- Edge cases ---------------------------------------------------------


def test_06_no_batch_dimension_leaks_into_the_returned_array():
    rng = np.random.RandomState(5)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 4
    sequence = rng.randn(seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)
    out = vit_encoder_block(sequence, num_heads, **params)
    assert out.ndim == 2


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_sequence_input():
    rng = np.random.RandomState(6)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 5
    sequence = rng.randn(seq_len, d_model)
    sequence_copy = sequence.copy()
    params = _random_block_params(rng, d_model, d_ff)
    vit_encoder_block(sequence, num_heads, **params)
    assert np.array_equal(sequence, sequence_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_underlying_transformer_block_is_the_same_already_torch_verified_implementation():
    # This function is a thin batching wrapper -- it adds a batch
    # dimension, delegates entirely to `transformer_block_forward`, and
    # removes the batch dimension again. `transformer_block_forward`
    # itself (05-transformers-llm/01-transformer-block/06-assemble-full-
    # block) is independently correctness-tested elsewhere in this
    # curriculum against its own layer-by-layer construction from
    # attention, layer norm, and feedforward pieces. What this test
    # verifies is specifically the ONLY thing this question adds:
    # unwrapping the batch dimension must not silently transpose or
    # reshape the sequence -- position i of the output must correspond
    # to position i of a direct, manually-batched call.
    rng = np.random.RandomState(7)
    d_model, d_ff, num_heads, seq_len = 8, 16, 2, 7
    sequence = rng.randn(seq_len, d_model)
    params = _random_block_params(rng, d_model, d_ff)

    out = vit_encoder_block(sequence, num_heads, **params)
    direct = transformer_block_forward(sequence[None, :, :], num_heads, **params)[0]
    for position in range(seq_len):
        assert np.allclose(out[position], direct[position])
