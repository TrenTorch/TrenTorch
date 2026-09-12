import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def split_heads(x: np.ndarray, num_heads: int) -> np.ndarray:
    """
    Splits `x` (shape (batch_size, seq_len, d_model)) into `num_heads`
    separate, SMALLER attention heads, each of dimension
    d_k = d_model // num_heads, giving each head its OWN slice of the
    full d_model-dimensional vector to work with. Returns shape
    (batch_size, num_heads, seq_len, d_k), with the head dimension moved
    to right after batch, so `[01-scaled-dot-product-attention]`'s
    function can treat (batch_size, num_heads) together as one combined
    leading "batch" dimension and process every head in parallel.
    """
    batch_size, seq_len, d_model = x.shape
    d_k = d_model // num_heads
    pass


def multi_head_attention_per_head(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    num_heads: int,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Splits query/key/value into num_heads separate heads (via
    split_heads), then runs `[01-scaled-dot-product-attention]`'s
    scaled_dot_product_attention ONCE, letting it process every head in
    parallel (since it's shape-agnostic to leading batch dimensions).
    Returns (output, weights), each still shaped with the SEPARATE head
    dimension: output is (batch_size, num_heads, seq_len, d_k).
    """
    pass
