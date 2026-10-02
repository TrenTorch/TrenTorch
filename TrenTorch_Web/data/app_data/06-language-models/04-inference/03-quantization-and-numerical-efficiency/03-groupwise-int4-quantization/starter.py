import numpy as np


def quantize_int4_groupwise(W: np.ndarray, group_size: int) -> dict:
    """
    W: weight matrix, shape (out_features, in_features), in_features
    divisible by group_size.

    Returns a dict with keys "quantized" (int matrix in [-7, 7]),
    "scale" (shape (out_features, n_groups)), and "dequantized".
    """
    # TODO: Reshape each row into (n_groups, group_size), compute one
    # scale per group (max(|.|)/7), quantize each group with its own
    # scale. See Theory hint for the reshape trick.
    pass
