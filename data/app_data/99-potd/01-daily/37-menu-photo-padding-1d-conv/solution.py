import numpy as np


def conv1d(x: np.ndarray, kernel: np.ndarray, mode: str) -> np.ndarray:
    k = len(kernel)

    if mode == "same":
        pad = k // 2
        signal = np.concatenate([np.zeros(pad), x, np.zeros(pad)])
    else:  # "valid"
        signal = x

    out_len = len(signal) - k + 1
    output = np.empty(out_len)
    for i in range(out_len):
        output[i] = np.sum(signal[i : i + k] * kernel)
    return output
