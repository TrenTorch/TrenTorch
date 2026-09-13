"""
pytest data/app_data/09-systems-distributed/02-parallelism/01-data-parallelism-gradient-averaging/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/02-parallelism/{Path(__file__).resolve().parent.name}")
local_gradient = _module.local_gradient
split_batch_across_workers = _module.split_batch_across_workers
average_gradients = _module.average_gradients
data_parallel_gradient = _module.data_parallel_gradient


def _full_batch_gradient(X, y, w):
    n = X.shape[0]
    return (2.0 / n) * (X.T @ (X @ w - y))


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_data_parallel_gradient_matches_full_batch_gradient():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(8, 3))
    y = rng.normal(size=8)
    w = rng.normal(size=3)

    full = _full_batch_gradient(X, y, w)
    parallel = data_parallel_gradient(X, y, w, num_workers=4)
    assert np.allclose(full, parallel)


def test_02_split_batch_produces_correct_number_of_equal_shards():
    X = np.arange(24).reshape(8, 3).astype(float)
    y = np.arange(8).astype(float)
    X_shards, y_shards = split_batch_across_workers(X, y, num_workers=4)
    assert len(X_shards) == 4
    assert all(xs.shape[0] == 2 for xs in X_shards)
    assert all(ys.shape[0] == 2 for ys in y_shards)


# --- General-case coverage --------------------------------------------


def test_03_works_for_various_worker_counts():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(12, 4))
    y = rng.normal(size=12)
    w = rng.normal(size=4)
    full = _full_batch_gradient(X, y, w)
    for num_workers in (1, 2, 3, 4, 6, 12):
        assert np.allclose(full, data_parallel_gradient(X, y, w, num_workers))


def test_04_local_gradient_matches_finite_difference():
    rng = np.random.default_rng(2)
    X_shard = rng.normal(size=(5, 3))
    y_shard = rng.normal(size=5)
    w = rng.normal(size=3)

    analytic = local_gradient(X_shard, y_shard, w)

    def loss(ww):
        return np.mean((X_shard @ ww - y_shard) ** 2)

    eps = 1e-6
    numeric = np.empty_like(w)
    for i in range(len(w)):
        wp, wm = w.copy(), w.copy()
        wp[i] += eps
        wm[i] -= eps
        numeric[i] = (loss(wp) - loss(wm)) / (2 * eps)
    assert np.allclose(analytic, numeric, atol=1e-4)


# --- Parameter handling -------------------------------------------------


def test_05_average_gradients_is_elementwise_mean():
    grads = [np.array([1.0, 2.0]), np.array([3.0, 4.0]), np.array([5.0, 6.0])]
    avg = average_gradients(grads)
    assert np.allclose(avg, [3.0, 4.0])


def test_06_single_worker_equals_full_batch():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(6, 2))
    y = rng.normal(size=6)
    w = rng.normal(size=2)
    full = _full_batch_gradient(X, y, w)
    assert np.allclose(full, data_parallel_gradient(X, y, w, num_workers=1))


# --- Edge cases ---------------------------------------------------------


def test_07_num_workers_equals_batch_size():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(5, 2))
    y = rng.normal(size=5)
    w = rng.normal(size=2)
    full = _full_batch_gradient(X, y, w)
    assert np.allclose(full, data_parallel_gradient(X, y, w, num_workers=5))


def test_08_local_gradient_shape_matches_weight_shape():
    rng = np.random.default_rng(5)
    X_shard = rng.normal(size=(4, 7))
    y_shard = rng.normal(size=4)
    w = rng.normal(size=7)
    grad = local_gradient(X_shard, y_shard, w)
    assert grad.shape == w.shape


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_inputs():
    rng = np.random.default_rng(6)
    X = rng.normal(size=(8, 3))
    y = rng.normal(size=8)
    w = rng.normal(size=3)
    X_copy, y_copy, w_copy = X.copy(), y.copy(), w.copy()
    data_parallel_gradient(X, y, w, num_workers=4)
    assert np.array_equal(X, X_copy)
    assert np.array_equal(y, y_copy)
    assert np.array_equal(w, w_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_unequal_worker_gradients_still_average_correctly():
    # Directly targets a mutant that hardcodes worker outputs or ignores
    # per-shard data (e.g. always uses the first shard's gradient):
    # skew half the data so per-shard gradients genuinely differ, and
    # confirm the average still lands on the true full-batch answer.
    rng = np.random.default_rng(7)
    X = np.vstack([rng.normal(loc=5.0, size=(4, 3)), rng.normal(loc=-5.0, size=(4, 3))])
    y = rng.normal(size=8)
    w = rng.normal(size=3)

    X_shards, y_shards = split_batch_across_workers(X, y, num_workers=2)
    worker_grads = [local_gradient(xs, ys, w) for xs, ys in zip(X_shards, y_shards)]
    assert not np.allclose(worker_grads[0], worker_grads[1])

    full = _full_batch_gradient(X, y, w)
    assert np.allclose(full, average_gradients(worker_grads))
