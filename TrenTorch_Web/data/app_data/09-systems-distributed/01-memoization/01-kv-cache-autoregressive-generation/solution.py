import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

autoregressive_decode_with_cache = load_solution(
    "06-inference/02-kv-cache-and-decoding/02-autoregressive-decoding-kv-cache"
).autoregressive_decode_with_cache


def _softmax_row(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)


def generate_without_cache(
    X_prompt: np.ndarray, W_Q: np.ndarray, W_K: np.ndarray, W_V: np.ndarray, new_tokens: list
) -> dict:
    X_prompt = np.array(X_prompt, dtype=float)
    d_k = W_K.shape[1]
    scale = 1.0 / np.sqrt(d_k)

    def full_forward(sequence: np.ndarray) -> np.ndarray:
        Q, K, V = sequence @ W_Q, sequence @ W_K, sequence @ W_V
        seq_len = sequence.shape[0]
        causal = np.tril(np.ones((seq_len, seq_len)))
        scores = np.where(causal == 0, -np.inf, Q @ K.T * scale)
        weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
        weights /= weights.sum(axis=-1, keepdims=True)
        return weights @ V

    prefill_out = full_forward(X_prompt)

    sequence = X_prompt
    outputs = []
    for x_new in new_tokens:
        sequence = np.vstack([sequence, np.array(x_new, dtype=float)[None, :]])
        full_output = full_forward(sequence)
        outputs.append(full_output[-1])

    return {
        "prefill_output": prefill_out,
        "generated_outputs": np.array(outputs) if outputs else np.zeros((0, X_prompt.shape[1])),
        "final_cache_len": sequence.shape[0],
    }


def outputs_match(X_prompt: np.ndarray, W_Q: np.ndarray, W_K: np.ndarray, W_V: np.ndarray, new_tokens: list) -> bool:
    cached = autoregressive_decode_with_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    uncached = generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    return bool(
        np.allclose(cached["prefill_output"], uncached["prefill_output"], atol=1e-8)
        and np.allclose(cached["generated_outputs"], uncached["generated_outputs"], atol=1e-8)
    )
