import numpy as np


def multi_head_latent_attention(
    X: np.ndarray,
    W_Q: np.ndarray,
    W_DKV: np.ndarray,
    W_UK: np.ndarray,
    W_UV: np.ndarray,
    W_O: np.ndarray,
    n_heads: int,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    X: shape (seq_len, d_model)
    W_DKV: shape (d_model, d_latent)
    W_UK, W_UV: shape (d_latent, n_heads * d_head)

    Returns (output, latent_cache): output has shape (seq_len, d_model),
    latent_cache (= c) has shape (seq_len, d_latent).
    """
    # TODO: Compute the latent c = X @ W_DKV once, up-project into full
    # K, V via W_UK/W_UV, reshape into n_heads heads, then run the same
    # attention loop as multi_head_attention. Return both output and c.
    pass
