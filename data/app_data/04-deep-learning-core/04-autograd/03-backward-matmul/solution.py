import numpy as np


def matmul_backward(grad_output: np.ndarray, a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    grad_a = grad_output @ b.T
    grad_b = a.T @ grad_output
    return grad_a, grad_b
