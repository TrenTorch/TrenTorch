import numpy as np


def quantize_int8_per_channel(W: np.ndarray) -> dict:
    """
    W: weight matrix, shape (out_features, in_features).

    Returns a dict with keys "quantized" (int matrix), "scale" (one
    value per output row), and "dequantized" (float matrix).
    """
    # TODO: Compute one scale per row (max(|W[o,:]|)/127, or 0 for an
    # all-zero row), quantize each row with its own scale, broadcasting
    # scale[:, None] over the row. See Theory hint.
    pass
