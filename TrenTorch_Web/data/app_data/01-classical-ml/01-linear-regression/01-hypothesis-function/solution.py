import numpy as np


def linear(input: np.ndarray, weight: np.ndarray, bias: np.ndarray | None = None) -> np.ndarray:
    output = input @ weight.T
    if bias is not None:
        output = output + bias
    return output
