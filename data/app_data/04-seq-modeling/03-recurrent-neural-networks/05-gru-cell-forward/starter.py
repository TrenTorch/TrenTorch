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
    """
    One step of a GRU cell, matching torch.nn.GRUCell's convention:
    weights/biases packed as [reset gate, update gate, new/candidate],
    only THREE chunks (not four, unlike `[04-lstm-cell-forward]`), and
    no separate cell state, just a single hidden state h, like a vanilla
    RNN, but with gating.

        r = sigmoid(Wir x + bir + Whr h + bhr)     # reset gate
        z = sigmoid(Wiz x + biz + Whz h + bhz)     # update gate
        n = tanh(Win x + bin + r * (Whn h + bhn))  # candidate, reset-GATED
        h_next = (1 - z) * n + z * h

    A genuinely subtle detail worth getting exactly right: the reset
    gate `r` multiplies ONLY the hidden-state contribution to the
    candidate `n` (`Whn h + bhn`), NOT the input contribution
    (`Win x + bin`), the input and hidden pre-activations for `n` must
    be kept SEPARATE until after `r` has been applied to the hidden
    half specifically.
    """
    hidden_size = h_prev.shape[-1]
    gates_ih = x @ weight_ih.T + bias_ih
    gates_hh = h_prev @ weight_hh.T + bias_hh
    pass
