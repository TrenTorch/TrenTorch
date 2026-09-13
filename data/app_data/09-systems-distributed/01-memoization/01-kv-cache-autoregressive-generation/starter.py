import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

autoregressive_decode_with_cache = load_solution(
    "06-inference/02-kv-cache-and-decoding/02-autoregressive-decoding-kv-cache"
).autoregressive_decode_with_cache


def generate_without_cache(
    X_prompt: np.ndarray, W_Q: np.ndarray, W_K: np.ndarray, W_V: np.ndarray, new_tokens: list
) -> dict:
    """
    The SAME autoregressive generation task as
    06-inference/02-kv-cache-and-decoding's autoregressive_decode_with_cache,
    but with no cache at all: at every single new token, recompute Q, K,
    V for the ENTIRE sequence-so-far from scratch, then run the full
    causal-attention forward pass over that whole sequence, and keep
    only the newest position's output.

    Returns the exact same dict shape:
    {"prefill_output": ..., "generated_outputs": ..., "final_cache_len": ...}
    """
    # TODO: write a helper that runs one full causal-attention forward
    # pass over an arbitrary sequence (Q,K,V = sequence @ W_Q/W_K/W_V,
    # causal-masked scores, softmax, weighted sum against V). Call it
    # once on X_prompt for prefill_output. Then, for each new token:
    # append it to the running sequence, re-run the SAME full forward
    # pass over the now-longer sequence, and keep only the last row of
    # the output as this step's generated output.
    pass


def outputs_match(X_prompt: np.ndarray, W_Q: np.ndarray, W_K: np.ndarray, W_V: np.ndarray, new_tokens: list) -> bool:
    """
    Caching is a pure optimization, not an approximation -- it should
    produce EXACTLY the same numbers as recomputing everything from
    scratch, just with less redundant work. Returns True iff
    autoregressive_decode_with_cache and generate_without_cache agree,
    within floating-point tolerance, on both prefill_output and
    generated_outputs.
    """
    # TODO: call both functions with the same inputs, compare
    # "prefill_output" and "generated_outputs" with np.allclose, and
    # return True only if both match.
    pass
