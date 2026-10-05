import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    shifted = x - x.max(axis=axis, keepdims=True)
    exp_shifted = np.exp(shifted)
    return exp_shifted / exp_shifted.sum(axis=axis, keepdims=True)


def scaled_dot_product_attention(
    query: np.ndarray, key: np.ndarray, value: np.ndarray
) -> np.ndarray:
    d_k = query.shape[-1]
    scores = query @ np.swapaxes(key, -1, -2) / np.sqrt(d_k)
    weights = softmax(scores, axis=-1)
    return weights @ value


def row_wise_attention(
    table: np.ndarray, w_query: np.ndarray, w_key: np.ndarray, w_value: np.ndarray
) -> np.ndarray:
    query = table @ w_query
    key = table @ w_key
    value = table @ w_value
    return scaled_dot_product_attention(query, key, value)
