import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize = load_solution("08-systems-performance/02-quantization/01-quantize-float32-to-int8").quantize
dequantize = load_solution("08-systems-performance/02-quantization/02-dequantize-int8-to-float32").dequantize


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
