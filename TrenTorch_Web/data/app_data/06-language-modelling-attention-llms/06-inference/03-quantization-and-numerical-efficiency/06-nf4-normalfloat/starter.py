import numpy as np

NF4_LEVELS = np.array([-1.0, -0.6961928009986877, -0.5250730514526367, -0.39491748809814453, -0.28444138169288635, -0.18477343022823334, -0.09105003625225449, 0.0, 0.07958029955625534, 0.16093020141391754, 0.24611230194568542, 0.33791524171829224, 0.44070982933883667, 0.5626170039176941, 0.7229568362236755, 1.0])


def nf4_quantize(w: np.ndarray, block_size: int):
    """Returns (codes, scales): 4-bit codes (0..15) per value and one absmax scale per block."""
    # TODO
    pass


def nf4_dequantize(codes: np.ndarray, scales: np.ndarray, block_size: int) -> np.ndarray:
    """Reconstructs float values from codes and per-block scales."""
    # TODO
    pass
