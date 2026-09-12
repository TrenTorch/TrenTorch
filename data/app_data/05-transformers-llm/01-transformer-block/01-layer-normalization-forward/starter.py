import numpy as np


def layer_norm_forward(x: np.ndarray, gamma: np.ndarray, beta: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """
    Layer Normalization, applied along the LAST axis (the feature axis,
    e.g. `d_model` for a token's embedding), independently for each
    position: normalize to zero mean and unit variance, then apply a
    learned per-feature scale `gamma` and shift `beta`.
    """
    pass
