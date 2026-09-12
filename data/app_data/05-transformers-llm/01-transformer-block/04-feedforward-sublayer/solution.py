import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear_forward = load_solution("03-dl-training/02-layers/01-linear-forward").linear_forward
gelu_forward = load_solution("02-deep-learning-core/02-activations/05-gelu").gelu_forward


def feedforward_sublayer(
    x: np.ndarray,
    weight1: np.ndarray,
    bias1: np.ndarray,
    weight2: np.ndarray,
    bias2: np.ndarray,
) -> np.ndarray:
    hidden = gelu_forward(linear_forward(x, weight1, bias1))
    return linear_forward(hidden, weight2, bias2)
