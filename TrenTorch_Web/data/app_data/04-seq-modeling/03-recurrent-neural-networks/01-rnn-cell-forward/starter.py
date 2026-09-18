import numpy as np


def rnn_cell_forward(
    x: np.ndarray,
    h_prev: np.ndarray,
    weight_ih: np.ndarray,
    weight_hh: np.ndarray,
    bias_ih: np.ndarray,
    bias_hh: np.ndarray,
) -> np.ndarray:
    """
    One step of a vanilla RNN cell. `x` is the CURRENT time step's input
    (shape (batch_size, input_size)); `h_prev` is the PREVIOUS time
    step's hidden state (shape (batch_size, hidden_size)). Combines both
    through their own linear transformations (`[03-dl-training/02-
    layers/01-linear-forward]`-style, one weight/bias pair for each),
    sums the results, and squashes through tanh to produce the NEW
    hidden state.
    """
    pass
