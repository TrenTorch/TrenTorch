"""
pytest data/app_data/06-inference/02-kv-cache-and-decoding/02-autoregressive-decoding-kv-cache/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

autoregressive_decode_with_cache = load_solution(
    f"06-inference/02-kv-cache-and-decoding/{Path(__file__).resolve().parent.name}"
).autoregressive_decode_with_cache


def test_three_token_prompt_generate_two():
    result = autoregressive_decode_with_cache(
        X_prompt=np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
        W_Q=np.eye(2), W_K=np.eye(2), W_V=np.eye(2),
        new_tokens=[[1.0, 1.0], [0.0, 0.0]],
    )
    assert result["final_cache_len"] == 5
    assert result["generated_outputs"].shape == (2, 2)
    assert result["prefill_output"].shape == (3, 2)


def test_prompt_only_no_generation():
    result = autoregressive_decode_with_cache(
        X_prompt=np.array([[1.0, 0.0], [0.0, 1.0]]),
        W_Q=np.eye(2), W_K=np.eye(2), W_V=np.array([[2.0, 0.0], [0.0, 2.0]]),
        new_tokens=[],
    )
    assert result["final_cache_len"] == 2
    assert result["generated_outputs"].shape == (0, 2)


def test_single_token_prompt_generate_three():
    result = autoregressive_decode_with_cache(
        X_prompt=np.array([[1.0, 1.0]]),
        W_Q=np.eye(2), W_K=np.array([[0.0, 1.0], [1.0, 0.0]]), W_V=np.eye(2),
        new_tokens=[[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]],
    )
    assert result["final_cache_len"] == 4


def test_incremental_cache_matches_recomputing_from_scratch():
    # The whole point: decoding with a growing cache must give bit-identical
    # results to running full (non-incremental) causal attention over the
    # entire sequence-so-far at every step.
    rng = np.random.default_rng(0)
    d_model = 4
    W_Q, W_K, W_V = (rng.normal(size=(d_model, d_model)) for _ in range(3))
    X_prompt = rng.normal(size=(2, d_model))
    new_tokens = [rng.normal(size=d_model) for _ in range(3)]

    result = autoregressive_decode_with_cache(X_prompt, W_Q, W_K, W_V, new_tokens)

    # Recompute step 2 (the last generated token) from scratch: full causal
    # attention over prompt + all new tokens up to and including it.
    full_seq = np.vstack([X_prompt] + [np.array(t) for t in new_tokens])
    Q_full, K_full, V_full = full_seq @ W_Q, full_seq @ W_K, full_seq @ W_V
    n = full_seq.shape[0]
    causal = np.tril(np.ones((n, n)))
    scores = np.where(causal == 0, -np.inf, Q_full @ K_full.T / np.sqrt(d_model))
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights /= weights.sum(axis=-1, keepdims=True)
    full_out = weights @ V_full

    assert np.allclose(result["generated_outputs"][-1], full_out[-1], atol=1e-8)


def test_prefill_is_causal():
    # Prefill output at position 0 must only depend on position 0's own V
    # (nothing to attend to but itself under a causal mask).
    result = autoregressive_decode_with_cache(
        X_prompt=np.array([[1.0, 0.0], [5.0, 5.0]]),
        W_Q=np.eye(2), W_K=np.eye(2), W_V=np.eye(2),
        new_tokens=[],
    )
    assert np.allclose(result["prefill_output"][0], [1.0, 0.0])
