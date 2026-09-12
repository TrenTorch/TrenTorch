import numpy as np


def _softmax_row(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)


def autoregressive_decode_with_cache(
    X_prompt: np.ndarray, W_Q: np.ndarray, W_K: np.ndarray, W_V: np.ndarray, new_tokens: list
) -> dict:
    X_prompt = np.array(X_prompt, dtype=float)
    d_k = W_K.shape[1]
    scale = 1.0 / np.sqrt(d_k)

    Q_p, K_cache, V_cache = X_prompt @ W_Q, X_prompt @ W_K, X_prompt @ W_V
    prompt_len = X_prompt.shape[0]
    causal = np.tril(np.ones((prompt_len, prompt_len)))
    scores = Q_p @ K_cache.T * scale
    scores = np.where(causal == 0, -np.inf, scores)
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights /= weights.sum(axis=-1, keepdims=True)
    prefill_out = weights @ V_cache

    outputs = []
    for x_new in new_tokens:
        x_new = np.array(x_new, dtype=float)
        q_new = x_new @ W_Q
        k_new = x_new @ W_K
        v_new = x_new @ W_V
        K_cache = np.vstack([K_cache, k_new[None, :]])
        V_cache = np.vstack([V_cache, v_new[None, :]])

        scores = (K_cache @ q_new) * scale
        w = _softmax_row(scores)
        outputs.append(w @ V_cache)

    return {
        "prefill_output": prefill_out,
        "generated_outputs": np.array(outputs) if outputs else np.zeros((0, X_prompt.shape[1])),
        "final_cache_len": K_cache.shape[0],
    }
