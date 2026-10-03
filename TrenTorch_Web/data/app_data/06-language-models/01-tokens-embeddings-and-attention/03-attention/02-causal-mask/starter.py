import numpy as np


def build_causal_mask(seq_len: int) -> np.ndarray:
    """
    Builds an additive causal (autoregressive) mask: shape
    (seq_len, seq_len), where entry [i, j] is 0 if position j is at or
    before position i (allowed to attend), and -inf if position j comes
    AFTER position i (forbidden, since a generative model must never see
    a token it hasn't generated yet). Ready to pass directly as the
    `mask` argument to `[01-scaled-dot-product-attention]`'s
    scaled_dot_product_attention.
    """
    pass
