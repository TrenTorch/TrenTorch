import numpy as np


def relu_forward(x):
    """ReLU forward: max(0, x), elementwise."""
    return np.maximum(0, x)


def relu_backward(grad_output, x):
    """ReLU backward: pass the gradient through only where x > 0."""
    return grad_output * (x > 0)
