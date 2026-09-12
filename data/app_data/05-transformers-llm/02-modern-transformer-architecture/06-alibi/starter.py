import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def compute_alibi_slopes(num_heads: int) -> np.ndarray:
    """
    ALiBi's per-head slopes: a GEOMETRIC sequence starting at
    `2 ** (-8 / num_heads)`, with that same value as the common ratio,
    so slopes shrink by a fixed factor from head to head. Returns an
    array of shape `(num_heads,)`.
    """
    pass


def compute_alibi_bias(seq_len: int, num_heads: int) -> np.ndarray:
    """
    A per-head, per-position-pair bias: `bias[h, i, j] = -slopes[h] * (i - j)`,
    shape `(num_heads, seq_len, seq_len)`. More negative for KEY positions
    `j` further in the PAST relative to query position `i`.
    """
    pass


def alibi_causal_mask(seq_len: int, num_heads: int) -> np.ndarray:
    """
    Combines `compute_alibi_bias` with
    `[04-seq-modeling/04-attention/02-causal-mask]`'s causal mask into a
    single additive mask, shape `(num_heads, seq_len, seq_len)`, ready to
    pass directly as `scaled_dot_product_attention`'s `mask` argument.
    """
    pass
