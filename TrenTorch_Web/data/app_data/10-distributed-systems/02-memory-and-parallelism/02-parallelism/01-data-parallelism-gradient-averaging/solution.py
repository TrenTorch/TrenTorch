import numpy as np


def local_gradient(X_shard: np.ndarray, y_shard: np.ndarray, w: np.ndarray) -> np.ndarray:
    n_shard = X_shard.shape[0]
    predictions = X_shard @ w
    return (2.0 / n_shard) * (X_shard.T @ (predictions - y_shard))


def split_batch_across_workers(X: np.ndarray, y: np.ndarray, num_workers: int):
    return list(np.array_split(X, num_workers)), list(np.array_split(y, num_workers))


def average_gradients(worker_gradients: list) -> np.ndarray:
    return np.mean(worker_gradients, axis=0)


def data_parallel_gradient(X: np.ndarray, y: np.ndarray, w: np.ndarray, num_workers: int) -> np.ndarray:
    X_shards, y_shards = split_batch_across_workers(X, y, num_workers)
    worker_gradients = [local_gradient(xs, ys, w) for xs, ys in zip(X_shards, y_shards)]
    return average_gradients(worker_gradients)
