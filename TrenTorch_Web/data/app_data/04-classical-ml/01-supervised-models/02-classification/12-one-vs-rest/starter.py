
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear
sigmoid = load_solution("classification-sigmoid").sigmoid
train_logistic_regression = load_solution("classification-training-loop").train_logistic_regression


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
