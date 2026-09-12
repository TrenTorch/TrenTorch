import numpy as np


def autoregressive_decode_with_cache(
    X_prompt: np.ndarray, W_Q: np.ndarray, W_K: np.ndarray, W_V: np.ndarray, new_tokens: list
) -> dict:
    """
    X_prompt: shape (prompt_len, d_model)
    W_Q, W_K, W_V: shape (d_model, d_model)
    new_tokens: list of new input feature vectors, one per decode step

    Returns a dict with keys "prefill_output", "generated_outputs" and
    "final_cache_len".
    """
    # TODO: Prefill -- one batched causal attention pass over X_prompt,
    # building K_cache/V_cache. Then for each new token, compute its own
    # Q/K/V, append K/V to the cache, and attend the new query over the
    # whole cache. See Theory for the exact prefill/decode split.
    pass
