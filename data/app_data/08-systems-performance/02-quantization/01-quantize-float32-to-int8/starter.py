import numpy as np


def compute_scale_zero_point(x: np.ndarray, num_bits: int = 8) -> tuple[float, int]:
    """
    x: any-shape float array
    num_bits: bit width of the target integer type (8 for int8)

    Affine ("zero-point") quantization maps x's actual [min, max] range
    onto the integer type's full representable range
    [-2^(num_bits-1), 2^(num_bits-1) - 1], via one scale (the size of one
    integer "step" in the original float units) and one zero_point (the
    integer value that represents float 0.0).
    """
    # TODO: qmin, qmax = -(2**(num_bits-1)), 2**(num_bits-1) - 1.
    # scale = (x.max() - x.min()) / (qmax - qmin), guarding against a
    # constant array (x.max() == x.min()) by falling back to scale=1.0.
    # zero_point = round(qmin - x.min() / scale), clipped into
    # [qmin, qmax] and cast to a plain int.
    pass


def quantize(x: np.ndarray, num_bits: int = 8) -> tuple[np.ndarray, float, int]:
    """
    Returns (q, scale, zero_point): q is x mapped into the integer
    range via compute_scale_zero_point's scale/zero_point, rounded to
    the nearest integer and clipped to stay in range, stored as int8.
    """
    # TODO: get scale/zero_point from compute_scale_zero_point, then
    # q = round(x / scale + zero_point), clipped to [qmin, qmax] and
    # cast to np.int8.
    pass
