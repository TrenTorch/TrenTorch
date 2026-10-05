
import numpy as np

from _load import load_solution

quantize = load_solution("systems-perf-quantize-float32-to-int8").quantize
dequantize = load_solution("systems-perf-dequantize-int8-to-float32").dequantize


def quantize_weight_matrix(weight: np.ndarray) -> dict:
    q, scale, zero_point = quantize(weight)
    reconstructed = dequantize(q, scale, zero_point)

    original_bytes = weight.size * 4  # float32
    quantized_bytes = q.size * 1  # int8

    return {
        "quantized": q,
        "scale": scale,
        "zero_point": zero_point,
        "compression_ratio": original_bytes / quantized_bytes,
        "max_abs_error": float(np.max(np.abs(weight - reconstructed))),
        "mean_abs_error": float(np.mean(np.abs(weight - reconstructed))),
    }
