import numpy as np


def rnn_cell_forward(
    x: np.ndarray,
    h_prev: np.ndarray,
    weight_ih: np.ndarray,
    weight_hh: np.ndarray,
    bias_ih: np.ndarray,
    bias_hh: np.ndarray,
) -> np.ndarray:
    return np.tanh(x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh)
