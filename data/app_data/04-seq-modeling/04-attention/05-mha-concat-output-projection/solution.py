import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

multi_head_attention_per_head = load_solution(
    "04-seq-modeling/04-attention/04-mha-split-heads"
).multi_head_attention_per_head


def concat_heads(x: np.ndarray) -> np.ndarray:
    batch_size, num_heads, seq_len, d_k = x.shape
    x = x.transpose(0, 2, 1, 3)
    return x.reshape(batch_size, seq_len, num_heads * d_k)


def multi_head_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    num_heads: int,
    weight_o: np.ndarray,
    bias_o: np.ndarray,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    per_head_output, weights = multi_head_attention_per_head(query, key, value, num_heads, mask=mask)
    concatenated = concat_heads(per_head_output)
    output = concatenated @ weight_o.T + bias_o
    return output, weights
