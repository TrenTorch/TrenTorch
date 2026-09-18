import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def split_heads(x: np.ndarray, num_heads: int) -> np.ndarray:
    batch_size, seq_len, d_model = x.shape
    d_k = d_model // num_heads
    x = x.reshape(batch_size, seq_len, num_heads, d_k)
    return x.transpose(0, 2, 1, 3)


def multi_head_attention_per_head(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    num_heads: int,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    query_heads = split_heads(query, num_heads)
    key_heads = split_heads(key, num_heads)
    value_heads = split_heads(value, num_heads)

    output, weights = scaled_dot_product_attention(query_heads, key_heads, value_heads, mask=mask)
    return output, weights
