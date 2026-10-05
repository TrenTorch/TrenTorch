import numpy as np


def local_gradient(X_shard: np.ndarray, y_shard: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    The ordinary MSE gradient (03-mse-gradient's formula), computed on
    just ONE worker's shard of the batch: (2 / n_shard) * X_shard.T @
    (X_shard @ w - y_shard).
    """
    # TODO: implement
    pass


def split_batch_across_workers(X: np.ndarray, y: np.ndarray, num_workers: int):
    """
    Splits X and y into `num_workers` contiguous shards each (assume
    the batch size divides evenly, like a real DDP setup requires).
    Returns (X_shards, y_shards), each a list of arrays.
    """
    # TODO: use np.array_split on both X and y.
    pass


def average_gradients(worker_gradients: list) -> np.ndarray:
    """
    Elementwise average of a list of same-shape gradient arrays --
    what a real all-reduce averages across workers after backward.
    """
    # TODO: implement
    pass


def data_parallel_gradient(X: np.ndarray, y: np.ndarray, w: np.ndarray, num_workers: int) -> np.ndarray:
    """
    Full toy data-parallel step: split the batch, compute each
    worker's local gradient independently, then average them --
    should equal the full-batch gradient when shards are equal size.
    """
    # TODO: split_batch_across_workers, map local_gradient over the
    # shards, then average_gradients.
    pass
