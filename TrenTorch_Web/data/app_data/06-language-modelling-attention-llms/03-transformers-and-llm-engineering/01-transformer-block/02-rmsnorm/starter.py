import numpy as np


def rmsnorm_forward(x: np.ndarray, gamma: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """
    RMSNorm: like `[01-layer-normalization-forward]`'s LayerNorm, but
    without mean-centering and without an additive shift (`beta`). Scale
    `x` down by its own root-mean-square along the last axis, then apply
    a learned per-feature multiplicative scale `gamma`.
    """
    pass
