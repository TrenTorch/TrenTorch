import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize = load_solution("08-systems-performance/02-quantization/01-quantize-float32-to-int8").quantize


def dequantize(q: np.ndarray, scale: float, zero_point: int) -> np.ndarray:
    """
    q: int8 array (or any integer array), the output of quantize()
    scale, zero_point: the exact values quantize() returned alongside q

    Inverts quantize()'s forward mapping: integer units back to float
    units. Never perfectly recovers the original values (that data was
    permanently lost when quantize() rounded to the nearest integer),
    but should be very close.
    """
    # TODO: reverse the forward mapping x/scale + zero_point: subtract
    # zero_point, then multiply by scale. Cast q to a float dtype first,
    # subtracting from an int8 array can silently wrap around instead of
    # producing a negative float.
    pass


def quantization_error(x: np.ndarray, q: np.ndarray, scale: float, zero_point: int) -> float:
    """
    x: the original float array quantize() was called on
    q, scale, zero_point: quantize(x)'s own output

    Returns the maximum absolute difference between the original values
    and what dequantizing q reconstructs -- how much information
    quantization actually lost, in the original float units.
    """
    # TODO: dequantize q, then return the maximum absolute elementwise
    # difference against x, as a plain float.
    pass
