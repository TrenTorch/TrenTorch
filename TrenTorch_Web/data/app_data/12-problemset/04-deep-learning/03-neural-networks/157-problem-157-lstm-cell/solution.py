import numpy as np

def solve(x, h, c, W, b):
    gates = np.asarray(W) @ np.r_[x, h] + b
    i, f, o, g = np.split(gates, 4)
    sigmoid = lambda z: 1 / (1 + np.exp(-z))
    cell = sigmoid(f) * c + sigmoid(i) * np.tanh(g)
    return sigmoid(o) * np.tanh(cell), cell
