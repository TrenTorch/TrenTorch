import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

softmax_axis1 = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax


def softmax_last_axis(Z: np.ndarray) -> np.ndarray:
    """
    `[01-classical-ml/02-classification/06-softmax-cce]`'s softmax is
    fixed to `axis=1`, correct for its own 2D (batch_size, num_classes)
    use case, but attention scores can have ANY number of leading batch
    and head dimensions (`(batch, heads, seq_len_q, seq_len_k)`, for
    `[04-multi-head-attention-split]`), and softmax always needs to
    apply along the LAST axis, whatever that happens to be.

    This function GENERALIZES Part 1's softmax to work over the last
    axis of an array of ANY rank, by RESHAPING down to a 2D array (where
    the fixed axis=1 already means "the last axis"), calling Part 1's
    softmax UNCHANGED, and reshaping the result back to the original
    shape.
    """
    original_shape = Z.shape
    pass
