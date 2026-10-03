import numpy as np


def mse_gradient(X, y, w):
    """
    X: 2D array of shape (m, d), the rows given to the model
    y: 1D array of shape (m,), the targets for those rows
    w: 1D array of shape (d,), the current weights

    Returns:
        The gradient of mean((X @ w - y) ** 2) with respect to w,
        a 1D array of shape (d,), averaged over the m rows given.
    """
    # TODO: Implement the gradient from Theory.
    pass


def make_batches(num_samples, batch_size, rng):
    """
    num_samples: how many rows the dataset has
    batch_size: how many rows per batch
    rng: a numpy Generator, e.g. np.random.default_rng(0)

    Returns:
        A list of 1D integer index arrays. Together they hold every
        index in range(num_samples) exactly once, in a freshly shuffled
        order drawn with a single rng.permutation call. Every batch has
        batch_size indices except possibly the last, which holds the
        remainder.
    """
    # TODO: Shuffle the indices once, then cut them into batches.
    pass


def mini_batch_gradient_descent(X, y, w0, learning_rate, batch_size, num_epochs, rng):
    """
    X, y: the dataset, shapes (m, d) and (m,)
    w0: starting weights, shape (d,)
    learning_rate: a small positive float
    batch_size: rows per update
    num_epochs: number of full passes over the data
    rng: a numpy Generator

    Returns:
        A list of 1 + num_epochs * ceil(m / batch_size) weight vectors:
        w0, followed by the weights after each update. X, y and w0 must
        not be modified.
    """
    # TODO: Implement the epoch and batch loops from Theory.
    pass
