import numpy as np


def mse_gradient(X, y, w):
    return 2.0 * X.T @ (X @ w - y) / len(y)


def make_batches(num_samples, batch_size, rng):
    order = rng.permutation(num_samples)
    return [order[start : start + batch_size] for start in range(0, num_samples, batch_size)]


def mini_batch_gradient_descent(X, y, w0, learning_rate, batch_size, num_epochs, rng):
    w = np.array(w0, dtype=float)
    trajectory = [w.copy()]
    for _ in range(num_epochs):
        for batch in make_batches(len(y), batch_size, rng):
            w = w - learning_rate * mse_gradient(X[batch], y[batch], w)
            trajectory.append(w.copy())
    return trajectory
