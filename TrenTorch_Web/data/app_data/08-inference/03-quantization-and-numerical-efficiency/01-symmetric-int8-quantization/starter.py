import numpy as np


def quantize_int8_symmetric(x: np.ndarray) -> dict:
    """
    x: array of any shape, treated as a flat set of values.

    Returns a dict with keys "quantized" (int array), "scale" (float),
    and "dequantized" (float array, same shape as x).
    """
    # TODO: Compute scale = max(|x|) / 127 (0 if x is all zeros), then
    # round(x / scale) clipped to [-127, 127], then dequantize as q * scale.
    pass
