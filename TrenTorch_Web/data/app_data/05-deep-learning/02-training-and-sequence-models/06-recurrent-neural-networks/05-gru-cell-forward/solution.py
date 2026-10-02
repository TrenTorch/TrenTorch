import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def gru_cell_forward(
    x: np.ndarray,
    h_prev: np.ndarray,
    weight_ih: np.ndarray,
    weight_hh: np.ndarray,
    bias_ih: np.ndarray,
    bias_hh: np.ndarray,
) -> np.ndarray:
    hidden_size = h_prev.shape[-1]

    gates_ih = x @ weight_ih.T + bias_ih
    gates_hh = h_prev @ weight_hh.T + bias_hh

    r_gate = sigmoid(gates_ih[:, 0:hidden_size] + gates_hh[:, 0:hidden_size])
    z_gate = sigmoid(
        gates_ih[:, hidden_size : 2 * hidden_size] + gates_hh[:, hidden_size : 2 * hidden_size]
    )
    n_gate = np.tanh(
        gates_ih[:, 2 * hidden_size : 3 * hidden_size]
        + r_gate * gates_hh[:, 2 * hidden_size : 3 * hidden_size]
    )

    h_next = (1.0 - z_gate) * n_gate + z_gate * h_prev
    return h_next
