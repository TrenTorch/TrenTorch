import numpy as np


def bptt_gradient_norms(seq_len: int, weight_hh: np.ndarray, grad_h_final: np.ndarray) -> list[float]:
    grad_h = grad_h_final
    norms = [float(np.linalg.norm(grad_h))]

    for _ in range(seq_len):
        grad_h = grad_h @ weight_hh
        norms.append(float(np.linalg.norm(grad_h)))

    return norms
