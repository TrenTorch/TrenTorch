import numpy as np

FP8_E4M3_MAX = 448.0
MANTISSA_BITS = 3


def quantize_fp8_blockwise(W: np.ndarray, block_rows: int, block_cols: int) -> dict:
    """
    W: weight matrix, shape (rows, cols); rows divisible by block_rows,
    cols divisible by block_cols.

    Returns a dict with keys "quantized_fp8_sim", "scale" (shape
    (rows // block_rows, cols // block_cols)), and "dequantized".
    """
    # TODO: Split W into 2D blocks, compute one scale per block
    # (max(|.|)/448), simulate 3-mantissa-bit rounding on the scaled
    # values with np.frexp/np.ldexp. See Theory hint.
    pass
