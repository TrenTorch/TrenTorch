import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
train_logistic_regression = load_solution(
    "01-classical-ml/02-classification/05-training-loop"
).train_logistic_regression


def train_one_vs_rest(
    input: np.ndarray, target: np.ndarray, num_classes: int, lr: float, epochs: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    One-vs-Rest: train num_classes INDEPENDENT binary logistic
    regression classifiers, one per class, each answering "is this
    example class k, or NOT" (rest lumped together as the negative
    class). `train_logistic_regression` is already provided above.

    Returns (weights, biases): weights is (num_classes, in_features),
    biases is (num_classes,), stacked in exactly the shape `linear`
    already expects, one row/entry per class's own binary classifier.
    """
    pass


def predict_one_vs_rest(input: np.ndarray, weights: np.ndarray, biases: np.ndarray) -> np.ndarray:
    """
    Runs every class's binary classifier on `input` at once (via
    `linear`'s general multi-output convention) and predicts whichever
    class's classifier is MOST confident (highest sigmoid score),
    regardless of whether that score exceeds 0.5.
    """
    pass
