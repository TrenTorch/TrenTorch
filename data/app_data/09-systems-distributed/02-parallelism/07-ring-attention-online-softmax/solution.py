import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def attention_chunk_stats(query: np.ndarray, key_chunk: np.ndarray, value_chunk: np.ndarray):
    d_k = query.shape[-1]
    scores = query @ key_chunk.T / np.sqrt(d_k)
    chunk_max = np.max(scores, axis=-1, keepdims=True)
    exp_scores = np.exp(scores - chunk_max)
    chunk_output = exp_scores @ value_chunk
    chunk_sum = np.sum(exp_scores, axis=-1, keepdims=True)
    return chunk_output, chunk_sum, chunk_max


def merge_chunk_stats(acc_output, acc_sum, acc_max, chunk_output, chunk_sum, chunk_max):
    new_max = np.maximum(acc_max, chunk_max)
    correction_acc = np.exp(acc_max - new_max)
    correction_chunk = np.exp(chunk_max - new_max)
    new_output = acc_output * correction_acc + chunk_output * correction_chunk
    new_sum = acc_sum * correction_acc + chunk_sum * correction_chunk
    return new_output, new_sum, new_max


def ring_attention(query: np.ndarray, key_chunks: list, value_chunks: list) -> np.ndarray:
    n_queries, d_v = query.shape[0], value_chunks[0].shape[-1]
    acc_output = np.zeros((n_queries, d_v))
    acc_sum = np.zeros((n_queries, 1))
    acc_max = np.full((n_queries, 1), -np.inf)

    for key_chunk, value_chunk in zip(key_chunks, value_chunks):
        chunk_output, chunk_sum, chunk_max = attention_chunk_stats(query, key_chunk, value_chunk)
        acc_output, acc_sum, acc_max = merge_chunk_stats(
            acc_output, acc_sum, acc_max, chunk_output, chunk_sum, chunk_max
        )

    return acc_output / acc_sum
