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
    in_features = input.shape[1]
    weights = np.zeros((num_classes, in_features))
    biases = np.zeros(num_classes)
    for class_index in range(num_classes):
        binary_target = (target == class_index).astype(float)
        weight, bias = train_logistic_regression(input, binary_target, lr, epochs)
        weights[class_index] = weight.flatten()
        biases[class_index] = bias.item()
    return weights, biases


def predict_one_vs_rest(input: np.ndarray, weights: np.ndarray, biases: np.ndarray) -> np.ndarray:
    scores = sigmoid(linear(input, weights, biases))
    return np.argmax(scores, axis=1)
