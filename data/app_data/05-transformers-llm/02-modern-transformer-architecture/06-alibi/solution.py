import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def compute_alibi_slopes(num_heads: int) -> np.ndarray:
    ratio = 2.0 ** (-8.0 / num_heads)
    return ratio ** np.arange(1, num_heads + 1)


def compute_alibi_bias(seq_len: int, num_heads: int) -> np.ndarray:
    slopes = compute_alibi_slopes(num_heads)
    positions = np.arange(seq_len)
    distance = positions[:, None] - positions[None, :]  # (seq_len, seq_len)
    return -slopes[:, None, None] * distance[None, :, :]


def alibi_causal_mask(seq_len: int, num_heads: int) -> np.ndarray:
    causal_mask = build_causal_mask(seq_len)
    alibi_bias = compute_alibi_bias(seq_len, num_heads)
    return alibi_bias + causal_mask[None, :, :]
