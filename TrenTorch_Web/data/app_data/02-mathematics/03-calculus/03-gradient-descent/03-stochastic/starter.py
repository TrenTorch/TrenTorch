import numpy as np


def sample_gradient(x_i, y_i, w):
    """
    x_i: 1D array of shape (d,), one example's features
    y_i: float, that example's target
    w: 1D array of shape (d,), the current weights

    Returns:
        The gradient of (x_i @ w - y_i) ** 2 with respect to w,
        a 1D array of shape (d,).
    """
    # TODO: Implement the single-example gradient from Theory.
    pass


def stochastic_gradient_descent(X, y, w0, learning_rate, num_epochs, rng):
    """
    X, y: the dataset, shapes (m, d) and (m,)
    w0: starting weights, shape (d,)
    learning_rate: a small positive float
    num_epochs: number of full passes over the data
    rng: a numpy Generator, e.g. np.random.default_rng(0)

    Returns:
        A list of 1 + num_epochs * m weight vectors: w0, followed by
        the weights after each single-example update. Each epoch uses
        every example exactly once, in an order drawn with one
        rng.permutation(m) call. X, y and w0 must not be modified.
    """
    # TODO: Implement the epoch loop and the per-example updates from Theory.
    pass
