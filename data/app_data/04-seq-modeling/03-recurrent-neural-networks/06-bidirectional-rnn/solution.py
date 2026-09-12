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
    seq_len = x_seq.shape[0]

    h_fwd = h0_forward
    forward_outputs = []
    for t in range(seq_len):
        h_fwd = rnn_cell_forward(x_seq[t], h_fwd, weight_ih_fwd, weight_hh_fwd, bias_ih_fwd, bias_hh_fwd)
        forward_outputs.append(h_fwd)

    h_bwd = h0_backward
    backward_outputs = []
    for t in reversed(range(seq_len)):
        h_bwd = rnn_cell_forward(x_seq[t], h_bwd, weight_ih_bwd, weight_hh_bwd, bias_ih_bwd, bias_hh_bwd)
        backward_outputs.append(h_bwd)
    backward_outputs.reverse()

    combined = [
        np.concatenate([f, b], axis=-1) for f, b in zip(forward_outputs, backward_outputs)
    ]
    return np.stack(combined, axis=0)
