import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def lstm_cell_forward(
    x: np.ndarray,
    h_prev: np.ndarray,
    c_prev: np.ndarray,
    weight_ih: np.ndarray,
    weight_hh: np.ndarray,
    bias_ih: np.ndarray,
    bias_hh: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    hidden_size = h_prev.shape[-1]
    gates = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh

    i_gate = sigmoid(gates[:, 0:hidden_size])
    f_gate = sigmoid(gates[:, hidden_size : 2 * hidden_size])
    g_gate = np.tanh(gates[:, 2 * hidden_size : 3 * hidden_size])
    o_gate = sigmoid(gates[:, 3 * hidden_size : 4 * hidden_size])

    c_next = f_gate * c_prev + i_gate * g_gate
    h_next = o_gate * np.tanh(c_next)

    return h_next, c_next
