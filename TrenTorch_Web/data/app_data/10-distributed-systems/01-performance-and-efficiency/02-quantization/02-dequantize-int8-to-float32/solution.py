
import numpy as np

from _load import load_solution

quantize = load_solution("systems-perf-quantize-float32-to-int8").quantize


def dequantize(q: np.ndarray, scale: float, zero_point: int) -> np.ndarray:
    return (q.astype(np.float32) - zero_point) * scale


def quantization_error(x: np.ndarray, q: np.ndarray, scale: float, zero_point: int) -> float:
    reconstructed = dequantize(q, scale, zero_point)
    return float(np.max(np.abs(x - reconstructed)))
