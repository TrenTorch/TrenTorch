import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward
relu_backward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_backward


def linear_backward(grad_output: np.ndarray, input: np.ndarray, weight: np.ndarray):
    """
    Standard Linear-layer backward pass (the same chain-rule reasoning
    03-mse-gradient's Theory built up): given the gradient flowing back
    from this layer's output, and the input/weight this layer's
    forward pass used, returns (grad_input, grad_weight, grad_bias).
    """
    # TODO: grad_input = grad_output @ weight. grad_weight =
    # grad_output.T @ input. grad_bias = grad_output.sum(axis=0).
    pass


def forward_full(x: np.ndarray, weights: list, biases: list):
    """
    Runs a full stack of (Linear -> ReLU) layers, STORING every
    intermediate activation and pre-activation along the way -- the
    standard, memory-hungry way backprop is normally implemented,
    since the backward pass needs those exact intermediate values.

    Returns (final_output, activations, pre_activations):
    activations[0] is x itself, activations[i+1] is layer i's ReLU
    output; pre_activations[i] is layer i's Linear output, BEFORE ReLU.
    """
    # TODO: loop over (w, b) pairs in zip(weights, biases), computing
    # z = linear(current, w, b) (append to pre_activations), then
    # current = relu_forward(z) (append to activations), starting
    # activations as [x].
    pass


def backward_full(grad_output: np.ndarray, activations: list, pre_activations: list, weights: list):
    """
    Standard backward pass through the SAME stack forward_full just
    ran, using the stored activations/pre_activations directly (no
    recomputation needed -- they're already sitting in memory).

    Returns (grad_x, grad_weights, grad_biases) -- grad_weights/
    grad_biases are lists, one entry per layer, in the SAME order as
    the original `weights`/`biases` lists.
    """
    # TODO: walk the layers in REVERSE order. At each layer i: relu_backward
    # using pre_activations[i], then linear_backward using
    # activations[i] and weights[i]. Collect grad_weight/grad_bias
    # (inserted at the front, since you're walking backward), and pass
    # grad_input on to the next (earlier) layer.
    pass


def forward_checkpointed(x: np.ndarray, weights: list, biases: list) -> np.ndarray:
    """
    The SAME forward computation as forward_full, but keeps NOTHING in
    memory except the running `current` value -- no activations list,
    no pre_activations list. Only the final output is returned.
    """
    # TODO: the same loop as forward_full, but without building up any
    # lists at all -- just reassign `current` each iteration.
    pass


def backward_checkpointed(grad_output: np.ndarray, x: np.ndarray, weights: list, biases: list):
    """
    Since forward_checkpointed kept nothing, the backward pass has to
    RECOMPUTE the forward pass first (from the original input x, the
    one thing that WAS kept) to regenerate the activations/
    pre_activations backward_full actually needs -- trading compute
    (one extra forward pass) for memory (no stored intermediates).

    Must return EXACTLY the same (grad_x, grad_weights, grad_biases)
    backward_full would, given the same original computation.
    """
    # TODO: call forward_full(x, weights, biases) to regenerate
    # activations/pre_activations, then call backward_full with them.
    pass


def count_stored_activations(num_layers: int, use_checkpointing: bool) -> int:
    """
    Returns how many activation arrays end up held in memory
    simultaneously: num_layers + 1 (every activation, including the
    input) without checkpointing, or just 1 (only the original input)
    with checkpointing.
    """
    # TODO: return 1 if use_checkpointing else num_layers + 1.
    pass
