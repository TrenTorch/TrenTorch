"""
pytest data/app_data/09-systems-distributed/02-parallelism/06-tensor-parallel-matmul/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/02-parallelism/{Path(__file__).resolve().parent.name}")
column_parallel_linear = _module.column_parallel_linear
row_parallel_linear = _module.row_parallel_linear
split_weight_by_output_features = _module.split_weight_by_output_features
split_by_input_features = _module.split_by_input_features

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def _random_layer(seed, batch=5, in_f=9, out_f=6):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(batch, in_f))
    W = rng.normal(size=(out_f, in_f))
    b = rng.normal(size=out_f)
    return x, W, b


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_column_parallel_matches_full_linear():
    x, W, b = _random_layer(0)
    full = linear(x, W, b)
    w_shards, b_shards = split_weight_by_output_features(W, b, num_gpus=3)
    out = column_parallel_linear(x, w_shards, b_shards)
    assert np.allclose(out, full)


def test_02_row_parallel_matches_full_linear():
    x, W, b = _random_layer(1)
    full = linear(x, W, b)
    x_shards, w_shards = split_by_input_features(x, W, num_gpus=3)
    out = row_parallel_linear(x_shards, w_shards, b)
    assert np.allclose(out, full)


# --- General-case coverage --------------------------------------------


def test_03_column_parallel_works_for_various_gpu_counts():
    x, W, b = _random_layer(2, out_f=12)
    full = linear(x, W, b)
    for num_gpus in (1, 2, 4, 12):
        w_shards, b_shards = split_weight_by_output_features(W, b, num_gpus)
        assert np.allclose(column_parallel_linear(x, w_shards, b_shards), full)


def test_04_row_parallel_works_for_various_gpu_counts():
    x, W, b = _random_layer(3, in_f=12)
    full = linear(x, W, b)
    for num_gpus in (1, 2, 3, 4, 6, 12):
        x_shards, w_shards = split_by_input_features(x, W, num_gpus)
        assert np.allclose(row_parallel_linear(x_shards, w_shards, b), full)


def test_05_column_parallel_output_has_correct_total_width():
    x, W, b = _random_layer(4, out_f=10)
    w_shards, b_shards = split_weight_by_output_features(W, b, num_gpus=4)
    out = column_parallel_linear(x, w_shards, b_shards)
    assert out.shape == (x.shape[0], 10)


# --- Parameter handling -------------------------------------------------


def test_06_split_weight_produces_correct_number_of_shards():
    _, W, b = _random_layer(5, out_f=12)
    w_shards, b_shards = split_weight_by_output_features(W, b, num_gpus=4)
    assert len(w_shards) == 4
    assert len(b_shards) == 4
    assert sum(w.shape[0] for w in w_shards) == 12


def test_07_split_by_input_features_produces_matching_shard_widths():
    x, W, b = _random_layer(6, in_f=12)
    x_shards, w_shards = split_by_input_features(x, W, num_gpus=4)
    for xs, ws in zip(x_shards, w_shards):
        assert xs.shape[-1] == ws.shape[1]


# --- Edge cases ---------------------------------------------------------


def test_08_single_gpu_is_a_no_op_for_both_schemes():
    x, W, b = _random_layer(7)
    full = linear(x, W, b)

    w_shards, b_shards = split_weight_by_output_features(W, b, num_gpus=1)
    assert np.allclose(column_parallel_linear(x, w_shards, b_shards), full)

    x_shards, w_shards2 = split_by_input_features(x, W, num_gpus=1)
    assert np.allclose(row_parallel_linear(x_shards, w_shards2, b), full)


def test_09_uneven_gpu_split_still_reconstructs_correctly():
    x, W, b = _random_layer(8, out_f=10, in_f=10)
    w_shards, b_shards = split_weight_by_output_features(W, b, num_gpus=3)
    x_shards, w_shards2 = split_by_input_features(x, W, num_gpus=3)
    full = linear(x, W, b)
    assert np.allclose(column_parallel_linear(x, w_shards, b_shards), full)
    assert np.allclose(row_parallel_linear(x_shards, w_shards2, b), full)


# --- Independent correctness oracle -----------------------------------


def test_10_row_parallel_partials_genuinely_differ_before_summing():
    # Directly targets a mutant that just returns one partial (e.g.
    # the first GPU's) instead of genuinely summing all of them --
    # confirm the partials are not all identical/zero before the sum
    # is what actually reconstructs the correct answer.
    x, W, b = _random_layer(9, in_f=9)
    x_shards, w_shards = split_by_input_features(x, W, num_gpus=3)
    partials = [linear(xs, ws) for xs, ws in zip(x_shards, w_shards)]
    assert not np.allclose(partials[0], partials[1])

    full = linear(x, W, b)
    assert np.allclose(row_parallel_linear(x_shards, w_shards, b), full)
