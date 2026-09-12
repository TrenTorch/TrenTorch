import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

rnn_cell_forward = load_solution("04-seq-modeling/03-recurrent-neural-networks/01-rnn-cell-forward").rnn_cell_forward


def bidirectional_rnn_forward(
    x_seq: np.ndarray,
    h0_forward: np.ndarray,
    h0_backward: np.ndarray,
    weight_ih_fwd: np.ndarray,
    weight_hh_fwd: np.ndarray,
    bias_ih_fwd: np.ndarray,
    bias_hh_fwd: np.ndarray,
    weight_ih_bwd: np.ndarray,
    weight_hh_bwd: np.ndarray,
    bias_ih_bwd: np.ndarray,
    bias_hh_bwd: np.ndarray,
) -> np.ndarray:
    """
    A vanilla RNN that processes `x_seq` (shape (seq_len, batch_size,
    input_size)) TWICE: once forward (position 0 to seq_len-1, exactly
    `[01-rnn-cell-forward]` applied repeatedly), and once BACKWARD
    (position seq_len-1 down to 0, its OWN separate set of weights), so
    that every position's final representation has seen BOTH everything
    before it AND everything after it in the sequence, something a
    single-direction RNN can never see (position 2's forward-only hidden
    state has no way to know what happens at position 8).

    Returns a single array of shape (seq_len, batch_size, 2*hidden_size):
    at every time step, the forward direction's hidden state CONCATENATED
    with the backward direction's hidden state AT THAT SAME ORIGINAL
    time step (not reversed back-to-front, the output must be in the
    ORIGINAL time order, even though the backward pass computed its
    values in reverse order internally).
    """
    seq_len = x_seq.shape[0]
    pass
