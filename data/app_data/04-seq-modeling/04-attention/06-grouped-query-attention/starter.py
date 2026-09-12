import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

split_heads = load_solution("04-seq-modeling/04-attention/04-mha-split-heads").split_heads
scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def repeat_kv_heads(x: np.ndarray, num_repeats: int) -> np.ndarray:
    """
    Repeats each KV head CONSECUTIVELY `num_repeats` times along the
    head axis (axis 1): (batch, num_kv_heads, seq_len, d_k) becomes
    (batch, num_kv_heads * num_repeats, seq_len, d_k), with kv head 0
    repeated `num_repeats` times in a row, then kv head 1, and so on.
    """
    pass


def grouped_query_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    num_query_heads: int,
    num_kv_heads: int,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Grouped-Query Attention: like `[04-mha-split-heads]`'s ordinary
    Multi-Head Attention, but with FEWER key/value heads than query
    heads (num_query_heads must be evenly divisible by num_kv_heads).
    Each GROUP of num_query_heads/num_kv_heads consecutive query heads
    shares the SAME key/value head, rather than every query head having
    its own dedicated key/value head.

    `query` has shape (batch, seq_len, num_query_heads * d_k);
    `key`/`value` have shape (batch, seq_len, num_kv_heads * d_k), a
    SMALLER last dimension than `query`, since they have fewer heads.
    """
    pass
