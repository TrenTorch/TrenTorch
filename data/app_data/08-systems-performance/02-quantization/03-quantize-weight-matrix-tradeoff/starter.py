import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize = load_solution("08-systems-performance/02-quantization/01-quantize-float32-to-int8").quantize
dequantize = load_solution("08-systems-performance/02-quantization/02-dequantize-int8-to-float32").dequantize


def quantize_weight_matrix(weight: np.ndarray) -> dict:
    """
    weight: a 2D (or any-shape) float32 array, e.g. a real Linear
        layer's weight matrix

    Quantizes the whole matrix with a single shared scale/zero_point
    (the same "per-tensor" scheme 01/02 use), then reports the
    practical tradeoff: how much smaller is the quantized version, and
    how much accuracy did it cost.

    Returns a dict: {
        "quantized": the int8 array,
        "scale": ..., "zero_point": ...,
        "compression_ratio": original_bytes / quantized_bytes (assuming
            the original was float32),
        "max_abs_error": worst single-element reconstruction error,
        "mean_abs_error": average reconstruction error across all elements,
    }
    """
    # TODO: call quantize(weight) to get (q, scale, zero_point), call
    # dequantize(q, scale, zero_point) to get the reconstruction, then
    # compute compression_ratio as (weight.size * 4) / (q.size * 1)
    # (float32 bytes vs int8 bytes), and the max/mean absolute error
    # between weight and the reconstruction.
    pass
