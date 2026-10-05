import numpy as np


def logit_lens(resid: np.ndarray, W_U: np.ndarray, norm_weight: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """RMSNorm each layer's residual, then unembed: (L, d) -> (L, V)."""
    # TODO
    pass


def target_rank_by_layer(logits: np.ndarray, target: int) -> np.ndarray:
    """For each layer, the number of tokens with a strictly larger logit than `target`."""
    # TODO
    pass
