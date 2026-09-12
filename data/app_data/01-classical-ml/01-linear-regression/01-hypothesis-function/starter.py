import numpy as np


def linear(input: np.ndarray, weight: np.ndarray, bias: np.ndarray | None = None) -> np.ndarray:
    """
    input:  shape (batch_size, in_features)
    weight: shape (out_features, in_features)
    bias:   shape (out_features,), or None

    Returns:
        output with shape (batch_size, out_features)
    """
    # TODO: Implement the linear transformation from Theory.
    # Mirror torch.nn.functional.linear exactly: weight is stored as
    # (out_features, in_features), so you'll need its transpose to line
    # up with input for matrix multiplication.
    # Handle bias=None (no bias term) the same way PyTorch does.
    pass
