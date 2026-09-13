import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward
relu_backward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_backward


def linear_backward(grad_output: np.ndarray, input: np.ndarray, weight: np.ndarray):
    grad_input = grad_output @ weight
    grad_weight = grad_output.T @ input
    grad_bias = grad_output.sum(axis=0)
    return grad_input, grad_weight, grad_bias


def forward_full(x: np.ndarray, weights: list, biases: list):
    activations = [x]
    pre_activations = []
    current = x
    for w, b in zip(weights, biases):
        z = linear(current, w, b)
        pre_activations.append(z)
        current = relu_forward(z)
        activations.append(current)
    return current, activations, pre_activations


def backward_full(grad_output: np.ndarray, activations: list, pre_activations: list, weights: list):
    grad = grad_output
    grad_weights, grad_biases = [], []
    for i in reversed(range(len(weights))):
        grad = relu_backward(grad, pre_activations[i])
        grad_input, grad_w, grad_b = linear_backward(grad, activations[i], weights[i])
        grad_weights.insert(0, grad_w)
        grad_biases.insert(0, grad_b)
        grad = grad_input
    return grad, grad_weights, grad_biases


def forward_checkpointed(x: np.ndarray, weights: list, biases: list) -> np.ndarray:
    current = x
    for w, b in zip(weights, biases):
        current = relu_forward(linear(current, w, b))
    return current


def backward_checkpointed(grad_output: np.ndarray, x: np.ndarray, weights: list, biases: list):
    _, activations, pre_activations = forward_full(x, weights, biases)
    return backward_full(grad_output, activations, pre_activations, weights)


def count_stored_activations(num_layers: int, use_checkpointing: bool) -> int:
    if use_checkpointing:
        return 1
    return num_layers + 1
