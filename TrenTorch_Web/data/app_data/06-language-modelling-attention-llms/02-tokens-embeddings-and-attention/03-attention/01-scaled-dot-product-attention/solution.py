import numpy as np


def scaled_dot_product_attention(
    query: np.ndarray, key: np.ndarray, value: np.ndarray, mask: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray]:
    d_k = query.shape[-1]
    scores = query @ np.swapaxes(key, -2, -1) / np.sqrt(d_k)

    if mask is not None:
        scores = scores + mask

    scores_shift = scores - np.max(scores, axis=-1, keepdims=True)
    exp_scores = np.exp(scores_shift)
    weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)

    output = weights @ value
    return output, weights
