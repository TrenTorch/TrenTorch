
import numpy as np

from _load import load_solution

linear_forward = load_solution("dl-training-linear-forward").linear_forward
swish_forward = load_solution("dl-activation-swish").swish_forward


def swiglu_ffn(
    x: np.ndarray,
    weight_gate: np.ndarray,
    weight_up: np.ndarray,
    weight_down: np.ndarray,
) -> np.ndarray:
    zero_bias_ff = np.zeros(weight_gate.shape[0])
    zero_bias_model = np.zeros(weight_down.shape[0])

    gate = swish_forward(linear_forward(x, weight_gate, zero_bias_ff))
    up = linear_forward(x, weight_up, zero_bias_ff)
    hidden = gate * up
    return linear_forward(hidden, weight_down, zero_bias_model)
