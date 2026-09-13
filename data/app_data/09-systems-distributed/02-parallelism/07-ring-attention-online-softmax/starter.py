import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def attention_chunk_stats(query: np.ndarray, key_chunk: np.ndarray, value_chunk: np.ndarray):
    """
    The "online softmax" running statistics for ONE key/value chunk
    (as if it were the only chunk any GPU had ever seen): the raw
    (un-normalized) weighted value sum, the raw normalizer, and the
    row-wise max score used for numerical stability.

    Returns (chunk_output, chunk_sum, chunk_max).
    """
    # TODO: scores = query @ key_chunk.T / sqrt(d_k). chunk_max =
    # row-wise max of scores. exp_scores = exp(scores - chunk_max).
    # chunk_output = exp_scores @ value_chunk. chunk_sum = row-wise sum
    # of exp_scores.
    pass


def merge_chunk_stats(acc_output, acc_sum, acc_max, chunk_output, chunk_sum, chunk_max):
    """
    Combines a running (acc_*) online-softmax state with a new chunk's
    stats, using the standard rescale-and-add rule: since both were
    computed relative to DIFFERENT maxes, both must be rescaled onto a
    shared new max before they can be validly added together.

    Returns the updated (acc_output, acc_sum, acc_max).
    """
    # TODO: new_max = elementwise max(acc_max, chunk_max). Rescale both
    # acc_output/acc_sum and chunk_output/chunk_sum by exp(their old
    # max - new_max), then add them together.
    pass


def ring_attention(query: np.ndarray, key_chunks: list, value_chunks: list) -> np.ndarray:
    """
    Full ring-attention-style computation: process each key/value
    chunk ONE AT A TIME (as if each arrived from the next GPU around a
    ring), maintaining only the running (acc_output, acc_sum, acc_max)
    state -- never materializing the full attention matrix over the
    whole (concatenated) sequence at once.
    """
    # TODO: start acc_output as zeros, acc_sum as zeros, acc_max as
    # -inf (all shaped appropriately). Loop over zip(key_chunks,
    # value_chunks), calling attention_chunk_stats then
    # merge_chunk_stats each iteration. Return acc_output / acc_sum.
    pass
