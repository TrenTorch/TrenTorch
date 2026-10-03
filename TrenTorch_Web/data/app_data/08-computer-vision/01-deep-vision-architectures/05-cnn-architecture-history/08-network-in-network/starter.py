import numpy as np


def pointwise_mlp(x: np.ndarray, layers: list) -> np.ndarray:
    """Stack of 1x1 convolutions with ReLU between layers; last layer linear."""
    # TODO
    pass


def global_avg_pool(x: np.ndarray) -> np.ndarray:
    """(C, H, W) -> (C,) spatial means."""
    # TODO
    pass


def nin_logits(x: np.ndarray, layers: list) -> np.ndarray:
    """pointwise_mlp followed by global_avg_pool."""
    # TODO
    pass
