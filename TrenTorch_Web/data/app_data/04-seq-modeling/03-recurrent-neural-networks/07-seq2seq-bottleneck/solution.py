import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

rnn_cell_forward = load_solution("04-seq-modeling/03-recurrent-neural-networks/01-rnn-cell-forward").rnn_cell_forward


def encode_all_hidden_states(
    x_seq: np.ndarray,
    h0: np.ndarray,
    weight_ih: np.ndarray,
    weight_hh: np.ndarray,
    bias_ih: np.ndarray,
    bias_hh: np.ndarray,
) -> np.ndarray:
    seq_len = x_seq.shape[0]
    h = h0
    hidden_states = []
    for t in range(seq_len):
        h = rnn_cell_forward(x_seq[t], h, weight_ih, weight_hh, bias_ih, bias_hh)
        hidden_states.append(h)
    return np.stack(hidden_states, axis=0)


def get_bottleneck_context(hidden_states: np.ndarray) -> np.ndarray:
    return hidden_states[-1]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a_flat = a.reshape(-1)
    b_flat = b.reshape(-1)
    return float(np.dot(a_flat, b_flat) / (np.linalg.norm(a_flat) * np.linalg.norm(b_flat) + 1e-8))
