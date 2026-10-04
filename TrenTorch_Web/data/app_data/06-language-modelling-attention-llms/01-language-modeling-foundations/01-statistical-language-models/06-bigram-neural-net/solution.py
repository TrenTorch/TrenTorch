import numpy as np


def _softmax_rows(logits):
    shifted = logits - logits.max(axis=1, keepdims=True)
    e = np.exp(shifted)
    return e / e.sum(axis=1, keepdims=True)


def bigram_net_loss(W, xs, ys):
    p = _softmax_rows(W[xs])
    return float(-np.log(p[np.arange(len(xs)), ys]).mean())


def bigram_net_gradient(W, xs, ys):
    n = len(xs)
    p = _softmax_rows(W[xs])
    p[np.arange(n), ys] -= 1.0
    grad = np.zeros_like(W, dtype=float)
    np.add.at(grad, xs, p)
    return grad / n


def train_bigram_net(xs, ys, V, steps, lr):
    W = np.zeros((V, V))
    for _ in range(steps):
        W -= lr * bigram_net_gradient(W, xs, ys)
    return W
