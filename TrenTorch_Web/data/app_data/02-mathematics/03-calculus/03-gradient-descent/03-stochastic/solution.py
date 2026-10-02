import numpy as np


def sample_gradient(x_i, y_i, w):
    return 2.0 * (x_i @ w - y_i) * x_i


def stochastic_gradient_descent(X, y, w0, learning_rate, num_epochs, rng):
    w = np.array(w0, dtype=float)
    trajectory = [w.copy()]
    for _ in range(num_epochs):
        for i in rng.permutation(len(y)):
            w = w - learning_rate * sample_gradient(X[i], y[i], w)
            trajectory.append(w.copy())
    return trajectory
