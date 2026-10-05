import numpy as np


def perceptron_train(X: np.ndarray, y: np.ndarray, lr: float = 1.0, epochs: int = 100) -> tuple:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    w = np.zeros(X.shape[1])
    b = 0.0
    for _ in range(epochs):
        mistakes = 0
        for xi, yi in zip(X, y):
            prediction = 1 if xi @ w + b > 0 else 0
            error = yi - prediction
            if error != 0:
                w = w + lr * error * xi
                b += lr * error
                mistakes += 1
        if mistakes == 0:
            break
    return w, float(b)
