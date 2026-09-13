"""
pytest data/app_data/09-systems-distributed/02-parallelism/04-collective-communication-primitives/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/02-parallelism/{Path(__file__).resolve().parent.name}")
all_reduce_sum = _module.all_reduce_sum
all_gather = _module.all_gather
reduce_scatter_sum = _module.reduce_scatter_sum


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_all_reduce_sum_gives_every_worker_the_same_total():
    arrs = [np.array([1.0, 2.0]), np.array([3.0, 4.0]), np.array([5.0, 6.0])]
    result = all_reduce_sum(arrs)
    expected = np.array([9.0, 12.0])
    assert all(np.allclose(r, expected) for r in result)


def test_02_all_gather_reconstructs_the_full_array_for_everyone():
    shards = [np.array([1.0, 2.0]), np.array([3.0]), np.array([4.0, 5.0, 6.0])]
    result = all_gather(shards)
    expected = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    assert all(np.allclose(r, expected) for r in result)


# --- General-case coverage --------------------------------------------


def test_03_reduce_scatter_sum_gives_each_worker_only_its_own_chunk():
    rng = np.random.default_rng(0)
    arrs = [rng.normal(size=6) for _ in range(3)]
    result = reduce_scatter_sum(arrs)
    total = sum(arrs)
    expected_chunks = np.array_split(total, 3)
    for got, expected in zip(result, expected_chunks):
        assert np.allclose(got, expected)


def test_04_reduce_scatter_output_reconstructs_all_reduce_output():
    rng = np.random.default_rng(1)
    arrs = [rng.normal(size=8) for _ in range(4)]
    scattered = reduce_scatter_sum(arrs)
    reduced = all_reduce_sum(arrs)
    assert np.allclose(np.concatenate(scattered), reduced[0])


def test_05_all_gather_preserves_rank_order():
    shards = [np.array([float(i)]) for i in range(5)]
    result = all_gather(shards)
    assert np.allclose(result[0], [0.0, 1.0, 2.0, 3.0, 4.0])


# --- Parameter handling -------------------------------------------------


def test_06_works_with_two_workers():
    arrs = [np.array([1.0]), np.array([2.0])]
    assert np.allclose(all_reduce_sum(arrs)[0], [3.0])
    assert np.allclose(all_reduce_sum(arrs)[1], [3.0])


def test_07_all_reduce_result_has_same_length_as_input_list():
    arrs = [np.ones(4) for _ in range(7)]
    result = all_reduce_sum(arrs)
    assert len(result) == 7


# --- Edge cases ---------------------------------------------------------


def test_08_single_worker_is_a_no_op_for_all_reduce_and_all_gather():
    arr = [np.array([1.0, 2.0, 3.0])]
    assert np.allclose(all_reduce_sum(arr)[0], arr[0])
    assert np.allclose(all_gather(arr)[0], arr[0])


def test_09_reduce_scatter_matches_all_reduce_for_single_worker():
    arr = [np.array([1.0, 2.0, 3.0, 4.0])]
    result = reduce_scatter_sum(arr)
    assert len(result) == 1
    assert np.allclose(result[0], arr[0])


# --- Independent correctness oracle -----------------------------------


def test_10_all_three_collectives_agree_on_the_same_underlying_data():
    # Directly targets a mutant that implements one collective in
    # terms of a different (wrong) operation, e.g. averaging instead
    # of summing: cross-check all three against the same raw data and
    # each other's well-known algebraic relationship.
    rng = np.random.default_rng(2)
    n_workers = 4
    per_worker = [rng.normal(size=6) for _ in range(n_workers)]

    reduced = all_reduce_sum(per_worker)
    scattered = reduce_scatter_sum(per_worker)
    gathered = all_gather(scattered)

    true_sum = sum(per_worker)
    assert np.allclose(reduced[0], true_sum)
    assert np.allclose(np.concatenate(scattered), true_sum)
    assert np.allclose(gathered[0], true_sum)
