import numpy as np


def rnn_cell_backward(
    grad_h: np.ndarray,
    h_next: np.ndarray,
    x: np.ndarray,
    h_prev: np.ndarray,
    weight_ih: np.ndarray,
    weight_hh: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    grad_z = grad_h * (1.0 - h_next**2)

    grad_x = grad_z @ weight_ih
    grad_weight_ih = grad_z.T @ x
    grad_bias_ih = grad_z.sum(axis=0)

    grad_h_prev = grad_z @ weight_hh
    grad_weight_hh = grad_z.T @ h_prev
    grad_bias_hh = grad_z.sum(axis=0)

    return grad_x, grad_h_prev, grad_weight_ih, grad_weight_hh, grad_bias_ih, grad_bias_hh
