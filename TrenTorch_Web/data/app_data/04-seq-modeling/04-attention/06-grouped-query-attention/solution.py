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
    return np.repeat(x, num_repeats, axis=1)


def grouped_query_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    num_query_heads: int,
    num_kv_heads: int,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    query_heads = split_heads(query, num_query_heads)
    key_heads = split_heads(key, num_kv_heads)
    value_heads = split_heads(value, num_kv_heads)

    num_repeats = num_query_heads // num_kv_heads
    key_heads_repeated = repeat_kv_heads(key_heads, num_repeats)
    value_heads_repeated = repeat_kv_heads(value_heads, num_repeats)

    output, weights = scaled_dot_product_attention(
        query_heads, key_heads_repeated, value_heads_repeated, mask=mask
    )
    return output, weights
