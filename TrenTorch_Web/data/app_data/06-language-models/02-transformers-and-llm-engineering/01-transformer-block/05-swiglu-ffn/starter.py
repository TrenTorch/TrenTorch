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
    """
    LLaMA-style SwiGLU-gated feed-forward sublayer (no biases, matching
    real modern LLM implementations). Two SEPARATE, bias-free linear
    projections of `x` up to `d_ff`: a "gate" branch passed through
    Swish/SiLU, and an "up" branch left linear. Their ELEMENTWISE
    PRODUCT is then projected back down to `d_model`.
    """
    pass
