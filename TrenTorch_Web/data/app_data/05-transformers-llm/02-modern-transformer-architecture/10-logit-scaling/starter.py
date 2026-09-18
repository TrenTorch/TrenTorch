import numpy as np


def scale_logits_before_softmax(logits: np.ndarray, d_model: int) -> np.ndarray:
    """
    Scales vocabulary logits down by `1 / sqrt(d_model)` before they're
    passed to softmax, exactly the same numerical-stability motivation as
    `[04-seq-modeling/04-attention/01-scaled-dot-product-attention]`'s
    `1/sqrt(d_k)` scaling of attention scores.
    """
    pass
