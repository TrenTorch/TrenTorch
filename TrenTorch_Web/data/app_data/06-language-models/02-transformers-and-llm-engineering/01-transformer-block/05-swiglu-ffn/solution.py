import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

linear_forward = load_solution("05-deep-learning/02-training-and-sequence-models/02-layers/01-linear-forward").linear_forward
swish_forward = load_solution("05-deep-learning/01-core-mechanics/02-activations/06-swish").swish_forward


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
