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
    """
    LoRA bolts a low-rank, trainable update onto a FROZEN Linear layer
    (linear-regression-hypothesis-function's `linear`): the base
    weight/bias never change, and the entire adaptation happens
    through lora_A (rank x in_features) and lora_B (out_features x
    rank), scaled by alpha/rank. Returns (output, cache), where cache
    holds whatever lora_backward will need.
    """
    # TODO: scale = alpha / rank. intermediate = input @ lora_A.T.
    # delta = scale * (intermediate @ lora_B.T). base_output =
    # linear(input, base_weight, base_bias). Return (base_output +
    # delta, (input, intermediate)).
    pass


def lora_backward(grad_output: np.ndarray, cache: tuple, lora_B: np.ndarray, alpha: float, rank: int):
    """
    Backward pass for ONLY the trainable LoRA matrices -- base_weight
    and base_bias are frozen, so they get NO gradient at all here
    (unlike an ordinary Linear layer's backward, which would also
    return grad_weight/grad_bias). Returns (grad_A, grad_B).
    """
    # TODO: unpack (input, intermediate) from cache. scale = alpha /
    # rank. grad_B = scale * (grad_output.T @ intermediate).
    # grad_intermediate = scale * (grad_output @ lora_B). grad_A =
    # grad_intermediate.T @ input.
    pass
