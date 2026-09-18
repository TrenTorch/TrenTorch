import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize = load_solution("08-systems-performance/02-quantization/01-quantize-float32-to-int8").quantize


def dequantize(q: np.ndarray, scale: float, zero_point: int) -> np.ndarray:
    return (q.astype(np.float32) - zero_point) * scale


def quantization_error(x: np.ndarray, q: np.ndarray, scale: float, zero_point: int) -> float:
    reconstructed = dequantize(q, scale, zero_point)
    return float(np.max(np.abs(x - reconstructed)))
