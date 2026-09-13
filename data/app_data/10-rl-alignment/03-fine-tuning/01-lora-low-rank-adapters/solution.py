import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def lora_forward(
    input: np.ndarray,
    base_weight: np.ndarray,
    base_bias: np.ndarray,
    lora_A: np.ndarray,
    lora_B: np.ndarray,
    alpha: float,
    rank: int,
):
    scale = alpha / rank
    intermediate = input @ lora_A.T
    delta = scale * (intermediate @ lora_B.T)
    base_output = linear(input, base_weight, base_bias)
    output = base_output + delta
    cache = (input, intermediate)
    return output, cache


def lora_backward(grad_output: np.ndarray, cache: tuple, lora_B: np.ndarray, alpha: float, rank: int):
    input, intermediate = cache
    scale = alpha / rank
    grad_B = scale * (grad_output.T @ intermediate)
    grad_intermediate = scale * (grad_output @ lora_B)
    grad_A = grad_intermediate.T @ input
    return grad_A, grad_B
