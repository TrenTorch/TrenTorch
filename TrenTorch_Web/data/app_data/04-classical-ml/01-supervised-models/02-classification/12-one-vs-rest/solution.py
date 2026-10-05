
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear
sigmoid = load_solution("classification-sigmoid").sigmoid
train_logistic_regression = load_solution("classification-training-loop").train_logistic_regression


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
