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
    """
    One step of an LSTM cell, matching torch.nn.LSTMCell's exact
    convention: `weight_ih`/`weight_hh`/`bias_ih`/`bias_hh` are STACKED,
    containing all FOUR gates' own weights back to back, in order
    [input gate, forget gate, cell gate, output gate], so `weight_ih`
    has shape (4 * hidden_size, input_size).

    Besides the hidden state h (carried between steps like a vanilla
    RNN's), an LSTM ALSO carries a separate cell state c, an additive
    "memory highway" gated additions/removals flow through, specifically
    designed to avoid `[03-bptt-vanishing-exploding]`'s repeated-
    multiplication problem.

        gates = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh
        i, f, g, o = split gates into 4 equal chunks of size hidden_size
        i = sigmoid(i)   # input gate: how much of the new candidate to let in
        f = sigmoid(f)   # forget gate: how much of the old cell state to keep
        g = tanh(g)      # candidate values
        o = sigmoid(o)   # output gate: how much of the cell state to expose

        c_next = f * c_prev + i * g
        h_next = o * tanh(c_next)
    """
    hidden_size = h_prev.shape[-1]
    gates = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh
    pass
