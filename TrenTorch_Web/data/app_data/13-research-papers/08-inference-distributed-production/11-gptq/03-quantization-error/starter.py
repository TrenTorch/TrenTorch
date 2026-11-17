import numpy as np


def quantization_error(x, bits):
    """
    x: weight values
    bits: number of bits used for quantization

    Returns:
        The mean absolute error between x and its quantize-then-dequantize version, as a float.
    """
    # TODO: Quantize x symmetrically, dequantize, and average the absolute differences (see Theory).
    pass
