
import numpy as np

from _load import load_solution

split_heads = load_solution("seq-attention-mha-split-heads").split_heads
scaled_dot_product_attention = load_solution("seq-attention-scaled-dot-product").scaled_dot_product_attention


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
