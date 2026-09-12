import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

multi_head_attention_per_head = load_solution(
    "04-seq-modeling/04-attention/04-mha-split-heads"
).multi_head_attention_per_head


def concat_heads(x: np.ndarray) -> np.ndarray:
    """
    The exact INVERSE of `[04-mha-split-heads]`'s split_heads: takes
    (batch_size, num_heads, seq_len, d_k) and recombines it back into
    (batch_size, seq_len, d_model), where d_model = num_heads * d_k,
    putting each head's output back into its own CONSECUTIVE chunk of
    the full-width vector.
    """
    batch_size, num_heads, seq_len, d_k = x.shape
    pass


def multi_head_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    num_heads: int,
    weight_o: np.ndarray,
    bias_o: np.ndarray,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    The FULL Multi-Head Attention forward pass: split into heads and
    compute per-head attention (via `[04-mha-split-heads]`'s
    multi_head_attention_per_head, already provided), concatenate every
    head's output back into one d_model-wide vector (via concat_heads,
    above), then apply a learned OUTPUT PROJECTION (a plain
    `[03-dl-training/02-layers/01-linear-forward]`-style linear layer,
    weight_o/bias_o), which lets the model learn how to best COMBINE the
    different heads' separate contributions, rather than just naively
    stacking them side by side.
    """
    pass
