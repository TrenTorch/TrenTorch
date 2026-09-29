import numpy as np

FP8_E4M3_MAX = 448.0
MANTISSA_BITS = 3


def _round_to_mantissa_bits(x, bits=MANTISSA_BITS):
    mantissa, exponent = np.frexp(x)
    step = 2.0 ** (-bits)
    rounded_mantissa = np.round(mantissa / step) * step
    return np.ldexp(rounded_mantissa, exponent)


def quantize_fp8_blockwise(W: np.ndarray, block_rows: int, block_cols: int) -> dict:
    W = np.array(W, dtype=float)
    rows, cols = W.shape
    assert rows % block_rows == 0 and cols % block_cols == 0
    n_br, n_bc = rows // block_rows, cols // block_cols

    W_blocks = W.reshape(n_br, block_rows, n_bc, block_cols).transpose(0, 2, 1, 3)
    max_abs = np.max(np.abs(W_blocks), axis=(-2, -1))
    scale = np.where(max_abs > 0, max_abs / FP8_E4M3_MAX, 0.0)

    safe_scale = np.where(scale == 0, 1.0, scale)
    scaled = W_blocks / safe_scale[:, :, None, None]
    fp8_sim = _round_to_mantissa_bits(scaled)
    fp8_sim = np.where(scale[:, :, None, None] == 0, 0.0, fp8_sim)

    dequant_blocks = fp8_sim * scale[:, :, None, None]

    fp8_sim_full = fp8_sim.transpose(0, 2, 1, 3).reshape(rows, cols)
    dequant_full = dequant_blocks.transpose(0, 2, 1, 3).reshape(rows, cols)
    return {"quantized_fp8_sim": fp8_sim_full, "scale": scale, "dequantized": dequant_full}
