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
    """
    Runs `[01-rnn-cell-forward]`'s rnn_cell_forward across the whole
    input sequence `x_seq` (shape (seq_len, batch_size, input_size)),
    returning EVERY step's hidden state, shape
    (seq_len, batch_size, hidden_size). This is the "encoder": in a
    classic (pre-attention) seq2seq model, ALL of these except the very
    LAST one get thrown away; get_bottleneck_context, below, keeps only
    that final one.
    """
    seq_len = x_seq.shape[0]
    pass


def get_bottleneck_context(hidden_states: np.ndarray) -> np.ndarray:
    """
    Extracts the classic seq2seq "context vector": just the LAST hidden
    state from encode_all_hidden_states's full sequence. This single,
    FIXED-size vector is all the information the decoder gets to work
    with about the ENTIRE input sequence, no matter how long it was.
    """
    pass


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Cosine similarity between two arrays (flattened first): 1.0 means
    identical direction, 0.0 means orthogonal (unrelated), negative
    means pointing in substantially different directions.
    """
    pass
