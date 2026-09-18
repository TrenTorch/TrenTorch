import numpy as np


def linear_forward(x: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    The forward pass of a fully connected layer, matching torch.nn.Linear's
    exact convention: `weight` has shape (out_features, in_features), NOT
    (in_features, out_features), and `x` can be a batch: shape
    (batch_size, in_features).
    """
    pass
