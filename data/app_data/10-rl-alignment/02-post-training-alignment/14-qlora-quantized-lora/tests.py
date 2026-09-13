"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/14-qlora-quantized-lora/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
compute_int8_scale = _module.compute_int8_scale
quantize_int8 = _module.quantize_int8
dequantize_int8 = _module.dequantize_int8
lora_delta = _module.lora_delta
qlora_linear_forward = _module.qlora_linear_forward
count_trainable_parameters = _module.count_trainable_parameters


def _random_setup(seed, batch=4, in_f=8, out_f=6, rank=2):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(batch, in_f))
    W = rng.normal(size=(out_f, in_f)) * 0.1
    A = rng.normal(size=(rank, in_f)) * 0.01
    B = rng.normal(size=(out_f, rank)) * 0.01
    return x, W, A, B


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_quantize_dequantize_round_trips_approximately():
    weight = np.array([1.0, -0.5, 0.25, -1.0])
    scale = compute_int8_scale(weight)
    quantized = quantize_int8(weight, scale)
    dequantized = dequantize_int8(quantized, scale)
    assert np.allclose(dequantized, weight, atol=0.02)


def test_02_qlora_output_shape_matches_a_plain_linear_layer():
    x, W, A, B = _random_setup(0)
    scale = compute_int8_scale(W)
    q = quantize_int8(W, scale)
    out = qlora_linear_forward(x, q, scale, A, B, alpha=4, rank=2)
    assert out.shape == (x.shape[0], W.shape[0])


# --- General-case coverage --------------------------------------------


def test_03_quantized_weight_dtype_is_int8():
    weight = np.array([10.0, -20.0, 5.0])
    scale = compute_int8_scale(weight)
    quantized = quantize_int8(weight, scale)
    assert quantized.dtype == np.int8


def test_04_qlora_output_close_to_full_precision_base_plus_lora():
    x, W, A, B = _random_setup(1)
    scale = compute_int8_scale(W)
    q = quantize_int8(W, scale)
    qlora_out = qlora_linear_forward(x, q, scale, A, B, alpha=4, rank=2)
    full_precision_approx = x @ W.T + lora_delta(x, A, B, alpha=4, rank=2)
    assert np.allclose(qlora_out, full_precision_approx, atol=0.05)


def test_05_lora_delta_matches_hand_computation():
    x = np.array([[1.0, 2.0]])
    A = np.array([[1.0, 0.0]])  # rank 1, in_features 2
    B = np.array([[2.0]])  # out_features 1, rank 1
    delta = lora_delta(x, A, B, alpha=2.0, rank=1)
    # x @ A.T = [[1]], @ B.T = [[2]], * (alpha/rank=2) = [[4]]
    assert np.allclose(delta, [[4.0]])


# --- Parameter handling -------------------------------------------------


def test_06_qlora_trains_far_fewer_parameters_than_full_finetune():
    counts = count_trainable_parameters(in_features=4096, out_features=4096, rank=16)
    assert counts["qlora"] < counts["full_finetune"] / 100


def test_07_trainable_parameter_formula_matches_hand_computation():
    counts = count_trainable_parameters(in_features=10, out_features=20, rank=4)
    assert counts["full_finetune"] == 200
    assert counts["qlora"] == 4 * 10 + 20 * 4


# --- Edge cases ---------------------------------------------------------


def test_08_dequantize_recovers_a_simple_known_value():
    # scale=0.1, quantized value 50 -> dequantized should be exactly 5.0
    dequantized = dequantize_int8(np.array([50], dtype=np.int8), scale=0.1)
    assert np.isclose(dequantized[0], 5.0)


def test_09_rank_one_is_always_far_smaller_than_full_finetune():
    counts = count_trainable_parameters(in_features=64, out_features=64, rank=1)
    assert counts["qlora"] < counts["full_finetune"] / 30


# --- Independent correctness oracle -----------------------------------


def test_10_lora_delta_is_a_genuine_low_rank_update_not_a_full_rank_one():
    # Directly targets a mutant that computes a full-rank delta (e.g.
    # input @ some_full_matrix instead of the low-rank A/B
    # factorization) -- the rank of the delta's contribution across a
    # batch of MANY different inputs should never exceed `rank`.
    rng = np.random.default_rng(2)
    batch, in_f, out_f, rank = 20, 10, 8, 2
    x = rng.normal(size=(batch, in_f))
    A = rng.normal(size=(rank, in_f))
    B = rng.normal(size=(out_f, rank))
    delta = lora_delta(x, A, B, alpha=1.0, rank=rank)
    matrix_rank = np.linalg.matrix_rank(delta)
    assert matrix_rank <= rank
